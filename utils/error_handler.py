from utils.logger import setup_logger
from typing import Callable, Any

logger = setup_logger(__name__)


async def handle_async_errors(
    func: Callable,
    error_message: str,
    raise_on_error: bool = False,
    default_return: Any = None,
) -> Any:
    """
    Wrapper for handling async function errors with logging.

    Args:
        func: Async function to execute
        error_message: Error message to log
        raise_on_error: Whether to raise the error after logging
        default_return: Value to return on error if not raising

    Returns:
        Function result or default_return on error
    """
    try:
        return await func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        if raise_on_error:
            raise
        return default_return


def handle_sync_errors(
    func: Callable,
    error_message: str,
    raise_on_error: bool = False,
    default_return: Any = None,
) -> Any:
    """
    Wrapper for handling sync function errors with logging.

    Args:
        func: Sync function to execute
        error_message: Error message to log
        raise_on_error: Whether to raise the error after logging
        default_return: Value to return on error if not raising

    Returns:
        Function result or default_return on error
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        if raise_on_error:
            raise
        return default_return
