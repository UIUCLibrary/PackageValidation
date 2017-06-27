import os

import pytest

import dcc_qc.checkers.hathi_submit_factory
import pathlib
from dcc_qc.checkers import error_message
from dcc_qc import checkers

BASE_ROOT = "T://"


# =======================
# Fixtures
# =======================

@pytest.fixture
def hathi_2693684_package(tmpdir):
    files = [
        "2693684/00000001.jp2", "2693684/00000001.txt",
        "2693684/00000002.jp2", "2693684/00000002.txt",
        "2693684/00000003.jp2", "2693684/00000003.txt",
        "2693684/00000004.jp2", "2693684/00000004.txt",
        "2693684/00000005.jp2", "2693684/00000005.txt",
        "2693684/00000006.jp2", "2693684/00000006.txt",
        "2693684/00000007.jp2", "2693684/00000007.txt",
        "2693684/00000008.jp2", "2693684/00000008.txt",
        "2693684/00000009.jp2", "2693684/00000009.txt",
        "2693684/00000010.jp2", "2693684/00000010.txt",
        "2693684/00000011.jp2", "2693684/00000011.txt",
        "2693684/00000012.jp2", "2693684/00000012.txt",
        "2693684/00000013.jp2", "2693684/00000013.txt",
        "2693684/00000014.jp2", "2693684/00000014.txt",
        "2693684/00000015.jp2", "2693684/00000015.txt",
        "2693684/00000016.jp2", "2693684/00000016.txt",
        "2693684/00000017.jp2", "2693684/00000017.txt",
        "2693684/00000018.jp2", "2693684/00000018.txt",
        "2693684/00000019.jp2", "2693684/00000019.txt",
        "2693684/00000020.jp2", "2693684/00000020.txt",
        "2693684/00000021.jp2", "2693684/00000021.txt",
        "2693684/00000022.jp2", "2693684/00000022.txt",
        "2693684/00000023.jp2", "2693684/00000023.txt",
        "2693684/00000024.jp2", "2693684/00000024.txt",
        "2693684/00000025.jp2", "2693684/00000025.txt",
        "2693684/00000026.jp2", "2693684/00000026.txt",
        "2693684/00000027.jp2", "2693684/00000027.txt",
        "2693684/00000028.jp2", "2693684/00000028.txt",
        "2693684/00000029.jp2", "2693684/00000029.txt",
        "2693684/00000030.jp2", "2693684/00000030.txt",
        "2693684/00000031.jp2", "2693684/00000031.txt",
        "2693684/00000032.jp2", "2693684/00000032.txt",
        "2693684/00000033.jp2", "2693684/00000033.txt",
        "2693684/00000034.jp2", "2693684/00000034.txt",
        "2693684/00000035.jp2", "2693684/00000035.txt",
        "2693684/00000036.jp2", "2693684/00000036.txt",
        "2693684/00000037.jp2", "2693684/00000037.txt",
        "2693684/00000038.jp2", "2693684/00000038.txt",
        "2693684/00000039.jp2", "2693684/00000039.txt",
        "2693684/00000040.jp2", "2693684/00000040.txt",
        "2693684/00000041.jp2", "2693684/00000041.txt",
        "2693684/00000042.jp2", "2693684/00000042.txt",
        "2693684/00000043.jp2", "2693684/00000043.txt",
        "2693684/00000044.jp2", "2693684/00000044.txt",
        "2693684/00000045.jp2", "2693684/00000045.txt",
        "2693684/00000046.jp2", "2693684/00000046.txt",
        "2693684/00000047.jp2", "2693684/00000047.txt",
        "2693684/00000048.jp2", "2693684/00000048.txt",
        "2693684/00000049.jp2", "2693684/00000049.txt",
        "2693684/00000050.jp2", "2693684/00000050.txt",
        "2693684/00000051.jp2", "2693684/00000051.txt",
        "2693684/00000052.jp2", "2693684/00000052.txt",
        "2693684/00000053.jp2", "2693684/00000053.txt",
        "2693684/00000054.jp2", "2693684/00000054.txt",
        "2693684/00000055.jp2", "2693684/00000055.txt",
        "2693684/00000056.jp2", "2693684/00000056.txt",
        "2693684/checksum.md5",
        "2693684/marc.xml",
        "2693684/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir @ pytest.fixture


@pytest.fixture
def hathi_2942435_package(tmpdir):
    files = [
        "2942435/00000001.jp2", "2942435/00000001.txt",
        "2942435/00000002.jp2", "2942435/00000002.txt",
        "2942435/00000003.jp2", "2942435/00000003.txt",
        "2942435/00000004.jp2", "2942435/00000004.txt",
        "2942435/00000005.jp2", "2942435/00000005.txt",
        "2942435/00000006.jp2", "2942435/00000006.txt",
        "2942435/00000007.jp2", "2942435/00000007.txt",
        "2942435/00000008.jp2", "2942435/00000008.txt",
        "2942435/00000009.jp2", "2942435/00000009.txt",
        "2942435/00000010.jp2", "2942435/00000010.txt",
        "2942435/00000011.jp2", "2942435/00000011.txt",
        "2942435/00000012.jp2", "2942435/00000012.txt",
        "2942435/00000013.jp2", "2942435/00000013.txt",
        "2942435/00000014.jp2", "2942435/00000014.txt",
        "2942435/00000015.jp2", "2942435/00000015.txt",
        "2942435/00000016.jp2", "2942435/00000016.txt",
        "2942435/00000017.jp2", "2942435/00000017.txt",
        "2942435/00000018.jp2", "2942435/00000018.txt",
        "2942435/00000019.jp2", "2942435/00000019.txt",
        "2942435/00000020.jp2", "2942435/00000020.txt",
        "2942435/00000021.jp2", "2942435/00000021.txt",
        "2942435/00000022.jp2", "2942435/00000022.txt",
        "2942435/00000023.jp2", "2942435/00000023.txt",
        "2942435/00000024.jp2", "2942435/00000024.txt",
        "2942435/00000025.jp2", "2942435/00000025.txt",
        "2942435/00000026.jp2", "2942435/00000026.txt",
        "2942435/00000027.jp2", "2942435/00000027.txt",
        "2942435/00000028.jp2", "2942435/00000028.txt",
        "2942435/00000029.jp2", "2942435/00000029.txt",
        "2942435/00000030.jp2", "2942435/00000030.txt",
        "2942435/00000031.jp2", "2942435/00000031.txt",
        "2942435/00000032.jp2", "2942435/00000032.txt",
        "2942435/00000033.jp2", "2942435/00000033.txt",
        "2942435/00000034.jp2", "2942435/00000034.txt",
        "2942435/00000035.jp2", "2942435/00000035.txt",
        "2942435/00000036.jp2", "2942435/00000036.txt",
        "2942435/00000037.jp2", "2942435/00000037.txt",
        "2942435/00000038.jp2", "2942435/00000038.txt",
        "2942435/00000039.jp2", "2942435/00000039.txt",
        "2942435/00000040.jp2", "2942435/00000040.txt",
        "2942435/00000041.jp2", "2942435/00000041.txt",
        "2942435/00000042.jp2", "2942435/00000042.txt",
        "2942435/00000043.jp2", "2942435/00000043.txt",
        "2942435/00000044.jp2", "2942435/00000044.txt",
        "2942435/00000045.jp2", "2942435/00000045.txt",
        "2942435/00000046.jp2", "2942435/00000046.txt",
        "2942435/00000047.jp2", "2942435/00000047.txt",
        "2942435/00000048.jp2", "2942435/00000048.txt",
        "2942435/00000049.jp2", "2942435/00000049.txt",
        "2942435/00000050.jp2", "2942435/00000050.txt",
        "2942435/00000051.jp2", "2942435/00000051.txt",
        "2942435/00000052.jp2", "2942435/00000052.txt",
        "2942435/00000053.jp2", "2942435/00000053.txt",
        "2942435/00000054.jp2", "2942435/00000054.txt",
        "2942435/00000055.jp2", "2942435/00000055.txt",
        "2942435/00000056.jp2", "2942435/00000056.txt",
        "2942435/checksum.md5",
        "2942435/marc.xml",
        "2942435/meta.yml",
    ]


@pytest.fixture
def hathi_6852190_package(tmpdir):
    files = [
        "6852190/00000001.jp2", "6852190/00000001.txt",
        "6852190/00000002.jp2", "6852190/00000002.txt",
        "6852190/00000003.jp2", "6852190/00000003.txt",
        "6852190/00000004.jp2", "6852190/00000004.txt",
        "6852190/00000005.jp2", "6852190/00000005.txt",
        "6852190/00000006.jp2", "6852190/00000006.txt",
        "6852190/00000007.jp2", "6852190/00000007.txt",
        "6852190/00000008.jp2", "6852190/00000008.txt",
        "6852190/00000009.jp2", "6852190/00000009.txt",
        "6852190/00000010.jp2", "6852190/00000010.txt",
        "6852190/00000011.jp2", "6852190/00000011.txt",
        "6852190/00000012.jp2", "6852190/00000012.txt",
        "6852190/00000013.jp2", "6852190/00000013.txt",
        "6852190/00000014.jp2", "6852190/00000014.txt",
        "6852190/00000015.jp2", "6852190/00000015.txt",
        "6852190/00000016.jp2", "6852190/00000016.txt",
        "6852190/00000017.jp2", "6852190/00000017.txt",
        "6852190/00000018.jp2", "6852190/00000018.txt",
        "6852190/00000019.jp2", "6852190/00000019.txt",
        "6852190/00000020.jp2", "6852190/00000020.txt",
        "6852190/00000021.jp2", "6852190/00000021.txt",
        "6852190/00000022.jp2", "6852190/00000022.txt",
        "6852190/checksum.md5",
        "6852190/marc.xml",
        "6852190/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir

@pytest.fixture
def hathi_7213538_package(tmpdir):
    files = [
        "7213538/00000001.jp2", "7213538/00000001.txt",
        "7213538/00000002.jp2", "7213538/00000002.txt",
        "7213538/00000003.jp2", "7213538/00000003.txt",
        "7213538/00000004.jp2", "7213538/00000004.txt",
        "7213538/00000005.jp2", "7213538/00000005.txt",
        "7213538/00000006.jp2", "7213538/00000006.txt",
        "7213538/00000007.jp2", "7213538/00000007.txt",
        "7213538/00000008.jp2", "7213538/00000008.txt",
        "7213538/00000009.jp2", "7213538/00000009.txt",
        "7213538/00000010.jp2", "7213538/00000010.txt",
        "7213538/00000011.jp2", "7213538/00000011.txt",
        "7213538/00000012.jp2", "7213538/00000012.txt",
        "7213538/00000013.jp2", "7213538/00000013.txt",
        "7213538/00000014.jp2", "7213538/00000014.txt",
        "7213538/00000015.jp2", "7213538/00000015.txt",
        "7213538/00000016.jp2", "7213538/00000016.txt",
        "7213538/00000017.jp2", "7213538/00000017.txt",
        "7213538/00000018.jp2", "7213538/00000018.txt",
        "7213538/00000019.jp2", "7213538/00000019.txt",
        "7213538/00000020.jp2", "7213538/00000020.txt",
        "7213538/00000021.jp2", "7213538/00000021.txt",
        "7213538/00000022.jp2", "7213538/00000022.txt",
        "7213538/00000023.jp2", "7213538/00000023.txt",
        "7213538/00000024.jp2", "7213538/00000024.txt",
        "7213538/00000025.jp2", "7213538/00000025.txt",
        "7213538/00000026.jp2", "7213538/00000026.txt",
        "7213538/00000027.jp2", "7213538/00000027.txt",
        "7213538/00000028.jp2", "7213538/00000028.txt",
        "7213538/00000029.jp2", "7213538/00000029.txt",
        "7213538/00000030.jp2", "7213538/00000030.txt",
        "7213538/00000031.jp2", "7213538/00000031.txt",
        "7213538/00000032.jp2", "7213538/00000032.txt",
        "7213538/00000033.jp2", "7213538/00000033.txt",
        "7213538/00000034.jp2", "7213538/00000034.txt",
        "7213538/00000035.jp2", "7213538/00000035.txt",
        "7213538/00000036.jp2", "7213538/00000036.txt",
        "7213538/00000037.jp2", "7213538/00000037.txt",
        "7213538/00000038.jp2", "7213538/00000038.txt",
        "7213538/00000039.jp2", "7213538/00000039.txt",
        "7213538/00000040.jp2", "7213538/00000040.txt",
        "7213538/00000041.jp2", "7213538/00000041.txt",
        "7213538/00000042.jp2", "7213538/00000042.txt",
        "7213538/00000043.jp2", "7213538/00000043.txt",
        "7213538/00000044.jp2", "7213538/00000044.txt",
        "7213538/00000045.jp2", "7213538/00000045.txt",
        "7213538/00000046.jp2", "7213538/00000046.txt",
        "7213538/00000047.jp2", "7213538/00000047.txt",
        "7213538/00000048.jp2", "7213538/00000048.txt",
        "7213538/00000049.jp2", "7213538/00000049.txt",
        "7213538/00000050.jp2", "7213538/00000050.txt",
        "7213538/00000051.jp2", "7213538/00000051.txt",
        "7213538/00000052.jp2", "7213538/00000052.txt",
        "7213538/00000053.jp2", "7213538/00000053.txt",
        "7213538/00000054.jp2", "7213538/00000054.txt",
        "7213538/checksum.md5",
        "7213538/marc.xml",
        "7213538/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir


@pytest.fixture
def hathi_7213857_package(tmpdir):
    files = [
        "7213857/00000001.jp2", "7213857/00000001.txt",
        "7213857/00000002.jp2", "7213857/00000002.txt",
        "7213857/00000003.jp2", "7213857/00000003.txt",
        "7213857/00000004.jp2", "7213857/00000004.txt",
        "7213857/00000005.jp2", "7213857/00000005.txt",
        "7213857/00000006.jp2", "7213857/00000006.txt",
        "7213857/00000007.jp2", "7213857/00000007.txt",
        "7213857/00000008.jp2", "7213857/00000008.txt",
        "7213857/00000009.jp2", "7213857/00000009.txt",
        "7213857/00000010.jp2", "7213857/00000010.txt",
        "7213857/00000011.jp2", "7213857/00000011.txt",
        "7213857/00000012.jp2", "7213857/00000012.txt",
        "7213857/00000013.jp2", "7213857/00000013.txt",
        "7213857/00000014.jp2", "7213857/00000014.txt",
        "7213857/00000015.jp2", "7213857/00000015.txt",
        "7213857/00000016.jp2", "7213857/00000016.txt",
        "7213857/00000017.jp2", "7213857/00000017.txt",
        "7213857/00000018.jp2", "7213857/00000018.txt",
        "7213857/checksum.md5",
        "7213857/marc.xml",
        "7213857/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir


@pytest.fixture
def hathi_7213932_package(tmpdir):
    files = [
        "7213932/00000001.jp2", "7213932/00000001.txt",
        "7213932/00000002.jp2", "7213932/00000002.txt",
        "7213932/00000003.jp2", "7213932/00000003.txt",
        "7213932/00000004.jp2", "7213932/00000004.txt",
        "7213932/00000005.jp2", "7213932/00000005.txt",
        "7213932/00000006.jp2", "7213932/00000006.txt",
        "7213932/00000007.jp2", "7213932/00000007.txt",
        "7213932/00000008.jp2", "7213932/00000008.txt",
        "7213932/00000009.jp2", "7213932/00000009.txt",
        "7213932/00000010.jp2", "7213932/00000010.txt",
        "7213932/00000011.jp2", "7213932/00000011.txt",
        "7213932/00000012.jp2", "7213932/00000012.txt",
        "7213932/00000013.jp2", "7213932/00000013.txt",
        "7213932/00000014.jp2", "7213932/00000014.txt",
        "7213932/00000015.jp2", "7213932/00000015.txt",
        "7213932/00000016.jp2", "7213932/00000016.txt",
        "7213932/00000017.jp2", "7213932/00000017.txt",
        "7213932/00000018.jp2", "7213932/00000018.txt",
        "7213932/00000019.jp2", "7213932/00000019.txt",
        "7213932/00000020.jp2", "7213932/00000020.txt",
        "7213932/00000021.jp2", "7213932/00000021.txt",
        "7213932/00000022.jp2", "7213932/00000022.txt",
        "7213932/00000023.jp2", "7213932/00000023.txt",
        "7213932/00000024.jp2", "7213932/00000024.txt",
        "7213932/00000025.jp2", "7213932/00000025.txt",
        "7213932/00000026.jp2", "7213932/00000026.txt",
        "7213932/00000027.jp2", "7213932/00000027.txt",
        "7213932/00000028.jp2", "7213932/00000028.txt",
        "7213932/00000029.jp2", "7213932/00000029.txt",
        "7213932/00000030.jp2", "7213932/00000030.txt",
        "7213932/00000031.jp2", "7213932/00000031.txt",
        "7213932/00000032.jp2", "7213932/00000032.txt",
        "7213932/00000033.jp2", "7213932/00000033.txt",
        "7213932/00000034.jp2", "7213932/00000034.txt",
        "7213932/checksum.md5",
        "7213932/marc.xml",
        "7213932/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir


@pytest.fixture
def hathi_7214043_package(tmpdir):
    files = [
        "7214043/00000001.jp2", "7214043/00000001.txt",
        "7214043/00000002.jp2", "7214043/00000002.txt",
        "7214043/00000003.jp2", "7214043/00000003.txt",
        "7214043/00000004.jp2", "7214043/00000004.txt",
        "7214043/00000005.jp2", "7214043/00000005.txt",
        "7214043/00000006.jp2", "7214043/00000006.txt",
        "7214043/00000007.jp2", "7214043/00000007.txt",
        "7214043/00000008.jp2", "7214043/00000008.txt",
        "7214043/00000009.jp2", "7214043/00000009.txt",
        "7214043/00000010.jp2", "7214043/00000010.txt",
        "7214043/00000011.jp2", "7214043/00000011.txt",
        "7214043/00000012.jp2", "7214043/00000012.txt",
        "7214043/00000013.jp2", "7214043/00000013.txt",
        "7214043/00000014.jp2", "7214043/00000014.txt",
        "7214043/00000015.jp2", "7214043/00000015.txt",
        "7214043/00000016.jp2", "7214043/00000016.txt",
        "7214043/00000017.jp2", "7214043/00000017.txt",
        "7214043/00000018.jp2", "7214043/00000018.txt",
        "7214043/00000019.jp2", "7214043/00000019.txt",
        "7214043/00000020.jp2", "7214043/00000020.txt",
        "7214043/00000021.jp2", "7214043/00000021.txt",
        "7214043/00000022.jp2", "7214043/00000022.txt",
        "7214043/00000023.jp2", "7214043/00000023.txt",
        "7214043/00000024.jp2", "7214043/00000024.txt",
        "7214043/00000025.jp2", "7214043/00000025.txt",
        "7214043/00000026.jp2", "7214043/00000026.txt",
        "7214043/00000027.jp2", "7214043/00000027.txt",
        "7214043/00000028.jp2", "7214043/00000028.txt",
        "7214043/00000029.jp2", "7214043/00000029.txt",
        "7214043/00000030.jp2", "7214043/00000030.txt",
        "7214043/00000031.jp2", "7214043/00000031.txt",
        "7214043/00000032.jp2", "7214043/00000032.txt",
        "7214043/00000033.jp2", "7214043/00000033.txt",
        "7214043/00000034.jp2", "7214043/00000034.txt",
        "7214043/00000035.jp2", "7214043/00000035.txt",
        "7214043/00000036.jp2", "7214043/00000036.txt",
        "7214043/00000037.jp2", "7214043/00000037.txt",
        "7214043/00000038.jp2", "7214043/00000038.txt",
        "7214043/00000039.jp2", "7214043/00000039.txt",
        "7214043/00000040.jp2", "7214043/00000040.txt",
        "7214043/00000041.jp2", "7214043/00000041.txt",
        "7214043/00000042.jp2", "7214043/00000042.txt",
        "7214043/00000043.jp2", "7214043/00000043.txt",
        "7214043/00000044.jp2", "7214043/00000044.txt",
        "7214043/00000045.jp2", "7214043/00000045.txt",
        "7214043/00000046.jp2", "7214043/00000046.txt",
        "7214043/00000047.jp2", "7214043/00000047.txt",
        "7214043/00000048.jp2", "7214043/00000048.txt",
        "7214043/00000049.jp2", "7214043/00000049.txt",
        "7214043/00000050.jp2", "7214043/00000050.txt",
        "7214043/00000051.jp2", "7214043/00000051.txt",
        "7214043/00000052.jp2", "7214043/00000052.txt",
        "7214043/00000053.jp2", "7214043/00000053.txt",
        "7214043/00000054.jp2", "7214043/00000054.txt",
        "7214043/00000055.jp2", "7214043/00000055.txt",
        "7214043/00000056.jp2", "7214043/00000056.txt",
        "7214043/00000057.jp2", "7214043/00000057.txt",
        "7214043/00000058.jp2", "7214043/00000058.txt",
        "7214043/00000059.jp2", "7214043/00000059.txt",
        "7214043/00000060.jp2", "7214043/00000060.txt",
        "7214043/00000061.jp2", "7214043/00000061.txt",
        "7214043/00000062.jp2", "7214043/00000062.txt",
        "7214043/00000063.jp2", "7214043/00000063.txt",
        "7214043/00000064.jp2", "7214043/00000064.txt",
        "7214043/00000065.jp2", "7214043/00000065.txt",
        "7214043/00000066.jp2", "7214043/00000066.txt",
        "7214043/00000067.jp2", "7214043/00000067.txt",
        "7214043/00000068.jp2", "7214043/00000068.txt",
        "7214043/00000069.jp2", "7214043/00000069.txt",
        "7214043/00000070.jp2", "7214043/00000070.txt",
        "7214043/00000071.jp2", "7214043/00000071.txt",
        "7214043/00000072.jp2", "7214043/00000072.txt",
        "7214043/00000073.jp2", "7214043/00000073.txt",
        "7214043/00000074.jp2", "7214043/00000074.txt",
        "7214043/checksum.md5",
        "7214043/marc.xml",
        "7214043/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir@pytest.fixture

@pytest.fixture
def hathi_7215655_package(tmpdir):
    files = [
        "7215655/00000001.jp2", "7215655/00000001.txt",
        "7215655/00000002.jp2", "7215655/00000002.txt",
        "7215655/00000003.jp2", "7215655/00000003.txt",
        "7215655/00000004.jp2", "7215655/00000004.txt",
        "7215655/00000005.jp2", "7215655/00000005.txt",
        "7215655/00000006.jp2", "7215655/00000006.txt",
        "7215655/00000007.jp2", "7215655/00000007.txt",
        "7215655/00000008.jp2", "7215655/00000008.txt",
        "7215655/00000009.jp2", "7215655/00000009.txt",
        "7215655/00000010.jp2", "7215655/00000010.txt",
        "7215655/00000011.jp2", "7215655/00000011.txt",
        "7215655/00000012.jp2", "7215655/00000012.txt",
        "7215655/00000013.jp2", "7215655/00000013.txt",
        "7215655/00000014.jp2", "7215655/00000014.txt",
        "7215655/00000015.jp2", "7215655/00000015.txt",
        "7215655/00000016.jp2", "7215655/00000016.txt",
        "7215655/00000017.jp2", "7215655/00000017.txt",
        "7215655/00000018.jp2", "7215655/00000018.txt",
        "7215655/00000019.jp2", "7215655/00000019.txt",
        "7215655/00000020.jp2", "7215655/00000020.txt",
        "7215655/checksum.md5",
        "7215655/marc.xml",
        "7215655/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir

@pytest.fixture
def hathi_7215682_package(tmpdir):
    files = [
        "7215682/00000001.jp2", "7215682/00000001.txt",
        "7215682/00000002.jp2", "7215682/00000002.txt",
        "7215682/00000003.jp2", "7215682/00000003.txt",
        "7215682/00000004.jp2", "7215682/00000004.txt",
        "7215682/00000005.jp2", "7215682/00000005.txt",
        "7215682/00000006.jp2", "7215682/00000006.txt",
        "7215682/00000007.jp2", "7215682/00000007.txt",
        "7215682/00000008.jp2", "7215682/00000008.txt",
        "7215682/00000009.jp2", "7215682/00000009.txt",
        "7215682/00000010.jp2", "7215682/00000010.txt",
        "7215682/00000011.jp2", "7215682/00000011.txt",
        "7215682/00000012.jp2", "7215682/00000012.txt",
        "7215682/00000013.jp2", "7215682/00000013.txt",
        "7215682/00000014.jp2", "7215682/00000014.txt",
        "7215682/00000015.jp2", "7215682/00000015.txt",
        "7215682/00000016.jp2", "7215682/00000016.txt",
        "7215682/00000017.jp2", "7215682/00000017.txt",
        "7215682/00000018.jp2", "7215682/00000018.txt",
        "7215682/checksum.md5",
        # "7215682/marc.xml", # MISSING marc
        "7215682/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir


@pytest.fixture
def hathi_7215700_package(tmpdir):
    files = [
        "7215700/00000001.jp2", "7215700/00000001.txt",
        "7215700/00000002.jp2", "7215700/00000002.txt",
        "7215700/00000003.jp2", "7215700/00000003.txt",
        "7215700/00000004.jp2", "7215700/00000004.txt",
        "7215700/00000005.jp2", "7215700/00000005.txt",
        "7215700/00000006.jp2", "7215700/00000006.txt",
        "7215700/00000007.jp2", "7215700/00000007.txt",
        "7215700/00000008.jp2", "7215700/00000008.txt",
        "7215700/00000009.jp2", "7215700/00000009.txt",
        "7215700/00000010.jp2", "7215700/00000010.txt",
        "7215700/00000011.jp2", "7215700/00000011.txt",
        "7215700/00000012.jp2", "7215700/00000012.txt",
        "7215700/00000013.jp2", "7215700/00000013.txt",
        "7215700/00000014.jp2", "7215700/00000014.txt",
        "7215700/00000015.jp2", "7215700/00000015.txt",
        "7215700/00000016.jp2", "7215700/00000016.txt",
        "7215700/00000017.jp2", "7215700/00000017.txt",
        "7215700/00000018.jp2", "7215700/00000018.txt",
        "7215700/00000019.jp2", "7215700/00000019.txt",
        "7215700/00000020.jp2", "7215700/00000020.txt",
        "7215700/00000021.jp2", "7215700/00000021.txt",
        "7215700/00000022.jp2", "7215700/00000022.txt",
        "7215700/00000023.jp2", "7215700/00000023.txt",
        "7215700/00000024.jp2", "7215700/00000024.txt",
        "7215700/00000025.jp2", "7215700/00000025.txt",
        "7215700/00000026.jp2", "7215700/00000026.txt",
        # "7215700/checksum.md5", # MISSING CHECKSUM
        "7215700/marc.xml",
        "7215700/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir

@pytest.fixture
def hathi_7465982_package(tmpdir):
    files = [
        "7465982/00000001.jp2",
        "7465982/00000002.jp2", "7465982/00000002.txt",
        "7465982/00000003.jp2", "7465982/00000003.txt",
        "7465982/00000004.jp2",
        "7465982/00000005.jp2", "7465982/00000005.txt",
        "7465982/00000006.jp2", "7465982/00000006.txt",
        "7465982/00000007.jp2", "7465982/00000007.txt",
        "7465982/00000008.jp2", "7465982/00000008.txt",
        "7465982/00000009.jp2", "7465982/00000009.txt",
        "7465982/00000010.jp2", "7465982/00000010.txt",
        "7465982/00000011.jp2", "7465982/00000011.txt",
        "7465982/00000012.jp2", "7465982/00000012.txt",
        "7465982/00000013.jp2", "7465982/00000013.txt",
        "7465982/00000014.jp2", "7465982/00000014.txt",
        "7465982/00000015.jp2", "7465982/00000015.txt",
        "7465982/00000016.jp2", "7465982/00000016.txt",
        "7465982/00000017.jp2", "7465982/00000017.txt",
        "7465982/00000018.jp2", "7465982/00000018.txt",
        "7465982/00000019.jp2", "7465982/00000019.txt",
        "7465982/00000020.jp2", "7465982/00000020.txt",
        "7465982/00000021.jp2", "7465982/00000021.txt",
        "7465982/00000022.jp2", "7465982/00000022.txt",
        "7465982/00000023.jp2", "7465982/00000023.txt",
        "7465982/00000024.jp2", "7465982/00000024.txt",
        "7465982/00000025.jp2", "7465982/00000025.txt",
        "7465982/00000026.jp2", "7465982/00000026.txt",
        "7465982/00000027.jp2", "7465982/00000027.txt",
        "7465982/00000028.jp2", "7465982/00000028.txt",
        "7465982/00000029.jp2", "7465982/00000029.txt",
        "7465982/00000030.jp2", "7465982/00000030.txt",
        "7465982/00000031.jp2", "7465982/00000031.txt",
        "7465982/00000032.jp2", "7465982/00000032.txt",
        "7465982/00000033.jp2", "7465982/00000033.txt",
        "7465982/00000034.jp2", "7465982/00000034.txt",
        "7465982/checksum.md5",
        "7465982/marc.xml",
        "7465982/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir

@pytest.fixture
def hathi_8102529_package(tmpdir):
    files = [
        "8102529/00000001.jp2", "8102529/00000001.txt",
        "8102529/00000002.jp2", "8102529/00000002.txt",
        "8102529/00000003.jp2", "8102529/00000003.txt",
        "8102529/00000004.jp2", "8102529/00000004.txt",
        "8102529/00000005.jp2", "8102529/00000005.txt",
        "8102529/00000006.jp2", "8102529/00000006.txt",
        "8102529/00000007.jp2", "8102529/00000007.txt",
        "8102529/00000008.jp2", "8102529/00000008.txt",
        "8102529/00000009.jp2", "8102529/00000009.txt",
        "8102529/00000010.jp2", "8102529/00000010.txt",
        "8102529/00000011.jp2", "8102529/00000011.txt",
        "8102529/00000012.jp2", "8102529/00000012.txt",
        "8102529/00000013.jp2", "8102529/00000013.txt",
        "8102529/00000014.jp2", "8102529/00000014.txt",
        "8102529/00000015.jp2", "8102529/00000015.txt",
        "8102529/00000016.jp2", "8102529/00000016.txt",
        "8102529/00000017.jp2", "8102529/00000017.txt",
        "8102529/00000018.jp2", "8102529/00000018.txt",
        "8102529/00000019.jp2", "8102529/00000019.txt",
        "8102529/00000020.jp2", "8102529/00000020.txt",
        "8102529/00000021.jp2", "8102529/00000021.txt",
        "8102529/00000022.jp2", "8102529/00000022.txt",
        "8102529/00000023.jp2", "8102529/00000023.txt",
        "8102529/00000024.jp2", "8102529/00000024.txt",
        "8102529/00000025.jp2", "8102529/00000025.txt",
        "8102529/00000026.jp2", "8102529/00000026.txt",
        "8102529/checksum.md5",
        "8102529/marc.xml",
        "8102529/meta.yml",
    ]

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    return tmpdir


# =======================
# Tests
# =======================
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_job_identifier_bad(access_7209692):
#     invalid_files = ["00000004.tif", '00000008.tif']
#
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.metadata_checker()
#
#     for root, dirs, files in os.walk(access_7209692):
#         for file_ in files:
#
#             file_name = os.path.join(root, file_)
#             result = validator.check(file_name)
#             if file_ in invalid_files:
#                 assert not result.valid
#             else:
#                 assert result.valid is True
#
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_metadata_title_incorrect(access_7209692):
#     invalid_files = ["00000014.tif", '00000022.tif']
#
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.metadata_checker()
#
#     for root, dirs, files in os.walk(access_7209692):
#         for file_ in files:
#
#             file_name = os.path.join(root, file_)
#             result = validator.check(file_name)
#             if file_ in invalid_files:
#                 assert not result.valid
#             else:
#                 assert result.valid is True
#
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_metadata_credit_line_missing(access_7209692):
#     invalid_files = ["00000023.tif"]
#
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.metadata_checker()
#
#     for root, dirs, files in os.walk(access_7209692):
#         for file_ in files:
#
#             file_name = os.path.join(root, file_)
#             result = validator.check(file_name)
#             if file_ in invalid_files:
#                 assert not result.valid
#             else:
#                 assert result.valid is True
#
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_metadata_creator_missing(access_7209692):
#     invalid_files = ["00000026.tif"]
#
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.metadata_checker()
#
#     for root, dirs, files in os.walk(access_7209692):
#         for file_ in files:
#
#             file_name = os.path.join(root, file_)
#             result = validator.check(file_name)
#             if file_ in invalid_files:
#                 assert not result.valid
#             else:
#                 assert result.valid is True
#
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_specs_incorrect(access_7210012):
#     invalid_files = ["00000007.tif",
#                      "00000016.tif",
#                      "00000027.tif",
#                      "00000033.tif"]
#
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.technical_checker()
#
#     for root, dirs, files in os.walk(access_7210012):
#         for file_ in files:
#
#             file_name = os.path.join(root, file_)
#             result = validator.check(file_name)
#             if file_ in invalid_files:
#                 assert not result.valid
#             else:
#                 assert result.valid is True
#
#
# @pytest.mark.skip(reason="No way to test this currently")
# def test_access_specs_correct(access_good):
#     validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
#     validator = validator_factory.technical_checker()
#
#     for root, dirs, files in os.walk(access_good):
#         for file_ in files:
#             file_name = os.path.join(root, file_)
#             assert validator.check(file_name) is True

@pytest.mark.skip(reason="no files named incorrectly")
def test_access_file_naming_incorrect(access_7210012):
    invalid_files = ["0000020.tif", "0000020.txt"]

    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.naming_checker()

    for root, dirs, files in os.walk(access_7210012):
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files or os.path.splitext(file_name)[1] != ".tif":
                assert not result.valid, "The file {} was NOT listed as invalid".format(file_)
                for error_ in result.errors:
                    assert isinstance(error_, error_message.ValidationError)
            else:
                assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_access_file_naming_correct(hathi_8102529_package):
    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.naming_checker()

    for root, dirs, files in os.walk(hathi_8102529_package):
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            assert result.valid is True, "The file {} was listed as invalid".format(file_)



def test_access_files_found_all(hathi_8102529_package):
    path = os.path.join(hathi_8102529_package, "8102529")

    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.completeness_checker()
    result = validator.check(path)
    if result.errors:
        for error in result.errors:
            print(error.message)
    assert result.valid


def test_access_files_missing_ocr(hathi_7465982_package):
    path = os.path.join(hathi_7465982_package, "7465982")

    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.completeness_checker()
    result = validator.check(path)
    assert not result.valid
    for error in result.errors:
        print(error.message)


def test_access_files_missing_checksum(hathi_7215700_package):
    path = os.path.join(hathi_7215700_package, "7215700")

    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.completeness_checker()
    result = validator.check(path)
    assert not result.valid
    for error in result.errors:
        # Missing checksum.md5
        print(error.message)


def test_access_files_missing_marc(hathi_7215682_package):
    path = os.path.join(hathi_7215682_package, "7215682")

    validator_factory = dcc_qc.checkers.hathi_submit_factory.AccessCheckers()
    validator = validator_factory.completeness_checker()
    result = validator.check(path)
    assert not result.valid
    for error in result.errors:
        # Missing marc.xml
        print(error.message)

