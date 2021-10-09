#!/usr/bin/env python3

"""Interactive tool for repositories cloning from GitHub"""

import sys
import requests
import subprocess


def get_repos_metadata(user = "vikian050194"):
    """Info about get_repos_metadata.

    Args:
        user: GitHub user name

    Returns:
        List of repositories metadata
    """

    url = f"https://api.github.com/users/{user}/repos"
    r = requests.get(url = url)

    return r.json()


def do_interactive_clone(repos, url_type):
    """Go through list of repositories and clone some of them according to user response

    Args:
        repos: List of repositories metadata
    """

    url = None

    if url_type == "ssh":
        url = "ssh_url"
    if url_type == "http":
        url = "clone_url"

    for repo in repos:
        print("%s: %s"%(repo["name"], repo["language"]))
        print("Clone this repo? (y/n/exit)")
        response = input()

        if response == "y":
            bashCommand = ["git", "clone" , repo[url], repo["name"].lower().replace('-', '/', 1)]
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output)

        if response == "exit":
            break


def clone_repos(url_type):
    """Entry point"""

    try:
        repos = get_repos_metadata()
        reposCount = len(repos)
        print(f"{reposCount} repositories are discovered")

        if len(repos) != 0:
            do_interactive_clone(repos, url_type)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    url_type = "ssh"

    if len(sys.argv) == 2:
        url_type = sys.argv[1];

    clone_repos(url_type)
