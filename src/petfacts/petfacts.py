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
from sys import platform  # For detecting the running os
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
        fact_json = rsession.get(
            'http://dog-api.kinduff.com/api/facts?number=1')
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

# This function runs if petfacts is being ran on a Linux machine.
def run_on_linux(config: configparser.ConfigParser, animal_data: AnimalGetter):
    config.read('config.ini')

    tmp_save_path: str = str(PurePosixPath(config['tmp_paths']['linux_tmp_path']))
    save_path: str = str(PurePosixPath(config['paths']['linux_path']))

    # Parse our linux paths
    tmp_save_path_parsed: str = Parser.get_linux_path(tmp_save_path)
    save_path_parsed: str = Parser.get_linux_path(save_path)
    print(Parser.get_linux_path(tmp_save_path))

    # If the save directory for petfacts isn't found, create it.
    if not os.path.exists(save_path_parsed):
        print(f"{save_path_parsed} not found creating...")
        os.makedirs(save_path_parsed)

    # If the tmp directory isnt found in the save directory create it.
    if not os.path.exists(tmp_save_path_parsed):
        print(f"{tmp_save_path_parsed} not found creating...")
        os.makedirs(tmp_save_path_parsed)

    try:
        img_bytes = requests.get(animal_data['image']).content
        with open(tmp_saved_path_parsed + "/tmp_img" + Parser.get_extension(animal_data['image']), 'wb') as img:
            img.write(img_bytes)

        # Create our new image
        img = CreateImage.create(animal_data['fact'], f"{tmp_saved_path_parsed}/tmp_img{Parser.get_extension(animal_data['image'])}", 15, 15)

        # Save the image to the drive
        CreateImage.save(f"{img_saved_path_parsed}/tmp_img{Parser.get_extension(animal_data['image'])}", img)
    except FileNotFoundError as err:
        print(f"Couldn't find or create directory: {err}")
    except OSError as err:
        print("Couldn't write file possibly due to wrong permissions.")


# This function runs if the program is being ran on windows
# This function parses and saves the image and fact data based on the windows file system stucture and path.
def run_on_win32(config: configparser.ConfigParser, animal_data: dict):
    config.read('config.ini')  # Read the config file
    # Get our windows path parsed and ready...oh Windows...
    tmp_save_path = str(PureWindowsPath(config['tmp_paths']['win_tmp_path']))
    save_path = str(PureWindowsPath(config['paths']['windows_path']))
    print(Parser.get_win_path(tmp_save_path))

    # Parse our paths
    save_path_parsed = Parser.get_win_path(save_path)
    tmp_save_path_parsed = Parser.get_win_path(tmp_save_path)

    if not os.path.exists(Parser.get_win_path(tmp_save_path)):
        os.makedirs(tmp_save_path_parsed)
    try:
        # print(animal_data['image'])
        # print(Parser.get_extension(animal_data['image']))
        # Get the content of the image url
        img_bytes = requests.get(animal_data['image']).content
        with open(tmp_save_path_parsed + "\\tmp_img" + Parser.get_extension(animal_data['image']), 'wb') as img:
            img.write(img_bytes)

        img = CreateImage.create(
            animal_data['fact'], f"{tmp_save_path_parsed}\\tmp_img{Parser.get_extension(animal_data['image'])}", 15, 15)
        CreateImage.save(
            f"{Parser.get_win_path(save_path_parsed)}\\image{Parser.get_extension(animal_data['image'])}", img)
    except FileNotFoundError as err:
        print(f"Couldn't find or create dir: {err}")
    except OSError as err:
        print(
            f"Couldn't write to path {Parser.get_win_path(tmp_save_path)}: {err}")
        print("Make sure you have proper permissions to write to this file, on windows this script might have to be ran as Administrator!")


def main():
    config: configparser.ConfigParser = configparser.ConfigParser()
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='Petfacts',
        description='A pet fact and pet image generator.',
        epilog='GitHub: CodeCanna, Email: codecannamw@gmail.com'
    )

    # Define program options
    parser.add_argument('--dog', action='store_true', help='Get a random dog fact with or without image.')
    parser.add_argument('--cat', action='store_true', help='Get a random cat fact with or without image.')
    parser.add_argument('--noimage', action='store_true', help='Specify that you just want a fact with no image.')

    args = parser.parse_args()

    # Check our platform
    if platform == 'win32':
        config_path = Path('.\\config.ini')
        request_session = requests.session()
        if args.noimage:
            animal_getter = AnimalGetter(random_animal(), request_session, config_path, False)
            animal_data = animal_getter.get(config)

            fact = animal_data['fact']
            type(fact)
            exit(0)
        else:   
            animal_getter = AnimalGetter(random_animal(), request_session, config_path, True)
            animal_data = animal_getter.get(config)

            # Run this program for windows, handle the different file paths.
            run_on_win32(config, animal_data)
    elif platform == 'linux' or 'linux2':
        config_path = Path('./config.ini')
        request_session = requests.session()

        if args.noimage:
            animal_getter = AnimalGetter(random_animal(), request_session, config_path, False)
            animal_data = animal_getter.get(config)

            fact = animal_data['fact']
            type(fact)
            exit(0)
        else:
            animal_getter = AnimalGetter(random_animal(), request_session, config_path, True)
            animal_data = animal_getter.get(config)

            run_on_linux(config, animal_data)
            print("Linux")
    elif platform == 'darwin':
        print("Mac")

# Our usual python stuffs
if __name__ == '__main__':
    main()
