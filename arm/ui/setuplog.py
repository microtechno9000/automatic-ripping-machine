"""
ARM UI log definition
"""
import logging
from logging.handlers import RotatingFileHandler


def setuplog(log_filename: str, max_size: int, max_count: int):
    """
    Configures the logging settings for a Flask application.

    This function defines a dictionary-based logging configuration that specifies:
    - The format of log messages.
    - Handlers for outputting log messages (e.g., to WSGI stream, console, or null).
    - The root logger's log level and default handler.

    The configuration includes:
    - A `default` formatter for log messages with a specific format, including timestamp, severity, and location.
    - Handlers:
        - `wsgi`: Sends logs to Flask's WSGI error stream.
        - `console`: Outputs logs to the console with a level of `INFO`.
        - `file`: Outputs Flask logs to the specified file
        - `null`: Ignores log messages.
    - The root logger with a `DEBUG` level and `wsgi` handler.

    Returns:
        dict: A logging configuration dictionary compatible with `logging.config.dictConfig`.
    """

    # Set max size from MB to bytes
    max_size = max_size * 1048576

    config = ({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s ARM: %(module)s.%(funcName)s %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'rotating_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_filename,
                'mode': 'a',  # Append to the log file
                'maxBytes': max_size,  # Maximum file size
                'backupCount': max_count,  # Number of backup files to keep
                'formatter': 'default'
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            'flask': {
                'level': 'DEBUG',
                'handlers': ['wsgi', 'rotating_file'],  # Ensure Flask logger uses handlers
                'propagate': True  # Ensure it propagates logs to root
            },
            'root': {  # Root logger
                'level': 'DEBUG',
                'handlers': ['wsgi', 'rotating_file'],
            }
        }
    })

    return config
