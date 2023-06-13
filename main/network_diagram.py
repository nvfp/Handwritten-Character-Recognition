import math
import numba as nb
import numpy as np
import time
import tkinter as tk

from mykit.app.label import Label
from mykit.kit.color import getgray, rgb_to_hex, interpolate_with_black
from mykit.kit.utils import printer

from main.neural_network import NeuralNetwork
from main.misc import THEME_BORDER_COLOR, THEME_FONT_COLOR


LABELS = '0123456789abcdefghijklmnopqrstuvwxyz'

## [from left edge, input to 1st-hidden, 1st to 2nd-hidden, ..., last-hidden to output]
NEURON_PAD_X = [40, 230, 120, 120, 150]
## [input, 1st-hidden, 2nd-hidden, ..., last-hidden, output]
NEURON_PAD_Y = [6, 14, 14, 14, 20]
NEURON_RADIUS = [3, 5, 5, 5, 6]
NEURON_MAX_LUM = 250
NEURON_BD_WIDTH = [1, 1, 1, 1, 2]
NEURON_BD_COLOR = ['#4fc778', '#fafbfa', '#fafbfa', '#fafbfa', '#ead76c']

COLOR_POSITIVE = np.array((200, 40, 10))
COLOR_NEGATIVE = np.array((9, 130, 211))
COLOR_DESICION = '#4fc778'

WEIGHT_MIN_ALPHA = 0.1

## optimization purposes
SHOWN_INPUT_NEURON_RATIO = 0.55  # if 0.75 -> only show 3/4 of the input-neurons (where the span location on `draw_pad` is as center as possible)
SHOWN_INPUT_NEURON_SCALE = 0.30  # if 0.75 -> only show 3/4 of the span, (3/4)^2 of all input-neurons
SHOWN_HIDDEN_NEURON_RATIO = 1  # if 0.5 -> only show the half of hidden neurons at each hidden layer
THRESHOLD = [0.1, 0.1, 0.1, 0.1, 0.005]  # only redraw if the change is significant


color_positive_in_hex = rgb_to_hex(*COLOR_POSITIVE)
color_negative_in_hex = rgb_to_hex(*COLOR_NEGATIVE)


@nb.njit
def line_overlay(screen: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: np.ndarray):
    """color: if red -> (255, 0, 0) or [255, 0, 0] or np.array([255, 0, 0])"""

    dx = x1 - x0
    dy = y1 - y0

    ## direction
    _x = 1 if dx > 0 else -1
    _y = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = _x, 0, 0, _y
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, _y, _x, 0
    
    ## optimization purposes
    dx2 = 2*dx
    dy2 = 2*dy

    d = dy2 - dx
    y = 0

    for x in range(dx + 1):

        screen[y0 + x*xy + y*yy, x0 + x*xx + y*yx] = color
        if d >= 0:
            y += 1
            d -= dx2
        d += dy2

class Weights:
    """for optimization purposes, the weight-lines represented as an image."""

    tk_img = None

    def __init__(self, page: tk.Canvas, nn: NeuralNetwork, width, height, tl_x, tl_y):

        self.page = page
        self.nn = nn
        self.width = width
        self.height = height
        self.tl_x = tl_x
        self.tl_y = tl_y

        self.screen = np.zeros((self.height, self.width, 3))
        self.lines = {}
        self.ppm_header = f'P6 {self.width} {self.height} 255 '.encode()

        for i in range(nn.n_layer - 1):

            l1 = NetworkDiagram.shown_neurons[i]
            l2 = NetworkDiagram.shown_neurons[i+1]

            H = (len(l1) - 1)*NEURON_PAD_Y[i]
            X1 = sum(NEURON_PAD_X[:i+1])
            Y1 = round((self.height - H)*0.5)

            H = (len(l2) - 1)*NEURON_PAD_Y[i+1]
            X2 = sum(NEURON_PAD_X[:i+1+1])
            Y2 = round((self.height - H)*0.5)

            for j, idx1 in enumerate(l1.keys()):
                for k, idx2 in enumerate(l2.keys()):

                    y1 = Y1 + NEURON_PAD_Y[i]*j
                    y2 = Y2 + NEURON_PAD_Y[i+1]*k

                    if nn.weights[i][idx2, idx1] >= 0:
                        line_overlay(self.screen, X1, y1, X2, y2, COLOR_POSITIVE*WEIGHT_MIN_ALPHA)
                    else:
                        line_overlay(self.screen, X1, y1, X2, y2, COLOR_NEGATIVE*WEIGHT_MIN_ALPHA)

                    self.lines[(i, idx2, idx1)] = (X1, y1, X2, y2)

        self.altered = True
        self.redraw()

    def alter_weight(self, i, j, k, src):
        """src: the activation value of the neuron that feeds the weight-line, with interval: [-1, 1]"""

        if self.nn.weights[i][j, k] >= 0:
            line_overlay(self.screen, *self.lines[(i, j, k)], COLOR_POSITIVE*abs(src))
        else:
            line_overlay(self.screen, *self.lines[(i, j, k)], COLOR_NEGATIVE*abs(src))
        
        self.altered = True

    def redraw(self):
        if self.altered:
            ppm = self.ppm_header + self.screen.astype(np.uint8).tobytes()
            Weights.tk_img = tk.PhotoImage(width=self.width, height=self.height, data=ppm, format='PPM')
            self.page.delete('weights')
            self.page.create_image(self.tl_x, self.tl_y, image=Weights.tk_img, anchor='nw', tags='weights')
            self.page.tag_lower('weights')
            self.altered = False


