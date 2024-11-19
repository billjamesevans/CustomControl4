# customControl4/director.py

import aiohttp
import async_timeout
import json
import logging
import ssl

from .error_handling import check_response_for_error

_LOGGER = logging.getLogger(__name__)


class Director:
    def __init__(self, ip, director_token, session: aiohttp.ClientSession = None):
        """Creates a Director object to interact with the Control4 Director."""
        self.ip = ip
        self.director_token = director_token
        self.session = session
        self.base_url = f"https://{ip}/api/v1"

        # Create SSL context to ignore certificate verification
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def send_get_request(self, endpoint):
        """Sends a GET request to the specified endpoint."""
        headers = {"Authorization": f"Bearer {self.director_token}"}
        url = f"{self.base_url}{endpoint}"

        if self.session is None:
            self.session = aiohttp.ClientSession()

        async with async_timeout.timeout(30):  # Increased timeout
            try:
                async with self.session.get(url, headers=headers, ssl=self.ssl_context) as response:
                    text = await response.text()
                    await check_response_for_error(text)
                    return text
            except Exception as e:
                _LOGGER.error(f"GET request failed: {e}")
                raise

    async def send_post_request(self, endpoint, command, params=None):
        """Sends a POST request with a command to the specified endpoint."""
        headers = {"Authorization": f"Bearer {self.director_token}"}
        url = f"{self.base_url}{endpoint}"
        data = {"command": command}
        if params:
            data.update(params)

        if self.session is None:
            self.session = aiohttp.ClientSession()

        async with async_timeout.timeout(30):  # Increased timeout
            try:
                async with self.session.post(
                    url, headers=headers, json=data, ssl=self.ssl_context
                ) as response:
                    text = await response.text()
                    await check_response_for_error(text)
                    return text
            except Exception as e:
                _LOGGER.error(f"POST request failed: {e}")
                raise

    async def get_all_items(self, limit=50, offset=0):
        """Retrieves all items from the Director in batches."""
        all_items = []
        while True:
            endpoint = f"/items?limit={limit}&offset={offset}"
            response = await self.send_get_request(endpoint)
            json_data = json.loads(response)
            items = json_data.get("items", [])
            if not items:
                break
            all_items.extend(items)
            offset += limit
        return all_items

    async def get_item_info(self, item_id):
        """Retrieves information about a specific item."""
        response = await self.send_get_request(f"/items/{item_id}")
        json_data = json.loads(response)
        return json_data

    async def close(self):
        """Closes the aiohttp session if it was created by this instance."""
        if self.session:
            await self.session.close()
