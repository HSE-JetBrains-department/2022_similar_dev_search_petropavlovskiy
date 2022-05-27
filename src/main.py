from config import *
from helpers import *
import fire


# 1. git part
def get_repo(url, path):
    """
    Returns list of commits in repository.
    :param path: path to JSON
    :param url: repository url
    :return: list of commits
    """
    save_data(get_repository_info(url), path)


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
