# pyControl4/error_handling.py

class Control4Error(Exception):
    """Base exception class for Control4 errors."""

class AuthenticationError(Control4Error):
    """Exception raised for authentication errors."""

class DirectorCommunicationError(Control4Error):
    """Exception raised for Director communication errors."""

class DeviceOperationError(Control4Error):
    """Exception raised for device operation errors."""