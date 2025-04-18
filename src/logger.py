import io
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# class Logger:
#     """Centralized logging configuration for the application."""
    
#     # Log levels dictionary for easy configuration
#     LOG_LEVELS = {
#         "debug": logging.DEBUG,
#         "info": logging.INFO,
#         "warning": logging.WARNING,
#         "error": logging.ERROR,
#         "critical": logging.CRITICAL
#     }
    
#     def __init__(self, log_dir="logs", console_level="info", file_level="debug"):
#         """
#         Initialize the logger with specified configuration.
        
#         Args:
#             log_dir (str): Directory to store log files
#             console_level (str): Logging level for console output
#             file_level (str): Logging level for file output
#         """
#         # Create logs directory if it doesn't exist
#         self.log_dir = Path(log_dir)
#         self.log_dir.mkdir(exist_ok=True)
        
#         # Generate filenames with timestamps
#         timestamp = datetime.now().strftime("%Y%m%d")
#         self.log_file = self.log_dir / f"app_{timestamp}.log"
#         self.error_file = self.log_dir / f"errors_{timestamp}.log"
        
#         # Set up the root logger
#         self.logger = logging.getLogger()
#         self.logger.setLevel(logging.DEBUG)  # Capture all logs
#         self.logger.handlers = []  # Clear existing handlers
        
#         # Configure console handler
#         self._setup_console_handler(console_level)
        
#         # Configure file handlers
#         self._setup_file_handlers(file_level)
        
#         # Log initial message
#         self.logger.info("Logging system initialized")
    
#     def _setup_console_handler(self, level):
#         """Set up console handler with specified log level."""
#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.setLevel(self.LOG_LEVELS.get(level.lower(), logging.INFO))
        
#         # Create formatter for console (more concise)
#         console_formatter = logging.Formatter(
#             "%(asctime)s [%(levelname)s] %(message)s",
#             datefmt="%H:%M:%S"
#         )
#         console_handler.setFormatter(console_formatter)
#         self.logger.addHandler(console_handler)

        
#     def _setup_file_handlers(self, level):
#         """Set up file handlers for regular logs and errors."""
#         # Create detailed formatter for files
#         file_formatter = logging.Formatter(
#             "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
#             datefmt="%Y-%m-%d %H:%M:%S"
#         )
        
#         # Regular log file - all logs at specified level
#         file_handler = logging.FileHandler(self.log_file)
#         file_handler.setLevel(self.LOG_LEVELS.get(level.lower(), logging.DEBUG))
#         file_handler.setFormatter(file_formatter)
#         self.logger.addHandler(file_handler)
        
#         # Error log file - only ERROR and CRITICAL
#         error_handler = logging.FileHandler(self.error_file)
#         error_handler.setLevel(logging.ERROR)
#         error_handler.setFormatter(file_formatter)
#         self.logger.addHandler(error_handler)
    
    # def get_logger(self, name=None):
    #     """Get a named logger for a specific module."""
    #     return logging.getLogger(name)

class Logger:
    """Centralized logging configuration for the application."""
    
    # Log levels dictionary for easy configuration
    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    def __init__(self, log_dir="logs", console_level="info", file_level="debug"):
        # Create logs directory if it doesn't exist
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Generate filenames with timestamps
        timestamp = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"app_{timestamp}.log"
        self.error_file = self.log_dir / f"errors_{timestamp}.log"
        
        # Set up the root logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # Capture all logs
        self.logger.handlers = []  # Clear existing handlers
        
        # Configure console and file handlers
        self._setup_console_handler(console_level)
        self._setup_file_handlers(file_level)

        # Suppress unwanted library logs
        self._suppress_library_logs()

        # # Log initial message
        # self.logger.info("Logging system initialized")

    def _setup_console_handler(self, level):
        """Set up console handler with specified log level."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.LOG_LEVELS.get(level.lower(), logging.INFO))

        # Create formatter for console (more concise)
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handlers(self, level):
        """Set up file handlers for regular logs and errors."""
        # Create detailed formatter for files
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Regular log file - all logs at specified level
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.LOG_LEVELS.get(level.lower(), logging.DEBUG))
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error log file - only ERROR and CRITICAL
        error_handler = logging.FileHandler(self.error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)

    def _suppress_library_logs(self):
        """Suppress logs from all libraries by setting their log level to WARNING."""
        # List of known libraries to suppress (or set their log level to WARNING)
        libraries = [
            "llama_index",
            "sentence_transformers",
            "fsspec",
            # Add other libraries you want to suppress here
        ]
        
        for lib in libraries:
            logging.getLogger(lib).setLevel(logging.WARNING)
            self.logger.debug(f"Log level for {lib} set to WARNING.")

    def get_logger(self, name=None):
        """Get a named logger for a specific module."""
        return logging.getLogger(name)

# Create a default logger instance
default_logger = Logger()

def get_logger(name=None):
    """Convenience function to get a logger."""
    return default_logger.get_logger(name)