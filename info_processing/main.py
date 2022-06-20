import json
from collections import defaultdict

import fire

from git.helpers import get_repository_info, save_data

from pathlib2 import Path


def get_repo(url: str, path_to_output: str):
    """
    Save data about repository to json file.
    :param path: path to JSON
    :param url: repository url
    :return: list of commits
    """
    path = Path("/mnt/c/Users/User1337/PycharmProjects/2022_similar_dev_search_petropavlovskiy2/list_of_repositories"
                ".txt")
    with open(path.resolve(), "r") as file_with_repos:
        repos_list = json.loads(file_with_repos.read())
    all_repos_info = defaultdict()
    path_to_output = Path(path_to_output)
    for repo_url in repos_list:
        repo_owner = repo_url.split("/")[3]
        repo_name = repo_url.split("/")[4]
        repo_name = f"{repo_owner}_{repo_name}"
        repo_info = get_repository_info(repo_url, repo_name)
        all_repos_info[repo_name] = repo_info

    # lst = Path(path).read_text().split('\n')
    # res_lst = []
    # for item in lst:
    #     dr = item
    #     if not item.isalnum() and item != "Python":
    #         res_lst.append(item.strip())
    # res = {
    #     "res": res_lst
    # }
    # with open(path.resolve(), "w") as f:
    #     f.write(json.dumps(res_lst, indent=6, ensure_ascii=False))
    save_data(all_repos_info, path_to_output)
    # save_data(get_stargazers("scikit-learn/scikit-learn", "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", 5),
    #           Path("/mnt/c/Users/User1337/Downloads/star.json"))


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
