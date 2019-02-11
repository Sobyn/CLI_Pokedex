"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *11 February 2019*\n
**Author:** Anonymous
"""

import requests
import json
import argparse as ap

url = requests.get('https://pokeapi.co/api/v2/')
jData = url.json()

parser = ap.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-n')
group.add_argument()
result = parser.parse_args()


def intro():
    print("\nWelcome to the Pokedex!\n"
          
          "\nWith the Pokedex, you can search through \n"
          "a vast collection of Pokemon-related information!\n"
          
          "\nYou're seeing this message because you started the \n"
          "program without any flags specified.\n"
          
          "\nFeel free to restart the program, \n"
          "but this time include the '-h' flag.\n"
          "\nExample:\t'python pokedex.py -h'")


if __name__ == '__main__':
    intro()
