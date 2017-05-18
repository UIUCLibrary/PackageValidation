import pytest
from dcc_qc import packages

TEST_PATH = "T:\HenryTest-PSR_2\DCC\Package_GOOD\\20170424_CavagnaCollectionRBML_tg"


@pytest.fixture
def hathi_sample_package():
    return packages.create_package("Hathi", root_path=TEST_PATH)


def test_get_hathi_package(hathi_sample_package):
    assert isinstance(hathi_sample_package, packages.Hathi)


def test_load_hathi_package(hathi_sample_package):
    assert len(hathi_sample_package) == 7


def test_hathi_package_iter(hathi_sample_package):
    for item in hathi_sample_package:
        print(item)
