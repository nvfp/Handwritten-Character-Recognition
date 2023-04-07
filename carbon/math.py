import numpy as _np


def tanh(x: float, /, *, derivative: bool = False) -> float:

    z = _np.tanh(x)

    if derivative:
        return 1 - z*z
    else:
        return z


def sigmoid(x: float, /, *, derivative: bool = False) -> float:
    
    z = 1/(1 + _np.exp(-x))

    if derivative:
        return z*(1 - z)
    else:
        return z