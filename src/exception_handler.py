import sys
import traceback
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class ApplicationError(Exception):
    """Base exception class for application-specific errors."""
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

class DocumentProcessingError(ApplicationError):
    """Exception raised for errors during document processing."""
    pass

class IndexingError(ApplicationError):
    """Exception raised for errors during document indexing."""
    pass

class LLMError(ApplicationError):
    """Exception raised for errors with LLM interactions."""
    pass

class FileOperationError(ApplicationError):
    """Exception raised for errors during file operations."""
    pass

def handle_exceptions(func):
    """
    Decorator to handle and log exceptions in a consistent way.
    
    Usage:
        @handle_exceptions
        def my_function():
            # function code
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApplicationError as e:
            # Log application-specific errors
            # logger.error(f"{e.__class__.__name__}: {e.message}")
            try:
                logger.error(f"{e.__class__.__name__}: {e.message}")
            except Exception as logging_exception:
                # Fallback in case logging itself fails
                print(f"Logging failed: {logging_exception}")

            if e.original_exception:
                logger.debug(f"Original exception: {str(e.original_exception)}")
                logger.debug(traceback.format_exc())
            raise
        except Exception as e:
            # Log unexpected errors
            logger.critical(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.critical(traceback.format_exc())
            raise ApplicationError(f"An unexpected error occurred in {func.__name__}", e)
    return wrapper

def global_exception_handler(exctype, value, tb):
    """
    Global exception handler to catch unhandled exceptions.
    
    To use:
        sys.excepthook = global_exception_handler
    """
    logger.critical("".join(traceback.format_exception(exctype, value, tb)))
    print(f"\nERROR: {str(value)}")
    print("This error has been logged. Check the error log for details.")

# Set the global exception handler
sys.excepthook = global_exception_handler