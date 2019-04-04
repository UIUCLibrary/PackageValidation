import os
import pathlib
import shutil

import pytest
from dcc_qc import packages

TEST_PATH = r"T:\HenryTest-PSR_2\DCC\Package_GOOD\\20170424_CavagnaCollectionRBML_tg"


@pytest.fixture(scope="session")
def hathi_sample_package(tmpdir_factory):
    files = [
        "access/7212907/00000001.tif", "access/7212907/00000002.tif",
        "access/7212907/00000003.tif", "access/7212907/00000004.tif",
        "access/7212907/00000005.tif", "access/7212907/00000006.tif",
        "access/7212907/00000007.tif", "access/7212907/00000008.tif",
        "access/7212907/00000009.tif", "access/7212907/00000010.tif",
        "access/7212907/00000011.tif", "access/7212907/00000012.tif",
        "access/7212907/00000013.tif", "access/7212907/00000014.tif",
        "access/7212907/00000015.tif", "access/7212907/00000016.tif",
        "access/7212907/00000017.tif", "access/7212907/00000018.tif",
        "access/7212907/00000019.tif", "access/7212907/00000020.tif",
        "access/7212907/00000021.tif", "access/7212907/00000022.tif",
        "access/7212907/Thumbs.db", "access/7212938/00000001.tif",
        "access/7212938/00000002.tif", "access/7212938/00000003.tif",
        "access/7212938/00000004.tif", "access/7212938/00000005.tif",
        "access/7212938/00000006.tif", "access/7212938/00000007.tif",
        "access/7212938/00000008.tif", "access/7212938/00000009.tif",
        "access/7212938/00000010.tif", "access/7212938/00000011.tif",
        "access/7212938/00000012.tif", "access/7212938/00000013.tif",
        "access/7212938/00000014.tif", "access/7212938/00000015.tif",
        "access/7212938/00000016.tif", "access/7212938/00000017.tif",
        "access/7212938/00000018.tif", "access/7212938/00000019.tif",
        "access/7212938/00000020.tif", "access/7212938/00000021.tif",
        "access/7212938/00000022.tif", "access/7212938/00000023.tif",
        "access/7212938/00000024.tif", "access/7212938/00000025.tif",
        "access/7212938/00000026.tif", "access/7212938/00000027.tif",
        "access/7212938/00000028.tif", "access/7212938/00000029.tif",
        "access/7212938/00000030.tif", "access/7212938/00000031.tif",
        "access/7212938/00000032.tif", "access/7212938/00000033.tif",
        "access/7212938/00000034.tif", "access/7212938/00000035.tif",
        "access/7212938/00000036.tif", "access/7212938/00000037.tif",
        "access/7212938/00000038.tif", "access/7212938/00000039.tif",
        "access/7212938/00000040.tif", "access/7212938/00000041.tif",
        "access/7212938/00000042.tif", "access/7212938/00000043.tif",
        "access/7212938/00000044.tif", "access/7212938/00000045.tif",
        "access/7212938/00000046.tif", "access/7212938/00000047.tif",
        "access/7212938/00000048.tif", "access/7212938/00000049.tif",
        "access/7212938/00000050.tif", "access/7212938/00000051.tif",
        "access/7212938/00000052.tif", "access/7212938/00000053.tif",
        "access/7212938/00000054.tif", "access/7212938/00000055.tif",
        "access/7212938/00000056.tif", "access/7212938/00000057.tif",
        "access/7212938/00000058.tif", "access/7212938/00000059.tif",
        "access/7212938/00000060.tif", "access/7212938/00000061.tif",
        "access/7212938/00000062.tif", "access/7212938/00000063.tif",
        "access/7212938/00000064.tif", "access/7212938/00000065.tif",
        "access/7212938/00000066.tif", "access/7212938/00000067.tif",
        "access/7212938/00000068.tif", "access/7212938/00000069.tif",
        "access/7212938/00000070.tif", "access/7212938/Thumbs.db",
        "access/7212977/00000001.tif", "access/7212977/00000002.tif",
        "access/7212977/00000003.tif", "access/7212977/00000004.tif",
        "access/7212977/00000005.tif", "access/7212977/00000006.tif",
        "access/7212977/00000007.tif", "access/7212977/00000008.tif",
        "access/7212977/00000009.tif", "access/7212977/00000010.tif",
        "access/7212977/00000011.tif", "access/7212977/00000012.tif",
        "access/7212977/00000013.tif", "access/7212977/00000014.tif",
        "access/7212977/00000015.tif", "access/7212977/00000016.tif",
        "access/7212977/00000017.tif", "access/7212977/00000018.tif",
        "access/7212977/00000019.tif", "access/7212977/00000020.tif",
        "access/7212977/00000021.tif", "access/7212977/00000022.tif",
        "access/7212977/00000023.tif", "access/7212977/00000024.tif",
        "access/7212977/00000025.tif", "access/7212977/00000026.tif",
        "access/7212977/Thumbs.db", "access/7212995/00000001.tif",
        "access/7212995/00000002.tif", "access/7212995/00000003.tif",
        "access/7212995/00000004.tif", "access/7212995/00000005.tif",
        "access/7212995/00000006.tif", "access/7212995/00000007.tif",
        "access/7212995/00000008.tif", "access/7212995/00000009.tif",
        "access/7212995/00000010.tif", "access/7212995/00000011.tif",
        "access/7212995/00000012.tif", "access/7212995/00000013.tif",
        "access/7212995/00000014.tif", "access/7212995/00000015.tif",
        "access/7212995/00000016.tif", "access/7212995/00000017.tif",
        "access/7212995/00000018.tif", "access/7212995/00000019.tif",
        "access/7212995/00000020.tif", "access/7212995/00000021.tif",
        "access/7212995/00000022.tif", "access/7212995/00000023.tif",
        "access/7212995/00000024.tif", "access/7212995/Thumbs.db",
        "access/7213108/00000001.tif", "access/7213108/00000002.tif",
        "access/7213108/00000003.tif", "access/7213108/00000004.tif",
        "access/7213108/00000005.tif", "access/7213108/00000006.tif",
        "access/7213108/00000007.tif", "access/7213108/00000008.tif",
        "access/7213108/00000009.tif", "access/7213108/00000010.tif",
        "access/7213108/00000011.tif", "access/7213108/00000012.tif",
        "access/7213108/00000013.tif", "access/7213108/00000014.tif",
        "access/7213108/00000015.tif", "access/7213108/00000016.tif",
        "access/7213108/00000017.tif", "access/7213108/00000018.tif",
        "access/7213108/00000019.tif", "access/7213108/00000020.tif",
        "access/7213108/00000021.tif", "access/7213108/00000022.tif",
        "access/7213108/00000023.tif", "access/7213108/00000024.tif",
        "access/7213108/00000025.tif", "access/7213108/00000026.tif",
        "access/7213108/Thumbs.db", "access/7213163/00000001.tif",
        "access/7213163/00000002.tif", "access/7213163/00000003.tif",
        "access/7213163/00000004.tif", "access/7213163/00000005.tif",
        "access/7213163/00000006.tif", "access/7213163/00000007.tif",
        "access/7213163/00000008.tif", "access/7213163/00000009.tif",
        "access/7213163/00000010.tif", "access/7213163/00000011.tif",
        "access/7213163/00000012.tif", "access/7213163/00000013.tif",
        "access/7213163/00000014.tif", "access/7213163/00000015.tif",
        "access/7213163/00000016.tif", "access/7213163/00000017.tif",
        "access/7213163/00000018.tif", "access/7213163/00000019.tif",
        "access/7213163/00000020.tif", "access/7213163/00000021.tif",
        "access/7213163/00000022.tif", "access/7213163/Thumbs.db",
        "access/7213184/00000001.tif", "access/7213184/00000002.tif",
        "access/7213184/00000003.tif", "access/7213184/00000004.tif",
        "access/7213184/00000005.tif", "access/7213184/00000006.tif",
        "access/7213184/00000007.tif", "access/7213184/00000008.tif",
        "access/7213184/00000009.tif", "access/7213184/00000010.tif",
        "access/7213184/00000011.tif", "access/7213184/00000012.tif",
        "access/7213184/00000013.tif", "access/7213184/00000014.tif",
        "access/7213184/00000015.tif", "access/7213184/00000016.tif",
        "access/7213184/00000017.tif", "access/7213184/00000018.tif",
        "access/7213184/00000019.tif", "access/7213184/00000020.tif",
        "access/7213184/00000021.tif", "access/7213184/00000022.tif",
        "access/7213184/00000023.tif", "access/7213184/00000024.tif",
        "access/7213184/00000025.tif", "access/7213184/00000026.tif",
        "access/7213184/00000027.tif", "access/7213184/00000028.tif",
        "access/7213184/Thumbs.db", "preservation/7212907/00000001.tif",
        "preservation/7212907/00000002.tif", "preservation/7212907/00000003.tif",
        "preservation/7212907/00000004.tif", "preservation/7212907/00000005.tif",
        "preservation/7212907/00000006.tif", "preservation/7212907/00000007.tif",
        "preservation/7212907/00000008.tif", "preservation/7212907/00000009.tif",
        "preservation/7212907/00000010.tif", "preservation/7212907/00000011.tif",
        "preservation/7212907/00000012.tif", "preservation/7212907/00000013.tif",
        "preservation/7212907/00000014.tif", "preservation/7212907/00000015.tif",
        "preservation/7212907/00000016.tif", "preservation/7212907/00000017.tif",
        "preservation/7212907/00000018.tif", "preservation/7212907/00000019.tif",
        "preservation/7212907/00000020.tif", "preservation/7212907/00000021.tif",
        "preservation/7212907/00000022.tif", "preservation/7212907/target_l_001.tif",
        "preservation/7212907/target_l_002.tif", "preservation/7212907/target_r_001.tif",
        "preservation/7212907/target_r_002.tif", "preservation/7212907/Thumbs.db",
        "preservation/7212938/00000001.tif", "preservation/7212938/00000002.tif",
        "preservation/7212938/00000003.tif", "preservation/7212938/00000004.tif",
        "preservation/7212938/00000005.tif", "preservation/7212938/00000006.tif",
        "preservation/7212938/00000007.tif", "preservation/7212938/00000008.tif",
        "preservation/7212938/00000009.tif", "preservation/7212938/00000010.tif",
        "preservation/7212938/00000011.tif", "preservation/7212938/00000012.tif",
        "preservation/7212938/00000013.tif", "preservation/7212938/00000014.tif",
        "preservation/7212938/00000015.tif", "preservation/7212938/00000016.tif",
        "preservation/7212938/00000017.tif", "preservation/7212938/00000018.tif",
        "preservation/7212938/00000019.tif", "preservation/7212938/00000020.tif",
        "preservation/7212938/00000021.tif", "preservation/7212938/00000022.tif",
        "preservation/7212938/00000023.tif", "preservation/7212938/00000024.tif",
        "preservation/7212938/00000025.tif", "preservation/7212938/00000026.tif",
        "preservation/7212938/00000027.tif", "preservation/7212938/00000028.tif",
        "preservation/7212938/00000029.tif", "preservation/7212938/00000030.tif",
        "preservation/7212938/00000031.tif", "preservation/7212938/00000032.tif",
        "preservation/7212938/00000033.tif", "preservation/7212938/00000034.tif",
        "preservation/7212938/00000035.tif", "preservation/7212938/00000036.tif",
        "preservation/7212938/00000037.tif", "preservation/7212938/00000038.tif",
        "preservation/7212938/00000039.tif", "preservation/7212938/00000040.tif",
        "preservation/7212938/00000041.tif", "preservation/7212938/00000042.tif",
        "preservation/7212938/00000043.tif", "preservation/7212938/00000044.tif",
        "preservation/7212938/00000045.tif", "preservation/7212938/00000046.tif",
        "preservation/7212938/00000047.tif", "preservation/7212938/00000048.tif",
        "preservation/7212938/00000049.tif", "preservation/7212938/00000050.tif",
        "preservation/7212938/00000051.tif", "preservation/7212938/00000052.tif",
        "preservation/7212938/00000053.tif", "preservation/7212938/00000054.tif",
        "preservation/7212938/00000055.tif", "preservation/7212938/00000056.tif",
        "preservation/7212938/00000057.tif", "preservation/7212938/00000058.tif",
        "preservation/7212938/00000059.tif", "preservation/7212938/00000060.tif",
        "preservation/7212938/00000061.tif", "preservation/7212938/00000062.tif",
        "preservation/7212938/00000063.tif", "preservation/7212938/00000064.tif",
        "preservation/7212938/00000065.tif", "preservation/7212938/00000066.tif",
        "preservation/7212938/00000067.tif", "preservation/7212938/00000068.tif",
        "preservation/7212938/00000069.tif", "preservation/7212938/00000070.tif",
        "preservation/7212938/target_l_001.tif", "preservation/7212938/target_l_002.tif",
        "preservation/7212938/target_r_001.tif", "preservation/7212938/target_r_002.tif",
        "preservation/7212938/Thumbs.db", "preservation/7212977/00000001.tif",
        "preservation/7212977/00000002.tif", "preservation/7212977/00000003.tif",
        "preservation/7212977/00000004.tif", "preservation/7212977/00000005.tif",
        "preservation/7212977/00000006.tif", "preservation/7212977/00000007.tif",
        "preservation/7212977/00000008.tif", "preservation/7212977/00000009.tif",
        "preservation/7212977/00000010.tif", "preservation/7212977/00000011.tif",
        "preservation/7212977/00000012.tif", "preservation/7212977/00000013.tif",
        "preservation/7212977/00000014.tif", "preservation/7212977/00000015.tif",
        "preservation/7212977/00000016.tif", "preservation/7212977/00000017.tif",
        "preservation/7212977/00000018.tif", "preservation/7212977/00000019.tif",
        "preservation/7212977/00000020.tif", "preservation/7212977/00000021.tif",
        "preservation/7212977/00000022.tif", "preservation/7212977/00000023.tif",
        "preservation/7212977/00000024.tif", "preservation/7212977/00000025.tif",
        "preservation/7212977/00000026.tif", "preservation/7212977/target_l_001.tif",
        "preservation/7212977/target_l_002.tif", "preservation/7212977/target_r_001.tif",
        "preservation/7212977/target_r_002.tif", "preservation/7212977/Thumbs.db",
        "preservation/7212995/00000001.tif", "preservation/7212995/00000002.tif",
        "preservation/7212995/00000003.tif", "preservation/7212995/00000004.tif",
        "preservation/7212995/00000005.tif", "preservation/7212995/00000006.tif",
        "preservation/7212995/00000007.tif", "preservation/7212995/00000008.tif",
        "preservation/7212995/00000009.tif", "preservation/7212995/00000010.tif",
        "preservation/7212995/00000011.tif", "preservation/7212995/00000012.tif",
        "preservation/7212995/00000013.tif", "preservation/7212995/00000014.tif",
        "preservation/7212995/00000015.tif", "preservation/7212995/00000016.tif",
        "preservation/7212995/00000017.tif", "preservation/7212995/00000018.tif",
        "preservation/7212995/00000019.tif", "preservation/7212995/00000020.tif",
        "preservation/7212995/00000021.tif", "preservation/7212995/00000022.tif",
        "preservation/7212995/00000023.tif", "preservation/7212995/00000024.tif",
        "preservation/7212995/target_l_001.tif", "preservation/7212995/target_l_002.tif",
        "preservation/7212995/target_r_001.tif", "preservation/7212995/target_r_002.tif",
        "preservation/7212995/Thumbs.db", "preservation/7213108/00000001.tif",
        "preservation/7213108/00000002.tif", "preservation/7213108/00000003.tif",
        "preservation/7213108/00000004.tif", "preservation/7213108/00000005.tif",
        "preservation/7213108/00000006.tif", "preservation/7213108/00000007.tif",
        "preservation/7213108/00000008.tif", "preservation/7213108/00000009.tif",
        "preservation/7213108/00000010.tif", "preservation/7213108/00000011.tif",
        "preservation/7213108/00000012.tif", "preservation/7213108/00000013.tif",
        "preservation/7213108/00000014.tif", "preservation/7213108/00000015.tif",
        "preservation/7213108/00000016.tif", "preservation/7213108/00000017.tif",
        "preservation/7213108/00000018.tif", "preservation/7213108/00000019.tif",
        "preservation/7213108/00000020.tif", "preservation/7213108/00000021.tif",
        "preservation/7213108/00000022.tif", "preservation/7213108/00000023.tif",
        "preservation/7213108/00000024.tif", "preservation/7213108/00000025.tif",
        "preservation/7213108/00000026.tif", "preservation/7213108/target_l_001.tif",
        "preservation/7213108/target_l_002.tif", "preservation/7213108/target_r_001.tif",
        "preservation/7213108/target_r_002.tif", "preservation/7213108/Thumbs.db",
        "preservation/7213163/00000001.tif", "preservation/7213163/00000002.tif",
        "preservation/7213163/00000003.tif", "preservation/7213163/00000004.tif",
        "preservation/7213163/00000005.tif", "preservation/7213163/00000006.tif",
        "preservation/7213163/00000007.tif", "preservation/7213163/00000008.tif",
        "preservation/7213163/00000009.tif", "preservation/7213163/00000010.tif",
        "preservation/7213163/00000011.tif", "preservation/7213163/00000012.tif",
        "preservation/7213163/00000013.tif", "preservation/7213163/00000014.tif",
        "preservation/7213163/00000015.tif", "preservation/7213163/00000016.tif",
        "preservation/7213163/00000017.tif", "preservation/7213163/00000018.tif",
        "preservation/7213163/00000019.tif", "preservation/7213163/00000020.tif",
        "preservation/7213163/00000021.tif", "preservation/7213163/00000022.tif",
        "preservation/7213163/target_l_001.tif", "preservation/7213163/target_l_002.tif",
        "preservation/7213163/target_r_001.tif", "preservation/7213163/target_r_002.tif",
        "preservation/7213163/Thumbs.db", "preservation/7213184/00000001.tif",
        "preservation/7213184/00000002.tif", "preservation/7213184/00000003.tif",
        "preservation/7213184/00000004.tif", "preservation/7213184/00000005.tif",
        "preservation/7213184/00000006.tif", "preservation/7213184/00000007.tif",
        "preservation/7213184/00000008.tif", "preservation/7213184/00000009.tif",
        "preservation/7213184/00000010.tif", "preservation/7213184/00000011.tif",
        "preservation/7213184/00000012.tif", "preservation/7213184/00000013.tif",
        "preservation/7213184/00000014.tif", "preservation/7213184/00000015.tif",
        "preservation/7213184/00000016.tif", "preservation/7213184/00000017.tif",
        "preservation/7213184/00000018.tif", "preservation/7213184/00000019.tif",
        "preservation/7213184/00000020.tif", "preservation/7213184/00000021.tif",
        "preservation/7213184/00000022.tif", "preservation/7213184/00000023.tif",
        "preservation/7213184/00000024.tif", "preservation/7213184/00000025.tif",
        "preservation/7213184/00000026.tif", "preservation/7213184/00000027.tif",
        "preservation/7213184/00000028.tif", "preservation/7213184/target_l_001.tif",
        "preservation/7213184/target_l_002.tif", "preservation/7213184/target_r_001.tif",
        "preservation/7213184/target_r_002.tif", "preservation/7213184/Thumbs.db",

    ]
    tmpdir = tmpdir_factory.mktemp("hathi_sample_package_1", numbered=False)

    for file_ in files:
        short_path, filename = os.path.split(file_)
        full_path = os.path.join(str(tmpdir), short_path)
        os.makedirs(full_path, exist_ok=True)
        pathlib.Path(os.path.join(full_path, filename)).touch()
    yield tmpdir
    shutil.rmtree(tmpdir)
    # return packages.create_package("Hathi", root_path=str(tmpdir))


