import os

from pathlib2 import Path

clone_path = f"{Path().cwd().parent}/repos"

if not os.path.exists(clone_path):
    os.makedirs(clone_path)

