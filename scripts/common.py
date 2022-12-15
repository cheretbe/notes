import os
import subprocess

def upgrade_compose_container_versions(compose_dir, version_maps):
    print(f"Destroying container(s) in {compose_dir}")
    subprocess.check_call(
        ("docker", "compose", "down"),
        cwd=compose_dir
    )

    print("Updating .env file")
    with open(
            os.path.join(compose_dir, ".env"), "r+", encoding="utf-8"
    ) as conf_f:
        conf = conf_f.read()
        for version_map in version_maps:
            print(f"{version_map[0]} => {version_map[1]}")
            conf = conf.replace(version_map[0], version_map[1])
        conf_f.seek(0)
        conf_f.write(conf)
        conf_f.truncate()

    if os.path.isfile(os.path.join(compose_dir, "docker-compose.local.yml")):
        save_conf_cmd = (
            "docker compose -f docker-compose.yml -f docker-compose.local.yml "
            "config > local-data/config_$(date +%Y-%m-%d_%H-%M).txt"
        )
        up_cmd = (
            "docker", "compose", "-f", "docker-compose.yml", "-f", "docker-compose.local.yml",
            "up", "-d"
        )
    else:
        save_conf_cmd = (
            "docker compose "
            "config > local-data/config_$(date +%Y-%m-%d_%H-%M).txt"
        )
        up_cmd = ("docker", "compose", "up", "-d")

    print(f"Saving current config in {compose_dir}")
    os.makedirs(os.path.join(compose_dir, "local-data"), exist_ok=True)
    subprocess.check_call(
        save_conf_cmd,
        shell=True,
        cwd=compose_dir
    )
    print(f"Starting container(s) in {compose_dir}")
    subprocess.check_call(
        up_cmd,
        cwd=compose_dir
    )
