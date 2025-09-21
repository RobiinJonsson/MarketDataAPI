"""
Utilities for API calls including retry logic, rate limiting, and error handling.
"""

import logging
import random
import time
from datetime import UTC, datetime
from functools import wraps

from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout, RequestException

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Base exception for API-related errors."""

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status code: {self.status_code})"
        return self.message


class RetryExhaustedError(ApiError):
    """Raised when all retry attempts have been exhausted."""

    pass


class RateLimitError(ApiError):
    """Raised when API rate limit has been reached."""

    pass


class ApiTimeoutError(ApiError):
    """Raised when API request times out."""

    pass


def retry_with_backoff(
    max_retries=3,
    initial_backoff=1,
    max_backoff=60,
    backoff_factor=2,
    jitter=True,
    retryable_exceptions=(RequestException,),
    retryable_status_codes=(429, 500, 502, 503, 504),
):
    """
    Decorator that retries a function with exponential backoff when specified exceptions occur.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        initial_backoff: Initial backoff time in seconds (default: 1)
        max_backoff: Maximum backoff time in seconds (default: 60)
        backoff_factor: Multiplier for backoff time after each retry (default: 2)
        jitter: Whether to add random jitter to backoff time (default: True)
        retryable_exceptions: Tuple of exceptions that should trigger a retry (default: RequestException)
        retryable_status_codes: Tuple of status codes that should trigger a retry (default: 429, 500, 502, 503, 504)

    Returns:
        Decorated function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            backoff = initial_backoff

            while True:
                try:
                    response = func(*args, **kwargs)

                    # If the function returns a response object with status code
                    if (
                        hasattr(response, "status_code")
                        and response.status_code in retryable_status_codes
                    ):
                        if response.status_code == 429:
                            logger.warning(
                                f"Rate limit exceeded when calling {func.__name__}. Retry {retries+1}/{max_retries}"
                            )
                            raise RateLimitError(
                                f"Rate limit exceeded",
                                status_code=response.status_code,
                                response=response,
                            )
                        logger.warning(
                            f"Received status code {response.status_code} when calling {func.__name__}. "
                            f"Retry {retries+1}/{max_retries}"
                        )
                        raise HTTPError(f"HTTP error {response.status_code}", response=response)

                    # Check if response is a dict with an error key (our API format)
                    if isinstance(response, dict) and "error" in response:
                        error_msg = response["error"]
                        if "rate limit" in error_msg.lower():
                            logger.warning(
                                f"Rate limit error in response from {func.__name__}. "
                                f"Retry {retries+1}/{max_retries}"
                            )
                            raise RateLimitError(error_msg)

                    return response

                except retryable_exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Retry limit exceeded for {func.__name__}: {str(e)}")
                        if (
                            isinstance(e, HTTPError)
                            and hasattr(e, "response")
                            and e.response.status_code == 429
                        ):
                            raise RateLimitError(
                                f"Rate limit exceeded after {max_retries} retries",
                                status_code=e.response.status_code,
                                response=e.response,
                            )
                        elif isinstance(e, (ConnectTimeout, ReadTimeout)):
                            raise ApiTimeoutError(f"API timeout after {max_retries} retries") from e
                        elif isinstance(e, HTTPError):
                            raise ApiError(
                                f"HTTP error after {max_retries} retries",
                                status_code=(
                                    e.response.status_code if hasattr(e, "response") else None
                                ),
                                response=e.response if hasattr(e, "response") else None,
                            ) from e
                        raise RetryExhaustedError(
                            f"All retry attempts failed for {func.__name__}"
                        ) from e

                    # Calculate backoff time with exponential increase
                    current_backoff = min(backoff * (backoff_factor ** (retries - 1)), max_backoff)

                    # Add jitter if enabled (between 80% and 120% of current backoff)
                    if jitter:
                        current_backoff *= random.uniform(0.8, 1.2)

                    logger.warning(
                        f"Retry {retries}/{max_retries} for {func.__name__} after error: {str(e)}. "
                        f"Backing off for {current_backoff:.2f} seconds."
                    )

                    time.sleep(current_backoff)

        return wrapper

    return decorator


def log_api_call(func):
    """
    Decorator that logs API call details including timing and response status.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"API call started: {func.__name__}")

        try:
            result = func(*args, **kwargs)

            # Calculate execution time
            exec_time = time.time() - start_time

            # Determine if it was successful
            if isinstance(result, dict) and "error" in result:
                logger.error(
                    f"API call failed: {func.__name__} - {result['error']} (took {exec_time:.2f}s)"
                )
            else:
                logger.info(f"API call succeeded: {func.__name__} (took {exec_time:.2f}s)")

            return result

        except Exception as e:
            # Calculate execution time
            exec_time = time.time() - start_time
            logger.error(f"API call exception: {func.__name__} - {str(e)} (took {exec_time:.2f}s)")
            raise

    return wrapper
