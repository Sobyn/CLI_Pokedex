"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *11 February 2019*\n
**Author:** Anonymous
"""

# For ASCII art to work, please install the program 'pokemon'
# with 'pip install pokemon' in your terminal of choice.

from unicurses import *
import requests
import json
import argparse as ap
import os
import textwrap

parser = ap.ArgumentParser("\nWelcome to the Pokedex!\n"
                           "\nWith the Pokedex, you can search through \n"
                           "a vast collection of Pokemon-related information!\n")
group = parser.add_mutually_exclusive_group()
group.add_argument('-n', '--name', help="Specify the name or ID (1-807) of the Pokemon. "
                                         "Beware! ASCII art is not available for "
                                         "Generation 7 Pokemon (ID's from 722 - 807).")
group.add_argument('-t', '--type', help="Specify a Pokemon type.\n")
args = parser.parse_args()


class Pokemon:
    def name(self):
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        poke_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/' + args.name.lower())
        json_name = json.loads(poke_name.content)
        json_species = json.loads(poke_species.content)

        mvwaddstr(poppopp, 0, 1, 'Pokemon Info:', A_BOLD)

        mvwaddstr(poppopp, 3, 1, 'ID:', A_BOLD)
        mvwaddstr(poppopp, 3, 15, json_name['id'])

        mvwaddstr(poppopp, 5, 1, 'Name:', A_BOLD)
        mvwaddstr(poppopp, 5, 15, json_name['name'].capitalize())

        mvwaddstr(poppopp, 7, 1, 'Height (m):', A_BOLD)
        mvwaddstr(poppopp, 7, 15, json_name['height'] / 10)

        mvwaddstr(poppopp, 9, 1, 'Weight (kg):', A_BOLD)
        mvwaddstr(poppopp, 9, 15, json_name['weight'] / 10)

        mvwaddstr(poppopp, 11, 1, 'Category:', A_BOLD)

        if json_species['genera'][2]['language']['name'] == 'en':
            mvwaddstr(poppopp, 11, 15, json_species['genera'][2]['genus'])
        else:
            mvwaddstr(poppopp, 11, 15, "Unable to retrieve English category text.")

        typelist = []
        for type in json_name['types']:
            typelist.append(type['type']['name'])

        mvwaddstr(poppopp, 13, 1, 'Types:', A_BOLD)
        mvwaddstr(poppopp, 13, 15, ', '.join(typelist).capitalize())

        if json_species['flavor_text_entries'][1]['language']['name'] == 'en':
            lang = 1
        else:
            lang = 2

        species = json_species['flavor_text_entries'][lang]['flavor_text']
        ascii_art = "Press any key to see an image of the Pokemon."
        exit_message = "Or press the END-key to exit the program right away."
        vinduTekst(poppopp, 1, 16, storrelseX - hmargin - vmargin - pmargin * 2, species)
        vinduTekst(bakgrunn, 1, storrelseY - 3, storrelseX - hmargin - vmargin - pmargin * 2, ascii_art)
        vinduTekst(bakgrunn, 1, storrelseY - 2, storrelseX - hmargin - vmargin - pmargin * 2, exit_message)

    def art(self):
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        json_name = json.loads(poke_name.content)

        if print(args.name) == print(json_name['id']):
            args.name = json_name['name']

        mvwaddstr(bakgrunn, 1, 1, os.system("pokemon --pokemon {}".format(args.name)))

    def type(self):
        poke_type = requests.get('https://pokeapi.co/api/v2/type/' + args.type.lower())
        json_type = json.loads(poke_type.content)

        ddfl = []
        for type in json_type['damage_relations']['double_damage_from']:
            ddfl.append(type['name'].capitalize())

        ddtl = []
        for type in json_type['damage_relations']['double_damage_to']:
            ddtl.append(type['name'].capitalize())

        hdfl = []
        for type in json_type['damage_relations']['half_damage_from']:
            hdfl.append(type['name'].capitalize())

        hdtl = []
        for type in json_type['damage_relations']['half_damage_to']:
            hdtl.append(type['name'].capitalize())

        ndfl = []
        for type in json_type['damage_relations']['no_damage_from']:
            ndfl.append(type['name'].capitalize())

        ndtl = []
        for type in json_type['damage_relations']['no_damage_to']:
            ndtl.append(type['name'].capitalize())

        mvwaddstr(poppopp, 0, 1, 'Type Info:', A_BOLD)

        mvwaddstr(poppopp, 3, 1, 'ID:', A_BOLD)
        mvwaddstr(poppopp, 3, 15, json_type['id'])

        mvwaddstr(poppopp, 5, 1, 'Name:', A_BOLD)
        mvwaddstr(poppopp, 5, 15, json_type['name'].capitalize())

        mvwaddstr(poppopp, 7, 1, 'Damage Relations:', A_BOLD)

        mvwaddstr(poppopp, 9, 1, 'Double Damage From:', A_BOLD)
        mvwaddstr(poppopp, 10, 1, ', '.join(ddfl))

        mvwaddstr(poppopp, 12, 1, 'Double Damage To:', A_BOLD)
        mvwaddstr(poppopp, 13, 1, ', '.join(ddtl))

        mvwaddstr(poppopp, 15, 1, 'Half Damage From:', A_BOLD)
        mvwaddstr(poppopp, 16, 1, ', '.join(hdfl))

        mvwaddstr(poppopp, 18, 1, 'Half Damage To:', A_BOLD)
        mvwaddstr(poppopp, 19, 1, ', '.join(hdtl))

        mvwaddstr(poppopp, 21, 1, 'No Damage From:', A_BOLD)
        mvwaddstr(poppopp, 22, 1, ', '.join(ndfl))

        mvwaddstr(poppopp, 24, 1, 'No Damage To:', A_BOLD)
        mvwaddstr(poppopp, 25, 1, ', '.join(ndtl))

        exit_message = "Press the END-key to exit the program right away."
        vinduTekst(bakgrunn, 1, storrelseY - 2, storrelseX - hmargin - vmargin - pmargin * 2, exit_message)


stdscr = initscr()  # initializes the standard screen

# Skru på fargestøtte
start_color()

# Tastaturfjas
noecho()  # Skru av at man ser hvilket tegn som er trykket
cbreak()  # Gets raw key inputs but allows CRTL+C to work
keypad(stdscr, True)  # Get arrow keys etc.

# Bakgrunn,hvot på sort.
init_pair(1, COLOR_YELLOW, COLOR_RED)
init_pair(2, COLOR_WHITE, COLOR_BLACK)


# høyde, bredde, x, y
def lagVindu(y, x, startx, starty):
    lokalt = newwin(y, x, startx, starty)
    #box(lokalt, 0, 0)
    #mvwaddch(lokalt, 2, 0, ACS_LTEE)
    #mvwhline(lokalt, 2, 1, ACS_HLINE, x - 2)
    #mvwaddch(lokalt, 2, x - 1, ACS_RTEE)
    return lokalt


def vinduTekst(vindu, startx, starty, bredde, tekst):
    # Erstatt line breaks og carriage returns med mellomrom
    # erstatt så doble mellomrom med ett mellomrom. Dett hindrer at ORD\nORD ender opp som ORDORD
    tekst = tekst.replace('\r', ' ').replace('\n', ' ').replace('  ', ' ')

    linjer = textwrap.wrap(tekst, bredde)
    l = 0
    for i in linjer:
        mvwaddstr(vindu, starty + l, startx, i, A_NORMAL)
        l += 1

    return


storrelse = getmaxyx(stdscr)

storrelseX = storrelse[1]
storrelseY = storrelse[0]

bakgrunn = lagVindu(storrelseY, storrelseX, 0, 0)
wbkgd(bakgrunn, COLOR_PAIR(2))
box(bakgrunn)  # , 0,0)
bakgrunnPanel = new_panel(bakgrunn)

hmargin = 10
vmargin = 10
tmargin = 4
bmargin = 4
pmargin = 1

poppopp = lagVindu(storrelseY - tmargin - bmargin, storrelseX - hmargin - vmargin, tmargin, vmargin)
wbkgd(poppopp, COLOR_PAIR(1))
box(poppopp)
poppoppPanel = new_panel(poppopp)

#flavor_window = lagVindu(5, 68, 17, 6)
#wbkgd(flavor_window, COLOR_PAIR(1))
#flavor_windowPanel = new_panel(flavor_window)

#vinduTekst(poppopp, 1, 3, storrelseX - hmargin - vmargin - pmargin * 2, species)

# Sett på farger, fargepar nummer 4
#wattron(bakgrunn, COLOR_PAIR(3))
#
## move cursor, spesifiser window, legg til string til vinduet
## mv           w                  addstr
#mvwaddstr(poppopp, 1, 1, "Dette programmet er et test-program.", A_BOLD)


try:
    if args.name:
        Pokemon.name(args.name)

    if args.type:
        Pokemon.type(args.type)

except json.decoder.JSONDecodeError:
    print("\nOops! Something went wrong!\n"
          "Make sure the Pokemon name or type \n"
          "you tried to enter was spelled correctly!")
#
#wattroff(bakgrunn, COLOR_PAIR(3))
#
#mvwaddstr(bakgrunn, storrelseY - 2, 1, "Or press the END-key to exit the program right away.", A_BOLD)

# Tegn vinduet bakgrunn
update_panels()
doupdate()

tast = 0
i = 1

keypad(bakgrunn, True)

try:
    while tast != KEY_END:
        i = i + 1
        tast = wgetch(bakgrunn)
        if i == 2:
            wclear(bakgrunn)
            wrefresh(bakgrunn)
            wbkgd(bakgrunn, COLOR_PAIR(2))
            box(bakgrunn)  # , 0,0)
            bakgrunnPanel = new_panel(bakgrunn)
            Pokemon.art(args.name)
        if i == 3:
            break
except AttributeError:
    pass

# Rydde opp på skjermen!
wclear(bakgrunn)
wrefresh(bakgrunn)
endwin()

print("Exiting......\n")
