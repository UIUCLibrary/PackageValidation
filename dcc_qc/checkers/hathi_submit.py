import os
import re

from dcc_qc import checkers
from dcc_qc.checkers.abs_checkers import AbsChecker
from dcc_qc.checkers import error_message


class PresCompletenessChecker(AbsChecker):
    @staticmethod
    def find_missing_by_number(path):
        files = [x.name for x in filter(lambda i: os.path.splitext(i.name)[1] == ".tif", os.scandir(path))]
        if not files:
            raise FileNotFoundError("No files found in {}".format(path))
        values = []
        for f in files:
            try:
                values.append(int(os.path.splitext(f)[0]))
            except ValueError as e:
                pass
        highest_value = sorted(values)[-1]
        if highest_value > 99999999:
            raise ValueError("Unable to determine the expected file names based on files in path")

        for i in range(1, highest_value):
            expected_file_name = "{}.tif".format(str(i).zfill(8))
            if expected_file_name not in os.listdir(path):
                yield expected_file_name

    def check(self, path):
        valid = True
        errors = []
        required_files = (
            "checksum.md5",
            "marc.xml",
            "meta.yml",
        )
        error_group = path.split(os.sep)[-1]
        try:
            missing = list(self.find_missing_by_number(path))

            if missing:
                valid = False
                new_error = error_message.ValidationError(
                    "Expected files [{}] not found in preservation folder".format(", ".join(missing)),
                    group=error_group)
                new_error.source = path
                errors.append(new_error)
        except ValueError as e:
            valid = False
            new_error = error_message.ValidationError("Error trying to find missing files. Reason: {}".format(e),
                                                      group=error_group)
            new_error.source = path
            errors.append(new_error)
        except FileNotFoundError as e:
            valid = False
            new_error = error_message.ValidationError(e, group=error_group)
            new_error.source = path
            errors.append(new_error)
            # return checkers.Results(self.checker_name(), valid=valid, errors=errors)
        # Find missing required_files
        missing = list(self.find_missing_required_files(path=path, expected_files=required_files))
        if missing:
            valid = False
            new_error = error_message.ValidationError(
                "Missing expected file(s), [{}]".format(", ".join(missing)), group=error_group)
            new_error.source = path
            errors.append(new_error)
        return checkers.Results(self.checker_name(), valid=valid, errors=errors)

    @staticmethod
    def checker_name():
        return "Preservation Directory Completeness Test"

    @staticmethod
    def find_missing_required_files(path, expected_files):
        for expected_file in expected_files:
            if expected_file not in os.listdir(path):
                yield expected_file


class PresNamingChecker(AbsChecker):
    valid_extensions = [".tif"]
    ignore_extension = [".db"]
    valid_naming_scheme = re.compile("^\d{8}$")

    @staticmethod
    def checker_name():
        return "Preservation File Naming Check Test"

    def check(self, path):
        valid = True
        errors = []
        file_location = os.path.dirname(path)
        basename, extension = os.path.splitext(os.path.basename(path))
        if extension not in self.ignore_extension:

            if extension not in self.valid_extensions:
                valid = False
                new_error = error_message.ValidationError(
                    "Invalid preservation file extension: \"{}\"".format(extension),
                    group=path)
                new_error.source = path
                errors.append(new_error)

            # Check the image files have the full 8 digits
            if extension == ".tif":
                if "target" not in basename:
                    if PresNamingChecker.valid_naming_scheme.match(basename) is None:
                        valid = False
                        new_error = error_message.ValidationError(
                            "Does not match the valid preservation file naming pattern",
                            group=file_location.split(os.sep)[-1])
                        new_error.source = path
                        errors.append(new_error)

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)


class PresMetadataChecker(AbsChecker):
    # TODO: Create PresMetadataChecker() class

    @staticmethod
    def checker_name():
        return "Preservation Metadata Checker"

    def check(self, path):
        raise NotImplementedError()


class PresTechnicalChecker(AbsChecker):
    # TODO: Create PresTechnicalChecker() class

    @staticmethod
    def checker_name():
        return "Preservation Technical Specs Checker"

    def check(self, path):
        raise NotImplementedError()


