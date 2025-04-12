"""
ARM Utilities Functions for:
    Logs

Functions
    - get_info - get a directory list of logs
    - validate_logfile - check logfile existence
    - generate_arm_cat - generate only ARM logs from file
    - generate_full_log - Gets/tails all lines from log file
"""
import os
from pathlib import Path
from time import strftime, localtime, sleep
from werkzeug.routing import ValidationError
from flask import current_app as app

import config.config as cfg


def get_info(directory: str):
    """
    Retrieve statistics for files in a specified directory.

    This function reads various statistics for each file in the given directory.
    It is primarily used for the "view logs" page to display file information.

    Parameters:
        directory (str): The path to the directory from which to read file statistics.

    Returns:
        log_dir (tuple):
            file_list (list):
            - filename (str): The name of the file
            - access_time (date): formatted according to 'DATE_FORMAT' in 'cfg.arm_config'
            - create_time (date): formatted according to 'DATE_FORMAT' in 'cfg.arm_config'
            - file_size (str): in kilobytes (KB), formatted with one decimal place and comma as thousand separator
            error (bool): True if an error occurred reading directory
            error_string (str): Error string
    """
    app.logger.debug(f"Generating directory listing for: {directory}")
    log_dir = dict()
    log_dir['file_list'] = []
    log_dir['error'] = False
    log_dir['error_string'] = ""

    # Error catch - missing directory
    if not os.path.exists(directory):
        app.logger.error(f"Log directory does not exist: {directory}")
        log_dir['error'] = True
        log_dir['error_string'] = f"Log directory does not exist: {directory}"
        return log_dir

    # Error catch - directory not valid
    if not os.path.isdir(directory):
        app.logger.error(f"Log path is not a directory: {directory}")
        log_dir['error'] = True
        log_dir['error_string'] = f"Log path is not a directory: {directory}"
        return log_dir

    # Read in the log directory and return a list of all files
    try:
        for i in os.listdir(directory):
            filename = os.path.join(directory, i)

            # Skip if not a file
            if not os.path.isfile(filename):
                continue

            # Get log folder file details
            try:
                file_stats = os.stat(os.path.join(directory, i))
                file_size = os.path.getsize(os.path.join(directory, i))
                file_size = round((file_size / 1024), 1)
                file_size = f"{file_size :,.1f}"
                create_time = strftime(cfg.arm_config['DATE_FORMAT'], localtime(file_stats.st_ctime))
                access_time = strftime(cfg.arm_config['DATE_FORMAT'], localtime(file_stats.st_atime))
                log_dir['file_list'].append([i, access_time, create_time, file_size])
            except OSError as e:
                app.logger.warning(f"Could not access file '{filename}': {e}")
                log_dir['error'] = True
                log_dir['error_string'] = log_dir['error_string'].append(f"Could not access file '{filename}': {e}")
                continue

    except OSError as e:
        app.logger.error(f"Failed to list directory '{directory}': {e}")
        log_dir['error'] = True
        log_dir['error_string'] = f"Failed to list directory '{directory}': {e}"
        return log_dir

    return log_dir


def validate_logfile(logfile: str, mode: str, my_file: Path) -> None:
    """
    Check if the logfile provided by the user is valid.

    This function validates the logfile name and checks for invalid characters or patterns.
    It also verifies the existence of the logfile at the specified path.

    :param logfile: The name of the logfile to validate.
    :param mode: A mode parameter used by the JSON API.
    :param my_file: The full base path to the logfile, represented as a Path object.

    :return: None

    :raise ValidationError: If the logfile name contains invalid characters ("/" or "../") or if "mode" is None.
    :raise FileNotFoundError: If the logfile cannot be found at the specified path.
    """
    app.logger.debug(f"Logfile: {logfile}")
    if logfile is None or "../" in logfile or mode is None or logfile.find("/") != -1:
        raise ValidationError("logfile doesnt pass sanity checks")

    if not my_file.is_file():
        # logfile doesnt exist throw out error template
        raise FileNotFoundError("File not found")


def generate_arm_cat(full_path):
    """
    Read from a log file and only output lines containing "ARM:".

    This function reads a log file line by line and yields lines that contain the substring "ARM:".

    :param full_path: The full path to the job log file.
    :type full_path: str

    :return: Yields lines from the log file that contain "ARM:".
    :rtype: generator of str
    """
    read_log_file = open(full_path)
    while True:
        new = read_log_file.readline()
        if new:
            if "ARM:" in new:
                yield new
            else:
                sleep(1)


def generate_full_log(full_path):
    """
    Continuously read and yield all lines from a log file.

    This function attempts to read the entire contents of a log file in real-time,
    yielding the contents. If an error occurs with the default encoding, it will
    retry with UTF-8 encoding and ignore errors.

    :param full_path: The full path to the job log file.
    :type full_path: str

    :return: Yields the contents of the log file.
    :rtype: generator of str

    :raises FileNotFoundError: If the log file is not found.
    :raises UnicodeDecodeError: If there is an encoding error with UTF-8 encoding.
    :raises OSError: If other file-related errors occur.
    """
    try:
        with open(full_path) as read_log_file:
            while True:
                yield read_log_file.read()
                sleep(1)
    except (UnicodeDecodeError, OSError) as e:
        app.logger.error(f"Error reading file: {str(full_path)} error: {str(e)}")
        try:
            with open(full_path, encoding="utf8", errors='ignore') as read_log_file:
                while True:
                    yield read_log_file.read()
                    sleep(1)
        except (UnicodeDecodeError, OSError) as e:
            app.logger.error(f"Error reading file {full_path} with UTF-8 encoding: {e}")
            raise e
