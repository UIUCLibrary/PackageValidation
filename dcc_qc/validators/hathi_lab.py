import os
import re

from dcc_qc import validators
from dcc_qc.validators.abs_validators import AbsValidator


class PresCompletenessChecker(AbsValidator):
    def check(self, path):
        valid = True
        errors = []
        required_files = (
            "target_l_001.tif",
            "target_l_002.tif",
            "target_r_001.tif",
            "target_r_002.tif",
        )

        missing = []
        for required_file in required_files:
            if required_file not in os.listdir(path):
                missing.append(required_file)
        if missing:
            valid = False
            errors.append("{} is missing the following files: {}.".format(path, ", ".join(sorted(required_files))))
        return validators.Results(self.validator_name(), valid=valid, errors=errors)

    @staticmethod
    def validator_name():
        return "Preservation Directory Completeness Test"


class PresNamingChecker(AbsValidator):
    valid_extensions = [".tif"]
    ignore_extension = [".db"]
    valid_naming_scheme = re.compile("^\d{8}$")

    @staticmethod
    def validator_name():
        return "Preservation File Naming Check Test"

    def check(self, path):
        valid = True
        errors = []

        basename, extension = os.path.splitext(os.path.basename(path))
        if extension not in self.ignore_extension:

            if extension not in self.valid_extensions:
                valid = False
                errors.append("Invalid preservation file extension: \"{}\"".format(extension))

            # Check the image files have the full 8 digits
            if extension == ".tif":
                if "target" not in basename:
                    if PresNamingChecker.valid_naming_scheme.match(basename) is None:
                        valid = False
                        errors.append(
                            "In path, {}, \"{}\" does not match the valid file naming pattern for preservation files. "
                            "This is test is case sensitive.".format(
                                os.path.dirname(path),
                                os.path.basename(path)))

        return validators.Results(self.validator_name(), valid=valid, errors=errors)


class PresMetadataChecker(AbsValidator):
    # TODO: Create PresMetadataChecker() class

    @staticmethod
    def validator_name():
        return "Preservation Metadata Checker"

    def check(self, path):
        raise NotImplementedError()


class PresTechnicalChecker(AbsValidator):
    # TODO: Create PresTechnicalChecker() class

    @staticmethod
    def validator_name():
        return "Preservation Technical Specs Checker"

    def check(self, path):
        raise NotImplementedError()


class AccessCompletenessChecker(AbsValidator):
    @staticmethod
    def validator_name():
        return "Access Directory Completeness Test"

    def check(self, path: str):
        """
        Make sure that all files included in this folder are tiff files 
        and contain nothing else
        Args:
            path: 

        Returns:

        """
        required_files = set()
        # required_files = {"checksum.md5", "marc.xml", "meta.yml"}
        valid_image_extensions = [".tif"]
        valid_text_extensions = []
        errors = []
        valid = True
        image_files = set()
        text_files = set()

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
        for _file in required_files:
            valid = False
            errors.append("{} is missing {}".format(path, _file))

        # # check that for every .tif file there is a matching .txt
        # for img_path, img_file in image_files:
        #     basename, ext = os.path.splitext(img_file)
        #     required_text_file = basename + ".txt"
        #     if (img_path, required_text_file) not in text_files:
        #         valid = False
        #         errors.append(
        #             "{} is missing a matching {} file.".format(os.path.join(img_path, img_file), required_text_file))
        #
        # # check that for every .txt file there is a matching .tif
        # for txt_path, txt_file in text_files:
        #     basename, ext = os.path.splitext(txt_file)
        #     required_tif_file = basename + ".tif"
        #     if (txt_path, required_tif_file) not in image_files:
        #         valid = False
        #         errors.append("{} is missing a matching {}".format(os.path.join(txt_path, txt_file), required_tif_file))

        return validators.Results(self.validator_name(), valid=valid, errors=errors)


class AccessNamingChecker(AbsValidator):
    valid_extensions = [".tif"]
    ignore_extension = [".db"]
    valid_naming_scheme = re.compile("^\d{8}$")

    @staticmethod
    def validator_name():
        return "Access File Naming Checker Test"

    def check(self, path):
        valid = True
        errors = []

        basename, extension = os.path.splitext(os.path.basename(path))
        if extension not in self.ignore_extension:

            if extension not in self.valid_extensions:
                valid = False
                errors.append("The file \"{}\" in {} has a file extension not allowed in this folder: \"{}\"".format(
                    os.path.basename(path), os.path.dirname(path), extension))

            # Check the image files have the full 8 digits
            if self.valid_naming_scheme.match(basename) is None:
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file pattern for access files. "
                    "This is test is case sensitive.".format(basename))
                #
                # # The only xml file should be marc.xml
                # if extension == ".xml":
                #     if basename != "marc":
                #         valid = False
                #         errors.append(
                #             "\"{}\" does not match the valid file pattern for preservation files".format(basename))
                #
                # # The only yml file should be meta.yml
                # if extension == ".yml":
                #     if basename != "meta":
                #         valid = False
                #         errors.append(
                #             "\"{}\" does not match the valid file result_type pattern for preservation files".format(basename))

        return validators.Results(self.validator_name(), valid=valid, errors=errors)


class AccessMetadataChecker(AbsValidator):
    # TODO: Create AccessMetadataChecker() class
    @staticmethod
    def validator_name():
        return "Access File Metadata Checker"

    def check(self, path):
        raise NotImplementedError()


class AccessTechnicalChecker(AbsValidator):
    @staticmethod
    def validator_name():
        return "Access Technical Metadata Checker"

    # TODO: Create AccessTechnicalChecker() class

    def check(self, path):
        raise NotImplementedError()


class PackageChecker(AbsValidator):
    @staticmethod
    def validator_name():
        return "Package completeness checker"

    @staticmethod
    def find_root_directory_errors(path):
        required_directories = {"access", "preservation"}
        for item in os.scandir(path):
            if item.is_dir():
                if item.name in required_directories:
                    required_directories.remove(item.name)
                else:
                    yield "{} is an invalid folder.".format(item.path)
            elif item.is_file():
                yield "{} is an invalid file.".format(item.path)

        if required_directories:
            for folder in required_directories:
                yield "{} is missing required folder {}".format(path, folder)

    @staticmethod
    def find_subdirectory_errors(path):
        preservation_folder = os.path.join(path, "preservation")
        access_folder = os.path.join(path, "access")
        preservation_folders = os.listdir(preservation_folder)
        access_folders = os.listdir(access_folder)

        # find missing matching preservation folders
        master = set(preservation_folders)
        for access in access_folders:
            master.remove(access)

        for item_left in master:
            yield "missing matching {} in {}".format(item_left, preservation_folder)

        # find missing matching access folders
        master = set(access_folders)
        for preservation in preservation_folders:
            master.remove(preservation)

        for item_left in master:
            yield "missing matching {} in {}".format(item_left, access_folder)

    def check(self, path):
        valid = True
        errors = []
        for error in self.find_root_directory_errors(path):
            valid = False
            errors.append(error)

        if valid:
            for error in self.find_subdirectory_errors(path):
                valid = False
                errors.append(error)

        return validators.Results(self.validator_name(), valid=valid, errors=errors)
