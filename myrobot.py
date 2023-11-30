import threading

import websockets
import asyncio

uri = "ws://localhost:8765/robot"


async def send_robot_message(ws):
    while True:
        message = await get_input("Geben Sie ihre Nachricht ein: ")
        if message == "close":
            await ws.close()
            exit()
        else:
            await ws.send(message)


async def receive_robot_messages(ws):
    while True:
        message = await ws.recv()
        print(f"\n{message}")


async def get_input(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: input(prompt))


async def main():
    async with websockets.connect(uri) as ws:
        await asyncio.gather(send_robot_message(ws), receive_robot_messages(ws))

if __name__ == "__main__":
    thread = threading.Thread(target=lambda: asyncio.run(main()))
    thread.start()
    thread.join()
