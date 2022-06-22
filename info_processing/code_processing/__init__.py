import os

from pathlib2 import Path

TREE_SITTER_PATH = f"{Path().cwd().parent}/treesitter"

if not os.path.exists(TREE_SITTER_PATH):
    os.makedirs(TREE_SITTER_PATH)
