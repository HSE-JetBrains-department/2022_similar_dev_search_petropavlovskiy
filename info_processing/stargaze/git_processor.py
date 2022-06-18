import calendar
import logging
import time
from typing import Dict, List

from github import Github, RateLimitExceededException

logger = logging.getLogger(__name__)


def get_stargazers(repo_name: str, github_token: str, number_of_repo: int) -> Dict[str, List[str]]:
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
    count = 0
    for user in repository.get_stargazers():
        if count > 10:
            break
        try:
            for i, starred_repo in enumerate(user.get_starred()):
                if i >= number_of_repo:
                    break
                repositories.append(starred_repo.full_name)
            user_to_repo[str(user.name)] = repositories
            repositories = []
            count+=1
        except RateLimitExceededException as e:
            print(f"Rate limit exception: {e}")
            logger.info("Rate limit exception: {e}")
            wait_for_request(github)

    return user_to_repo


def wait_for_request(github_account: Github):
    """
    Wait until GitHub API is usable again
    :param github_account: account
    """
    search_rate_limit = github_account.get_rate_limit().search
    reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())

    time.sleep(max(0, reset_timestamp - calendar.timegm(time.gmtime())))
