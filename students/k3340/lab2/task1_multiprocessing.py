import multiprocessing as mp
import time

from config import TOTAL_N, WORKERS
from sum_utils import calculate_sum, expected_total, split_range


def worker(args: tuple[int, int]) -> int:
    start, end = args
    return calculate_sum(start, end)


def main() -> None:
    ranges = split_range(TOTAL_N, WORKERS)

    started = time.perf_counter()
    with mp.Pool(processes=WORKERS) as pool:
        partials = pool.map(worker, ranges)
    elapsed = time.perf_counter() - started

    total = sum(partials)
    expected = expected_total(TOTAL_N)
    print(f"multiprocessing: sum={total}, expected={expected}, ok={total == expected}")
    print(f"multiprocessing: elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
