from pip._internal.req import parse_requirements

import setuptools

install_reqs = ["fire",
                "dulwich",
                "tqdm"
                "PyGithub",
                "pathlib2",
                "setuptools",
                "pip",
                "tree-sitter",
                "enry"]

setuptools.setup(
    name="similar_dev_search_petropavlovskiy",
    version="0.1",
    description="Similar developers search poject",
    setup_requires=install_reqs,
    packages=setuptools.find_packages(),
    install_requires=install_reqs
)
