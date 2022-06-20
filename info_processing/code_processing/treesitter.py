import logging
import os
from collections import Counter
from typing import Dict

from dulwich.porcelain import clone
from dulwich.repo import Repo

from pathlib2 import Path

from tree_sitter import Language, Parser

parser = Parser()
logger = logging.getLogger(__name__)


def setup_tree_sitter_parser() -> None:
    """
    Function sets up the parser for Python, JavaScript and Java languages cloning the repositories, that contain
    grammars.
    :return: Returns parser.
    """
    tree_sitter_python = clone_repo("https://github.com/tree-sitter/tree-sitter-python")
    tree_sitter_javascript = clone_repo("https://github.com/tree-sitter/tree-sitter-javascript")
    tree_sitter_java = clone_repo("https://github.com/tree-sitter/tree-sitter-java")
    path_to_build = str(Path(f"{Path.cwd().parent}/build/my-languages.so"))
    Language.build_library(
        path_to_build,
        [
            str(Path(tree_sitter_python.path)),
            str(Path(tree_sitter_javascript.path)),
            str(Path(tree_sitter_java.path))
        ]
    )


def process_identifiers(blob_path: str, language: str) -> Dict:
    """
    Method which takes variable and classes names, imports
    :param blob_path: path to file with code
    :param language: code language in file
    :return:
    """

    ident_vector = {"variables": Counter(), "functions": Counter(), "imports": Counter(), "classes": Counter()}
    if language == "":
        return ident_vector
    file_lang = Language(f"{Path().cwd().parent}/build/my-languages.so", language)
    parser.set_language(file_lang)
    file_lang = get_query(file_lang, language)
    try:
        with open(blob_path, "r") as file:
            code = bytes(file.read(), "utf8")
        for index, identifier in enumerate(file_lang.captures(parser.parse(code).root_node)):
            node = identifier[0]
            capture_type = identifier[1]
            ident = code[node.start_byte: node.end_byte].decode()
            ident_vector["variables" if capture_type == "var_name" else (
                "classes" if capture_type == "class_name" else (
                    "imports" if capture_type == "dotted_name" else "functions"))][ident] += 1
        return ident_vector
    except Exception as e:
        print(e)


def clone_repo(path: str) -> Repo:
    """
    Function cloned repo, if it is not existed, otherwise instantiate the existing one.
    :param: The path in local directory or url to GitHub repository.
    :return: Repository instance.
    """
    repo_name = path[path.rfind('/') + 1:]
    path_to_repo = str(Path(f"{Path().cwd().parent}/treesitter/{repo_name}"))
    parent_path = str(Path(path_to_repo).parent)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    return Repo(path_to_repo) if os.path.exists(path_to_repo) else clone(path, path_to_repo)


def get_query(file_lang: Language, language: str) -> Language:
    if language == "python":
        file_lang = file_lang.query("""
                    (assignment left: (identifier) @var_name)
                    (class_definition name: (identifier) @class_name)
                    (function_definition name: (identifier) @func_name)
                    (import_from_statement (dotted_name (identifier)) @dotted_name)
                    (import_statement (dotted_name (identifier)) @dotted_name)
                    (aliased_import (dotted_name (identifier)) @dotted_name)
                   """)
    elif language == "javascript":
        file_lang = file_lang.query("""
                    (variable_declarator name: (identifier) @var_name)
                    (class_declaration name: (identifier) @class_name)
                    (function_declaration name: (identifier) @func_name)
                   """)
    else:
        file_lang = file_lang.query("""
                                   (field_declaration declarator: (variable_declarator name: (identifier) @var_name))
                                   (class_declaration name: (identifier) @class_name)
                                   (method_declaration name: (identifier) @func_name)
                                   (method_declaration (formal_parameters(formal_parameter (identifier) @func_name)))
                                  """)
    return file_lang
