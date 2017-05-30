from setuptools import setup
import dcc_qc
setup(
    name=dcc_qc.__title__,
    version=dcc_qc.__version__,
    packages=[
        'dcc_qc',
        'dcc_qc.packages',
        'dcc_qc.task_states',
        'dcc_qc.validators',
    ],
    test_suite="tests",
    tests_require=['pytest'],
    url=dcc_qc.__url__,
    entry_points={"console_scripts": ["qcpkg = dcc_qc.cli:main"]},
    license='',
    author=dcc_qc.__author__,
    author_email=dcc_qc.__author_email__,
    description=dcc_qc.__description__
)
