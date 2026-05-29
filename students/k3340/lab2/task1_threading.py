import threading
import time

from config import TOTAL_N, WORKERS
from sum_utils import calculate_sum, expected_total, split_range


def worker(start: int, end: int, results: list[int], index: int) -> None:
    results[index] = calculate_sum(start, end)


def main() -> None:
    ranges = split_range(TOTAL_N, WORKERS)
    results = [0] * WORKERS
    threads: list[threading.Thread] = []

    started = time.perf_counter()
    for index, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=worker, args=(start, end, results, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    elapsed = time.perf_counter() - started

    expected = expected_total(TOTAL_N)
    print(f"threading: sum={total}, expected={expected}, ok={total == expected}")
    print(f"threading: elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
