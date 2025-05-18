# customControl4/account.py

import aiohttp
import async_timeout
import json
import logging

from .error_handling import check_response_for_error

AUTHENTICATION_ENDPOINT = "https://apis.control4.com/authentication/v1/rest"
CONTROLLER_AUTHORIZATION_ENDPOINT = (
    "https://apis.control4.com/authentication/v1/rest/authorization"
)
GET_CONTROLLERS_ENDPOINT = "https://apis.control4.com/account/v3/rest/accounts"
APPLICATION_KEY = "78f6791373d61bea49fdb9fb8897f1f3af193f11"  # Updated Application Key

_LOGGER = logging.getLogger(__name__)


class Account:
    def __init__(self, username, password, session: aiohttp.ClientSession = None):
        """Creates a Control4 account object."""
        self.username = username
        self.password = password
        self.session = session
        self.account_bearer_token = None

    async def authenticate(self):
        """Authenticates with the Control4 API to retrieve an account bearer token."""
        data = {
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
                    "applicationKey": APPLICATION_KEY,
                    "password": self.password,
                    "userName": self.username,
                },
            }
        }

        if self.session is None:
            self.session = aiohttp.ClientSession()

        async with async_timeout.timeout(10):
            async with self.session.post(
                AUTHENTICATION_ENDPOINT, json=data
            ) as response:
                text = await response.text()
                await check_response_for_error(text)
                json_data = json.loads(text)
                _LOGGER.debug(f"Authentication response: {json_data}")
                try:
                    self.account_bearer_token = json_data["authToken"]["token"]
                    _LOGGER.info("Account authenticated successfully.")
                except KeyError:
                    _LOGGER.error("Authentication failed.")
                    _LOGGER.error(f"Response received: {json_data}")
                    raise Exception("Authentication failed.")

    async def get_controllers(self):
        """Retrieves a list of controllers registered to the account."""
        if not self.account_bearer_token:
            raise Exception("Authenticate first before retrieving controllers.")

        headers = {"Authorization": f"Bearer {self.account_bearer_token}"}

        async with async_timeout.timeout(10):
            async with self.session.get(
                GET_CONTROLLERS_ENDPOINT, headers=headers
            ) as response:
                text = await response.text()
                await check_response_for_error(text)
                json_data = json.loads(text)
                account_info = json_data.get("account", {})
                controllers = account_info.get("controllers", [])
                return controllers

    async def get_director_token(self, controller_common_name):
        """Retrieves a director bearer token for local communication with the controller."""
        if not self.account_bearer_token:
            raise Exception("Authenticate first before retrieving director token.")

        headers = {"Authorization": f"Bearer {self.account_bearer_token}"}
        data = {
            "serviceInfo": {
                "commonName": controller_common_name,
                "services": "director",
            }
        }

        async with async_timeout.timeout(10):
            async with self.session.post(
                CONTROLLER_AUTHORIZATION_ENDPOINT, headers=headers, json=data
            ) as response:
                text = await response.text()
                await check_response_for_error(text)
                json_data = json.loads(text)
                _LOGGER.debug(f"Director token response: {json_data}")
                try:
                    director_token = json_data["authToken"]["token"]
                    _LOGGER.info("Director token retrieved successfully.")
                    return director_token
                except KeyError:
                    _LOGGER.error("Failed to retrieve director token.")
                    _LOGGER.error(f"Response received: {json_data}")
                    raise Exception("Failed to retrieve director token.")

    async def close(self):
        """Closes the aiohttp session if it was created by this instance."""
        if self.session:
            await self.session.close()
