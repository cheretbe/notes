#!/usr/bin/env python3


import argparse
import requests
import pathlib
import urllib.parse

# import pprint

# curl -sS -d "username=user@seafile.local&password=$my_pwd" http://seafile.domain.tld:8080/api2/auth-token/ | jq
# scripts/seafile/list_modified_files.py http://seafile.domain.tld 2025-01-12 2025-01-14 ~/temp/some_dir -t $my_token

# https://seafile-api.readme.io/reference/post_api2-auth-token
# https://seafile-api.readme.io/reference/get_api-v2-1-admin-logs-file-update
# https://seafile-api.readme.io/reference/get_api2-repos-repo-id-file


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("seafile_host")
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    parser.add_argument("dest_path")
    parser.add_argument("-t", "--token", action="store")

    return parser.parse_args()


def check_http_response(response):
    if response.status_code != 200:
        raise Exception(
            "HTTP call has failed. Status code: {code} - {text}".format(
                code=response.status_code, text=response.text
            )
        )


def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)


def main():
    args = parse_args()

    headers = {"Accept": "application/json", "Authorization": f"Token {args.token}"}
    api21_url = f"{args.seafile_host}/api/v2.1"
    api2_url = f"{args.seafile_host}/api2"
    response = requests.get(
        f"{api21_url}/admin/logs/file-update/?start={args.start_date}&end={args.end_date}",
        headers=headers,
    )
    check_http_response(response)
    # pprint.pprint(response.json())

    file_data = {}

    for commit in response.json():
        response = requests.get(
            f"{api21_url}/repos/{commit['repo_id']}/commits/{commit['commit_id']}/",
            headers=headers,
        )
        check_http_response(response)
        # pprint.pprint(response.json())

        for commit_diff in response.json()["commit_diffs"]:
            # print(commit_diff["op_type"])
            # print("    path: " + commit_diff["path"])
            # print("    new_path: " + commit_diff["new_path"])
            path = pathlib.Path(commit_diff["path"])
            if (commit_diff["op_type"] not in ["newdir", "deldir", "removed"]) and (
                path.suffix.lower() != ".lck"
            ):
                if commit["repo_id"] not in file_data:
                    file_data[commit["repo_id"]] = {
                        "repo_name": commit["repo_name"],
                        "files": set(),
                    }
                file_data[commit["repo_id"]]["files"].add(str(path))

    for repo_id, repo in file_data.items():
        for file in sorted(repo["files"]):
            print(repo["repo_name"] + ": " + file)
            response = requests.get(
                f"{api2_url}/repos/{repo_id}/file/?p="
                + urllib.parse.quote(file, safe=""),
                headers=headers,
            )
            if response.status_code == 404:
                print("[!!!] 404, ignoring")
            else:
                check_http_response(response)
                # print(response.text)
                local_file_path = (
                    pathlib.Path(args.dest_path).expanduser()
                    / repo["repo_name"]
                    / file.lstrip("/")
                )
                print(local_file_path)
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                download_file(url=response.text.strip('"'), dest_path=local_file_path)


if __name__ == "__main__":
    main()
