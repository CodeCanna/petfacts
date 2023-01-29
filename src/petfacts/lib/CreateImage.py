from .TextModifier import TextModifier
from PIL import Image, ImageDraw, ImageFont
from pathlib import *

class CreateImage:    
    """
    text = Text to print to the image
    image = path to the tmp image to edit
    xp = The percentage desired from image width
    yp = The percentage desired from image height
    """
    @classmethod
    def create(cls, text: str, image: str, x: int, y: int):# -> Image:
        with Image.open(image) as img:
            image_editted = ImageDraw.Draw(img)
            modifier = TextModifier(30) # To wrap out text on the image
            text_array = modifier.modify(text)
            font = ImageFont.truetype('fonts/sans_rounded.ttf', size=30)
            for line in text_array: # Loop throught the array of strings returned from TextModifier.modify()
                y = y + 35 # Add the size of the font plus five to Y for each line.
                image_editted.text((x, y), line, fill=(255, 255, 255), font=font)
            return img

    @classmethod
    def save(cls, path: str, image_to_save: Image.Image) -> None:
        try:
            print(path)
            image_to_save.save(path)
        except FileNotFoundError as err:
            print(f"Couldn't find file or path: {err}")