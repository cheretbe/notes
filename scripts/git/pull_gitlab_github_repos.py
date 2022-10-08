#!/usr/bin/env python3

import argparse
import os
import sys
import types
import subprocess
import pathlib

import gitlab
import ghapi.core

script_dir = pathlib.Path(__file__).resolve().parent
credential_helper = os.path.join(str(script_dir), "env_var_credential_helper.py")

def pull_repo(repo, dest_path):
    service_dir = os.path.join(dest_path, repo.service)
    repo_dir = os.path.join(dest_path, repo.service, repo.path)
    if os.path.exists(repo_dir):
        print("\nPulling ", repo_dir)
        subprocess.check_call(
            ("git", "pull"),
            stdin=subprocess.DEVNULL,
            cwd=repo_dir,
            env={
                "GIT_ASKPASS": credential_helper,
                "CUSTOM_GIT_USERNAME": repo.user,
                "CUSTOM_GIT_PASSWORD": repo.token
            }
        )
    else:
        os.makedirs(service_dir, exist_ok=True)
        print("\ngit", "clone", repo.url)
        subprocess.check_call(
            ("git", "clone", repo.url),
            stdin=subprocess.DEVNULL,
            cwd=service_dir,
            env={
                "GIT_ASKPASS": credential_helper,
                "CUSTOM_GIT_USERNAME": repo.user,
                "CUSTOM_GIT_PASSWORD": repo.token
            }
        )

def main(args):
    exit_code = 0

    repos_to_pull = []

    try:
        print("Reading gitlab repos")
        # https://python-gitlab.readthedocs.io/en/stable/index.html
        gl_conn = gitlab.Gitlab(
            url="https://git.chere.one",
            private_token=args.gitlab_token
        )
        gl_conn.auth()
        projects = gl_conn.projects.list(owned=True, get_all=True)
        for project in projects:
            repos_to_pull.append(
                types.SimpleNamespace(
                    service="gitlab",
                    url=project.http_url_to_repo,
                    path=project.path,
                    user=args.gitlab_user,
                    token=args.gitlab_token
                )
            )
    except Exception as ex: # pylint: disable=broad-except
        print(ex)
        exit_code = 1

    try:
        print("Reading github repos")
        gh_api = ghapi.core.GhApi(owner=args.github_user, token=args.github_token)
        for repo in gh_api.repos.list_for_authenticated_user():
            repos_to_pull.append(
                types.SimpleNamespace(
                    service="github",
                    url=repo.html_url,
                    path=repo.name,
                    user=args.github_user,
                    token=args.github_token
                )
            )
    except Exception as ex: # pylint: disable=broad-except
        print(ex)
        exit_code = 1

    args.dest_path = os.path.expanduser(args.dest_path)
    os.makedirs(args.dest_path, exist_ok=True)

    for repo in repos_to_pull:
        try:
            pull_repo(repo, args.dest_path)
        except Exception as ex: # pylint: disable=broad-except
            print(ex)
            exit_code = 1

    return exit_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Git repo backup script",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.epilog = (
        "Usage example:\n"
        "./pull_gitlab_github_repos.py /path/to/a/dir/ "
        "--gitlab-user user1 --gitlab-token 000000 "
        "--github-user user2 --github-token 000000\n"
    )

    parser.add_argument("dest_path", help="Destination path")

    parser.add_argument(
        "--gitlab-token", default=None,
        help="GitLab instance auth token"
    )
    parser.add_argument(
        "--gitlab-user", default=None,
        help="GitLab instance user name"
    )
    parser.add_argument(
        "--github-token", default=None,
        help="GitHub auth token"
    )
    parser.add_argument(
        "--github-user", default=None,
        help="GitHub user name"
    )

    sys.exit(main(parser.parse_args()))
