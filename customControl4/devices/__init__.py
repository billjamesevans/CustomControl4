# customControl4/devices/__init__.py

from .light import Light
from .relay import Relay
from .room import Room   # Ensure this line exists

__all__ = ["Light", "Relay", "Room"]
