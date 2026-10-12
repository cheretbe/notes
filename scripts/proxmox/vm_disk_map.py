#!/usr/bin/env python3

"""Map physical disks to the Proxmox VMs/CTs that live on them.

Groups by physical disk by default; use --by-vm to group by guest instead.
Attribution is LVM-based: guest disks are expected to be LVM logical volumes
(`vm-<vmid>-*`). File-based (dir/qcow2) and ZFS/zvol storage is not mapped;
physical disks with no attributable LVM volume are shown as "(unattributed)".

Run on the Proxmox host it inspects. `lvs`/`qm`/`pct` need root; when not run as
root the script prepends `sudo -n`, so it works over SSH with passwordless sudo.
"""

import argparse
import json
import os
import re
import subprocess
import sys

VM_LV_RE = re.compile(r"^vm-(\d+)-")


def run(cmd, privileged=False):
    if privileged and os.geteuid() != 0:
        cmd = ["sudo", "-n"] + cmd
    return subprocess.check_output(cmd, text=True)


def parse_lvs():
    """Return list of (vg_name, lv_name, lv_size, [physical_device, ...])."""
    out = run(
        [
            "lvs",
            "-o", "vg_name,lv_name,lv_size,devices",
            "--noheadings",
            "--separator", "|",
        ],
        privileged=True,
    )
    rows = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        vg, lv, size, devices = line.split("|", 3)
        # "devices" looks like "/dev/sdf(0)" or "/dev/sda(0),/dev/sdb(0)".
        devs = []
        for part in devices.split(","):
            part = part.strip()
            if not part:
                continue
            devs.append(re.sub(r"\(\d+\)$", "", part))
        rows.append((vg.strip(), lv.strip(), size.strip(), devs))
    return rows


def parse_lsblk():
    """Return {kname: node} and a helper to resolve a device to its parent disk."""
    out = run(["lsblk", "-J", "-o", "NAME,KNAME,PKNAME,TYPE,SIZE,MODEL,SERIAL,TRAN"])
    data = json.loads(out)
    by_kname = {}

    def walk(nodes):
        for node in nodes:
            if node.get("kname"):
                by_kname[node["kname"]] = node
            if node.get("children"):
                walk(node["children"])

    walk(data.get("blockdevices", []))
    return by_kname


def resolve_disk(device_path, by_kname):
    """Resolve /dev/<name> (possibly a partition) to its parent physical disk node."""
    kname = device_path.rsplit("/", 1)[-1]
    node = by_kname.get(kname)
    seen = set()
    while node is not None and node.get("type") != "disk":
        parent = node.get("pkname")
        if not parent or parent in seen:
            break
        seen.add(parent)
        node = by_kname.get(parent)
    return node


def parse_guests():
    """Return {vmid: (name, type)} from `qm list` (VM) and `pct list` (CT)."""
    guests = {}
    for cmd, gtype in (("qm", "VM"), ("pct", "CT")):
        try:
            out = run([cmd, "list"], privileged=True)
        except subprocess.CalledProcessError:
            continue
        lines = out.splitlines()
        if not lines:
            continue
        for line in lines[1:]:  # skip header
            parts = line.split()
            if len(parts) < 2 or not parts[0].isdigit():
                continue
            vmid = int(parts[0])
            # `qm list` columns: VMID NAME STATUS ...; `pct list`: VMID Status Lock? Name
            if cmd == "qm":
                name = parts[1]
            else:
                # Name is the last column (Lock column may be empty/absent).
                name = parts[-1]
            guests[vmid] = (name, gtype)
    return guests


def build_records():
    by_kname = parse_lsblk()
    guests = parse_guests()

    records = []
    used_disks = set()
    # A segmented LV yields one `lvs` row per segment; collapse rows that land
    # on the same (disk, volume) so each volume is listed once per disk.
    seen = set()
    for vg, lv, lv_size, devs in parse_lvs():
        m = VM_LV_RE.match(lv)
        if m:
            vmid = int(m.group(1))
            name, gtype = guests.get(vmid, ("(unknown)", "?"))
        else:
            vmid = None
            name, gtype = "(system)", "-"
        for dev in devs:
            node = resolve_disk(dev, by_kname)
            disk = node["kname"] if node else dev.rsplit("/", 1)[-1]
            used_disks.add(disk)
            if (disk, vg, lv) in seen:
                continue
            seen.add((disk, vg, lv))
            records.append(
                {
                    "disk": disk,
                    "disk_size": node.get("size") if node else None,
                    "model": (node.get("model") or "").strip() if node else "",
                    "serial": (node.get("serial") or "").strip() if node else "",
                    "tran": (node.get("tran") or "").strip() if node else "",
                    "vmid": vmid,
                    "guest_name": name,
                    "guest_type": gtype,
                    "volume": lv,
                    "vg": vg,
                    "lv_size": lv_size,
                }
            )

    # Physical disks present on the host but with no attributable LVM volume.
    for kname, node in by_kname.items():
        if node.get("type") == "disk" and kname not in used_disks:
            records.append(
                {
                    "disk": kname,
                    "disk_size": node.get("size"),
                    "model": (node.get("model") or "").strip(),
                    "serial": (node.get("serial") or "").strip(),
                    "tran": (node.get("tran") or "").strip(),
                    "vmid": None,
                    "guest_name": "(unattributed)",
                    "guest_type": "-",
                    "volume": "",
                    "vg": "",
                    "lv_size": "",
                }
            )
    return records


