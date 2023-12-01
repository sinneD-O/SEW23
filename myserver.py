import websockets
import asyncio


connected = set()


async def app_handler(websocket):
    try:
        async for message in websocket:
            print(f"App sent message: {message}")
            if message == "close":
                connected.remove(websocket)
                break
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("App disconnected.")
        return websockets.exceptions.ConnectionClosedError


async def robot_handler(websocket):
    try:
        async for message in websocket:
            print(f"Robot sent message: {message}")
            if message == "close":
                connected.remove(websocket)
                return "close"
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Robot disconnected.")
        return websockets.exceptions.ConnectionClosedError


async def handler(websocket, path):
    connected.add(websocket)

    while True:
        try:
            if path == "/app":
                print(f"App Connected.")
                msg = await app_handler(websocket)
                if msg == "close":
                    break
            elif path == "/robot":
                print(f"Robot Connected.")
                msg = await robot_handler(websocket)
                if msg == "close":
                    break
            else:
                print(f"Unknown path: {path}")
        except websockets.exceptions.ConnectionClosedError:
            if path == "/app":
                print(f"App disconnected.")
            elif path == "/robot":
                print(f"Robot disconnected.")


async def main():
    start_server = await websockets.serve(handler, "localhost", 8765)

    await start_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
