from dcc_qc import profiles, packages
import pytest


def test_get_profiles():
    qc_profiles = profiles.get_available()
    assert "hathilab" in qc_profiles


@pytest.fixture
def hathi_profile():
    return profiles.get_profile("HathiLab")


def test_get_hathilab(hathi_profile):
    assert isinstance(hathi_profile, profiles.HathiLab)


def test_hathilab_correct_package_type(hathi_profile: profiles.HathiLab):
    assert isinstance(hathi_profile.get_package_type, packages.Hathi)
