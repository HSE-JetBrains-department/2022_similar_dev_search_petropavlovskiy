import logging

from github import Github

logger = logging.getLogger(__name__)


def get_stargazers(repo_name, github_token):
    github = Github(github_token)
    repository = github.get_repo(repo_name)
    user_to_repo = {}
    repositories = []
    for user in repository.get_stargazers():
        try:
            for i, starred_repo in enumerate(user.get_starred()):
                if i >= 10:
                    break
                repositories.append(starred_repo.full_name)
            user_to_repo[user] = repositories
            repositories = []
        except Exception as e:
            logger.info("Exception: {e}")

    return user_to_repo
