import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import PARSE_URLS, WORKERS
from parse_utils import parse_and_save


def main() -> None:
    started = time.perf_counter()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {executor.submit(parse_and_save, url): url for url in PARSE_URLS}
        for future in as_completed(futures):
            future.result()

    elapsed = time.perf_counter() - started
    print(f"threading parser: urls={len(PARSE_URLS)}, elapsed={elapsed:.4f}s, workers={WORKERS}")


if __name__ == "__main__":
    main()
