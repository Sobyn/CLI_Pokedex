"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *11 February 2019*\n
**Author:** Anonymous
"""

import requests
import json


def main():
    url = requests.get('https://pokeapi.co/api/v2/pokemon/charizard')
    jData = url.json()
    print("Welcome to the Pokedex!")
    print("With this program, you can search for"
          "a great amount of Pokemon-related information!")
    print("As of right now, you can search within the following topics:")
    print(jData)
#    inp = input("What would you like to search for?\n$> ")
#
#    print("The response contains {0} properties".format(len(jData)))
#    print("\n")
#    print(jData['ability'])


if __name__ == '__main__':
    main()
