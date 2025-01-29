import os


class MonitorConfig:
    """
    Configuration class for the monitoring system.

    This class contains settings for logging and MySQL database connection,
    with environment variable overrides where applicable.
    """

    # Log configuration
    log_path = "/home/arm/logs/"
    """str: Directory path where log files are stored."""

    log_file = "monitor.log"
    """str: Name of the log file."""

    log_level = os.getenv("loglevel", "INFO")
    """str: Logging level, retrieved from the environment variable `loglevel` (default: "INFO")."""

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    """str: Format for log messages, including timestamp, log level, and message."""

    log_size = 5*1024*1024
    """str: Max file size of log file in bytes."""

    # MySQL database configuration
    mysql_connector: str = 'mysql+mysqlconnector://'
    """str: Database connection prefix for MySQL using MySQL Connector/Python."""

    mysql_ip: str = os.getenv("MYSQL_IP", "127.0.0.1")
    """str: IP address of the MySQL database server, defaulting to `127.0.0.1` if not set in environment variables."""

    mysql_user: str = os.getenv("MYSQL_USER", "arm")
    """str: MySQL username, retrieved from the `MYSQL_USER` environment variable (default: "arm")."""

    mysql_password: str = os.getenv("MYSQL_PASSWORD", "example")
    """str: MySQL password, retrieved from the `MYSQL_PASSWORD` environment variable (default: "example")."""

    mysql_database: str = "arm"
    """str: Name of the MySQL database used for monitoring."""

    mysql_charset: str = '?charset=utf8mb4'
    """str: Character set for MySQL connections, ensuring support for UTF-8 extended characters."""

    mysql_uri: str = (
            mysql_connector + mysql_user + ':' + mysql_password + '@' + mysql_ip
            + '/' + mysql_database + mysql_charset
    )
    """str: Complete MySQL connection URI with credentials (unsanitized)."""

    mysql_uri_sanitised: str = (
            mysql_connector + mysql_user + ':*******' + '@' + mysql_ip
            + '/' + mysql_database + mysql_charset
    )
    """str: Sanitized MySQL connection URI (password replaced with asterisks for security)."""
