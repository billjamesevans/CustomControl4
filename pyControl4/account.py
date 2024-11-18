# pyControl4/account.py

import aiohttp
import asyncio
import logging

class Account:
    AUTH_ENDPOINT = "https://apis.control4.com/authentication/v1/rest"
    APP_KEY = "your_application_key_here"  # Replace with your application key

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession = None):
        self.username = username
        self.password = password
        self.session = session or aiohttp.ClientSession()
        self.account_token = None
        self.logger = logging.getLogger(__name__)

    async def authenticate(self):
        payload = {
            "clientInfo": {
                "device": {
                    "deviceName": "CustomClient",
                    "deviceUUID": "0000000000000000",
                    "make": "CustomClient",
                    "model": "CustomClient",
                    "os": "Python",
                    "osVersion": "3.x",
                },
                "userInfo": {
                    "applicationKey": self.APP_KEY,
                    "password": self.password,
                    "userName": self.username,
                },
            }
        }

        async with self.session.post(self.AUTH_ENDPOINT, json=payload) as response:
            data = await response.json()
            if response.status == 200 and "authToken" in data:
                self.account_token = data["authToken"]["token"]
                self.logger.info("Account authenticated successfully.")
            else:
                self.logger.error("Authentication failed.")
                raise Exception("Authentication failed.")

    async def get_controllers(self):
        if not self.account_token:
            raise Exception("Authenticate first before retrieving controllers.")

        headers = {"Authorization": f"Bearer {self.account_token}"}
        controllers_endpoint = "https://apis.control4.com/account/v3/rest/accounts"

        async with self.session.get(controllers_endpoint, headers=headers) as response:
            data = await response.json()
            if response.status == 200:
                return data.get("account", {})
            else:
                self.logger.error("Failed to retrieve controllers.")
                raise Exception("Failed to retrieve controllers.")

    async def get_director_token(self, controller_common_name: str):
        if not self.account_token:
            raise Exception("Authenticate first before retrieving director token.")

        headers = {"Authorization": f"Bearer {self.account_token}"}
        director_auth_endpoint = "https://apis.control4.com/authentication/v1/rest/authorization"
        payload = {
            "serviceInfo": {
                "commonName": controller_common_name,
                "services": "director",
            }
        }

        async with self.session.post(director_auth_endpoint, headers=headers, json=payload) as response:
            data = await response.json()
            if response.status == 200 and "authToken" in data:
                director_token = data["authToken"]["token"]
                self.logger.info("Director token retrieved successfully.")
                return director_token
            else:
                self.logger.error("Failed to retrieve director token.")
                raise Exception("Failed to retrieve director token.")

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()