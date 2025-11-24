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

port = int(os.environ.get("PORT", 6789))

async def main():
    async with websockets.serve(handle, "0.0.0.0", port):
        print("Server running at ws://ip:port")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":

    asyncio.run(main())