class NetworkDiagram:

    shown_neurons = None
    decision = None  # the last decision

    def optimize(self):
        """
        selecting the shown input neurons, weight-lines, and hidden neurons.
        also store their previous values.
        """

        grid = int(math.sqrt(self.nn.n_input))

        span = round(grid*SHOWN_INPUT_NEURON_RATIO)
        skip = round((grid - span)/2)  # skip the first `skip` rows and columns

        area = np.linspace(skip, skip + span - 1, round(span*SHOWN_INPUT_NEURON_SCALE)).astype(int).tolist()

        input_neurons = {}
        for row in area:
            for column in area:
                input_neurons[row + column*grid] = 0

        hidden_neurons = []
        for n in self.nn.hidden_layers:
            hidden_neurons.append({i: 0 for i in np.linspace(0, n - 1, round(n*SHOWN_HIDDEN_NEURON_RATIO)).astype(int).tolist()})

        NetworkDiagram.shown_neurons = [input_neurons, *hidden_neurons, {i: 0 for i in range(self.nn.n_output)}]

        printer(f'#shown neurons: {[len(i) for i in NetworkDiagram.shown_neurons]}')

    def __init__(self, page: tk.Canvas, nn: NeuralNetwork, width, height, tl_x, tl_y) -> None:
        """
        width, height: of the diagram (border is excluded).
        tl_x, tl_y: top-left of the diagram (not the diagram border).
        """

        self.page = page
        self.nn = nn

        page.create_rectangle(
            tl_x - 1, tl_y - 1,
            tl_x + width, tl_y + height,
            width=1, outline=THEME_BORDER_COLOR
        )
        Label(
            id='nd_title1', x=tl_x+20, y=tl_y+2,
            text=f'sizes: {nn.sizes}',
            font=('Consolas Bold', 9), anchor='nw',
            fg=THEME_FONT_COLOR, bg='#000000',
            tags=('clarity', 'nd')
        )
        Label(
            id='nd_title2', x=tl_x+227, y=tl_y,
            text='*not all input-neurons are shown',
            font='Arial 7', anchor='nw',
            fg='#b2b3b2', bg='#000000', tags=('clarity', 'nd')
        )

        self.optimize()

        printer('Weight-lines initialization..')
        self.weights = Weights(page, nn, width, height, tl_x, tl_y)
        printer('Weight-lines created.')

        for i, neuron_values in enumerate(NetworkDiagram.shown_neurons):

            H = (len(neuron_values) - 1)*NEURON_PAD_Y[i]
            X = tl_x + sum(NEURON_PAD_X[:i+1])
            Y = tl_y + (height - H)*0.5
            
            for j, neuron_idx in enumerate(neuron_values.keys()):

                page.create_oval(
                    X - NEURON_RADIUS[i],
                    Y + NEURON_PAD_Y[i]*j - NEURON_RADIUS[i],
                    X + NEURON_RADIUS[i],
                    Y + NEURON_PAD_Y[i]*j + NEURON_RADIUS[i],
                    fill='#000000',
                    width=NEURON_BD_WIDTH[i],
                    outline=NEURON_BD_COLOR[i],
                    tags=f'neuron_{i}_{neuron_idx}'
                )

                if i == (nn.n_layer - 1):
                    Label(
                        id=f'output_label_{j}', x=X+18, y=Y+NEURON_PAD_Y[i]*j,
                        text=LABELS[j],
                        font='Consolas 10', anchor='w',
                        fg='#dbe8fc', bg='#000000',
                        tags=['nd', 'train']
                    )
                    Label(
                        id=f'output_value_{j}', x=X+28, y=Y+NEURON_PAD_Y[i]*j,
                        text=': 0.00',
                        font='Consolas 10', anchor='w',
                        fg='#dbe8fc', bg='#000000',
                        tags=('clarity', 'nd', 'train')
                    )

    def recolor(self):
        """after feedforwarding"""

        # t0 = time.time()

        for i, neuron_values in enumerate(NetworkDiagram.shown_neurons):
            for neuron_idx, neuron_value in neuron_values.items():

                new = self.nn.a_values[i][neuron_idx, 0]
                if abs(new - neuron_value) > THRESHOLD[i]:

                    NetworkDiagram.shown_neurons[i][neuron_idx] = new

                    if i in {0, self.nn.n_layer - 1}:
                        self.page.itemconfigure(f'neuron_{i}_{neuron_idx}', fill=getgray(new, NEURON_MAX_LUM))
                    else:
                        if new >= 0:
                            color = interpolate_with_black(color_positive_in_hex, new)
                        else:
                            color = interpolate_with_black(color_negative_in_hex, -new)

                        self.page.itemconfigure(f'neuron_{i}_{neuron_idx}', fill=color)

                    if i < (self.nn.n_layer - 1):
                        for neuron_idx2 in NetworkDiagram.shown_neurons[i+1].keys():
                            self.weights.alter_weight(i, neuron_idx2, neuron_idx, new)

                    if i == (self.nn.n_layer - 1):
                        Label.set_text_by_id(f'output_value_{neuron_idx}', f': {new:.2f}')

        if NetworkDiagram.decision is None:
            self.page.itemconfigure(f'neuron_{i}_{self.nn.decision}', outline=COLOR_DESICION)
            NetworkDiagram.decision = self.nn.decision
        else:
            if self.nn.decision != NetworkDiagram.decision:
                self.page.itemconfigure(f'neuron_{i}_{NetworkDiagram.decision}', outline=NEURON_BD_COLOR[i])
                self.page.itemconfigure(f'neuron_{i}_{self.nn.decision}', outline=COLOR_DESICION)
                NetworkDiagram.decision = self.nn.decision

        self.weights.redraw()

        # printer(f'recolor time: {time.time()-t0}s')