import asyncio
from env_channel.server import EnvChannelServer


async def main():
    server = EnvChannelServer(host="0.0.0.0", port=8765)
    await server.start()
    print("EnvChannelServer started at ws://0.0.0.0:8765")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
