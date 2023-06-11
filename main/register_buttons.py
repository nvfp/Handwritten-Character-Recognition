import numpy as np
import os
import random
import tkinter as tk

from carbon.path import SafeJSON
from carbon.text import byteFmt
from carbon.utils import printer

from carbon_plug.gui.button import Button
from carbon_plug.gui.label import Label

from main.misc import SAVED_NETWORK_DIR_PTH


LABELS = '0123456789abcdefghijklmnopqrstuvwxyz'
MAP = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19,
    'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29,
    'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35
}


def register_buttons(
    NN_DATASET_RATIO,
    NN_N_EPOCH,
    NN_SAMPLE_SIZE,
    NN_LEARNING_RATE,
    NN_REGULARIZATION,
    NN_EARLY_STOP_AFTER,
    Runtime,
    root,
    page: tk.Canvas,
    draw_pad,
    dataset,
    nn,
    network_diagram,
    graph,
    output_box,
    show_result
):

    x = 45
    y = page.winfo_reqheight()*0.69

    def fn():
        draw_pad.clear()
        output_box.tell(None)
    Button(id='clear', x=x, y=y, label='clear', fn=fn, len=50)

    Button(id='feedforward', x=x+70, y=y, label='feedforward', fn=show_result, len=80)

    def fn():
        Runtime.realtime = not Runtime.realtime
        if Runtime.realtime:
            Button.set_lock_by_id('feedforward', True)
            Button.set_label_by_id('realtime', 'realtime (ON)')
        else:
            Button.set_lock_by_id('feedforward', False)
            Button.set_label_by_id('realtime', 'realtime (OFF)')
    Button(id='realtime', x=x+170, y=y, label='realtime (OFF)', fn=fn, len=100)


    x = 25
    y = page.winfo_reqheight()*0.69 + 35
    pad_x = 25
    pad_y = 29
    len = 20
    def fn_wrapper(idx):
        def fn():
            printer(f'Saving a new img_core of character {repr(LABELS[idx])}.')
            dataset.save(draw_pad.get_img_raw(), idx)
            text = (
                '======================\n'
                f'#training data: {round(NN_DATASET_RATIO*dataset.n):,}\n'
                f'#validation data: {round((1 - NN_DATASET_RATIO)*dataset.n):,}\n'
                f'total dataset: {dataset.n:,}\n'
                f'dataset size: {byteFmt(dataset.size)}'
            )
            Label.set_text_by_id('info1', text)
            draw_pad.clear()
        return fn
    for i, j in enumerate('1234567890'):
        Button(id=f'train_data_{j}', x=x+pad_x*i, y=y+pad_y*0, label=j, fn=fn_wrapper(MAP[j]), len=len, tags='clarity')
    for i, j in enumerate('qwertyuiop'):
        Button(id=f'train_data_{j}', x=x+pad_x*i+14, y=y+pad_y*1, label=j, fn=fn_wrapper(MAP[j]), len=len, tags='clarity')
    for i, j in enumerate('asdfghjkl'):
        Button(id=f'train_data_{j}', x=x+pad_x*i+21, y=y+pad_y*2, label=j, fn=fn_wrapper(MAP[j]), len=len, tags='clarity')
    for i, j in enumerate('zxcvbnm'):
        Button(id=f'train_data_{j}', x=x+pad_x*i+30, y=y+pad_y*3, label=j, fn=fn_wrapper(MAP[j]), len=len, tags='clarity')


    x = 40
    y = page.winfo_reqheight()*0.69 + 150

    def fn():
        graph.hide()  # hide if shown
        dataset.show()
    Button(id='open', x=x, y=y, label='open', fn=fn, len=45, tags='clarity')

    ## <train>
    def _fn(epoch):

        test_img_core, _ = random.choice(dataset.dataset)

        draw_pad.display(test_img_core)

        ff = np.zeros((nn.n_input, 1))
        for i, a in test_img_core:
            ff[i] = a

        nn.feedforward(ff)
        network_diagram.recolor()
        output_box.tell(nn.decision)

        text = (
            f'training status: {"ON" if (epoch < NN_N_EPOCH) else "OFF"}\n'
            f'epoch: {epoch}/{NN_N_EPOCH}\n'
            '======================\n'
            f'#learn: {nn.metadata["n_learn"]:,}\n'
            '======================\n'
            f'highest training accuracy  : {max(nn.metadata["t_acc"]):.2f}\n'
            f'last training accuracy     : {nn.metadata["t_acc"][-1]:.2f}\n'
            f'highest validation accuracy: {max(nn.metadata["v_acc"]):.2f}\n'
            f'last validation accuracy   : {nn.metadata["v_acc"][-1]:.2f}\n'
            '======================\n'
            f'lowest training cost  : {min(nn.metadata["t_cost"]):.2f}\n'
            f'last training cost    : {nn.metadata["t_cost"][-1]:.2f}\n'
            f'lowest validation cost: {min(nn.metadata["v_cost"]):.2f}\n'
            f'last validation cost  : {nn.metadata["v_cost"][-1]:.2f}'
        )
        Label.set_text_by_id('info2', text)

        root.update()

    def fn():

        if dataset.n < 10:
            printer('not enough data to train.')
            return

        text = (
            'training status: ON\n'
            f'epoch: -/{NN_N_EPOCH}\n'
            '======================\n'
            f'#learn: {nn.metadata["n_learn"]:,}\n'
            '======================\n'
            f'highest training accuracy  : {max(nn.metadata["t_acc"]) if (nn.metadata["t_acc"] != []) else 0:.2f}\n'
            f'last training accuracy     : {nn.metadata["t_acc"][-1] if (nn.metadata["t_acc"] != []) else 0:.2f}\n'
            f'highest validation accuracy: {max(nn.metadata["v_acc"]) if (nn.metadata["v_acc"] != []) else 0:.2f}\n'
            f'last validation accuracy   : {nn.metadata["v_acc"][-1] if (nn.metadata["v_acc"] != []) else 0:.2f}\n'
            '======================\n'
            f'lowest training cost  : {min(nn.metadata["t_cost"]) if (nn.metadata["t_cost"] != []) else 0:.2f}\n'
            f'last training cost    : {nn.metadata["t_cost"][-1] if (nn.metadata["t_cost"] != []) else 0:.2f}\n'
            f'lowest validation cost: {min(nn.metadata["v_cost"]) if (nn.metadata["v_cost"] != []) else 0:.2f}\n'
            f'last validation cost  : {nn.metadata["v_cost"][-1] if (nn.metadata["v_cost"] != []) else 0:.2f}'
        )
        Label.set_text_by_id('info2', text)

        Button.set_visibility_all(False)
        Label.set_visibility_all(False)
        Label.set_visibility_by_tag('train', True)
        graph.hide()  # hide if shown

        root.update()

        t_data, v_data = dataset.shuffle(NN_DATASET_RATIO)
        nn.train(t_data, NN_N_EPOCH, NN_SAMPLE_SIZE, NN_LEARNING_RATE, NN_REGULARIZATION, v_data, NN_EARLY_STOP_AFTER, fn=_fn)

        Button.set_visibility_all(True)
        Button.set_visibility_by_tag('dataset', False)
        Label.set_visibility_all(True)
        graph.show()

    Button(id='train', x=x+55, y=y, label='train', fn=fn, len=40, tags='clarity')
    ## </train>

    def fn():
        weights = [w.tolist() for w in nn.weights]
        biases = [b.tolist() for b in nn.biases]
        SafeJSON.rewrite(os.path.join(SAVED_NETWORK_DIR_PTH, 'weights.json'), weights)
        SafeJSON.rewrite(os.path.join(SAVED_NETWORK_DIR_PTH, 'biases.json'), biases)
        SafeJSON.rewrite(os.path.join(SAVED_NETWORK_DIR_PTH, 'metadata.json'), nn.metadata)
    Button(id='save', x=x+110, y=y, label='save', fn=fn, len=50, tags='clarity')


    def fn():
        Runtime.clarity = not Runtime.clarity
        if Runtime.clarity:
            Label.set_visibility_by_tag('clarity', False)
            Button.set_visibility_by_tag('clarity', False)
            Button.set_label_by_id('clarity', 'show')
        else:
            Label.set_visibility_by_tag('clarity', True)
            Button.set_visibility_by_tag('clarity', True)
            Button.set_label_by_id('clarity', 'hide')
    Button(id='clarity', x=35, y=page.winfo_reqheight()*0.95, label='hide', fn=fn, len=45)