import numpy as np
import tkinter as tk

from carbon_plug.gui.label import Label

from main.misc import THEME_BORDER_COLOR


GRID = 64
UPSCALE = 4  # image upscaling. if `4` -> each cell is 4x4 pixels
PEN_EDGE = 38
PEN_CORNER = 18


width = GRID*UPSCALE  # the draw pad side length (border is excluded)
kernel = np.ones((UPSCALE, UPSCALE))
ppm_header = f'P5 {width} {width} 255 '.encode()


class DrawPad:

    tk_img = None  # the image must be stored to prevent lost by Python's garbage collector

    def __init__(self, page: tk.Canvas, tl_x, tl_y) -> None:
        """tl_x, tl_y: top-left of the first cell (not the draw pad border)."""

        self.page = page
        self.tl_x = tl_x
        self.tl_y = tl_y

        self.img_raw = np.zeros((GRID, GRID))

        Label(
            id='draw_pad1',
            x=self.tl_x - 1, y=self.tl_y - 1,
            text=f'({GRID}x{GRID} inputs)',
            font=('Arial Bold', 9), anchor='sw',
            fg='#fafbfa', bg='#101110',
            tags='clarity'
        )
        self.page.create_rectangle(
            self.tl_x - 1, self.tl_y - 1,
            self.tl_x + width, self.tl_y + width,
            outline=THEME_BORDER_COLOR, width=1
        )
        self.redraw()

    def redraw(self):
        ppm = ppm_header + np.kron(self.img_raw, kernel).astype(np.uint8).tobytes()
        DrawPad.tk_img = tk.PhotoImage(width=width, height=width, data=ppm, format='PPM')
        self.page.delete('draw_pad')
        self.page.create_image(self.tl_x, self.tl_y, image=DrawPad.tk_img, anchor='nw', tags='draw_pad')

    def get_pressed(self):

        cursor_x = self.page.winfo_pointerx()
        if cursor_x < self.tl_x:
            return

        cursor_y = self.page.winfo_pointery()
        if cursor_y < self.tl_y:
            return

        if cursor_x >= (self.tl_x + width):
            return
        if cursor_y >= (self.tl_y + width):
            return

        ## row (y) and column (x) of the pressed cell
        x = (cursor_x - self.tl_x)//UPSCALE
        y = (cursor_y - self.tl_y)//UPSCALE

        not_hit_u_edge = y != 0
        not_hit_d_edge = y != (GRID - 1)

        to_alter = {(x, y): 255}

        if x != 0:
            if not_hit_u_edge:
                to_alter[(x-1, y-1)] = PEN_CORNER
            if not_hit_d_edge:
                to_alter[(x-1, y+1)] = PEN_CORNER
            to_alter[(x-1, y)] = PEN_EDGE
        
        if x != (GRID - 1):
            if not_hit_u_edge:
                to_alter[(x+1, y-1)] = PEN_CORNER
            if not_hit_d_edge:
                to_alter[(x+1, y+1)] = PEN_CORNER
            to_alter[(x+1, y)] = PEN_EDGE

        if not_hit_u_edge:
            to_alter[(x, y-1)] = PEN_EDGE

        if not_hit_d_edge:
            to_alter[(x, y+1)] = PEN_EDGE

        return to_alter

    def paint(self) -> bool:
        """if cell(s) altered -> return `True`. otherwise, `False`."""

        to_alter = self.get_pressed()
        if to_alter is None:
            return False

        for (x, y), lum in to_alter.items():
            self.img_raw[y, x] = min(255, self.img_raw[y, x] + lum)

        self.redraw()
        return True

    def clear(self):
        self.img_raw = np.zeros((GRID, GRID))
        self.redraw()

    def display(self, img_core: list[tuple[int, float]]):
        self.img_raw = np.zeros((GRID, GRID))
        for i, a in img_core:
            self.img_raw[i//GRID, i%GRID] = a*255
        self.redraw()

    def get_img_raw(self) -> np.ndarray:
        """return the centered and resized version"""

        ## coordinate of non-zero values
        coords = np.argwhere(self.img_raw)
        
        ## bounding box
        bb_l, bb_u = coords.min(axis=0)
        bb_r, bb_d = coords.max(axis=0)
        
        width = bb_r - bb_l + 1
        height = bb_d - bb_u + 1
        max_dim = max(width, height)

        rows = coords[:, 0] - bb_l + (max_dim - width) // 2
        cols = coords[:, 1] - bb_u + (max_dim - height) // 2

        centered = np.zeros((max_dim, max_dim))
        centered[rows, cols] = self.img_raw[coords[:, 0], coords[:, 1]]

        i = np.arange(GRID, dtype=np.float32) * (max_dim/GRID)
        i = i.astype(int)
        return centered[i[:, np.newaxis], i]