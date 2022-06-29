import unittest

from info_processing.code_processing.treesitter import process_identifiers, setup_tree_sitter_parser

from pathlib2 import Path


class TreeSitterTest(unittest.TestCase):
    def test_identifiers(self):
        setup_tree_sitter_parser()
        cwd = Path.cwd()
        if cwd.name != "test":
            cwd = str(Path(f"{cwd}/test"))
        path_to_file = str(Path(f"{cwd}/test_files/qwerty.java"))
        code_info = process_identifiers(path_to_file, "java")
        self.assertEqual(code_info["classes"]["Employee"], 1, "Found one class")


if __name__ == '__main__':
    unittest.main()
