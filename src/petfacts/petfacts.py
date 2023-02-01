#!/usr/bin/env python3
import argparse
import sys
import requests
import json
import random
import time
import configparser
import os

from pathlib import Path, PurePosixPath, PureWindowsPath
from sys import platform  # For detecting the running os (Linux, Windows, or Mac)
from lib.AnimalGetter import AnimalGetter
from lib.Parser import Parser
from lib.CreateImage import CreateImage

"""
Pet facts started off as a simple project to teach myself argparse on Python, but it kind of turned into a larger project.
This project has grown into a pet fact image generator.  It gets an image of a dog or cat, gets a random fact about it; then prints it out on top
of the image.

It saves the image to the disk for viewing or sharing.
"""

# Return the string 'dog' or 'cat' randomly.
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
def run_on_linux(config: configparser.ConfigParser, animal_data: dict[str, str]):
    config.read('config.ini')

    # Parse our linux paths
    tmp_save_path: str = str(PurePosixPath(config['tmp_paths']['linux_tmp_path']))
    save_path: str = str(PurePosixPath(config['paths']['linux_path']))

    # Parse our linux paths
    tmp_save_path_parsed: str = Parser.get_linux_path(tmp_save_path)
    save_path_parsed: str = Parser.get_linux_path(save_path)

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
        with open(tmp_save_path_parsed + "/tmp_img" + Parser.get_extension(animal_data['image']), 'wb') as img:
            img.write(img_bytes)

        # Create our new image
        img = CreateImage.create(animal_data['fact'], f"{tmp_save_path_parsed}/tmp_img{Parser.get_extension(animal_data['image'])}", 15, 15)

        # Save the image to the drive
        CreateImage.save(f"{save_path_parsed}/tmp_img{Parser.get_extension(animal_data['image'])}", img)
    except FileNotFoundError as err:
        print(f"Couldn't find or create directory: {err}")
    except OSError as err:
        print("Couldn't write file possibly due to wrong permissions.")

# This function runs if the program is being ran on windows
# This function parses and saves the image and fact data based on the windows file system stucture and path.
def run_on_win32(config: configparser.ConfigParser, animal_data: dict[str, str], filename: str):
    config.read('config.ini')  # Read the config file
    # Get our windows path parsed and ready...oh Windows...
    tmp_save_path = str(PureWindowsPath(config['tmp_paths']['win_tmp_path']))
    save_path = str(PureWindowsPath(config['paths']['windows_path']))

    # Parse our paths
    save_path_parsed = Parser.get_win_path(save_path)
    tmp_save_path_parsed = Parser.get_win_path(tmp_save_path)

    if not os.path.exists(Parser.get_win_path(tmp_save_path)):
        os.makedirs(tmp_save_path_parsed)
    try:
        # Get the content of the image url
        img_bytes = requests.get(animal_data['image']).content
        with open(tmp_save_path_parsed + "\\tmp_img" + Parser.get_extension(animal_data['image']), 'wb') as img:
            img.write(img_bytes)

        img = CreateImage.create(
            animal_data['fact'], f"{tmp_save_path_parsed}\\tmp_img{Parser.get_extension(animal_data['image'])}", 15, 15)
        CreateImage.save(
            f"{Parser.get_win_path(save_path_parsed)}\\{filename}{Parser.get_extension(animal_data['image'])}", img)
    except FileNotFoundError as err:
        print(f"Couldn't find or create dir: {err}")
    except OSError as err:
        print(f"Couldn't write to file, file either already exists or you do not have permissions to write files.")

def main():
    # Get the config file
    config: configparser.ConfigParser = configparser.ConfigParser()

    # Set up our argparse object for processing arguments.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='Petfacts',
        description='A pet fact and pet image generator.',
        epilog='GitHub: CodeCanna, Email: codecannamw@gmail.com'
    )

    # Define program options
    parser.add_argument('--dog', action='store_true', help='Get a random dog fact with or without image.')
    parser.add_argument('--cat', action='store_true', help='Get a random cat fact with or without image.')
    parser.add_argument('--noimage', action='store_true', help='Specify that you just want a fact with no image.')
    parser.add_argument("-s", "--saveas", help='Give the name of the image to save under without file extension.')

    # Parse our args
    args = parser.parse_args()

    # Check our platform; is it Linux, Mac, or Windows?  I'm trying to account for different file structures on different systems.
    if platform == 'win32':
        config_path = Path('.\\config.ini')
        request_session = requests.session()
        if args.noimage and args.cat: # Specify no image cat fact
            animal_getter = AnimalGetter('cat', request_session, config_path, False)
            animal_data = animal_getter.get(config)

            fact = animal_data['fact']
            type(fact)

            # Exit after typing the fact to the terminal.
            exit(0)
        elif args.noimage and args.dog: # Sepcify no image dog fact
            animal_getter = AnimalGetter('dog', request_session, config_path, False)
            animal_data = animal_getter.get(config)

            fact = animal_data['fact']
            type(fact)
            # Exit after typing the fact to the terminal.
            exit(0)
        elif args.cat:  
            animal_getter = AnimalGetter('cat', request_session, config_path, True)
            animal_data = animal_getter.get(config)

            # Run this program for windows, handle the different file paths.
            run_on_win32(config, animal_data, args.saveas)
        elif args.dog:
            animal_getter = AnimalGetter('dog', request_session, config_path, True)
            animal_data = animal_getter.get(config)

            # Run this program for windows, handle the different file paths.
            run_on_win32(config, animal_data, args.saveas)
        else:
            animal_getter = AnimalGetter(random_animal(), request_session, config_path, True)
            animal_data = animal_getter.get(config)

            # Run this program for windows, handle the different file paths.
            run_on_win32(config, animal_data, args.saveas)
    elif platform == 'linux' or 'linux2':
        config_path = Path('./config.ini')
        request_session = requests.session()

        if args.noimage and args.cat:
            animal_getter = AnimalGetter('cat', request_session, config_path, False)
            animal_data = animal_getter.get(config)

            fact = animal_data['fact']
            type(fact)

            # Exit after typing the fact to the terminal.
            exit(0)
        elif args.noimage and args.dog:
            animal_getter: AnimalGetter = AnimalGetter('dog', request_session, config_path, False)
            animal_data: dict[str, str] = animal_getter.get(config)

            # Get the actual fact we are going to print from the returned dict from AnimalGetter.get()
            fact = animal_data['fact']

            # Display the fact, but "type" it out.
            type(fact)

            # Exit after printing the fact
            exit(0)
        elif args.cat:
            animal_getter: AnimalGetter = AnimalGetter('cat', request_session, config_path, True)
            animal_data: dict[str, str] = animal_getter.get(config)

            # This funciton is called if this is ran on linux.
            run_on_linux(config, animal_data)
        elif args.dog:
            animal_getter: AnimalGetter = AnimalGetter('dog', request_session, config_path, True)
            animal_data: dict[str, str] = animal_getter.get(config)

            # This function is called if this is ran on linux.
            run_on_linux(config, animal_data)
        else:
            animal_getter: AnimalGetter = AnimalGetter(random_animal(), request_session, config_path, True)
            animal_data: dict[str, str] = animal_getter.get(config)

            run_on_linux(config, animal_data)
    elif platform == 'darwin':
        print("Mac")

# Our usual python stuffs
if __name__ == '__main__':
    main()