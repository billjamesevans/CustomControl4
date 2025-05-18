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

## Application Key

The `Account` class uses an application key when authenticating with the
Control4 API.  By default the library includes a built in key, but you can
provide your own either through the `Account` constructor or by setting the
`CONTROL4_APPLICATION_KEY` environment variable.
