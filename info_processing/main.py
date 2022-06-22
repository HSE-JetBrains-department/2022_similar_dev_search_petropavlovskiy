import json
from collections import defaultdict

import fire

from git.helpers import get_repository_info, save_data

from pathlib2 import Path


def get_repo(path_to_repos: str, clone_dir_path: str, path_to_output: str):
    """
    Save data about repositories to json file.

    :param path_to_output: path to JSON
    :clone_dir_path: path to directory with cloned repositories
    :param path_to_repos: path to file with urls to repositories
    """
    path = Path(path_to_repos)
    with open(path.resolve(), "r") as file_with_repos:
        repos_list = json.loads(file_with_repos.read())
    all_repos_info = defaultdict()
    path_to_output = Path(path_to_output)

    for repo_url in repos_list:
        repo_owner = repo_url.split("/")[3]
        repo_name = repo_url.split("/")[4]
        repo_name = f"{repo_owner}_{repo_name}"
        repo_info = get_repository_info(repo_url, repo_name, clone_dir_path)
        all_repos_info[repo_name] = repo_info

    save_data(all_repos_info, path_to_output)


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
