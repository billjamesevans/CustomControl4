# pyControl4/devices/relay.py

from ..director import Director

class Relay:
    def __init__(self, director: Director, item_id: int):
        self.director = director
        self.item_id = item_id

    async def get_state(self):
        item_info = await self.director.get_item_info(self.item_id)
        return item_info.get("properties", {}).get("relay_state", None)

    async def open(self):
        await self.director.send_command(self.item_id, "OPEN")

    async def close(self):
        await self.director.send_command(self.item_id, "CLOSE")

    async def toggle(self):
        await self.director.send_command(self.item_id, "TOGGLE")