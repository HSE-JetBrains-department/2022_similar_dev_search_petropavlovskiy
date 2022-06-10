from enry import *

from typing import Dict, Any

def process_languages(repo_info: Dict) -> dict[Any, dict[str, Any]]:
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
