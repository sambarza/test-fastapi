from fastapi import FastAPI
import asyncio

app = FastAPI()

counter = 0
task_incrementor = None
incrementor_status = "Stopped"


async def incrementor(delay: int):

    global counter
    global incrementor_status

    incrementor_status = "Running"

    while True:
        counter += 1
        await asyncio.sleep(delay)


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/start_counter/{delay}")
async def start_counter(delay: int):

    global task_incrementor
    global incrementor_status

    task_incrementor = asyncio.create_task(incrementor(delay))

    incrementor_status = "Started"

    return {"incrementor_status": incrementor_status}


@app.get("/get_counter")
async def get_counter():

    global counter

    return {"counter": counter}


@app.get("/get_incrementor_status")
async def get_incrementor_status():

    global incrementor_status

    return {"incrementor_status": incrementor_status}


@app.post("/stop_counter")
async def stop_counter():

    global counter
    global task_incrementor
    global incrementor_status

    counter_value_before_stop = counter
    task_incrementor.cancel()

    incrementor_status = "Stopped"

    return {
        "incrementor_status": incrementor_status,
        "value_before_stop": counter_value_before_stop,
    }
