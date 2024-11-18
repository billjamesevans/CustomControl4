# pyControl4/director.py

import aiohttp
import logging

class Director:
    def __init__(self, ip: str, token: str, session: aiohttp.ClientSession = None):
        self.ip = ip
        self.token = token
        self.session = session or aiohttp.ClientSession()
        self.base_url = f"https://{ip}/api/v1"
        self.logger = logging.getLogger(__name__)

    async def get_all_items(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/items"

        async with self.session.get(url, headers=headers, ssl=False) as response:
            data = await response.json()
            if response.status == 200:
                return data.get("items", [])
            else:
                self.logger.error("Failed to retrieve items from Director.")
                raise Exception("Failed to retrieve items from Director.")

    async def get_item_info(self, item_id: int):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/items/{item_id}"

        async with self.session.get(url, headers=headers, ssl=False) as response:
            data = await response.json()
            if response.status == 200:
                return data
            else:
                self.logger.error(f"Failed to retrieve info for item {item_id}.")
                raise Exception(f"Failed to retrieve info for item {item_id}.")

    async def send_command(self, item_id: int, command: str, params: dict = None):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/items/{item_id}/commands"
        payload = {"command": command}
        if params:
            payload.update(params)

        async with self.session.post(url, headers=headers, json=payload, ssl=False) as response:
            if response.status == 200:
                self.logger.info(f"Command '{command}' sent to item {item_id}.")
            else:
                self.logger.error(f"Failed to send command '{command}' to item {item_id}.")
                raise Exception(f"Failed to send command '{command}' to item {item_id}.")

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()