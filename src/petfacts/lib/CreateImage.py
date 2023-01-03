class CreateImage:
    def __init__(self, animal_data: AnimalGetter):
        self.animal_getter = animal_data
    
    # Returns the path of the created image
    @classmethod
    def image(self) -> str:
        pass