from fastapi import FastAPI
import uvicorn
import time as t, asyncio as aio
from models import CalculateRq, CalculateRs, Result

async def calculate_one(number: int, delay: float) -> Result:
    """
    Одна асинхронная задача:
    - ждёт `delay` секунд (event loop не блокируем),
    - считает квадрат и результат вместе с фактическим временем выполнения
    """
    start = t.perf_counter()
    await aio.sleep(delay)
    square = number ** 2
    elapsed = t.perf_counter() - start

    return Result(
        number = number,
        square = square,
        delay = delay,
        time=round(elapsed, 2),
    )

app = FastAPI(title = "HSE FastAPI demo :)")

@app.post("/calculate", response_model = CalculateRs)
async def calculate(rq: CalculateRq) -> CalculateRs:
    """
    Обрабатка запроса по асинхронной обработке квадратов с задержками
    """
    parallel_start = t.perf_counter()
    results = await aio.gather(
        *(calculate_one(n, d) for n, d in zip(rq.numbers, rq.delays))
    )
    total_time = t.perf_counter() - parallel_start
    sequential_time = sum(rq.delays)

    return CalculateRs(
        results = list(results),
        total_time = round(total_time, 2),
        parallel_faster_than_sequential = total_time < sequential_time,
    )

@app.get("/")
async def root():
    return {"message": "Your first FastAPI app, good job!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port = 8000
    )