class UnknownUnitError(ValueError):
    pass


def milliseconds_per(unit_name: str) -> int:
    """
    Return the number of milliseconds per time unit, where the time unit is one
    of ["millisecond", "second", "minute", "hour"]
    """
    options = {
        "millisecond": 1,
        "second": 1000,
        "minute": 60 * 1000,
        "hour": 60 * 60 * 1000,
    }

    try:
        return options[unit_name]
    except KeyError as k:
        raise UnknownUnitError(unit_name) from k
