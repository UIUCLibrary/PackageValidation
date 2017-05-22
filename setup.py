from setuptools import setup

setup(
    name='dcc_qc',
    version='0.0.1a',
    packages=['dcc_qc'],
    test_suite="tests",
    tests_require=['pytest'],
    url='https://github.com/UIUCLibrary/HathiTrustPackaging',
    entry_points={"console_scripts": ["qc = dcc_qc.cli:main"]},
    license='',
    author='Henry Borchers',
    author_email='hborcher@illinois.edu',
    description='This package is for performing automated quality control tests on file packages'
)
