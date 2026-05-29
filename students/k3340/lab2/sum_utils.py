def split_range(total: int, parts: int) -> list[tuple[int, int]]:
    chunk_size = total // parts
    ranges: list[tuple[int, int]] = []
    start = 1
    for index in range(parts):
        end = start + chunk_size - 1 if index < parts - 1 else total
        ranges.append((start, end))
        start = end + 1
    return ranges


def calculate_sum(start: int, end: int) -> int:
    """Sum of integers from start to end inclusive (O(1) per range)."""
    if start > end:
        return 0
    return (end * (end + 1) // 2) - ((start - 1) * start // 2)


def expected_total(n: int) -> int:
    return n * (n + 1) // 2
