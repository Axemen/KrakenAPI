import asyncio
import json

import websockets


async def main():
    uri = "wss://ws.kraken.com"

    subscribe = {
        "event": "subscribe",
        "pair": [
            "XBT/USD"
        ],
        "subscription": {
            "name": "ticker"
        }
    }

    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps(subscribe))
        response = ws.recv()
        print(response)
        print('Connected')

        while True:
            data = await ws.recv()
            print(data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
