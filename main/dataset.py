import numpy as np
import os
import random
import tkinter as tk

from mykit.app.button import Button
from mykit.app.label import Label
from mykit.kit.path import SafeJSON
from mykit.kit.utils import printer

from main.misc import SOFTWARE_DIR_PTH, THEME_BORDER_COLOR, THEME_FONT_COLOR


DATASET_DIR_PTH = os.path.join(SOFTWARE_DIR_PTH, 'dataset')

GRID = 64
N_OUTPUT = 10+26
LABELS = '0123456789abcdefghijklmnopqrstuvwxyz'
BG = '#020302'

PREVIEW_UPSCALE = 2
PREVIEW_PAD = 40
PORTION_X = 0.9
PORTION_Y = 0.9
SHIFT_TL_X = 160
SHIFT_TL_Y = 60


preview_side_len = GRID*PREVIEW_UPSCALE
kernel = np.ones((PREVIEW_UPSCALE, PREVIEW_UPSCALE))
ppm_header = f'P5 {preview_side_len} {preview_side_len} 255 '.encode()
input_indices = np.arange(GRID*GRID)


class Dataset:

    ncolumn = None
    nrow = None
    npreview = None
    nskip = 0
    tk_img = {}

    def __init__(self, page: tk.Canvas) -> None:

        self.page = page

        self.dataset = []
        self.n = 0  # total dataset
        self.n_char = {}  # number of datasets of each character
        self.size = 0

        for i in range(N_OUTPUT):

            pth = os.path.join(DATASET_DIR_PTH, f'{i}.json')

            k = 0
            for img_core in SafeJSON.read(pth):
                self.dataset.append((img_core, i))
                k += 1

            self.n += k
            self.n_char[i] = k
            self.size += os.path.getsize(pth)
            printer(f'Dataset-{i} is loaded.')

        pack = [
            ('close', self.hide),
            ('up', self.up),
            ('down', self.down),
            ('up2', self.up2),
            ('down2', self.down2),
            ('top', self.top),
            ('bottom', self.bottom),
            ('delete', self.delete),
        ]
        for i, (label, fn) in enumerate(pack):
            Button(id=f'dataset_{label}', x=40+60*i, y=15, label=label, fn=fn, width=50, locked=True, visible=False, tags='dataset', anchor='center')
        Button.set_lock_by_id('dataset_close', False)
        Button.set_lock_by_id('dataset_delete', False)

        Dataset.ncolumn = int(page.winfo_reqwidth()*PORTION_X//(preview_side_len + PREVIEW_PAD))
        Dataset.nrow = int(page.winfo_reqheight()*PORTION_Y//(preview_side_len + PREVIEW_PAD))
        Dataset.npreview = Dataset.ncolumn*Dataset.nrow
        printer(f'#preview: {Dataset.nrow}x{Dataset.ncolumn} [{Dataset.npreview}]')

    def redraw_previews(self):

        self.page.delete('dataset_previews')

        n = 0
        for i, (img_core, output_idx) in enumerate(self.dataset, 1):

            if i <= Dataset.nskip:
                continue

            if (i - Dataset.nskip) > Dataset.npreview:
                break

            tl_x = SHIFT_TL_X + (preview_side_len + PREVIEW_PAD)*(n%Dataset.ncolumn)
            tl_y = SHIFT_TL_Y + (preview_side_len + PREVIEW_PAD)*(n//Dataset.ncolumn)

            self.page.create_rectangle(
                tl_x - 1, tl_y - 1,
                tl_x + preview_side_len, tl_y + preview_side_len,
                width=1, outline=THEME_BORDER_COLOR,
                tags=('dataset', 'dataset_previews')
            )

            img_raw = np.zeros((GRID, GRID))
            for idx, a in img_core:
                img_raw[idx//GRID, idx%GRID] = a*255
            ppm = ppm_header + np.kron(img_raw, kernel).astype(np.uint8).tobytes()
            Dataset.tk_img[n] = tk.PhotoImage(width=preview_side_len, height=preview_side_len, data=ppm, format='PPM')
            self.page.create_image(tl_x, tl_y, image=Dataset.tk_img[n], anchor='nw', tags=('dataset', 'dataset_previews'))

            self.page.create_text(
                tl_x + preview_side_len/2,
                tl_y + preview_side_len + 10,
                text=f'{i}/{self.n}, label: {LABELS[output_idx]}',
                font='Consolas 9',
                fill=THEME_FONT_COLOR,
                tags=('dataset', 'dataset_previews')
            )
            n += 1

    def up(self):
        
        Button.set_lock_by_id('dataset_down', False)
        Button.set_lock_by_id('dataset_down2', False)
        Button.set_lock_by_id('dataset_bottom', False)

        Dataset.nskip -= Dataset.ncolumn
        if Dataset.nskip == 0:
            Button.set_lock_by_id('dataset_up', True)
            Button.set_lock_by_id('dataset_up2', True)
            Button.set_lock_by_id('dataset_top', True)

        self.redraw_previews()

    def down(self):
        
        Button.set_lock_by_id('dataset_up', False)
        Button.set_lock_by_id('dataset_up2', False)
        Button.set_lock_by_id('dataset_top', False)

        Dataset.nskip += Dataset.ncolumn
        if (self.n - Dataset.nskip) <= Dataset.npreview:
            Button.set_lock_by_id('dataset_down', True)
            Button.set_lock_by_id('dataset_down2', True)
            Button.set_lock_by_id('dataset_bottom', True)

        self.redraw_previews()

    def up2(self):
        
        Button.set_lock_by_id('dataset_down', False)
        Button.set_lock_by_id('dataset_down2', False)
        Button.set_lock_by_id('dataset_bottom', False)

        Dataset.nskip = max(0, Dataset.nskip - Dataset.npreview)
        if Dataset.nskip == 0:
            Button.set_lock_by_id('dataset_up', True)
            Button.set_lock_by_id('dataset_up2', True)
            Button.set_lock_by_id('dataset_top', True)

        self.redraw_previews()

    def down2(self):
        
        Button.set_lock_by_id('dataset_up', False)
        Button.set_lock_by_id('dataset_up2', False)
        Button.set_lock_by_id('dataset_top', False)

        Dataset.nskip += Dataset.npreview
        if (self.n - Dataset.nskip) <= Dataset.npreview:
            Button.set_lock_by_id('dataset_down', True)
            Button.set_lock_by_id('dataset_down2', True)
            Button.set_lock_by_id('dataset_bottom', True)

        self.redraw_previews()

    def top(self):
        
        Button.set_lock_by_id('dataset_down', False)
        Button.set_lock_by_id('dataset_down2', False)
        Button.set_lock_by_id('dataset_bottom', False)

        Dataset.nskip = 0
        Button.set_lock_by_id('dataset_up', True)
        Button.set_lock_by_id('dataset_up2', True)
        Button.set_lock_by_id('dataset_top', True)

        self.redraw_previews()

    def bottom(self):
        
        Button.set_lock_by_id('dataset_up', False)
        Button.set_lock_by_id('dataset_up2', False)
        Button.set_lock_by_id('dataset_top', False)

        Dataset.nskip = ((self.n - 1)//Dataset.ncolumn)*Dataset.ncolumn
        Button.set_lock_by_id('dataset_down', True)
        Button.set_lock_by_id('dataset_down2', True)
        Button.set_lock_by_id('dataset_bottom', True)

        self.redraw_previews()
    
    def delete(self):

        try:
            i = int(input(f'Dataset index to delete [0 - {self.n - 1}]: '))
            if (i < 0) or (i >= self.n):
                printer('Invalid index.')
                return
        except ValueError:
            printer('Canceled.')
            return

        img_core, idx = self.dataset[i]

        usr = input(f'Continue to delete img_core with label {repr(LABELS[idx])} [y: Yes] [q: Cancel]? ')
        if usr != 'y':
            printer('Canceled...')
            return

        pth = os.path.join(DATASET_DIR_PTH, f'{idx}.json')
        data = SafeJSON.read(pth)

        self.dataset.remove((img_core, idx))
        self.n -= 1
        self.n_char[idx] -= 1
        self.size -= len(str(img_core))

        data.remove(img_core)
        SafeJSON.rewrite(pth, data)
        printer('Image deleted.')

        self.page.itemconfigure('dataset_nchar', text=f'\n'.join([f'#{LABELS[i]}: {j:,}' for i, j in self.n_char.items()]))
        self.redraw_previews()

    def show(self):
        
        Button.set_visibility_all(False)
        Label.set_visibility_all(False)

        self.page.create_rectangle(
            0, 0,
            self.page.winfo_reqwidth(), self.page.winfo_reqheight(),
            fill=BG,
            tags='dataset'
        )
        self.page.create_text(
            20, 50,
            text=f'\n'.join([f'#{LABELS[i]}: {j:,}' for i, j in self.n_char.items()]),
            font='Consolas 11', justify='left', anchor='nw',
            fill=THEME_FONT_COLOR,
            tags=('dataset', 'dataset_nchar')
        )
        self.redraw_previews()
        Button.set_visibility_by_tag('dataset', True)

        if (self.n - Dataset.nskip) > Dataset.npreview:
            Button.set_lock_by_id('dataset_down', False)
            Button.set_lock_by_id('dataset_down2', False)
            Button.set_lock_by_id('dataset_bottom', False)

    def hide(self):

        Button.set_visibility_all(True)
        Button.set_visibility_by_tag('dataset', False)

        Label.set_visibility_all(True)

        self.page.delete('dataset')

    def shuffle(self, ratio):
        """if ratio = 0.75 -> 75% for training data, 25% for validation data"""

        random.shuffle(self.dataset)
        k = round(self.n*ratio)

        training_data = self.dataset[:k]
        validation_data = self.dataset[k:]

        return training_data, validation_data

    def save(self, img_raw: np.ndarray, idx: int):

        if not np.any(img_raw):
            printer('Blank image should not be saved.')
            return

        flat = img_raw.flatten()
        norm = np.round(flat/255, 2)
        mask = norm > 0
        img_core = [
            [x, y]
            for x, y in zip(input_indices[mask].tolist(), norm[mask].tolist())
        ]

        pth = os.path.join(DATASET_DIR_PTH, f'{idx}.json')
        data = SafeJSON.read(pth)

        if img_core in data:
            printer(f'This img_core with output-index {idx} is already exists.')
            return

        self.dataset.append((img_core, idx))
        self.n += 1
        self.n_char[idx] += 1
        self.size += len(str(img_core))

        data.append(img_core)
        SafeJSON.rewrite(pth, data)
        printer(f'New img_core with output-index {idx} is added.')