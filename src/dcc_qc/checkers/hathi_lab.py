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
            "target_l_001.tif",
            "target_l_002.tif",
            "target_r_001.tif",
            "target_r_002.tif",
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
        files = [x.name for x in filter(lambda i: os.path.splitext(i.name)[1] == ".tif", os.scandir(path))]

        values = []
        for f in files:
            try:
                values.append(int(os.path.splitext(f)[0]))
            except ValueError as e:
                pass
        try:
            highest_value = sorted(values)[-1]
            if highest_value > 99999999:
                raise ValueError("Unable to determine the expected file names based on files in path")

            for i in range(1, highest_value):
                expected_file_name = "{}.tif".format(str(i).zfill(8))
                if expected_file_name not in os.listdir(path):
                    yield expected_file_name
        except IndexError as e:
            raise
            # raise Exception("Unable to locate files in path {}".format(path))

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
        required_files = set()  # type: ignore
        # required_files = {"checksum.md5", "marc.xml", "meta.yml"}
        valid_image_extensions = [".tif"]
        valid_text_extensions = []  # type: ignore
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

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)


class AccessNamingChecker(AbsChecker):
    valid_extensions = [".tif"]
    ignore_extension = [".db"]
    valid_naming_scheme = re.compile("^\d{8}$")

    @staticmethod
    def checker_name():
        return "Access File Naming Checker Test"

    def check(self, path):
        valid = True
        errors = []
        file_location = os.path.dirname(path)
        basename, extension = os.path.splitext(os.path.basename(path))
        if extension not in self.ignore_extension:

            if extension not in self.valid_extensions:
                valid = False
                new_error = error_message.ValidationError(
                    "Invalid file type", group=path.split(os.sep)[-1])
                new_error.source = path
                errors.append(new_error)

            # Check the image files have the full 8 digits
            if self.valid_naming_scheme.match(basename) is None:
                valid = False
                new_error = error_message.ValidationError(
                    "Does not match the valid file pattern for preservation files",
                    group=file_location.split(os.sep)[-1])
                new_error.source = path
                errors.append(new_error)

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

    @staticmethod
    def check_for_missing_matching_preservation(access_folder, preservation_folder):
        extension_used = [".tif"]

        pres_files = list(filter(
            lambda i: i.is_file() and os.path.splitext(i.name)[1].lower() in extension_used,
            os.scandir(preservation_folder)))
        access_files = list(filter(
            lambda i: i.is_file() and os.path.splitext(i.name)[1].lower() in extension_used,
            os.scandir(access_folder)))

        access_set = {f.name: f for f in access_files}
        pres_set = {f.name: f for f in pres_files}
        return [i[1].path for i in filter(lambda f: f[0] not in pres_set, access_set.items())]

    @staticmethod
    def check_for_missing_matching_access(access_folder, preservation_folder):
        extension_used = [".tif"]
        pres_files_ignored = [
            "target_l_001.tif",
            "target_r_001.tif",
            "target_l_002.tif",
            "target_r_002.tif",
        ]

        pres_files = list(filter(
            lambda i: i.is_file() and
                      os.path.splitext(i.name)[1].lower() in extension_used and
                      i.name not in pres_files_ignored,
            os.scandir(preservation_folder)))
        access_files = list(filter(
            lambda i: i.is_file() and os.path.splitext(i.name)[1].lower() in extension_used,
            os.scandir(access_folder)))

        access_set = {f.name: f for f in access_files}
        pres_set = {f.name: f for f in pres_files}
        return [i[1].path for i in filter(lambda f: f[0] not in access_set, pres_set.items())]

    def check(self, path):
        # NOTE: this uses the package because of the way hathi packages are formatted
        valid = True
        errors = []
        # Check if everything in access folder is found same in the preservation folder

        missing_pres_files = self.check_for_missing_matching_preservation(
            access_folder=path.directories["access"],
            preservation_folder=path.directories["preservation"])
        if missing_pres_files:
            valid = False
            new_error = error_message.ValidationError(
                "The files [{}] were found in the access but not in the preservation folder".format(
                    ", ".join([os.path.basename(f) for f in missing_pres_files])),
                group=path.identifier
            )
            new_error.source = path.directories["access"]
            errors.append(new_error)

        missing_access_files = self.check_for_missing_matching_access(
            access_folder=path.directories["access"],
            preservation_folder=path.directories["preservation"])
        if missing_access_files:
            new_error = error_message.ValidationError(
                "The files [{}] were found in the preservation folder but not in the access folder".format(
                    ", ".join([os.path.basename(f) for f in missing_access_files])),
                group=path.identifier
            )
            new_error.source = path.directories["preservation"]
            errors.append(new_error)
        return checkers.Results(self.checker_name(), valid=valid, errors=errors)


class PackageStructureChecker(AbsChecker):
    @staticmethod
    def checker_name():
        return "Package structure checker"

    @staticmethod
    def find_root_directory_errors(path: str):
        required_directories = {"access", "preservation"}
        for item in os.scandir(path):
            if item.is_dir():
                if item.name in required_directories:
                    required_directories.remove(item.name)
                else:
                    new_error = error_message.ValidationError("{} is an invalid folder.".format(item.path), group=path)
                    new_error.source = path
                    yield new_error
            elif item.is_file():
                new_error = error_message.ValidationError("{} is an invalid file.".format(item.path), group=path)
                new_error.source = path
                yield new_error

        if required_directories:
            for folder in required_directories:
                new_error = error_message.ValidationError("{} is missing required folder {}".format(path, folder),
                                                          group=path)
                new_error.source = path
                yield new_error

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
            new_error = error_message.ValidationError(
                "missing matching {} in {}".format(item_left, preservation_folder), group=path)
            new_error.source = path
            yield new_error

        # find missing matching access folders
        master = set(access_folders)
        for preservation in preservation_folders:
            master.remove(preservation)

        for item_left in master:
            new_error = error_message.ValidationError("missing matching {} in {}".format(item_left, access_folder),
                                                      group=path)
            new_error.source = path
            yield new_error

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

        return checkers.Results(self.checker_name(), valid=valid, errors=errors)
