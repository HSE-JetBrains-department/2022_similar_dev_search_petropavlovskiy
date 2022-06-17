from typing import Dict

from enry import *

using_languages = ['python', 'java', 'javascript']


def process_languages(repo_info: Dict) -> dict:
    """
    Aggregates information about files and their languages.
    :param repo_info: dictionary with information about commits and their authors
    :return: dictionary of relations blob_path to language and blob_id
    """
    res = {}
    for key, value in repo_info['commits'].items():
        for info in value['changes']:
            res[info['blob_path']] = {
                'blob_id': info['blob_id'],
                'language': get_language_by_extension(info['blob_path']).language
            }

    return res


def get_language(blob_path: str) -> str:
    """
    Return programming language which is used in file
    :param blob_path: path to file
    :return: programming language
    """
    language = get_language_by_extension(blob_path).language.lower()
    return language if using_languages.__contains__(language) else ""
