import asyncio
import websockets

clients = set()

async def handle(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            await asyncio.gather(*[
                c.send(msg) for c in clients if c != ws
            ])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(ws)

async def main():
    async with websockets.serve(handle, "0.0.0.0", 24):
        print("Server running")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":

    asyncio.run(main())


