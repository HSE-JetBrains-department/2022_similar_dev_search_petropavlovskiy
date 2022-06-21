import logging
from collections import Counter
from typing import Dict

from info_processing.git.helpers import clone_repo

from pathlib2 import Path

from tree_sitter import Language, Parser

parser = Parser()
logger = logging.getLogger(__name__)
TREE_SITTER_PYTHON = clone_repo("https://github.com/tree-sitter/tree-sitter-python")
TREE_SITTER_JAVASCRIPT = clone_repo("https://github.com/tree-sitter/tree-sitter-javascript")
TREE_SITTER_JAVA = clone_repo("https://github.com/tree-sitter/tree-sitter-java")


def setup_tree_sitter_parser() -> None:
    """
    Function sets up the parser for Python, JavaScript and Java languages cloning the repositories, that contain
    grammars.
    :return: Returns parser.
    """
    path_to_build = str(Path(f"{Path.cwd().parent}/build/my-languages.so"))
    Language.build_library(
        path_to_build,
        [
            str(Path(TREE_SITTER_PYTHON.path)),
            str(Path(TREE_SITTER_JAVASCRIPT.path)),
            str(Path(TREE_SITTER_JAVA.path))
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
