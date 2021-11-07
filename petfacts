#!/usr/bin/env python3
import argparse
import sys
import requests
import json

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
        fact_json = rsession.get('https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1')
        fact = json.loads(fact_json.text)
    except json.JSONDecodeError as err:
        print(f"Invalid repsonse recieved, got {err}")

    return fact[0]['fact']

def main():
    # According to https://docs.python.org/3/library/argparse.html

    # We create an instance of a class called ArgumentParser
    arg_parser = argparse.ArgumentParser(description='Get fun facts about pets!')
    arg_parser.add_argument('--cat', action='store_true', default=False)

    arg_parser.add_argument('--dog', action='store_true', default=False)

    try:
        arg = arg_parser.parse_args()
    except argparse.ArgumentError as err:
        print(err)
        sys.exit(2)

    if arg.dog:
        print(dog_fact())
    elif arg.cat:
        print(cat_fact())

if __name__ == '__main__':
    main()