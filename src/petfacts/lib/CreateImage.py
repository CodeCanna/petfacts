from .TextModifier import TextModifier
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

class CreateImage:    
    """
    text = Text to print to the image
    image = path to the tmp image to edit
    x = The x coordinate of the text printed to image
    y = The y coordinate of the text printed to the image
    """
    @classmethod
    def create(cls, text: str, image: str, x: int, y: int) -> Image.Image:
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
    def save(cls, _path: str, image_to_save: Image.Image) -> None:
        try:
            # If the filename is already found raise an error.
            if os.path.exists(_path):
                raise(FileExistsError(f"File {_path} already exists.  Please choose another file name."))
            else:
                image_to_save.save(Path(_path))
                image_to_save.show()
        except FileExistsError as err:
            print(err)