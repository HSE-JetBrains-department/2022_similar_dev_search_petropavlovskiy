import os
from collections import Counter
from typing import Dict

from dulwich.porcelain import clone
from dulwich.repo import Repo
from pathlib2 import Path
from tree_sitter import Parser, Language

PARSER = Parser()

# languages = {"python": Language("../build/my-languages.so", "python"),
#              "javascript": Language("../build/my-languages.so", "javascript"),
#              "java": Language("../build/my-languages.so", "java")}
# queries = {"python": Language("../build/my-languages.so", "python").query("""
#         (assignment left: (identifier) @var_name)
#         (class_definition name: (identifier) @class_name)
#         (function_definition name: (identifier) @func_name)
#        """),
#            "javascript": Language("../build/my-languages.so", "javascript").query("""
#         (variable_declarator name: (identifier) @var_name)
#         (class_declaration name: (identifier) @class_name)
#         (function_declaration name: (identifier) @func_name)
#        """),
#            "java": Language("../build/my-languages.so", "java").query("""
#                    (variable_declarator name: (identifier) @var_name)
#                    (class_declaration name: (identifier) @class_name)
#                    (function_declaration name: (identifier) @func_name)
#                   """)
#            }


def setup_tree_sitter_parser(repo: Repo) -> None:
    """
    Function sets up the parser for Python, JavaScript and Java languages cloning the repositories, that contain
    grammars.
    :return: Returns parser.
    """
    tree_sitter_python = clone_repo("https://github.com/tree-sitter/tree-sitter-python.git")
    tree_sitter_javascript = clone_repo("https://github.com/tree-sitter/tree-sitter-javascript.git")
    tree_sitter_java = clone_repo("https://github.com/tree-sitter/tree-sitter-java.git")

    Language.build_library(
        f"{Path().cwd()}/treesitter/build/my-languages.so",
        [
            "tree-sitter-python",
            "tree-sitter-javascript",
            "tree-sitter-java"
        ]
    )


def process_variables(blob_path: str, language: str) -> Dict:
    JAVA_LANGUAGE = Language("build/my-languages.so", "java")
    JS_LANGUAGE = Language("build/my-languages.so", "javascript")
    PY_LANGUAGE = Language("build/my-languages.so", "python")
    file_lang = {
        "Java": JAVA_LANGUAGE,
        "Javascript": JS_LANGUAGE,
        "Python": PY_LANGUAGE
    }
    # PARSER.set_language(file_lang)
    # query = queries[file_lang]
    # with open(blob_path, "r") as file:
    #     code = bytes(file.read(), "utf8")
    ident_vector = {"variables": Counter(), "functions": Counter(), "imports": Counter()}
    # for index, identifier in enumerate(query.captures(PARSER.parse(code).root_node)):
    #     node = identifier[0]
    #     capture_type = identifier[1]
    #     ident = code[node.start_byte: node.end_byte].decode()
    #     ident_vector["variables" if capture_type == "var_name" else (
    #         "classes" if capture_type == "class_name" else "functions")][ident] += 1
    return ident_vector


def clone_repo(path: str) -> Repo:
    """
    Function cloned repo, if it is not existed, otherwise instantiate the existing one.
    :param: The path in local directory or url to GitHub repository.
    :return: Repository instance.
    """
    repo_name = path[path.rfind('/') + 1:]
    pth = f"{Path().cwd()}/{repo_name}"
    return Repo(pth) if os.path.exists(pth) else clone(path, pth)
