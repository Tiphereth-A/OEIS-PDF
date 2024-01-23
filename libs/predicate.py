def is_non_negative(_seq: list[int]) -> bool:
    return all(i >= 0 for i in _seq)


def in_range(_seq: list[int], min_value: int, max_value: int) -> bool:
    return all(min_value <= i <= max_value for i in _seq)


def is_sorted(_seq: list) -> bool:
    return all(_seq[i] <= _seq[i + 1] for i in range(len(_seq) - 1))


def is_rev_sorted(_seq: list) -> bool:
    return all(_seq[i] >= _seq[i + 1] for i in range(len(_seq) - 1))


def is_abs_sorted(_seq: list[int]) -> bool:
    return all(abs(_seq[i]) <= abs(_seq[i + 1]) for i in range(len(_seq) - 1))


def is_abs_rev_sorted(_seq: list[int]) -> bool:
    return all(abs(_seq[i]) >= abs(_seq[i + 1]) for i in range(len(_seq) - 1))


def is_valid(_seq: list[int]) -> bool:
    return in_range(_seq[:len(_seq) // 3], 0, 2 ** 32 - 1) and in_range(_seq[:len(_seq) // 2], 0, 2 ** 64 - 1) and is_sorted(_seq)
