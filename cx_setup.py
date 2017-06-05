from cx_Freeze import setup, Executable
import platform
import pytest
import dcc_qc

includes = ['pkg_resources'] + pytest.freeze_includes()
setup(
    name=dcc_qc.__title__,
    version=dcc_qc.__version__,
    packages=[
        'dcc_qc',
        'dcc_qc.packages',
        'dcc_qc.task_states',
        'dcc_qc.validators',
        'tests'
    ],
    url=dcc_qc.__url__,
    description=dcc_qc.__description__,
    executables={
        Executable("dcc_qc/cli.py",
                   targetName=("qcpkg.exe" if platform.system() == "Windows" else "qcpkg"))

    },
    options={"build_exe": {
                'includes': includes,
                "include_msvcr": True
            }
    },

)
