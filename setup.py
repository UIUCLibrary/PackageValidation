from setuptools import setup
import os

metadata = dict()
metadata_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dcc_qc', '__version__.py')
with open(metadata_file, 'r', encoding='utf-8') as f:
    exec(f.read(), metadata)


setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    packages=[
        'dcc_qc',
        'dcc_qc.packages',
        'dcc_qc.task_states',
        'dcc_qc.checkers',
        'dcc_qc.profiles',
        'dcc_qc.reports',
        'dcc_qc.validator',
    ],
    test_suite="tests",
    tests_require=['pytest'],
    url=metadata["__url__"],
    entry_points={"console_scripts": ["qcpkg = dcc_qc.cli:main"]},
    license='University of Illinois/NCSA Open Source License',
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    description=metadata["__description__"]
)
