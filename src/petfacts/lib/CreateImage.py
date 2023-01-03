import PIL

class CreateImage:
    def __init__(self, animal_data: AnimalGetter):
        self.animal_getter = animal_data
    
    def create(self, text: str, image: Path):
        pass