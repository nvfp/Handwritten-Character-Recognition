"""
This model is designed for 64x64 inputs and 36 outputs.

FAQ:
-Why `tkinter.PhotoImage` rather than `tkinter.canvas.create_line` to draw the weight-lines?
    On the author's machine, Tkinter canvas didn't perform well with more than 5000 items

"""
import numpy as np
import os
import time
import tkinter as tk

from carbon.gui.button import Button
from carbon.gui.label import Label
from carbon.path import Json
from carbon.time import get_dur
from carbon.utils import printer

from main.draw_pad import DrawPad, width as draw_pad_width
from main.dataset import Dataset
from main.neural_network import NeuralNetwork
from main.graph import Graph
from main.network_diagram import NetworkDiagram
from main.output_box import OutputBox
from main.register_buttons import register_buttons
from main.register_labels import register_labels
from main.misc import SOFTWARE_NAME, SOFTWARE_VER, SAVED_NETWORK_DIR_PTH, THEME_BACKGROUND


STARTUP_TIME = time.time()

NN_NEW = False  # if `True` -> generate new weights and biases
NN_SIZES = [64*64, 50, 40, 35, 10+26]
NN_DATASET_RATIO = 0.85
NN_N_EPOCH = 5
NN_SAMPLE_SIZE = 4
NN_LEARNING_RATE = 0.045
NN_REGULARIZATION = 0.001
NN_EARLY_STOP_AFTER = 2


class Runtime:
    realtime = False
    clarity = False


root = tk.Tk()
root.attributes('-fullscreen', True)
root.title(f'{SOFTWARE_NAME}_v{SOFTWARE_VER}')

page = tk.Canvas(
    master=root,
    width=root.winfo_screenwidth(),
    height=root.winfo_screenheight(),
    background=THEME_BACKGROUND,
    borderwidth=0, highlightthickness=0
)
page.place(x=0, y=0)

Button.page = page


draw_pad = DrawPad(page, 15, (page.winfo_reqheight() - 64*4)//2)
dataset = Dataset(page)

## <neural network>
if NN_NEW:
    weights = None
    biases = None
    metadata = None
else:

    printer('Loading the saved network.')
    weights = Json.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'weights.json'))
    weights = [np.array(w) for w in weights]

    biases = Json.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'biases.json'))
    biases = [np.array(b) for b in biases]

    metadata = Json.read(os.path.join(SAVED_NETWORK_DIR_PTH, 'metadata.json'))
    printer(f'Using network with {metadata["n_learn"]} total learns.')

nn = NeuralNetwork(sizes=NN_SIZES, weights=weights, biases=biases, metadata=metadata)
## </neural network>

NETWORK_DIAGRAM_WIDTH = 750
NETWORK_DIAGRAM_HEIGHT = 750
NETWORK_DIAGRAM_TL_X = draw_pad.tl_x + draw_pad_width + 10
NETWORK_DIAGRAM_TL_Y = (page.winfo_reqheight() - NETWORK_DIAGRAM_HEIGHT)*0.5
network_diagram = NetworkDiagram(
    page, nn,
    NETWORK_DIAGRAM_WIDTH, NETWORK_DIAGRAM_HEIGHT,
    NETWORK_DIAGRAM_TL_X, NETWORK_DIAGRAM_TL_Y,
)

graph = Graph(
    page, nn,
    NETWORK_DIAGRAM_WIDTH, NETWORK_DIAGRAM_HEIGHT,
    NETWORK_DIAGRAM_TL_X, NETWORK_DIAGRAM_TL_Y,
)

output_box = OutputBox(
    page,
    310,
    page.winfo_reqheight()*0.15,
    NETWORK_DIAGRAM_TL_X + NETWORK_DIAGRAM_WIDTH + 10,
    (page.winfo_reqheight() - page.winfo_reqheight()*0.15)*0.5,
)


def show_result():

    inputs_vectorized = np.round(draw_pad.get_img_raw()/255, 2).ravel().reshape((-1, 1))
    nn.feedforward(inputs_vectorized)

    network_diagram.recolor()
    output_box.tell(nn.decision)

def left_mouse_press(e):
    Button.press_listener()    
    if draw_pad.paint() and Runtime.realtime:
        show_result()
root.bind('<ButtonPress-1>', left_mouse_press)

def left_mouse_hold(e):
    if draw_pad.paint() and Runtime.realtime:
        show_result()
root.bind('<B1-Motion>', left_mouse_hold)

def left_mouse_release(e):
    Button.release_listener()
root.bind('<ButtonRelease-1>', left_mouse_release)


register_buttons(
    NN_DATASET_RATIO,
    NN_N_EPOCH,
    NN_SAMPLE_SIZE,
    NN_LEARNING_RATE,
    NN_REGULARIZATION,
    NN_EARLY_STOP_AFTER,
    Runtime,
    root,
    page,
    draw_pad,
    dataset,
    nn,
    network_diagram,
    graph,
    output_box,
    show_result
)

register_labels(
    NN_DATASET_RATIO,
    NN_N_EPOCH,
    NN_SAMPLE_SIZE,
    NN_LEARNING_RATE,
    NN_REGULARIZATION,
    NN_EARLY_STOP_AFTER,
    page, dataset, nn
)


def background_slow():
    Label.set_text_by_id('up_time', f'up time: {get_dur(time.time()-STARTUP_TIME)}')
    root.after(1000, background_slow)

def background_fast():
    Button.hover_listener()
    root.after(50, background_fast)

def exit(e):
    root.destroy()
    printer(f'Exit with total up-time {get_dur(time.time()-STARTUP_TIME)}.')
root.bind('<Escape>', exit)


if __name__ == '__main__':
    background_slow()
    background_fast()
    root.mainloop()