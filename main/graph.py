import tkinter as tk

from mykit.app.button import Button
from mykit.app.label import Label

from main.misc import THEME_BORDER_COLOR, THEME_FONT_COLOR


GRAPH_BG = '#020302'
TDATA_COLOR = '#296ab4'
VDATA_COLOR = '#c93a3a'
LINE_WIDTH = 3
PLOT_PORTION_X = 0.90
PLOT_PORTION_Y = 0.35
AXES_COLOR = '#010201'
PLOT_BG = '#d2b68d'
TAIL = 20


class Graph:

    def __init__(self, page: tk.Canvas, nn, width, height, tl_x, tl_y):

        self.page = page
        self.nn = nn
        self.width = width
        self.height = height
        self.tl_x = tl_x
        self.tl_y = tl_y

        Button(id='graph', x=tl_x+25, y=tl_y+height-17, label='show', fn=self.show, width=45, tags='clarity', anchor='center')

    def plot(self, title, t_data, v_data, xmax, ymax, width, height, tl_x, tl_y):

        self.page.create_text(
            tl_x, tl_y,
            text=title, font=('Arial Bold', 12), anchor='sw',
            fill=THEME_FONT_COLOR, tags='graph'
        )
        self.page.create_rectangle(
            tl_x, tl_y,
            tl_x + width, tl_y + height,
            fill=PLOT_BG, width=0, tags='graph'
        )

        origin_x = tl_x + width*0.06
        origin_y = tl_y + height - height*0.1
        x_axis_len = width*0.85
        y_axis_len = height*0.8

        self.page.create_text(
            origin_x - 4, origin_y + 1,
            text='0', font='Consolas 11', anchor='ne',
            fill=AXES_COLOR, tags='graph'
        )
        self.page.create_text(
            origin_x + x_axis_len/2, origin_y + 5,
            text='#epoch', font='Arial 11', anchor='n',
            fill=AXES_COLOR, tags='graph'
        )

        ## x-axis
        self.page.create_line(
            origin_x - TAIL, origin_y,
            origin_x + x_axis_len, origin_y,
            fill=AXES_COLOR, width=1, tags='graph'
        )
        self.page.create_text(
            origin_x + x_axis_len + 3, origin_y,
            text=xmax, font='Consolas 11',
            fill=AXES_COLOR, anchor='w', tags='graph'
        )

        ## y-axis
        self.page.create_line(
            origin_x, origin_y + TAIL,
            origin_x, origin_y - y_axis_len,
            fill=AXES_COLOR, width=1, tags='graph'
        )
        self.page.create_text(
            origin_x, origin_y - y_axis_len - 2,
            text=round(ymax, 2), font='Consolas 11',
            fill=AXES_COLOR, anchor='s', tags='graph'
        )

        t_vertices = []
        v_vertices = []
        for i, (j, k) in enumerate(zip(t_data, v_data), 1):  # it starts from 1 because the first epoch is labeled as 1
            x = origin_x + (i/xmax)*x_axis_len
            t_vertices += [x, origin_y - (j/ymax)*y_axis_len]
            v_vertices += [x, origin_y - (k/ymax)*y_axis_len]
        if t_vertices != []:
            self.page.create_line(*t_vertices, fill=TDATA_COLOR, width=LINE_WIDTH, tags='graph')
            self.page.create_line(*v_vertices, fill=VDATA_COLOR, width=LINE_WIDTH, tags='graph')

    def show(self):

        self.page.create_rectangle(
            self.tl_x - 1, self.tl_y - 1,
            self.tl_x + self.width, self.tl_y + self.height,
            fill=GRAPH_BG, width=1, outline=THEME_BORDER_COLOR, tags='graph'
        )

        ## header
        x = self.tl_x + self.width*0.12
        y = self.tl_y + self.height*0.09
        w = 30
        h = 6
        pad = 20
        self.page.create_rectangle(
            x - w/2, y - h/2,
            x + w/2, y + h/2,
            fill=TDATA_COLOR, width=0, tags='graph'
        )
        self.page.create_rectangle(
            x - w/2, y - h/2 + pad,
            x + w/2, y + h/2 + pad,
            fill=VDATA_COLOR, width=0, tags='graph'
        )
        self.page.create_text(
            x + w, y + 10,
            text='training data\nvalidation data', font=('Arial Bold', 13), justify='left',
            fill=THEME_FONT_COLOR, anchor='w', tags='graph'
        )

        ## plots
        n = len(self.nn.metadata['t_acc'])
        w = self.width*PLOT_PORTION_X
        h = self.height*PLOT_PORTION_Y
        pad = 40
        self.plot(
            title='Accuracy', t_data=self.nn.metadata['t_acc'], v_data=self.nn.metadata['v_acc'],
            xmax=n if (n > 0) else 1, ymax=1,
            width=w, height=h,
            tl_x=self.tl_x + 25, tl_y=self.tl_y + self.height - h*2 - pad*2,
        )
        self.plot(
            title='Cost', t_data=self.nn.metadata['t_cost'], v_data=self.nn.metadata['v_cost'],
            xmax=n if (n > 0) else 1,
            ymax=max(self.nn.metadata['t_cost'] + self.nn.metadata['v_cost']) if (n > 0) else 1,
            width=w, height=h,
            tl_x=self.tl_x + 25, tl_y=self.tl_y + self.height - h - pad,
        )

        Button.set_label_by_id('graph', 'hide')
        Button.set_fn_by_id('graph', self.hide)
        Label.set_visibility_by_tag('nd', False)

    def hide(self):
        self.page.delete('graph')
        Button.set_label_by_id('graph', 'show')
        Button.set_fn_by_id('graph', self.show)
        Label.set_visibility_by_tag('nd', True)