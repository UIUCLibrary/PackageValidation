import os
import shutil
import sys

import pytest

import dcc_qc.checkers.hathi_lab_factory
import pathlib
from dcc_qc.checkers import error_message
from dcc_qc import checkers

BASE_ROOT = "T://"


# =======================
# Fixtures
# =======================
@pytest.fixture(name="access_good", scope="session")
def files_access_good(tmpdir_factory):
    test_files = ["access/7212907/00000001.tif",
                  "access/7212907/00000002.tif",
                  "access/7212907/00000003.tif",
                  "access/7212907/00000004.tif",
                  "access/7212907/00000005.tif",
                  "access/7212907/00000006.tif",
                  "access/7212907/00000007.tif",
                  "access/7212907/00000008.tif",
                  "access/7212907/00000009.tif",
                  "access/7212907/00000010.tif",
                  "access/7212907/00000011.tif",
                  "access/7212907/00000012.tif",
                  "access/7212907/00000013.tif",
                  "access/7212907/00000014.tif",
                  "access/7212907/00000015.tif",
                  "access/7212907/00000016.tif",
                  "access/7212907/00000017.tif",
                  "access/7212907/00000018.tif",
                  "access/7212907/00000019.tif",
                  "access/7212907/00000020.tif",
                  "access/7212907/00000021.tif",
                  "access/7212907/00000022.tif"]

    tmpdir = tmpdir_factory.mktemp("access_good", numbered=False)
    for file_ in test_files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()

    yield str(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture(name="access_7209692", scope="session")
def files_access_bad_7209692(tmpdir_factory):
    """
    Note:
        Images 00000004, 00000008, have incorrect Job Identifier metadata.
        Incorrect: Preservation
        Correct: Access

        Images 00000014, 00000022 have incorrect Title metadata.
        Incorrect: Unica
        Correct: Cavagna Collection

        Image 00000023 missing Credit Line metadata.
        Image 00000026 missing Creator metadata.

    Returns:
    """
    bad_access_files = ["Access_BAD/7209692/00000001.txt",
                        "Access_BAD/7209692/00000002.tif",
                        "Access_BAD/7209692/00000002.txt",
                        "Access_BAD/7209692/00000003.tif",
                        "Access_BAD/7209692/00000003.txt",
                        "Access_BAD/7209692/00000004.tif",
                        "Access_BAD/7209692/00000004.txt",
                        "Access_BAD/7209692/00000005.tif",
                        "Access_BAD/7209692/00000005.txt",
                        "Access_BAD/7209692/00000006.tif",
                        "Access_BAD/7209692/00000006.txt",
                        "Access_BAD/7209692/00000007.tif",
                        "Access_BAD/7209692/00000007.txt",
                        "Access_BAD/7209692/00000008.tif",
                        "Access_BAD/7209692/00000008.txt",
                        "Access_BAD/7209692/00000009.tif",
                        "Access_BAD/7209692/00000009.txt",
                        "Access_BAD/7209692/00000010.tif",
                        "Access_BAD/7209692/00000010.txt",
                        "Access_BAD/7209692/00000011.tif",
                        "Access_BAD/7209692/00000011.txt",
                        "Access_BAD/7209692/00000012.tif",
                        "Access_BAD/7209692/00000012.txt",
                        "Access_BAD/7209692/00000013.tif",
                        "Access_BAD/7209692/00000013.txt",
                        "Access_BAD/7209692/00000014.tif",
                        "Access_BAD/7209692/00000014.txt",
                        "Access_BAD/7209692/00000015.tif",
                        "Access_BAD/7209692/00000015.txt",
                        "Access_BAD/7209692/00000016.tif",
                        "Access_BAD/7209692/00000016.txt",
                        "Access_BAD/7209692/00000017.tif",
                        "Access_BAD/7209692/00000017.txt",
                        "Access_BAD/7209692/00000018.tif",
                        "Access_BAD/7209692/00000018.txt",
                        "Access_BAD/7209692/00000019.tif",
                        "Access_BAD/7209692/00000019.txt",
                        "Access_BAD/7209692/00000020.tif",
                        "Access_BAD/7209692/00000020.txt",
                        "Access_BAD/7209692/00000021.tif",
                        "Access_BAD/7209692/00000021.txt",
                        "Access_BAD/7209692/00000022.tif",
                        "Access_BAD/7209692/00000022.txt",
                        "Access_BAD/7209692/00000023.tif",
                        "Access_BAD/7209692/00000023.txt",
                        "Access_BAD/7209692/00000024.tif",
                        "Access_BAD/7209692/00000024.txt",
                        "Access_BAD/7209692/00000025.tif",
                        "Access_BAD/7209692/00000025.txt",
                        "Access_BAD/7209692/00000026.tif",
                        "Access_BAD/7209692/00000026.txt",
                        "Access_BAD/7209692/checksum.md5",
                        "Access_BAD/7209692/marc.xml",
                        "Access_BAD/7209692/meta.yml",
                        "Access_BAD/7209692/Thumbs.db",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000001.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000001.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000002.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000002.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000003.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000003.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000004.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000004.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000005.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000005.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000006.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000006.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000007.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000007.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000008.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000008.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000009.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000009.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000010.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000010.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000011.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000011.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000012.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000012.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000013.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000013.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000014.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000014.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000015.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000015.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000016.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000016.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000017.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000017.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000018.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000018.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000019.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000019.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000020.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000020.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000021.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000021.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000022.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000022.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000023.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000023.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000024.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000024.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000025.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000025.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000026.tif.cof",
                        "Access_BAD/7209692/CaptureOne/Cache/Proxies/00000026.tif.cop",
                        "Access_BAD/7209692/CaptureOne/Cache/Thumbnails/00000001.tif.[fdafdd01-d550-4a5e-9b41-3d3be329cd87].cot"]
    # tmpdir = tmpdir_factory.getbasetemp()
    tmpdir = tmpdir_factory.mktemp("Access_BAD_7209692", numbered=False)
    for file_ in bad_access_files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    yield str(tmpdir)
    shutil.rmtree(tmpdir)



@pytest.fixture(name="access_7210012", scope="session")
def files_access_bad_7210012(tmpdir_factory):
    """
    Note:
        Images 00000007, 00000016, 00000027, 00000033 have incorrect specs for access files.
        Image and text file 0000020 is named incorrectly (missing one 0).

    Returns:
    """

    files = [
        "Access_BAD/7210012/00000001.tif",
        "Access_BAD/7210012/00000001.txt",
        "Access_BAD/7210012/00000002.tif",
        "Access_BAD/7210012/00000002.txt",
        "Access_BAD/7210012/00000003.tif",
        "Access_BAD/7210012/00000003.txt",
        "Access_BAD/7210012/00000004.tif",
        "Access_BAD/7210012/00000004.txt",
        "Access_BAD/7210012/00000005.tif",
        "Access_BAD/7210012/00000005.txt",
        "Access_BAD/7210012/00000006.tif",
        "Access_BAD/7210012/00000006.txt",
        "Access_BAD/7210012/00000007.tif",
        "Access_BAD/7210012/00000007.txt",
        "Access_BAD/7210012/00000008.tif",
        "Access_BAD/7210012/00000008.txt",
        "Access_BAD/7210012/00000009.tif",
        "Access_BAD/7210012/00000009.txt",
        "Access_BAD/7210012/00000010.tif",
        "Access_BAD/7210012/00000010.txt",
        "Access_BAD/7210012/00000011.tif",
        "Access_BAD/7210012/00000011.txt",
        "Access_BAD/7210012/00000012.tif",
        "Access_BAD/7210012/00000012.txt",
        "Access_BAD/7210012/00000013.tif",
        "Access_BAD/7210012/00000013.txt",
        "Access_BAD/7210012/00000014.tif",
        "Access_BAD/7210012/00000014.txt",
        "Access_BAD/7210012/00000015.tif",
        "Access_BAD/7210012/00000015.txt",
        "Access_BAD/7210012/00000016.tif",
        "Access_BAD/7210012/00000016.txt",
        "Access_BAD/7210012/00000017.tif",
        "Access_BAD/7210012/00000017.txt",
        "Access_BAD/7210012/00000018.tif",
        "Access_BAD/7210012/00000018.txt",
        "Access_BAD/7210012/00000019.tif",
        "Access_BAD/7210012/00000019.txt",
        "Access_BAD/7210012/00000021.tif",
        "Access_BAD/7210012/00000021.txt",
        "Access_BAD/7210012/00000022.tif",
        "Access_BAD/7210012/00000022.txt",
        "Access_BAD/7210012/00000023.tif",
        "Access_BAD/7210012/00000023.txt",
        "Access_BAD/7210012/00000024.tif",
        "Access_BAD/7210012/00000024.txt",
        "Access_BAD/7210012/00000025.tif",
        "Access_BAD/7210012/00000025.txt",
        "Access_BAD/7210012/00000026.tif",
        "Access_BAD/7210012/00000026.txt",
        "Access_BAD/7210012/00000027.tif",
        "Access_BAD/7210012/00000027.txt",
        "Access_BAD/7210012/00000028.tif",
        "Access_BAD/7210012/00000028.txt",
        "Access_BAD/7210012/00000029.tif",
        "Access_BAD/7210012/00000029.txt",
        "Access_BAD/7210012/00000030.tif",
        "Access_BAD/7210012/00000030.txt",
        "Access_BAD/7210012/00000031.tif",
        "Access_BAD/7210012/00000031.txt",
        "Access_BAD/7210012/00000032.tif",
        "Access_BAD/7210012/00000032.txt",
        "Access_BAD/7210012/00000033.tif",
        "Access_BAD/7210012/00000033.txt",
        "Access_BAD/7210012/00000034.tif",
        "Access_BAD/7210012/00000034.txt",
        "Access_BAD/7210012/0000020.tif",
        "Access_BAD/7210012/0000020.txt",
        "Access_BAD/7210012/checksum.md5",
        "Access_BAD/7210012/marc.xml",
        "Access_BAD/7210012/meta.yml",
        "Access_BAD/7210012/Thumbs.db",
    ]
    # tmpdir = tmpdir_factory.mktemp("Access_BAD")
    tmpdir = tmpdir_factory.mktemp("Access_BAD_7210012", numbered=False)

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        with open(os.path.join(full_path, filename), "w"):
            pass
        # pathlib.Path(os.path.join(full_path, filename)).touch()
    yield str(tmpdir)
    shutil.rmtree(tmpdir)
    # # print(, file=sys.stderr)
    # raise Exception(f"here {tmpdir}")


@pytest.fixture(name="access_7210438", scope="session")
def files_access_bad_7210438():
    """
    Note:
        All images have incorrect specs for access files.
        Missing text files.
        Missing checksum, marc, and meta.yml files.

    Returns:
    """

    foo = os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2/DCC/Access_BAD/7210438")))
    for root_, dirs, files in foo:
        for file_ in files:
            print(os.path.join(root_, file_))
    yield foo
    shutil.rmtree(foo)


@pytest.fixture(name="preservation_7208772", scope="session")
def files_preservation_bad_7208772(tmpdir_factory):
    """
    Note:
        All images have incorrect specs for preservation files.
        Missing targets.

    Returns:

    """
    files = [
        "00000001.tif",
        "00000002.tif",
        "00000003.tif",
        "00000004.tif",
        "00000005.tif",
        "00000006.tif",
        "00000007.tif",
        "00000008.tif",
        "00000009.tif",
        "00000010.tif",
        "00000011.tif",
        "00000012.tif",
        "00000013.tif",
        "00000014.tif",
        "00000015.tif",
        "00000016.tif",
        "00000017.tif",
        "00000018.tif",
        "00000019.tif",
        "00000020.tif",
        "00000021.tif",
        "00000022.tif",
        "00000023.tif",
        "00000024.tif",
        "00000025.tif",
        "00000026.tif",
        "00000027.tif",
        "00000028.tif",
        "00000029.tif",
        "00000030.tif",
    ]
    tmpdir = tmpdir_factory.mktemp("7208772", numbered=False)
    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    yield str(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture(name="preservation_7209934", scope="session")
def files_preservation_bad_7209934(tmpdir_factory):
    """
    Note:
        Images 00000005, 00000010, 00000015, 00000020, 00000025 have incorrect specs for preservation files.

    Returns:

    """

    files = [
        "00000001.tif",
        "00000002.tif",
        "00000003.tif",
        "00000004.tif",
        "00000005.tif",
        "00000006.tif",
        "00000007.tif",
        "00000008.tif",
        "00000009.tif",
        "00000010.tif",
        "00000011.tif",
        "00000012.tif",
        "00000013.tif",
        "00000014.tif",
        "00000015.tif",
        "00000016.tif",
        "00000017.tif",
        "00000018.tif",
        "00000019.tif",
        "00000020.tif",
        "00000021.tif",
        "00000022.tif",
        "00000023.tif",
        "00000024.tif",
        "00000025.tif",
        "00000026.tif",
        "00000027.tif",
        "00000028.tif",
        "Target_l_001.tif",
        "Target_l_002.tif",
        "target_r_001.tif",
        "Target_r_002.tif",
    ]
    # tmpdir = os.path.join(tmpdir_factory.getbasetemp(), "7209934")
    tmpdir = tmpdir_factory.mktemp("7209934", numbered=False)
    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    yield str(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture(name="preservation_good", scope="session")
def files_preservation_good(tmpdir_factory):
    """
    Note:
        Contains 6895567 & 7210439
        Both files have correct specs for preservation files.
        Targets present.

    Returns:

    """

    files = [
        "6895567/00000001.tif",
        "6895567/00000002.tif",
        "6895567/00000003.tif",
        "6895567/00000004.tif",
        "6895567/00000005.tif",
        "6895567/00000006.tif",
        "6895567/00000007.tif",
        "6895567/00000008.tif",
        "6895567/00000009.tif",
        "6895567/00000010.tif",
        "6895567/00000011.tif",
        "6895567/00000012.tif",
        "6895567/00000013.tif",
        "6895567/00000014.tif",
        "6895567/00000015.tif",
        "6895567/00000016.tif",
        "6895567/00000017.tif",
        "6895567/00000018.tif",
        "6895567/00000019.tif",
        "6895567/00000020.tif",
        "6895567/00000021.tif",
        "6895567/00000022.tif",
        "6895567/00000023.tif",
        "6895567/00000024.tif",
        "6895567/00000025.tif",
        "6895567/00000026.tif",
        "6895567/00000027.tif",
        "6895567/00000028.tif",
        "6895567/00000029.tif",
        "6895567/00000030.tif",
        "6895567/00000031.tif",
        "6895567/00000032.tif",
        "6895567/00000033.tif",
        "6895567/00000034.tif",
        "6895567/target_l_001.tif",
        "6895567/target_l_002.tif",
        "6895567/target_r_001.tif",
        "6895567/target_r_002.tif",
        "6895567/Thumbs.db",
        "7210439/00000001.tif",
        "7210439/00000002.tif",
        "7210439/00000003.tif",
        "7210439/00000004.tif",
        "7210439/00000005.tif",
        "7210439/00000006.tif",
        "7210439/00000007.tif",
        "7210439/00000008.tif",
        "7210439/00000009.tif",
        "7210439/00000010.tif",
        "7210439/00000011.tif",
        "7210439/00000012.tif",
        "7210439/00000013.tif",
        "7210439/00000014.tif",
        "7210439/00000015.tif",
        "7210439/00000016.tif",
        "7210439/00000017.tif",
        "7210439/00000018.tif",
        "7210439/00000019.tif",
        "7210439/00000020.tif",
        "7210439/00000021.tif",
        "7210439/00000022.tif",
        "7210439/00000023.tif",
        "7210439/00000024.tif",
        "7210439/00000025.tif",
        "7210439/00000026.tif",
        "7210439/target_l_001.tif",
        "7210439/target_l_002.tif",
        "7210439/target_r_001.tif",
        "7210439/target_r_002.tif",
        "7210439/Thumbs.db",

    ]
    tmpdir = tmpdir_factory.mktemp("preservation_good", numbered=False)
    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    yield str(tmpdir)
    shutil.rmtree(tmpdir)



# =======================
# Tests
# =======================

@pytest.mark.skip(reason="No way to test this currently")
def test_access_job_identifier_bad(access_7209692):
    invalid_files = ["00000004.tif", '00000008.tif']

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in os.walk(access_7209692):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


@pytest.mark.skip(reason="No way to test this currently")
def test_access_metadata_title_incorrect(access_7209692):
    invalid_files = ["00000014.tif", '00000022.tif']

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in os.walk(access_7209692):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


@pytest.mark.skip(reason="No way to test this currently")
def test_access_metadata_credit_line_missing(access_7209692):
    invalid_files = ["00000023.tif"]

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in os.walk(access_7209692):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


@pytest.mark.skip(reason="No way to test this currently")
def test_access_metadata_creator_missing(access_7209692):
    invalid_files = ["00000026.tif"]

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in os.walk(access_7209692):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


@pytest.mark.skip(reason="No way to test this currently")
def test_access_specs_incorrect(access_7210012):
    invalid_files = ["00000007.tif",
                     "00000016.tif",
                     "00000027.tif",
                     "00000033.tif"]

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.technical_checker()

    for root, dirs, files in os.walk(access_7210012):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


@pytest.mark.skip(reason="No way to test this currently")
def test_access_specs_correct(access_good):
    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.technical_checker()

    for root, dirs, files in os.walk(access_good):
        for file_ in files:
            file_name = os.path.join(root, file_)
            assert validator.check(file_name) is True


def test_access_file_naming_incorrect(access_7210012):
    invalid_files = ["0000020.tif", "0000020.txt"]

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
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


def test_access_file_naming_correct(access_good):
    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.naming_checker()

    for root, dirs, files in os.walk(access_good):
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_preservation_file_naming_correct(preservation_good):
    validator_factory = dcc_qc.checkers.hathi_lab_factory.PreservationCheckers()
    validator = validator_factory.naming_checker()

    for root, dirs, files in os.walk(preservation_good):
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_access_files_found_all(access_good):
    path = os.path.join(access_good, "access", "7212907")

    validator_factory = dcc_qc.checkers.hathi_lab_factory.AccessCheckers()
    validator = validator_factory.completeness_checker()
    result = validator.check(path)
    assert result.valid


def test_preservation_files_targets_missing(preservation_7208772):
    validator_factory = dcc_qc.checkers.hathi_lab_factory.PreservationCheckers()
    validator = validator_factory.completeness_checker()

    result = validator.check(preservation_7208772)
    assert not result.valid
    for error_ in result.errors:
        assert isinstance(error_, error_message.ValidationError)


@pytest.mark.skip(reason="No way to test this currently")
def test_preservation_incorrect_specs(preservation_7209934):
    invalid_files = ["6895567.tif", "7210439.tif"]

    validator_factory = dcc_qc.checkers.hathi_lab_factory.PreservationCheckers()
    validator = validator_factory.technical_checker()

    for root, dirs, files in os.walk(preservation_7209934):
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_get_suite():
    suite = dcc_qc.checkers.get_check_suite("HathiLab")
    assert isinstance(suite, dcc_qc.checkers.check_suite.HathiLab)
    pass