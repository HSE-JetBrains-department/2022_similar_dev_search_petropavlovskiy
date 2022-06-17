import logging
import os
import unittest

from git.helpers import get_repository_info

from pathlib2 import Path

logger = logging.getLogger(__name__)


class GitTest(unittest.TestCase):
    def test_repository_info_processing(self):
        test_repo_url = "https://github.com/MicrosoftDocs/pipelines-python-django"
        repo_name = "test_repo"
        repo_info = get_repository_info(test_repo_url, repo_name)
        print(repo_info)
        self.assertTrue(repo_info["commits"]["7267bb437c1a1a66ab36b9dc31ed5aee9f84a278"] != None)
        delete_cloned_repo(repo_name)


if __name__ == '__main__':
    unittest.main()


def delete_cloned_repo(repo_name: str):
    try:
        repo_path = str(Path(f"{Path().cwd().parent}/repos/{repo_name}"))
        os.rmdir(repo_path)
    except:
        logger.info("Can't delete cloned test repository")
