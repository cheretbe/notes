#!/usr/bin/env python3

import subprocess
import json


def main():
    dev_serials = []
    for line in subprocess.check_output(
        ["lsblk", "--nodeps", "-n", "-e7", "-o" "name,serial"], text=True
    ).splitlines():
        dev_serials.append(line.rstrip().split())

    c_data = json.loads(
        subprocess.check_output(["/opt/storcli64", "/call", "show", "all", "J"]).decode("utf-8")
    )

    output = [
        (
            "Drive",
            "Device",
            "EID:Slt",
            "DID",
            "State",
            "Size",
            "Intf",
            "Med",
            "Manufacturer Id",
            "Model Number",
            "NAND Vendor",
            "SN",
            "WWN",
        )
    ]
    for controller in c_data["Controllers"]:
        pd_info = controller["Response Data"].get("Physical Device Information", None)
        if pd_info:
            drives = []
            for info_key in pd_info.keys():
                if info_key.startswith("Drive /"):
                    drives.append(info_key.split(" ")[1])
            for drive in sorted(set(drives)):
                drive_info = pd_info[f"Drive {drive}"][0]
                drive_attributes = pd_info[f"Drive {drive} - Detailed Information"][
                    f"Drive {drive} Device attributes"
                ]
                output.append(
                    (
                        drive,
                        next(
                            (x[0] for x in dev_serials if x[1] == drive_attributes["SN"].strip()),
                            "not-found",
                        ),
                        drive_info["EID:Slt"],
                        drive_info["DID"],
                        drive_info["State"],
                        drive_info["Size"],
                        drive_info["Intf"],
                        drive_info["Med"],
                        drive_attributes["Manufacturer Id"].strip(),
                        drive_attributes["Model Number"].strip(),
                        drive_attributes["NAND Vendor"].strip(),
                        drive_attributes["SN"].strip(),
                        drive_attributes["WWN"].strip(),
                    )
                )

    column_sizes = [0] * len(output[0])
    for line in output:
        for i, item in enumerate(line):
            if len(str(item)) > column_sizes[i]:
                column_sizes[i] = len(str(item))

    for line in output:
        for i, item in enumerate(line):
            print(str(item).ljust(column_sizes[i] + 1), end="")
        print()


if __name__ == "__main__":
    main()
