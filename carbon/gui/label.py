import tkinter as _tk


class Label:

    labels: dict[str, 'Label'] = {}
    tags: dict[str, list['Label']] = {}

    def __init__(
        self,
        id: str,
        x: int,
        y: int,
        text: str,
        font: str | tuple[str, int] = 'Consolas 10',
        justify: str = 'left',
        anchor: str = 'nw',
        fg: str = '#fafbfa',
        bg: str = '#010201',
        visible: bool = True,
        tags: str | list[str] | None = None,
    ):

        if id in Label.labels:
            raise ValueError(f'The id {repr(id)} is duplicated.')
        Label.labels[id] = self

        self.x = x
        self.y = y
        self.text = text
        self.anchor = anchor
        self.visible = visible

        self.default_text = text

        self.label = _tk.Label(
            text=text, font=font, justify=justify,
            foreground=fg, background=bg,
        )

        if visible:
            self.label.place(x=x, y=y, anchor=anchor)

        if type(tags) is str:
            tag = tags
            if tag in Label.tags:
                Label.tags[tag].append(self)
            else:
                Label.tags[tag] = [self]
        elif (type(tags) is list) or (type(tags) is tuple):
            for tag in tags:
                if tag in Label.tags:
                    Label.tags[tag].append(self)
                else:
                    Label.tags[tag] = [self]

    def set_text(self, text: str | None, /):
        """if None -> set default text."""

        if text is None:
            text = self.default_text

        if text != self.text:
            self.text = text
            self.label.configure(text=text)

    @staticmethod
    def set_text_by_id(id: str, text: str | None, /):
        Label.labels[id].set_text(text)

    def set_visibility(self, visible: bool, /):

        if self.visible is not visible:
            self.visible = visible
            if visible:
                self.label.place(x=self.x, y=self.y, anchor=self.anchor)
            else:
                self.label.place_forget()

    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /):
        Label.labels[id].set_visibility(visible)

    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /):
        for label in Label.tags[tag]:
            label.set_visibility(visible)

    @staticmethod
    def set_visibility_all(visible: bool, /):
        for label in Label.labels.values():
            label.set_visibility(visible)