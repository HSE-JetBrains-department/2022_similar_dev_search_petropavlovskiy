import json

from dulwich.diff_tree import TreeChange
from dulwich.repo import Repo
from dulwich.porcelain import clone
from dulwich.walk import WalkEntry
import difflib
from tqdm import tqdm

# work with git
def get_repository_info(url: str):
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
    repo = clone(url)

    res = {
        'url': url,
        'commits': {}
    }

    # walk through changes
    for entry in tqdm(repo.get_walker()):
        commit = entry.commit
        commit_sha = commit.sha().hexdigest()
        if len(repo.get_parents(commit_sha, commit)) > 1:
            continue
        if commit_sha not in res['commits'].keys():
            res['commits'].update({
                commit_sha: {
                    'author': commit.author.decode(),
                    'changes': []
                }
            })
        changes = get_changes(entry, repo)
        res['commits'][commit_sha]['changes'] += changes

    return res


def get_changes(entry: WalkEntry, repo: Repo):
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


def get_change_info(change: TreeChange, repo: Repo):
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

    res = {
        'file': (change.new.path or change.old.path).decode(),
        'blob_id': (change.new.sha or change.old.sha).decode(),
        'added': 0,
        'deleted': 0
    }

    try:
        old_sha = change.old.sha
        new_sha = change.new.sha

        if old_sha is None:
            res['added'] = len(repo.get_object(new_sha).data.decode().splitlines())

        elif new_sha is None:
            res['deleted'] = len(repo.get_object(old_sha).data.decode().splitlines())

        else:
            differences = difflib.unified_diff(repo.get_object(old_sha).data.decode().splitlines(),
                                               repo.get_object(new_sha).data.decode().splitlines())
            for diff in differences:
                if diff.startswith("+") and not diff.startswith("++"):
                    res['added'] += 1
                if diff.startswith("-") and not diff.startswith("--"):
                    res['deleted'] += 1
    except UnicodeDecodeError as e:
        res = None

    return res


# work with files
def save_data(data, path):
    """
    Saves data as JSON file
    :param data: data to save
    :param path: file path
    :return: none
    """
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=6,  ensure_ascii=False))