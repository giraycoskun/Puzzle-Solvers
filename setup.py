"""Set up
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='myPuzzleSolvers',
    version='0.1',
    author='giraycoskun',
    author_email='giraycoskun@sabanciuniv.edu',
    description='Search Algorithms Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/giraycoskun/myPuzzleSolvers',
    license='MIT',
    packages=['mySearchAlgorithms'],
    install_requires=['heapq'],
)
