import asyncio
import time

from config import TOTAL_N, WORKERS
from sum_utils import calculate_sum, expected_total, split_range


async def calculate_sum_async(start: int, end: int) -> int:
    return await asyncio.to_thread(calculate_sum, start, end)


async def main_async() -> int:
    ranges = split_range(TOTAL_N, WORKERS)
    tasks = [calculate_sum_async(start, end) for start, end in ranges]
    partials = await asyncio.gather(*tasks)
    return sum(partials)


def main() -> None:
    started = time.perf_counter()
    total = asyncio.run(main_async())
    elapsed = time.perf_counter() - started

    expected = expected_total(TOTAL_N)
    print(f"async: sum={total}, expected={expected}, ok={total == expected}")
    print(f"async: elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