def print_table(rows):
    """Print a list of equal-length tuples as an aligned table (storcli_list.py style)."""
    if not rows:
        return
    widths = [0] * len(rows[0])
    for row in rows:
        for i, item in enumerate(row):
            widths[i] = max(widths[i], len(str(item)))
    for row in rows:
        print("".join(str(item).ljust(widths[i] + 1) for i, item in enumerate(row)))


def disk_sort_key(disk):
    # Group by device type prefix, then natural-ish by trailing number/letters.
    m = re.match(r"^([a-z]+)(.*)$", disk)
    return (m.group(1), m.group(2)) if m else (disk, "")


def output_by_disk(records):
    by_disk = {}
    for rec in records:
        by_disk.setdefault(rec["disk"], []).append(rec)

    first = True
    for disk in sorted(by_disk, key=disk_sort_key):
        if not first:
            print()
        first = False
        sample = by_disk[disk][0]
        header = f"/dev/{disk}  {sample['disk_size'] or '?'}"
        if sample["tran"]:
            header += f"  {sample['tran']}"
        if sample["model"]:
            header += f"  {sample['model']}"
        if sample["serial"]:
            header += f"  [{sample['serial']}]"
        print(header)

        guests = [r for r in by_disk[disk] if r["guest_name"] != "(unattributed)"]
        if not guests:
            print("  (unattributed)")
            continue
        table = [("  VMID", "TYPE", "GUEST", "VOLUME", "VG", "SIZE")]
        for r in sorted(guests, key=lambda r: (r["vmid"] is None, r["vmid"] or 0, r["volume"])):
            table.append(
                (
                    "  " + (str(r["vmid"]) if r["vmid"] is not None else "-"),
                    r["guest_type"],
                    r["guest_name"],
                    r["volume"],
                    r["vg"],
                    r["lv_size"],
                )
            )
        print_table(table)


def output_by_vm(records):
    by_vm = {}
    for rec in records:
        if rec["guest_name"] in ("(unattributed)",):
            continue
        by_vm.setdefault((rec["vmid"], rec["guest_name"], rec["guest_type"]), []).append(rec)

    first = True
    for (vmid, name, gtype) in sorted(by_vm, key=lambda k: (k[0] is None, k[0] or 0)):
        if not first:
            print()
        first = False
        vmid_s = str(vmid) if vmid is not None else "-"
        print(f"{vmid_s}  {name}  ({gtype})")
        table = [("  DISK", "VOLUME", "VG", "SIZE", "DISK", "MODEL", "SERIAL")]
        for r in sorted(by_vm[(vmid, name, gtype)], key=lambda r: (disk_sort_key(r["disk"]), r["volume"])):
            table.append(
                (
                    "  /dev/" + r["disk"],
                    r["volume"],
                    r["vg"],
                    r["lv_size"],
                    "/dev/" + r["disk"],
                    r["model"],
                    r["serial"],
                )
            )
        print_table(table)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--by-disk", action="store_true", help="group by physical disk (default)"
    )
    group.add_argument("--by-vm", action="store_true", help="group by VM/CT")
    parser.add_argument("--json", action="store_true", help="emit raw records as JSON")
    args = parser.parse_args()

    try:
        records = build_records()
    except FileNotFoundError as exc:
        sys.exit(f"required command not found: {exc.filename} (run on a Proxmox host)")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"command failed: {' '.join(exc.cmd)}")

    if args.json:
        print(json.dumps(records, indent=2))
    elif args.by_vm:
        output_by_vm(records)
    else:
        output_by_disk(records)


if __name__ == "__main__":
    main()
