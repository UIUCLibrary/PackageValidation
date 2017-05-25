import logging
import sys

def setup_logging():
    pass


def configure_logger(debug_mode=False, log_file=None):
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    std_handler = logging.StreamHandler(sys.stdout)
    if log_file:
        file_handler = logging.FileHandler(filename=log_file)
        logger.addHandler(file_handler)
    if debug_mode:
        std_handler.setLevel(logging.DEBUG)
        std_handler.setFormatter(debug_formatter)
    else:
        std_handler.setLevel(logging.INFO)

    # std_handler.setFormatter(debug_formatter)

    logger.addHandler(std_handler)
