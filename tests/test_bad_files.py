import os

import pytest

import dcc_qc.validators.hathi_lab_factory
from dcc_qc import validators

BASE_ROOT = "T:\\"


# =======================
# Fixtures
# =======================

@pytest.fixture(name="access_7209692")
def files_access_bad_7209692():
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

    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Access_BAD\7209692")))


@pytest.fixture(name="access_7210012")
def files_access_bad_7210012():
    """
    Note:
        Images 00000007, 00000016, 00000027, 00000033 have incorrect specs for access files.
        Image and text file 0000020 is named incorrectly (missing one 0).

    Returns:
    """

    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Access_BAD\7210012")))


@pytest.fixture(name="access_7210438")
def files_access_bad_7210438():
    """
    Note:
        All images have incorrect specs for access files.
        Missing text files.
        Missing checksum, marc, and meta.yml files.

    Returns:
    """

    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Access_BAD\7210438")))


@pytest.fixture(name="access_good")
def files_access_good():
    """
    Note:
        contains 7208771 and 7209666

        Both files have correct specs for access files.
        All text files, checksum, marc, and meta.yml files present.
        Metadata is correct.

    Returns:
    """
    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Access_GOOD")))


@pytest.fixture(name="preservation_7208772")
def files_preservation_bad_7208772():
    """
    Note:
        All images have incorrect specs for preservation files.
        Missing targets.

    Returns:

    """
    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Preservation_BAD\7208772")))


@pytest.fixture(name="preservation_7209934")
def files_preservation_bad_7209934():
    """
    Note:
        Images 00000005, 00000010, 00000015, 00000020, 00000025 have incorrect specs for preservation files.

    Returns:

    """
    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Preservation_BAD\7209934")))


@pytest.fixture(name="preservation_good")
def files_preservation_good():
    """
    Note:
        Contains 6895567 & 7210439
        Both files have correct specs for preservation files.
        Targets present.

    Returns:

    """
    return os.walk(os.path.normpath(os.path.join(BASE_ROOT, r"HenryTest-PSR_2\DCC\Preservation_GOOD")))


# =======================
# Tests
# =======================

def test_access_job_identifier_bad(access_7209692):
    invalid_files = ["00000004.tif", '00000008.tif']

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in access_7209692:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_access_metadata_title_incorrect(access_7209692):
    invalid_files = ["00000014.tif", '00000022.tif']

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in access_7209692:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_access_metadata_credit_line_missing(access_7209692):
    invalid_files = ["00000023.tif"]

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in access_7209692:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_access_metadata_creator_missing(access_7209692):
    invalid_files = ["00000026.tif"]

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.metadata_checker()

    for root, dirs, files in access_7209692:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_access_specs_incorrect(access_7210012):
    invalid_files = ["00000007.tif",
                     "00000016.tif",
                     "00000027.tif",
                     "00000033.tif"]

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.technical_checker()

    for root, dirs, files in access_7210012:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True


def test_access_specs_correct(access_good):
    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.technical_checker()

    for root, dirs, files in access_good:
        for file_ in files:
            file_name = os.path.join(root, file_)
            assert validator.check(file_name) is True


def test_access_file_naming_incorrect(access_7210012):
    invalid_files = ["0000020.tif", "0000020.txt"]

    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.naming_checker()

    for root, dirs, files in access_7210012:
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid, "The file {} was NOT listed as invalid".format(file_)
            else:
                assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_access_file_naming_correct(access_good):
    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.naming_checker()

    for root, dirs, files in access_good:
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_preservation_file_naming_correct(preservation_good):
    validator_factory = dcc_qc.validators.hathi_lab_factory.PreservationValidators()
    validator = validator_factory.naming_checker()

    for root, dirs, files in preservation_good:
        for file_ in files:

            if file_ == "Thumbs.db":
                continue

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            assert result.valid is True, "The file {} was listed as invalid".format(file_)


def test_access_files_found_all(access_good):
    validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
    validator = validator_factory.completeness_checker()

    path = next(access_good)[0]
    result = validator.check(path)
    assert result.valid


# def test_access_files_text_missing(access_7210438):
#     def has_missing_textfile_error(errors):
#         for error in errors:
#             if "is missing " in error and ".txt" in error:
#                 return True
#         else:
#             return False
#
#     validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
#     validator = validator_factory.completeness_checker()
#
#     path = next(access_7210438)[0]
#     result = validator.check(path)
#     assert not result.valid
#     assert has_missing_textfile_error(result.errors)
#     assert result.result_type == "Access Directory Completeness Test"


# def test_access_files_checksum_missing(access_7210438):
#     def has_missing_checksum_error(errors):
#         for error in errors:
#             if "is missing checksum.md5" in error:
#                 return True
#         else:
#             return False
#
#     validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
#     validator = validator_factory.completeness_checker()
#     path = next(access_7210438)[0]
#     result = validator.check(path)
#     assert not result.valid
#     assert has_missing_checksum_error(result.errors) is True


# def test_access_files_marc_missing(access_7210438):
#     def has_missing_marc_error(errors):
#         for error in errors:
#             if "is missing marc.xml" in error:
#                 return True
#         else:
#             return False
#
#     validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
#     validator = validator_factory.completeness_checker()
#
#     path = next(access_7210438)[0]
#     result = validator.check(path)
#
#     assert not result.valid
#     assert has_missing_marc_error(result.errors) is True
#
#
# def test_access_files_meta_missing(access_7210438):
#     validator_factory = dcc_qc.validators.hathi_lab_factory.AccessValidators()
#     validator = validator_factory.completeness_checker()
#
#     path = next(access_7210438)[0]
#     result = validator.check(path)
#     assert not result.valid


def test_preservation_files_targets_missing(preservation_7208772):
    validator_factory = dcc_qc.validators.hathi_lab_factory.PreservationValidators()
    validator = validator_factory.completeness_checker()
    path = next(preservation_7208772)[0]
    result = validator.check(path)
    assert not result.valid


def test_preservation_incorrect_specs(preservation_7209934):
    invalid_files = ["6895567.tif", "7210439.tif"]

    validator_factory = dcc_qc.validators.hathi_lab_factory.PreservationValidators()
    validator = validator_factory.technical_checker()

    for root, dirs, files in preservation_7209934:
        for file_ in files:

            file_name = os.path.join(root, file_)
            result = validator.check(file_name)
            if file_ in invalid_files:
                assert not result.valid
            else:
                assert result.valid is True
