import datetime as _datetime


def printer(__text: str, /) -> None:
    t = _datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{t}] {__text}')