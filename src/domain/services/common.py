def compute_growth_percentage(
    value_now: int | float,
    value_then: int | float,
) -> int:
    if value_then == 0:
        return 0
    return round((value_now - value_then) / value_then * 100)
