import logging
from typing import Dict, List

from github import Github
from github.NamedUser import NamedUser

logger = logging.getLogger(__name__)


def get_stargazers(repo_name: str, github_token: str, number_of_repo: int) -> dict[NamedUser, list[str]]:
    """
        Returns map of username to user's repositories.
        :param repo_name: repository where we search stargazers
        :param github_token: token for authentification
        :param number_of_repo: maximum number of starred repos
        :return: map
    """
    github = Github(github_token)
    repository = github.get_repo(repo_name)
    user_to_repo = {}
    repositories = []
    for user in repository.get_stargazers():
        try:
            for i, starred_repo in enumerate(user.get_starred()):
                if i >= number_of_repo:
                    break
                repositories.append(starred_repo.full_name)
            user_to_repo[user] = repositories
            repositories = []
        except Exception as e:
            logger.info("Exception: {e}")

    return user_to_repo
