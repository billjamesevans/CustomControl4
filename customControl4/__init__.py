# customControl4/__init__.py

from .account import Account
from .director import Director
from .websocket import WebSocketClient
from .error_handling import Control4Error
from .devices import Light, Relay, Room   # Ensure 'Room' is included here

__all__ = [
    "Account",
    "Director",
    "WebSocketClient",
    "Control4Error",
    "Light",
    "Relay",
    "Room",
    # Add other classes as needed
]