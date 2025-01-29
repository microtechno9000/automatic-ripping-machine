import logging
from logging.handlers import RotatingFileHandler

from ripper.monitor.MonitorConfig import MonitorConfig


def setup_logging(config: MonitorConfig) -> logging:
    """
    Configures and sets up logging based on the provided MonitorConfig.
    - Logs are appended instead of overwritten.
    - A maximum file size is enforced (5MB)

    Args:
        config (MonitorConfig): The configuration object containing logging parameters.

    Returns:
        logging.Logger: The configured logger instance.

    Raises:
        ValueError: If any required logging configuration parameter is missing.
    """

    # Configure file handler to append, and set a max size
    file_handler = RotatingFileHandler(
        filename=config.log_path + config.log_file,
        mode="a",  # Append mode
        maxBytes=config.log_size,  # Max file size in bytes
        encoding="utf-8"
    )

    logging.basicConfig(
        level=config.log_level,
        format=config.log_format,
        handlers=[
            file_handler,  # Log to file (append)
            logging.StreamHandler()  # Log to console
        ]
    )
    logger = logging.getLogger(__name__)

    return logger
