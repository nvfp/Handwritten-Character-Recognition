

def hexa_to_hex(fg: str, alpha: float, bg: str, /) -> str:
    """
    hexadecimal color code `fg` with given opacity `alpha` on background `bg`.
    the `fg` and `bg` must be a valid hexadecimal color code, and `alpha` value must in interval [0, 1].
    """

    fg = [int(fg[i:i+2], 16) for i in (1, 3, 5)]
    bg = [int(bg[i:i+2], 16) for i in (1, 3, 5)]

    r = round(fg[0]*alpha + bg[0]*(1 - alpha))
    g = round(fg[1]*alpha + bg[1]*(1 - alpha))
    b = round(fg[2]*alpha + bg[2]*(1 - alpha))

    return f'#{r:02x}{g:02x}{b:02x}'


def get_gray(alpha: float, max_lum: int = 255, /) -> str:
    """
    alpha interval: [0, 1].
    max_lum interval: [0, 255].
    """
    a = f'{round(max_lum*alpha):02x}'
    return f'#{a}{a}{a}'


def interpolate_with_black(color: str, alpha: float, /) -> str:

    color = [int(color[i:i+2], 16) for i in (1, 3, 5)]

    r = round(color[0]*alpha)
    g = round(color[1]*alpha)
    b = round(color[2]*alpha)

    return f'#{r:02x}{g:02x}{b:02x}'


def rgb_to_hex(r: int, g: int, b: int, /) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'