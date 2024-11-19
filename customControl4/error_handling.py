# customControl4/error_handling.py

import json
import logging

_LOGGER = logging.getLogger(__name__)


class Control4Error(Exception):
    """Base exception class for Control4 errors."""


class AuthenticationError(Control4Error):
    """Exception raised for authentication errors."""


class DirectorCommunicationError(Control4Error):
    """Exception raised for Director communication errors."""


class DeviceOperationError(Control4Error):
    """Exception raised for device operation errors."""


async def check_response_for_error(response_text):
    """Checks the response text for errors and raises exceptions accordingly."""
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        _LOGGER.error("Invalid JSON response.")
        raise Control4Error("Invalid JSON response.")

    if "code" in response_json and response_json["code"] != 200:
        code = response_json.get("code")
        message = response_json.get("message", "Unknown error.")
        _LOGGER.error(f"Error {code}: {message}")
        if code == 401:
            raise AuthenticationError(message)
        elif code == 404:
            raise DirectorCommunicationError(message)
        else:
            raise Control4Error(message)