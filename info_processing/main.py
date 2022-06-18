import fire

from git.helpers import get_repository_info, save_data

from pathlib2 import Path

from src.stargaze.git_processor import get_stargazers


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
    # repo_info = get_repository_info(url, repo_name)
    # save_data(repo_info, path)
    save_data(get_stargazers("scikit-learn/scikit-learn", "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", 5),
              Path("/mnt/c/Users/User1337/Downloads/star.json"))


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
