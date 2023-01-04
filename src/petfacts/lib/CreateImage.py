from PIL import Image, ImageDraw, ImageFont
from pathlib import *

class CreateImage:
    @classmethod
    def create(self, text: str, image: str, x=0, y=0) -> Image:
        with Image.open(image) as img:
            image_editted = ImageDraw.Draw(img)
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