import setuptools

install_reqs = parse_requirements('requirements.txt', session='hack')

setuptools.setup(
    name="similar_dev_search_petropavlovskiy",
    version="0.1",
    description="Similar developers search poject",
    setup_requires=install_reqs,
    packages=setuptools.find_packages(),
    install_requires=install_reqs
)
