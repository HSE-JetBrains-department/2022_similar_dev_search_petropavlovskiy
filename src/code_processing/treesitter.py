from collections import Counter
from typing import Dict

from tree_sitter import Parser, Language

PARSER = Parser()
JAVA_LANGUAGE = Language("build/my-languages.so", "java")
JS_LANGUAGE = Language("build/my-languages.so", "javascript")
PY_LANGUAGE = Language("build/my-languages.so", "python")
languages = {"python": Language("../build/my-languages.so", "python"),
             "javascript": Language("../build/my-languages.so", "javascript"),
             "java": Language("../build/my-languages.so", "java")}
queries = {"python": Language("../build/my-languages.so", "python").query("""
        (assignment left: (identifier) @var_name)
        (class_definition name: (identifier) @class_name)
        (function_definition name: (identifier) @func_name)
       """),
           "javascript": Language("../build/my-languages.so", "javascript").query("""
        (variable_declarator name: (identifier) @var_name)
        (class_declaration name: (identifier) @class_name)
        (function_declaration name: (identifier) @func_name)
       """),
           "java": Language("../build/my-languages.so", "java").query("""
                   (variable_declarator name: (identifier) @var_name)
                   (class_declaration name: (identifier) @class_name)
                   (function_declaration name: (identifier) @func_name)
                  """)
           }


def process_variables(blob_path: str, language: str) -> Dict:
    file_lang = {
        "Java": JAVA_LANGUAGE,
        "Javascript": JS_LANGUAGE,
        "Python": PY_LANGUAGE
    }
    PARSER.set_language(file_lang)
    query = queries[file_lang]
    with open(blob_path, "r") as file:
        code = bytes(file.read(), "utf8")
    ident_vector = {"variables": Counter(), "functions": Counter(), "imports": Counter()}
    for index, identifier in enumerate(query.captures(PARSER.parse(code).root_node)):
        node = identifier[0]
        capture_type = identifier[1]
        ident = code[node.start_byte: node.end_byte].decode()
        ident_vector["variables" if capture_type == "var_name" else (
            "classes" if capture_type == "class_name" else "functions")][ident] += 1
    return ident_vector
