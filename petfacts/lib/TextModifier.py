import textwrap

class TextModifier(textwrap.TextWrapper):
    def __init__(self, max_width: int) -> None:
        super().__init__(width=max_width)

    # Sets the max width of text written to an image before next line
    def modify(self, text: str):
        return self.wrap(text)