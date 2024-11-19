# customControl4/devices/light.py

from ..director import Director


class Light:
    def __init__(self, director: Director, item_id: int):
        self.director = director
        self.item_id = item_id

    async def get_state(self):
        item_info = await self.director.get_item_info(self.item_id)
        # Adjust based on actual API response structure
        state = item_info.get("properties", {}).get("value", None)
        return state

    async def set_level(self, level: int, ramp_rate: int = 0):
        if not 0 <= level <= 100:
            raise ValueError("Level must be between 0 and 100.")
        command = "RAMP_TO_LEVEL"
        params = {"LEVEL": level, "TIME": ramp_rate}
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", command, params
        )

    async def turn_on(self):
        await self.set_level(100)

    async def turn_off(self):
        await self.set_level(0)