class AccessCompletenessChecker(AbsChecker):

    @staticmethod
    def find_missing_by_number(path):
        def check_ext(ext):
            files = [x.name for x in filter(lambda i: os.path.splitext(i.name)[1] == ext, os.scandir(path))]
            values = []
            for f in files:
                try:
                    values.append(int(os.path.splitext(f)[0]))
                except ValueError as e:
                    pass
            if files:
                try:
                    highest_value = sorted(values)[-1]
                    if highest_value > 99999999:
                        raise ValueError("Unable to determine the expected file names based on files in path")

                    for i in range(1, highest_value):
                        expected_file_name = "{}{}".format(str(i).zfill(8),ext)
                        if expected_file_name not in os.listdir(path):
                            yield expected_file_name
                except IndexError as e:
                    raise
        for r in check_ext(".jp2"):
            yield r
        for r in check_ext(".txt"):
            yield r


    @staticmethod
    def checker_name():
        return "Access Directory Completeness Test"

    def check(self, path: str):
        """
        Make sure that all files included in this folder are tiff files 
        and contain nothing else

        Args:
            path: Path to the folder to check

        Returns: list of errors

        """
        required_files = set()
        required_files = {"checksum.md5", "marc.xml", "meta.yml"}
        valid_image_extensions = [".jp2"]
        valid_text_extensions = [".txt", ".xml", ".yml"]
        errors = []
        valid = True
        image_files = set()
        text_files = set()
        try:
            missing = list(self.find_missing_by_number(path))
            if missing:
                valid = False
                new_error = error_message.ValidationError(
                    "Expected files [{}] not found in access folder".format(", ".join(missing)),
                    group=path.split(os.sep)[-1])
                new_error.source = path
                errors.append(new_error)
        except ValueError as e:
            valid = False
            new_error = error_message.ValidationError("Error trying to find missing files. Reason: {}".format(e),
                                                      group=path.split(os.sep)[-1])
            new_error.source = path
            errors.append(new_error)

        # Sort the files into their own category
        for root, dirs, files in os.walk(path):
            for file_ in files:

                # if the filename is the required files set, remove them
                if file_ in required_files:
                    required_files.remove(file_)

                basename, ext = os.path.splitext(file_)
                if ext in valid_image_extensions:
                    image_files.add((root, file_))
                elif ext in valid_text_extensions:
                    text_files.add((root, file_))

        # If there are any files still in the required_files set are missing.
        if required_files:
            valid = False
            new_error = error_message.ValidationError(
                "Missing expected file(s), [{}]".format(", ".join(required_files)))
            new_error.source = path
            errors.append(new_error)
            # errors.append("{} is missing {}".format(path, _file))

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)


class AccessNamingChecker(AbsChecker):
    extensions_to_check = [".jp2", ".txt"]
    ignore_extension = [".db"]
    additional_package_files = [
        "marc.xml",
        "meta.yml",
        "checksum.md5",
    ]
    valid_naming_scheme = re.compile("^\d{8}$")

    @staticmethod
    def checker_name():
        return "Access File Naming Checker Test"

    def check(self, path):
        valid = True
        errors = []
        file_location = os.path.dirname(path)
        group_name = file_location.split(os.sep)[-1]
        basename, extension = os.path.splitext(os.path.basename(path))
        if extension in self.extensions_to_check:
            if self.valid_naming_scheme.match(basename) is None:
                valid = False
                new_error = error_message.ValidationError(
                    "Does not match the valid file pattern for preservation files",
                    group=group_name)
                new_error.source = path
                errors.append(new_error)

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)


class AccessMetadataChecker(AbsChecker):
    # TODO: Create AccessMetadataChecker() class
    @staticmethod
    def checker_name():
        return "Access File Metadata Checker"

    def check(self, path):
        raise NotImplementedError()


class AccessTechnicalChecker(AbsChecker):
    @staticmethod
    def checker_name():
        return "Access Technical Metadata Checker"

    # TODO: Create AccessTechnicalChecker() class

    def check(self, path):
        raise NotImplementedError()


class PackageComponentChecker(AbsChecker):
    @staticmethod
    def checker_name():
        return "Package component checker"


    def check(self, path):
        # NOTE: this uses the package because of the way hathi packages are formatted
        valid = True
        errors = []

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)



class PackageStructureChecker(AbsChecker):
    @staticmethod
    def checker_name():
        return "Package structure checker"


    def check(self, path):
        valid = True
        errors = []

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)
