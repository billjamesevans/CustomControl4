# customControl4/devices/room.py

from ..director import Director


class Room:
    def __init__(self, director: Director, item_id: int):
        self.director = director
        self.item_id = item_id

    async def is_on(self):
        item_info = await self.director.get_item_info(self.item_id)
        power_state = item_info.get("properties", {}).get("POWER_STATE", False)
        return bool(power_state)

    async def turn_off(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "ROOM_OFF"
        )

    async def set_volume(self, level: int):
        if not 0 <= level <= 100:
            raise ValueError("Volume level must be between 0 and 100.")
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "SET_VOLUME_LEVEL", {"LEVEL": level}
        )

    async def mute(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "MUTE_ON"
        )

    async def unmute(self):
        await self.director.send_post_request(
            f"/items/{self.item_id}/commands", "MUTE_OFF"
        )