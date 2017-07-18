from cx_Freeze import setup, Executable
import platform
import pytest
import dcc_qc

includes = ['pkg_resources'] + pytest.freeze_includes()


def create_msi_tablename(python_name, fullname):
    shortname = python_name[:6].replace("_", "").upper()
    longname = fullname
    return "{}|{}".format(shortname, longname)


EXECUTABLE_NAME = "qcpkg"

directory_table = [
    (
        "ProgramMenuFolder",  # Directory
        "TARGETDIR",  # Directory_parent
        "PMenu|Programs",  # DefaultDir
    ),
    (
        "PMenu",  # Directory
        "ProgramMenuFolder",  # Directory_parent
        create_msi_tablename(dcc_qc.__title__, dcc_qc.FULL_TITLE)
    ),
]
shortcut_table = [
    (
        "startmenuShortcutDoc",  # Shortcut
        "PMenu",  # Directory_
        "{} Documentation".format(create_msi_tablename(dcc_qc.__title__, dcc_qc.FULL_TITLE)),
        "TARGETDIR",  # Component_
        "[TARGETDIR]documentation.url",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        'TARGETDIR'  # WkDir
    ),
]

INCLUDE_FILES = [
    "documentation.url"
]

setup(
    name=dcc_qc.__title__,
    version=dcc_qc.__version__,
    packages=[
        'dcc_qc',
        'dcc_qc.packages',
        'dcc_qc.task_states',
        'dcc_qc.checkers',
        'dcc_qc.profiles',
        'dcc_qc.reports',
        'dcc_qc.validator',
        'tests'
    ],
    url=dcc_qc.__url__,
    description=dcc_qc.__description__,
    executables={
        Executable("dcc_qc/cli.py",
                   targetName=("{}.exe".format(EXECUTABLE_NAME) if platform.system() == "Windows" else EXECUTABLE_NAME))

    },
    options={
        "build_exe": {
            'includes': includes,
            "include_msvcr": True,
            "include_files": INCLUDE_FILES,
            "packages":['six', "appdirs", "packaging"],
        },
        "bdist_msi": {
            "upgrade-code": "{2FB4B947-68DA-45EC-956B-6A9B85D1E060}",
            "data": {
                "Shortcut": shortcut_table,
                "Directory": directory_table
            }
        }

    },

)
