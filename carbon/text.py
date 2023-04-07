import math as _math


_BYTE_UNIT = [
    'B',
    'KiB',
    'MiB',
    'GiB',
    'TiB',
    'PiB',
    'EiB',
    'ZiB',
    'YiB',
]
def byte(__bytes: int, /) -> str:

    if __bytes == 0:
        return '0 B'

    exp = _math.floor(_math.log(abs(__bytes), 1024))
    val = round( __bytes / _math.pow(1024, exp), 2)

    return f'{val} {_BYTE_UNIT[exp]}'