def test_get_hathi_package(hathi_sample_package):
    new_pkg = packages.create_package("Hathi", root_path=str(hathi_sample_package))
    assert isinstance(new_pkg, packages.Hathi)


def test_load_hathi_package(hathi_sample_package):
    new_pkg = packages.create_package("Hathi", root_path=str(hathi_sample_package))
    assert len(new_pkg) == 7


def test_hathi_package_iter(hathi_sample_package):
    new_pkg = packages.create_package("Hathi", root_path=str(hathi_sample_package))
    for item in new_pkg:
        assert isinstance(item, packages.abs_package.PackageItem)

def test_get_hathi_package_path_after(hathi_sample_package):
    new_pkg = packages.create_package("Hathi")
    new_pkg.root_path = str(hathi_sample_package)
    assert isinstance(new_pkg, packages.Hathi)


def test_load_hathi_package_path_after(hathi_sample_package):
    new_pkg = packages.create_package("Hathi")
    new_pkg.root_path = str(hathi_sample_package)
    # new_pkg = packages.create_package("Hathi", root_path=str(hathi_sample_package))
    assert len(new_pkg) == 7


def test_hathi_package_iter_path_after(hathi_sample_package):
    new_pkg = packages.create_package("Hathi")
    new_pkg.root_path = str(hathi_sample_package)
    for item in new_pkg:
        assert isinstance(item, packages.abs_package.PackageItem)
