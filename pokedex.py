"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *11 February 2019*\n
**Author:** Anonymous
"""

# For ASCII art to work, please install the program 'pokemon'
# with 'pip install pokemon' in your terminal of choice.

# from unicurses import *
import requests
import json
import argparse as ap
import os

parser = ap.ArgumentParser("\nWelcome to the Pokedex!\n"
                           "\nWith the Pokedex, you can search through \n"
                           "a vast collection of Pokemon-related information!\n")

parser.add_argument('-n', '--name', help="Specify the name or ID (1-807) of the Pokemon. "
                                         "Beware! ASCII art is not available for "
                                         "Generation 7 Pokemon (ID's from 722 - 807).")
parser.add_argument('-t', '--type', help="Specify a Pokemon type.\n")
args = parser.parse_args()


class Pokemon:
    def name(self):
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        poke_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/' + args.name.lower())
        json_name = json.loads(poke_name.content)
        json_species = json.loads(poke_species.content)

        print('\n\nPokemon Info:\n')
        print('ID:\t', json_name['id'])
        print('Name:\t', json_name['name'].capitalize())
        print('Height:\t', json_name['height'] / 10, 'meters')
        print('Weight:\t', json_name['weight'] / 10, 'kilograms')
        print()

        print('Category:')
        if json_species['genera'][2]['language']['name'] == 'en':
            print(json_species['genera'][2]['genus'])
        else:
            print("Unable to retrieve category.")
        print()

        print('Types:')
        for i in json_name['types']:
            print(i['type']['name'].capitalize())
        print()

        if json_species['flavor_text_entries'][1]['language']['name'] == 'en':
            print(json_species['flavor_text_entries'][1]['flavor_text'])
        else:
            print(json_species['flavor_text_entries'][2]['flavor_text'])
        print()
        Pokemon.art(args.name)

    def art(self):
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        json_name = json.loads(poke_name.content)

        if print(args.name) == print(json_name['id']):
            args.name = json_name['name']

        os.system("pokemon --pokemon {}".format(args.name))

    def type(self):
        poke_type = requests.get('https://pokeapi.co/api/v2/type/' + args.type.lower())
        json_type = json.loads(poke_type.content)

        print('\n\nType Info:\n')
        print('ID:\t', json_type['id'])
        print('Name:\t', json_type['name'].capitalize())
        print()
        print('Damage Relations:')
        for i in json_type['damage_relations']:
            print(i.capitalize() + ':\t')
            for x in json_type['damage_relations'][i]:
                print(x['name'].capitalize())
            print()


try:

    if args.name:
        Pokemon.name(args.name)

    if args.type:
        Pokemon.type(args.name)

except json.decoder.JSONDecodeError:
    print("\nOops! Something went wrong!\n"
          "Make sure the Pokemon name or type \n"
          "you tried to enter was spelled correctly!")
