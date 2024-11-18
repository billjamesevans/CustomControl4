# pyControl4/devices/room.py

from ..director import Director

class Room:
    def __init__(self, director: Director, item_id: int):
        self.director = director
        self.item_id = item_id

    async def is_on(self):
        item_info = await self.director.get_item_info(self.item_id)
        return item_info.get("properties", {}).get("power_state", False)

    async def turn_off(self):
        await self.director.send_command(self.item_id, "ROOM_OFF")

    async def set_volume(self, level: int):
        if not 0 <= level <= 100:
            raise ValueError("Volume level must be between 0 and 100.")
        await self.director.send_command(self.item_id, "SET_VOLUME_LEVEL", {"level": level})

    async def mute(self):
        await self.director.send_command(self.item_id, "MUTE_ON")

    async def unmute(self):
        await self.director.send_command(self.item_id, "MUTE_OFF")