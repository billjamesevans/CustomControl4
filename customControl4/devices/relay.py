# customControl4/devices/relay.py

from ..director import Director


class Relay:
    def __init__(self, director: Director, item_id: int):
        self.director = director
        self.item_id = item_id

    async def get_state(self):
        item_info = await self.director.get_item_info(self.item_id)
        # Adjust based on actual API response structure
        state = item_info.get("properties", {}).get("RelayState", None)
        return state

    async def open(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "OPEN"
        )

    async def close(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "CLOSE"
        )

    async def toggle(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "TOGGLE"
        )