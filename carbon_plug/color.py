




def interpolate_with_black(color: str, alpha: float, /) -> str:

    color = [int(color[i:i+2], 16) for i in (1, 3, 5)]

    r = round(color[0]*alpha)
    g = round(color[1]*alpha)
    b = round(color[2]*alpha)

    return f'#{r:02x}{g:02x}{b:02x}'
