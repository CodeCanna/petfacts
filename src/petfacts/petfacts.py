#!/usr/bin/env python3
import argparse
import sys
import requests
import json
import random
import time
import configparser
import os

from pathlib import *
from sys import platform # For detecting the running os
from lib.AnimalGetter import AnimalGetter
from lib.Parser import Parser
from lib.CreateImage import CreateImage

"""
This is a simple little project to help me learn argparse, an argument parser like getopt but has a few advantages.
Hopefully those advantages will be clear soon.
"""

# Get a random cat fact and return it as a string
def cat_fact() -> str:
    rsession = requests.session()
    try:
        fact_json = rsession.get('https://catfact.ninja/fact')
        fact = json.loads(fact_json.text)
    except json.JSONDecodeError as err:
        print(f"Couldn't show the cat fact because {err}")
    except requests.HTTPError as err:
        print(f"Couldn't get the cat fact due to this HTTP error: {err}")

    return fact['fact']

# Get a random dog fact and return it as a string
def dog_fact() -> str:
    rsession = requests.session()
    try:
        fact_json = rsession.get('http://dog-api.kinduff.com/api/facts?number=1')
        fact = json.loads(fact_json.text)
    except json.JSONDecodeError as err:
        print(f"Invalid repsonse recieved, got {err}")

    return fact['facts'][0]

# Choose a dog or cat string in an array and return it
def random_animal() -> str:
    animals = ['dog', 'cat']
    return animals[random.randrange(len(animals))]

# Add a delay to print each character for a nice effect
def type(string: str) -> None:
    # loop through the string characters and print them one at a time.
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)

def main():
    config = configparser.ConfigParser()
    """
    # According to https://docs.python.org/3/library/argparse.html
    # We create an instance of a class called ArgumentParser
    arg_parser = argparse.ArgumentParser(description='Get fun facts about pets!')

    # We can then add arguments from there with a function called add_argument()
    arg_parser.add_argument('--cat', action='store_true', default=False, help="Display a random cat fact.")
    arg_parser.add_argument('--dog', action='store_true', default=False, help="Display a random dog fact.")

    # Try creating an argparse Namespace object or handle exception
    try:
        arg = arg_parser.parse_args()
    except argparse.ArgumentError as err:
        print(err)
        sys.exit(2)

    # We can use if elif to go through each arg and check if its been passed
    if arg.dog:
        type(f"Random Dog Fact: {dog_fact()}")
    elif arg.cat:
        type(f"Random Cat Fact: {cat_fact()}")
    else:
        # Print a random cat or dog fact if no args are passed
        if random_animal() == 'dog':
            type(f"Random Dog Fact: {dog_fact()}")
        else:
            type(f"Random Cat Fact: {cat_fact()}")
    """
    animal_getter = AnimalGetter('cat', requests.session(), 'config.ini', True)
    animal_data = animal_getter.get(configparser.ConfigParser())


    # Check our platform
    if platform == 'win32':
        config.read('config.ini') # Read the config file
        tmp_save_path = str(PureWindowsPath(config['tmp_paths']['win_tmp_path'])) # Get our windows path parsed and ready...oh Windows...
        save_path = str(PureWindowsPath(config['paths']['windows_path']))
        print(Parser.get_win_path(tmp_save_path))

        # Parse our paths
        save_path_parsed = Parser.get_win_path(save_path)
        tmp_save_path_parsed = Parser.get_win_path(tmp_save_path)

        if not os.path.exists(Parser.get_win_path(tmp_save_path)):
            os.makedirs(tmp_save_path_parsed)
        try:
            print(animal_data['image'])
            print(Parser.get_extension(animal_data['image']))
            img_bytes = requests.get(animal_data['image']).content # Get the content of the image url
            with open(tmp_save_path_parsed + "\\tmp_img" + Parser.get_extension(animal_data['image']), 'wb') as img:
                img.write(img_bytes)

            img = CreateImage.create(animal_data['fact'], f"{tmp_save_path_parsed}\\tmp_img{Parser.get_extension(animal_data['image'])}", 15, 15)
            CreateImage.save(f"{Parser.get_win_path(save_path_parsed)}\\image{Parser.get_extension(animal_data['image'])}", img)
        except FileNotFoundError as err:
            print(f"Couldn't find or create dir: {err}")
        except OSError as err:
            print(f"Couldn't write to path {Parser.get_win_path(tmp_save_path)}: {err}")
            print("Make sure you have proper permissions to write to this file, on windows this script might have to be ran as Administrator!")           
    elif platform == 'linux' or 'linux2':
        print("Linux")
    elif platform == 'darwin':
        print("Mac")




if __name__ == '__main__':
    main()