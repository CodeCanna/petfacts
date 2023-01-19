import TextModifier
from PIL import Image, ImageDraw, ImageFont
from pathlib import *

class CreateImage:
    """
    text = Text to print to the image
    image = path to the tmp image to edit

    """
    @classmethod
    def create(self, text: str, image: str, xp: float, yp: float) -> Image:
        with Image.open(image) as img:
            image_editted = ImageDraw.Draw(img)
            modifier = TextModifier(30) # To wrap out text on the image
            print(img.width)
            print(img.height)
            font = ImageFont.truetype('fonts/sans_rounded.ttf', size=30)
            image_editted.text((x, y), text, fill=(255, 255, 255), font=font)

            return img

    @classmethod
    def save(self, path: str, image_to_save: Image) -> None:
        try:
            print(path)
            image_to_save.save(path)
        except FileNotFoundError as err:
            print(f"Couldn't find file or path: {err}")