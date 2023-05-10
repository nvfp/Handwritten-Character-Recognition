import tkinter as tk

from carbon_plug.gui.label import Label

from main.misc import THEME_BORDER_COLOR


NATO_PHONETIC_ALPHABET = {
    0: ('0', 'Zero'),
    1: ('1', 'One'),
    2: ('2', 'Two'),
    3: ('3', 'Three'),
    4: ('4', 'Four'),
    5: ('5', 'Five'),
    6: ('6', 'Six'),
    7: ('7', 'Seven'),
    8: ('8', 'Eight'),
    9: ('9', 'Nine'),
    10: ('a', 'Alfa'),
    11: ('b', 'Bravo'),
    12: ('c', 'Charlie'),
    13: ('d', 'Delta'),
    14: ('e', 'Echo'),
    15: ('f', 'Foxtrot'),
    16: ('g', 'Golf'),
    17: ('h', 'Hotel'),
    18: ('i', 'India'),
    19: ('j', 'Juliett'),
    20: ('k', 'Kilo'),
    21: ('l', 'Lima'),
    22: ('m', 'Mike'),
    23: ('n', 'November'),
    24: ('o', 'Oscar'),
    25: ('p', 'Papa'),
    26: ('q', 'Quebec'),
    27: ('r', 'Romeo'),
    28: ('s', 'Sierra'),
    29: ('t', 'Tango'),
    30: ('u', 'Uniform'),
    31: ('v', 'Victor'),
    32: ('w', 'Whiskey'),
    33: ('x', 'X-ray'),
    34: ('y', 'Yankee'),
    35: ('z', 'Zulu')
}

BG = '#030303'


class OutputBox:

    def __init__(self, page: tk.Canvas, width, height, tl_x, tl_y) -> None:

        page.create_rectangle(
            tl_x, tl_y,
            tl_x + width, tl_y + height,
            fill=BG, width=1, outline=THEME_BORDER_COLOR
        )
        Label(
            id='output_box1',
            x=tl_x + 10, y=tl_y + 10,
            text='output:',
            font='Consolas 11', anchor='nw',
            fg='#1dda18', bg=BG,
            tags='train'
        )
        Label(
            id='output_box2',
            x=tl_x + 10, y=tl_y + 50,
            text='draw me something..',
            font='Consolas 13', justify='left', anchor='nw',
            fg='#1dda18', bg=BG,
            tags='train'
        )

    def tell(self, idx: int | None):

        if idx is None:
            text = None
        else:

            if idx < 10:
                type = 'number'
            else:
                type = 'letter'
            char, word = NATO_PHONETIC_ALPHABET[idx]

            text = f'According to my understanding,\nit is the {type} {char}: {word}.'

        Label.set_text_by_id('output_box2', text)