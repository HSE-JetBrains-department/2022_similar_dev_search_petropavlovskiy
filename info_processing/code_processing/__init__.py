import os

from pathlib2 import Path

treesitter_path = f"{Path().cwd().parent}/treesitter"

if not os.path.exists(treesitter_path):
    os.makedirs(treesitter_path)
