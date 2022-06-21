import fire

from helpers import get_repository_info, save_data

from pathlib2 import Path


def get_repo(url, path):
    """
    Save data about repository to json file.
    :param path: path to JSON
    :param url: repository url
    :return: list of commits
    """
    path = Path(path)
    repo_owner = url.split("/")[3]
    repo_name = url.split("/")[4]
    repo_name = f"{repo_owner}_{repo_name}"
    repo_info = get_repository_info(url, repo_name)
    save_data(repo_info, path)


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
