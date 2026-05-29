import multiprocessing as mp
import time

from config import PARSE_URLS, WORKERS
from parse_utils import parse_and_save


def main() -> None:
    started = time.perf_counter()

    with mp.Pool(processes=min(WORKERS, len(PARSE_URLS))) as pool:
        pool.map(parse_and_save, PARSE_URLS)

    elapsed = time.perf_counter() - started
    print(f"multiprocessing parser: urls={len(PARSE_URLS)}, elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
