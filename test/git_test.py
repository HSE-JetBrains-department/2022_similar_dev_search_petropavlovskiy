import logging
import shutil
import unittest

from info_processing.git.helpers import get_repository_info

from pathlib2 import Path

logger = logging.getLogger(__name__)


class GitTest(unittest.TestCase):
    def test_repository_info_processing(self):
        cwd = Path.cwd()
        if cwd.name != "test":
            cwd = str(Path(f"{cwd}/test"))
        repo_url = "https://github.com/MicrosoftDocs/pipelines-python-django/"
        repo_name = "test_repo"
        dir_to_clone = str(Path(f"{Path().cwd().parent}/repos"))
        repo_info = get_repository_info(repo_url, repo_name, dir_to_clone)
        self.assertTrue(repo_info["commits"]["7267bb437c1a1a66ab36b9dc31ed5aee9f84a278"] is not None)
        delete_cloned_repo(repo_name)


if __name__ == '__main__':
    unittest.main()


def delete_cloned_repo(repo_name: str):
    try:
        repo_path = str(Path(f"{Path().cwd().parent}/repos/{repo_name}"))
        shutil.rmtree(repo_path)
    except Exception:
        logger.warning("Can't delete cloned test repository")
        pass
