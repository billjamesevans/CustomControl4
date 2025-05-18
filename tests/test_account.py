import sys
import types
import unittest
from unittest.mock import AsyncMock, patch

# Stub aiohttp and async_timeout to avoid external dependencies
aiohttp_stub = types.ModuleType('aiohttp')
class BaseClientSession:
    def __init__(self, *args, **kwargs):
        pass
aiohttp_stub.ClientSession = BaseClientSession
sys.modules.setdefault('aiohttp', aiohttp_stub)

async_timeout_stub = types.ModuleType('async_timeout')
class timeout:
    def __init__(self, *args, **kwargs):
        pass
    async def __aenter__(self):
        return None
    async def __aexit__(self, exc_type, exc, tb):
        pass
async_timeout_stub.timeout = timeout
sys.modules.setdefault('async_timeout', async_timeout_stub)

# Stub socketio to avoid dependency when importing the package
socketio_stub = types.ModuleType('socketio')
class AsyncClient:
    def __init__(self, *args, **kwargs):
        pass
socketio_stub.AsyncClient = AsyncClient
sys.modules.setdefault('socketio', socketio_stub)

from customControl4.account import Account, AUTHENTICATION_ENDPOINT

class DummyResponse:
    async def text(self):
        return '{"authToken": {"token": "abc123"}}'
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        pass

class DummySession(aiohttp_stub.ClientSession):
    def post(self, url, json):
        self.called_url = url
        self.called_json = json
        return DummyResponse()
    async def close(self):
        pass

class AccountTest(unittest.IsolatedAsyncioTestCase):
    async def test_authenticate_sets_token(self):
        session = DummySession()
        account = Account('user', 'pass', session=session)
        with patch('customControl4.account.check_response_for_error', new=AsyncMock()):
            await account.authenticate()
        self.assertEqual(account.account_bearer_token, 'abc123')
        self.assertEqual(session.called_url, AUTHENTICATION_ENDPOINT)
