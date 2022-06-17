import json
import os.path

from difflib import unified_diff

from typing import Dict, List

from dulwich.diff_tree import TreeChange
from dulwich.porcelain import clone
from dulwich.repo import Repo
from dulwich.walk import WalkEntry

from pathlib2 import Path

from code_processing.enry_processor import get_language
from code_processing.treesitter import process_identifiers

from code_processing.treesitter import setup_tree_sitter_parser

from tqdm import tqdm


def get_repository_info(url: str, repo_name: str) -> Dict:
    """
    Returns repository description.
    Result structure: {
        'url': <repository url>,
        'commits': {
            <commit sha>: {
                'author': <author name and email>,
                'changes': [{
                        'file': <path to changed file>,
                        'blob_id': <blob id>,
                        'added': <count of added rows>,
                        'deleted': <count of deleted rows>
                    },
                    ...
                ]
            },
            ...
        }
    }
    :param url: repository url
    :return: dict with repository description
    """
    if not url.endswith(".git"):
        url = url + ".git"

    clone_path = Path(f"{Path().cwd().parent}/repos/{repo_name}")
    if os.path.exists(clone_path):
        repo = Repo(clone_path.resolve())
    else:
        repo = clone(url, clone_path)

    setup_tree_sitter_parser()

    res = {
        "url": url,
        "commits": {}
    }

    for entry in tqdm(repo.get_walker()):
        commit = entry.commit
        commit_sha = commit.sha().hexdigest()
        if len(repo.get_parents(commit_sha, commit)) > 1:
            continue
        if commit_sha not in res["commits"].keys():
            res["commits"].update({
                commit_sha: {
                    "author": commit.author.decode(),
                    "changes": []
                }
            })
        changes = get_changes(entry, repo)
        res["commits"][commit_sha]["changes"] += changes

    return res


def get_changes(entry: WalkEntry, repo: Repo) -> List:
    """
    Returns changes list.
    :param entry: entry object
    :param repo: repository object
    :return: list of changes
    """
    res = []

    for changes in entry.changes():
        if type(changes) is not list:
            changes = [changes]
        for change in changes:
            change_dict = get_change_info(change, repo)
            res.append(change_dict)
    return res


def get_change_info(change: TreeChange, repo: Repo) -> Dict[str, str]:
    """
    Returns change info.
    Result structure: {
        'file': <path to changed file>,
        'blob_id': <blob id>,
        'added': <count of added rows>,
        deleted': <count of deleted rows>
    }
    :param change: change object
    :param repo: repository object
    :return: change as dict
    """
    blob_path = str(Path(f"{repo.path}/{(change.new.path or change.old.path).decode()}").absolute())
    print(f"language: {get_language(blob_path)}")
    res = {
        'file': (change.new.path or change.old.path).decode(),
        'blob_id': (change.new.sha or change.old.sha).decode(),
        "blob_path": blob_path,
        'added': 0,
        'deleted': 0,
        "code_info": {
            "language": get_language(blob_path)
        }

    }

    res["code_info"]["code_elements"] = process_identifiers(blob_path, res["code_info"]["language"])
    print(res)

    try:
        old_sha = change.old.sha
        new_sha = change.new.sha

        if old_sha is None:
            res["added"] = len(repo.get_object(new_sha).data.decode().splitlines())

        elif new_sha is None:
            res["deleted"] = len(repo.get_object(old_sha).data.decode().splitlines())

        else:
            differences = unified_diff(repo.get_object(old_sha).data.decode().splitlines(),
                                       repo.get_object(new_sha).data.decode().splitlines())
            for diff in differences:
                if diff.startswith("+") and not diff.startswith("++"):
                    res["added"] += 1
                if diff.startswith("-") and not diff.startswith("--"):
                    res["deleted"] += 1
    except UnicodeDecodeError as e:
        res = None

    return res


def save_data(data: Dict, path: Path):
    """
    Saves data as JSON file
    :param data: data to save
    :param path: file path
    :return: none
    """
    with open(path.resolve(), "w") as f:
        f.write(json.dumps(data, indent=6, ensure_ascii=False))
