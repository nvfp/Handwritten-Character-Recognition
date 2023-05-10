import tkinter as tk

from carbon_plug.gui.label import Label
from carbon_plug.text import byte

from main.misc import THEME_BACKGROUND, THEME_FONT_COLOR


def register_labels(
    NN_DATASET_RATIO,
    NN_N_EPOCH,
    NN_SAMPLE_SIZE,
    NN_LEARNING_RATE,
    NN_REGULARIZATION,
    NN_EARLY_STOP_AFTER,
    page: tk.Canvas, dataset, nn
):

    n_trainable_params = 0
    for i, j in enumerate(nn.sizes):
        if i > 0:
            n_trainable_params += j*nn.sizes[i-1]  # weights
            n_trainable_params += j  # biases
    Label(
        id='metadata',
        x=15, y=0,
        text=(
            '======================\n'
            'h_act = tanh\n'
            'o_act = sigmoid\n'
            'cost_fn = CrossEntropy\n'
            f'dataset_ratio = {NN_DATASET_RATIO}\n'
            f'n_epoch = {NN_N_EPOCH}\n'
            f'sample_size = {NN_SAMPLE_SIZE}\n'
            f'learning_rate = {NN_LEARNING_RATE}\n'
            f'regularization = {NN_REGULARIZATION}\n'
            f'early_stop_after = {NN_EARLY_STOP_AFTER}\n'
            '======================\n'
            f'#trainable params: {n_trainable_params:,}'
        ),
        font='Consolas 11', justify='left', anchor='nw',
        fg=THEME_FONT_COLOR, bg=THEME_BACKGROUND, tags='clarity',
    )

    Label(
        id='info1',
        x=page.winfo_reqwidth()*0.77, y=15,
        text=(
            '======================\n'
            f'#training data: {round(NN_DATASET_RATIO*dataset.n):,}\n'
            f'#validation data: {round((1 - NN_DATASET_RATIO)*dataset.n):,}\n'
            f'total dataset: {dataset.n:,}\n'
            f'dataset size: {byte(dataset.size)}'
        ),
        font='Consolas 12', justify='left', anchor='nw',
        fg=THEME_FONT_COLOR, bg=THEME_BACKGROUND, tags='clarity',
    )

    Label(
        id='info2',
        x=page.winfo_reqwidth()*0.77, y=page.winfo_reqheight()*0.6,
        text=(
            'training status: OFF\n'
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
        ),
        font='Consolas 11', justify='left', anchor='nw',
        fg=THEME_FONT_COLOR, bg=THEME_BACKGROUND,
        tags=['clarity', 'train'],
    )

    Label(
        id='up_time',
        x=96, y=page.winfo_reqheight()*0.95,
        text='up time: 0 sec', font='Arial 9',
        fg=THEME_FONT_COLOR, bg=THEME_BACKGROUND,
        tags=['clarity', 'train']
    )