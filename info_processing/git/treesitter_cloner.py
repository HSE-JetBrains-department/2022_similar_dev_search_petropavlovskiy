import os

from dulwich.porcelain import clone
from dulwich.repo import Repo

from pathlib2 import Path


def clone_treesitter_helpers(path: str) -> Repo:
    """
    Function cloned repo, if it is not existed, otherwise instantiate the existing one.
    :param: The path in local directory or url to GitHub repository.
    :return: Repository instance.
    """
    repo_name = path[path.rfind('/') + 1:]
    path_to_repo = str(Path(f"{Path().cwd().parent}/treesitter/{repo_name}"))
    parent_path = str(Path(path_to_repo).parent)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    return Repo(path_to_repo) if os.path.exists(path_to_repo) else clone(path, path_to_repo)
