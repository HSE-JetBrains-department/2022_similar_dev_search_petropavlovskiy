import fire

from helpers import *



def get_repo(url, path):
    """
    Save data about repository to json file.
    :param path: path to JSON
    :param url: repository url
    :return: list of commits
    """
    url = 'https://github.com/OmdenaAI/Arabic-Chapter'
    path = path.replace('\\','\\\\')
    with open(path) as file:
        lines = file.readlines()
        print(lines)
    save_data(get_repository_info(url), path)


if __name__ == "__main__":
    fire.Fire({
        "repo-info": get_repo
    })
