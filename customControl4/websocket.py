# customControl4/websocket.py

import aiohttp
import async_timeout
import socketio
import logging

_LOGGER = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(
        self,
        ip,
        director_token,
        session: aiohttp.ClientSession = None,
        connect_callback=None,
        disconnect_callback=None,
    ):
        """Creates a WebSocket client to receive real-time updates."""
        self.ip = ip
        self.director_token = director_token
        self.session = session or aiohttp.ClientSession()
        self.connect_callback = connect_callback
        self.disconnect_callback = disconnect_callback
        self.sio = socketio.AsyncClient(ssl_verify=False)
        self.connected = False

    async def connect(self):
        """Establishes the WebSocket connection."""
        url = f"wss://{self.ip}/socket.io/?transport=websocket"

        @self.sio.event
        async def connect():
            self.connected = True
            _LOGGER.info("WebSocket connected.")
            if self.connect_callback:
                await self.connect_callback()

        @self.sio.event
        async def disconnect():
            self.connected = False
            _LOGGER.info("WebSocket disconnected.")
            if self.disconnect_callback:
                await self.disconnect_callback()

        await self.sio.connect(
            url, headers={"Authorization": f"Bearer {self.director_token}"}
        )

    async def subscribe(self, item_ids, callback):
        """Subscribes to updates for specific item IDs."""
        if not self.connected:
            raise Exception("WebSocket is not connected.")

        @self.sio.on("event")
        async def on_event(data):
            _LOGGER.debug(f"Received event: {data}")
            await callback(data)

        # Send subscription message
        await self.sio.emit("subscribe", {"items": item_ids})

    async def disconnect(self):
        """Disconnects the WebSocket connection."""
        await self.sio.disconnect()