# customControl4

An improved Python library for interacting with Control4 systems.

## Features

- Asynchronous API calls using `aiohttp`
- Modular design for different device types (lights, relays, rooms, etc.)
- WebSocket support for real-time updates
- Custom error handling
- Easy-to-use classes for account authentication and director communication

## Installation

```bash
pip install -e .
```

## Usage

See `examples/example_usage.py` for a complete example of authenticating and
controlling a light.  Make sure the package dependencies are installed and
replace the placeholder credentials with your own Control4 account details.
