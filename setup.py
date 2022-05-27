import setuptools

setuptools.setup(
    name="similar_dev_search_petropavlovskiy",
    version="0.1",
    description="Similar developers search poject",
    setup_requires=["fire", "dulwich", "tqdm", "enry"],
    packages=setuptools.find_packages(),
    install_requires=["fire", "dulwich", "tqdm", "enry"]
)
