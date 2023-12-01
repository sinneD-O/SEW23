import threading

import websockets
import asyncio

uri = "ws://localhost:8765/robot"

in_job = False


async def start_action(ws):
    in_job = True
    duration = 5
    await ws.send(f"Starting job\nDuration: {duration}sec")
    while duration > 0:
        await asyncio.sleep(1)
        await ws.send(f"{duration}secs remaining...")
        duration -= 1
    await ws.send(f"Job done.")
    in_job = False


async def send_robot_message(ws):
    while True:
        message = await get_input("Geben Sie ihre Nachricht ein: ")
        if message == "start":
            if in_job:
                await ws.send("Robot is currently on a mission! Please wait.")
            else:
                await start_action(ws)
        elif message == "close":
            await ws.send(message)
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
