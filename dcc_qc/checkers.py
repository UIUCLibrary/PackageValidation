import os
import re
import abc


class Results:
    def __init__(self, valid, errors):
        self._valid = valid
        self._errors = errors

    @property
    def valid(self)->bool:
        return self._valid

    @property
    def errors(self)->list:
        return self._errors
# Results = namedtuple("Results", ["valid", "errors"])


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

        if extension not in self.valid_extensions:
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
    def check(self, path: str):
        """
        Look for image there is an equal text file and vice-versa
        Look for checksums.md5, marc.xml, and meta.yml files
        Args:
            path: 

        Returns:

        """
        required_files = {"checksum.md5", "marc.xml", "meta.yml"}
        valid_image_extensions = [".tif"]
        valid_text_extensions = [".txt"]
        errors = []
        valid = True
        image_files = set()
        text_files = set()

        # Sort the files into their own category
        for root, dirs, files in os.walk(path):
            for f in files:

                # if the filename is the required files set, remove them
                if f in required_files:
                    required_files.remove(f)

                basename, ext = os.path.splitext(f)
                if ext in valid_image_extensions:
                    image_files.add((root, f))
                elif ext in valid_text_extensions:
                    text_files.add((root, f))

        # If there are any files still in the required_files set are missing.
        for _file in required_files:
            valid = False
            errors.append("{} is missing {}".format(path, _file))

        # check that for every .tif file there is a matching .txt
        for img_path, img_file in image_files:
            basename, ext = os.path.splitext(img_file)
            required_text_file = basename + ".txt"
            if (img_path, required_text_file) not in text_files:
                valid = False
                errors.append("{} is missing a matching {} file.".format(os.path.join(img_path, img_file), required_text_file))

        # check that for every .txt file there is a matching .tif
        for txt_path, txt_file in text_files:
            basename, ext = os.path.splitext(txt_file)
            required_tif_file = basename + ".tif"
            if (txt_path, required_tif_file) not in image_files:
                valid = False
                errors.append("{} is missing a matching {}".format(os.path.join(txt_path, txt_file), required_tif_file))

        return Results(valid=valid, errors=errors)


class AccessNamingChecker(AbsValidator):
    valid_extensions = [".tif", ".txt", ".md5", ".xml", ".yml"]
    valid_naming_scheme = re.compile("^\d{8}$")

    def check(self, file):
        valid = True
        errors = []

        basename, extension = os.path.splitext(os.path.basename(file))

        if extension not in self.valid_extensions:
            valid = False
            errors.append("Invalid file access file extension: \"{}\"".format(extension))

        # Check the image files have the full 8 digits
        if extension == ".tif" or extension == ".txt":
            if self.valid_naming_scheme.match(basename) is None:
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        # The only xml file should be marc.xml
        if extension == ".xml":
            if basename != "marc":
                valid = False
                errors.append(
                    "\"{}\" does not match the valid file name pattern for preservation files".format(basename))

        # The only yml file should be meta.yml
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
