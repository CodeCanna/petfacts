import textwrap

class TextModifier(textwrap.TextWrapper):
    def __init__(self, max_width: int) -> None:
        super().__init__(width=max_width)

    def modify(self, text: str):
        return self.wrap(text)