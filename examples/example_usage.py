# examples/example_usage.py

import asyncio
from customControl4 import Account, Director, Light

async def main():
    # Create an account instance and authenticate
    account = Account("your_username", "your_password")
    await account.authenticate()

    # Get controllers and select one
    controllers = await account.get_controllers()
    controller_name = controllers.get("controllerCommonName")
    if not controller_name:
        print("No controllers found.")
        return

    # Get director token
    director_token = await account.get_director_token(controller_name)

    # Initialize Director instance
    director = Director("192.168.1.25", director_token)

    # Control a light
    light = Light(director, item_id=253)
    await light.turn_on()
    print("Light turned on.")
    await asyncio.sleep(2)
    await light.set_level(50)
    print("Light dimmed to 50%.")
    await asyncio.sleep(2)
    await light.turn_off()
    print("Light turned off.")

    # Close sessions
    await director.close()
    await account.close()

asyncio.run(main())
