import os
import re
from collections import namedtuple
import abc

Results = namedtuple("Results", ["valid", "errors"])


class AbsValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, file_):
        pass

class PresCompletenessChecker(AbsValidator):
    # TODO: Create PresCompletenessChecker() class
    def check(self, file):
        pass


class PresNamingChecker(AbsValidator):
    valid_extensions = [".tif"]
    valid_naming_scheme = re.compile("^\d{8}$")

    def check(self, file):
        valid = True
        errors = []

        basename, extension = os.path.splitext(os.path.basename(file))

        if extension not in PresNamingChecker.valid_extensions:
            valid = False
            errors.append("Invalid preservation file extension: \"{}\"".format(extension))

        # Check the image files have the full 8 digits
        if extension == ".tif":
            if "target" not in basename:
                if PresNamingChecker.valid_naming_scheme.match(basename) is None:
                    valid = False
                    errors.append(
                        "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        return Results(valid=valid, errors=errors)


class PresMetadataChecker(AbsValidator):
    # TODO: Create PresMetadataChecker() class
    def check(self, file):
        pass


class PresTechnicalChecker(AbsValidator):
    # TODO: Create PresTechnicalChecker() class
    def check(self, file):
        pass


class AccessCompletenessChecker(AbsValidator):
    # TODO: Create AccessCompletenessChecker() class
    def check(self, file):
        pass


class AccessNamingChecker(AbsValidator):
    # TODO: Create AccessNamingChecker() class
    valid_extensions = [".tif", ".txt", ".md5", ".xml", ".yml"]
    valid_naming_scheme = re.compile("^\d{8}$")

    def check(self, file):
        valid = True
        errors = []

        basename, extension = os.path.splitext(os.path.basename(file))

        if extension not in AccessNamingChecker.valid_extensions:
            valid = False
            errors.append("Invalid file access file extension: \"{}\"".format(extension))

        # Check the image files have the full 8 digits
        if extension == ".tif" or extension == ".txt":
            if AccessNamingChecker.valid_naming_scheme.match(basename) is None:
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        # The only xml file should be marc.xml
        if extension == ".xml":
            if basename != "marc":
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        # The only yaml file should be meta.yml
        if extension == ".yml":
            if basename != "meta":
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        return Results(valid=valid, errors=errors)


class AccessMetadataChecker(AbsValidator):
    # TODO: Create AccessMetadataChecker() class
    def check(self, file):
        pass


class AccessTechnicalChecker(AbsValidator):
    # TODO: Create AccessTechnicalChecker() class
    def check(self, file):
        pass