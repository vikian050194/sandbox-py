#!/usr/bin/env python3

"""Module docstring"""

import requests
import subprocess

def get_repos_metadata(user = "vikian050194"):
    """Info about get_repos_metadata.
    
    Args:
        nothing
        
    Returns: 
        List of repos metadata.
    """
    url = f"https://api.github.com/users/{user}/repos"
    r = requests.get(url = url)
    return r.json()


def do_interactive_clone(repos):
    """Info about do_interactive_clone.
    
    Args:
        repos: List of repos metadata.
    """
    for repo in repos:
        print("%s: %s"%(repo["name"], repo["language"]))
        print("Clone this repo? (y/n)") 
        response = input()
        
        if response == "y":
            bashCommand = ["git", "clone" , repo["clone_url"], repo["name"].lower()]
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output)


def clone_repos():
    try:
        repos = get_repos_metadata()
        reposCount = len(repos)
        print(f"{reposCount} repositories are discovered")
        
        if len(repos) != 0:
            do_interactive_clone(repos)
    except Exception as e:
        print(e)   


if __name__ == "__main__":
    clone_repos()#comment1
    #comment2
