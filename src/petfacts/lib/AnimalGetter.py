import os.path, configparser, requests, sys, json
from pathlib import Path

class AnimalGetter:
    def __init__(self, animal: str,  requests_obj: requests.Session, config_file: Path, with_pic: bool=False) -> None:
        self.animal = animal
        self.with_pic = with_pic
        self.request_obj = requests_obj
        self.config_file = config_file

    def get(self, config_parser: configparser.ConfigParser) -> dict:
        # Create a dictionary to return animal fact data
        animal_data: dict = {
            "animal": str,
            "fact": str,
            "image": str
        }

        # Check for config file
        try:
            if not Path('config.ini').is_file():
                raise Exception()
        except Exception:
            print(f"Couldn't fine file {self.config_file}!")

        config_parser.read(self.config_file) # read the config file

        # Handle retrieve an image with the fact? or not?
        if self.with_pic and self.animal == 'cat':
            try:
                cat_fact_obj = json.loads(self.request_obj.get(config_parser['urls']['cat_facts'].replace('"', '')).text)
                cat_image_obj = json.loads(self.request_obj.get(config_parser['urls']['cat_pics'].replace('"', '')).text)

                animal_data['animal'] = 'cat'
                animal_data['fact'] = cat_fact_obj['fact']
                animal_data['image'] = cat_image_obj[0]['url']
            except json.JSONDecodeError as err:
                print(err)
        elif not self.with_pic and self.animal == 'cat':
            try:
                cat_fact_obj = json.loads(self.request_obj.get(config_parser['urls']['cat_facts'].replace('"', '')).text) #strip double quotes from string
                animal_data['animal'] = 'cat'
                animal_data['fact'] = cat_fact_obj['fact']
                animal_data['image'] = None
            except json.JSONDecodeError as err:
                print(err)
        elif self.with_pic and self.animal == 'dog': # get dog fact and image
            try:
                dog_fact_obj = json.loads(self.request_obj.get(config_parser['urls']['dog_facts'].replace('"', '')).text)
                dog_image_obj = json.loads(self.request_obj.get(config_parser['urls']['dog_pics'].replace('"', '')).text)

                animal_data['animal'] = 'dog'
                animal_data['fact'] = dog_fact_obj['facts'][0]
                animal_data['image'] = dog_image_obj['message']
            except json.JSONDecodeError as err:
                print(err)
        elif not self.with_pic and self.animal == 'dog': # only get dog fact no image
            try:
                dog_fact_obj = json.loads(self.request_obj.get(config_parser['urls']['dog_facts'].replace('"', '')).text)

                animal_data['animal'] = 'dog'
                animal_data['fact'] = dog_fact_obj['facts'][0]
                animal_data['image'] = None
            except json.JSONDecodeError as err:
                print(err)
        return animal_data
