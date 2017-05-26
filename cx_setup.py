from cx_Freeze import setup, Executable
import platform
import pytest
includes = [
    'pkg_resources'
] + pytest.freeze_includes()
setup(
    name='dcc_qc',
    version='0.0.1',
    packages=[
        'dcc_qc',
        'dcc_qc.packages',
        'dcc_qc.task_states',
        'dcc_qc.validators',
        'tests'
    ],
    url='https://github.com/UIUCLibrary/HathiTrustPackaging',
    description='This package is for performing automated quality control tests on file packages',
    executables={
        Executable("dcc_qc/cli.py",
                   targetName=("qcpkg.exe" if platform.system() == "Windows" else "qcpkg"))

    },
    options={"build_exe": {'includes': includes}},

)
