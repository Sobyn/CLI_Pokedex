"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *11 February 2019*\n
**Author:** Anonymous
"""

import requests
import json
import argparse as ap

parser = ap.ArgumentParser("\nWelcome to the Pokedex!\n"
                           "\nWith the Pokedex, you can search through \n"
                           "a vast collection of Pokemon-related information!\n")

parser.add_argument('-n', '--name', action="store", help="Specify the name of the Pokemon.")
parser.add_argument('-t', '--type', action="store", help="Specify a Pokemon type.\n")
args = parser.parse_args()


def pokemon_name():
    poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name)
    poke_flavor = requests.get('https://pokeapi.co/api/v2/pokemon-species/' + args.name)
    json_name = json.loads(poke_name.content)
    json_flavor = json.loads(poke_flavor.content)

    print('\n\nPokemon Info:\n')
    print('ID:\t', json_name['id'])
    print('Name:\t', json_name['name'])
    print('Height:\t', json_name['height'] / 10, 'meters')
    print('Weight:\t', json_name['weight'] / 10, 'kilograms')
    print()
    print('Types:\t')
    for i in json_name['types']:
        print(i['type']['name'])
    print()
    for i in json_flavor['flavor_text_entries']:
        print(i['flavor_text_entries'][1]['flavor_text'])


def pokemon_type():
    poke_type = requests.get('https://pokeapi.co/api/v2/type/' + args.type)
    json_type = json.loads(poke_type.content)

    print('\n\nType Info:\n')
    print('ID:\t', json_type['id'])
    print('Name:\t', json_type['name'])
    print()


if args.name:
    pokemon_name()

if args.type:
    pokemon_type()
