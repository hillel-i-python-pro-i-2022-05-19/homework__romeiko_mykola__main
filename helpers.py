def isfloat(data: str) -> bool:
    try:
        float(data)
        return True
    except ValueError:
        return False


def calculate_average(data: list) -> float:
    return sum(data) / len(data)


