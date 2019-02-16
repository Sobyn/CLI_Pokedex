"""
**Name:** *pokedex.py*\n
**Created on** *11 February 2019*\n
**Last edited** *16 February 2019*\n
**Author:** Anonymous
"""
#
# Welcome to my Pokedex! This program retrieves select information from the Pokemon API,
# which is available at 'https://pokeapi.co'. The program is designed as a CLI program,
# as it requires that the user specifies one of two flags to specify what they want
# to search for.
#
# For ASCII art to work, please install the program 'pokemon'
# with 'pip install pokemon' in your terminal of choice.


# Importing the different modules required for this program to work:
# Unicurses for the graphical representation of the program;
# Requests for retrieving information from the Pokemon API
# JSON for encoding and decoding information in JSON format
# Argparse to enable the use of argument flags
# OS.System to enable the use of terminal commands from within the program
# Textwrap for handling text uniformly.
from unicurses import *
import requests
import json
import argparse as ap
from os import system
import textwrap

# Creating a variable for the ArgumentParser, and printing a welcome message
# that is visible upon calling '-h' when running the program.
# Then, creating a mutually exclusive group to ensure only one or the other flag works
# Two arguments are created; One for Pokemon names, and one for types;
# Each with their own help text to display when '-h' is called.
# A 'parse_args' variable is finally created, and will sort of work like the user's input from now on.
parser = ap.ArgumentParser("\nWelcome to the Pokedex!\n"
                           "\nWith the Pokedex, you can search through \n"
                           "a vast collection of Pokemon-related information!\n")
group = parser.add_mutually_exclusive_group()
group.add_argument('-n', '--name', help="Specify the name or ID (1-807) of the Pokemon. "
                                        "Beware! ASCII art is not available for "
                                        "Generation 7 Pokemon (ID's from 722 - 807).")
group.add_argument('-t', '--type',  help="Specify a Pokemon type.\n")
args = parser.parse_args()


# The class 'Pokemon' houses three methods; 'name', 'art' and 'type'.
class Pokemon:
    # The 'name' method retrieves select information about the Pokemon the user searches for
    def name(self):

        # The 'poke-{}' variables each retrieve information from each URL.
        # The URL is appended with the user's input, and converted to lower-case.
        # These two variables are, however, only temporary, as they are immediately used
        # in the 'json_loads' command to decode JSON content.
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        poke_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/' + args.name.lower())
        json_name = json.loads(poke_name.content)
        json_species = json.loads(poke_species.content)

        # Below are a number of messages getting printed and placed within specified coordinates.
        # 'popup' is related to unicurses, and is a window created after the class.
        # Some of the messages print information retrieved from the PokeAPI with the 'json_name' variable.
        # Height and weight are divided by 10, because the API displays each in hecto's and desimeters,
        # where meters and kilos are more desirable by the author.
        mvwaddstr(popup, 0, 1, 'Pokemon Info:', A_BOLD)

        mvwaddstr(popup, 3, 1, 'ID:', A_BOLD)
        mvwaddstr(popup, 3, 15, json_name['id'])

        mvwaddstr(popup, 5, 1, 'Name:', A_BOLD)
        mvwaddstr(popup, 5, 15, json_name['name'].capitalize())

        mvwaddstr(popup, 7, 1, 'Height (m):', A_BOLD)
        mvwaddstr(popup, 7, 15, json_name['height'] / 10)

        mvwaddstr(popup, 9, 1, 'Weight (kg):', A_BOLD)
        mvwaddstr(popup, 9, 15, json_name['weight'] / 10)

        # Category text has to be done differently, due to potential inconsistency in language.
        # The 'if' statement makes sure the English category text is shown.
        # English is presumably always in position '[2]', but in case it isn't, an error message is displayed.
        mvwaddstr(popup, 11, 1, 'Category:', A_BOLD)

        if json_species['genera'][2]['language']['name'] == 'en':
            mvwaddstr(popup, 11, 15, json_species['genera'][2]['genus'])
        else:
            mvwaddstr(popup, 11, 15, "Unable to retrieve English category text.")

        # Due to the potential of the Pokemon having either one or two types, a for-loop is necessary.
        typelist = []
        for type in json_name['types']:
            typelist.append(type['type']['name'])

        mvwaddstr(popup, 13, 1, 'Types:', A_BOLD)
        mvwaddstr(popup, 13, 15, ', '.join(typelist).capitalize())

        # The flavor text also has a language problem; The English version is always in
        # either position '[1]' or '[2]'. The if-statement checks for this before printing
        # the appropriate command.
        # The flavor text also utilizes the text-wrapping class 'windowtext'
        # created later in order to avoid unnatural line breaks, spacing and carriage returns.
        if json_species['flavor_text_entries'][1]['language']['name'] == 'en':
            lang = 1
        else:
            lang = 2
        species = json_species['flavor_text_entries'][lang]['flavor_text']
        window_text(popup, 1, 16, sizeX - rmargin - lmargin - pmargin * 2, species)

        # Finishing off the 'name' method are some instructions displayed at the bottom
        # of the 'background' set. This is specified here, because it's different from
        # the instructions for the 'type' method.
        ascii_art = "Press any key to see an image of the Pokemon."
        exit_message = "Or press the END-key to exit the program right away."
        window_text(background, 1, sizeY - 3, sizeX - rmargin - lmargin - pmargin * 2, ascii_art)
        window_text(background, 1, sizeY - 2, sizeX - rmargin - lmargin - pmargin * 2, exit_message)

    # The 'art' method shows an ASCII art representation of the Pokemon the user searched up.
    # This is shown after the user has clicked away from the intial screen.
    def art(self):

        # Like last time, the information is requested from the PokeAPI URL with the user's
        # input appended, and decoded.
        poke_name = requests.get('https://pokeapi.co/api/v2/pokemon/' + args.name.lower())
        json_name = json.loads(poke_name.content)

        # Here, the user input is checked. As the ASCII art program doesn't accept integers,
        # the input has to be converted to its string equivalent.
        if print(args.name) == print(json_name['id']):
            args.name = json_name['name']

        # With 'os.system', terminal commands can be run from within the program.
        # In this case, 'pokemon' is run with the user input appended
        # to bring up the ASCII art belonging to the Pokemon the user searched for.
        mvwaddstr(background, 2, 2, system("pokemon --pokemon {}".format(args.name)))

    # The 'type' method shows information about the Pokemon type the user searches for.
    def type(self):
        # Retrieving PokeAPI content and decoding
        poke_type = requests.get('https://pokeapi.co/api/v2/type/' + args.type.lower())
        json_type = json.loads(poke_type.content)

        # Each type has different damage relations to other types. The amount of
        # types within each damage relation varies greatly, so they're all first retrieved
        # and added to each of their own lists.
        # Naming convention: <Damage relation abbreviation> list
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

        # ID and name of the type is printed first.
        mvwaddstr(popup, 0, 1, 'Type Info:', A_BOLD)

        mvwaddstr(popup, 3, 1, 'ID:', A_BOLD)
        mvwaddstr(popup, 3, 15, json_type['id'])

        mvwaddstr(popup, 5, 1, 'Name:', A_BOLD)
        mvwaddstr(popup, 5, 15, json_type['name'].capitalize())

        # Damage relations are then presented by retrieving and printing
        # the information from each of their respective lists, with entries
        # separated by commas and spaces.
        mvwaddstr(popup, 7, 1, 'Damage Relations:', A_BOLD)

        mvwaddstr(popup, 9, 1, 'Double Damage From:', A_BOLD)
        mvwaddstr(popup, 10, 1, ', '.join(ddfl))

        mvwaddstr(popup, 12, 1, 'Double Damage To:', A_BOLD)
        mvwaddstr(popup, 13, 1, ', '.join(ddtl))

        mvwaddstr(popup, 15, 1, 'Half Damage From:', A_BOLD)
        mvwaddstr(popup, 16, 1, ', '.join(hdfl))

        mvwaddstr(popup, 18, 1, 'Half Damage To:', A_BOLD)
        mvwaddstr(popup, 19, 1, ', '.join(hdtl))

        mvwaddstr(popup, 21, 1, 'No Damage From:', A_BOLD)
        mvwaddstr(popup, 22, 1, ', '.join(ndfl))

        mvwaddstr(popup, 24, 1, 'No Damage To:', A_BOLD)
        mvwaddstr(popup, 25, 1, ', '.join(ndtl))

        # Creating an instructional exit message, and placing it at the bottom of 'background'.
        exit_message = "Press any key to exit the program."
        window_text(background, 1, sizeY - 2, sizeX - rmargin - lmargin - pmargin * 2, exit_message)


# Most lines from here on is related to Unicurses.
# This initializes the standard screen.
stdscr = initscr()

# Turns on color-support
start_color()

# Turning off characters being printed back, and getting raw key input, as well as arrow keys
noecho()
cbreak()
keypad(stdscr, True)

# Creating the two color sets being used;
# #1 is for the pop-up window, #2 is for the background
init_pair(1, COLOR_YELLOW, COLOR_RED)
init_pair(2, COLOR_WHITE, COLOR_BLACK)


# Function for creating windows. Takes 4 arguments:
# The first two are for size, while the latter two are for position
def make_window(y, x, startx, starty):
    local = newwin(y, x, startx, starty)
    return local


# Function that creates "text windows" for proper text wrapping.
# Takes 5 arguments; Window to display text in, 2 for minimum text box size,
# width of text box, and the text to wrap.
def window_text(window, startx, starty, width, text):

    # Removing line breaks, returns and spaces
    tekst = text.replace('\r', ' ').replace('\n', ' ').replace('  ', ' ')

    # Text wrapping
    lines = textwrap.wrap(text, width)
    l = 0
    for i in lines:
        mvwaddstr(window, starty + l, startx, i, A_NORMAL)
        l += 1
    return

# Defining the maximum size of the window, as well as set coordinates for X and Y
max_size = getmaxyx(stdscr)
sizeX = max_size[1]
sizeY = max_size[0]

# Creating the background with the 'window' function,
# setting it to use a specified color set,
# creating a box along the edge equal to the size,
# and creating a panel.
background = make_window(sizeY, sizeX, 0, 0)
wbkgd(background, COLOR_PAIR(2))
box(background)  # , 0,0)
bakgrunnPanel = new_panel(background)

# Specifying the margins in order to allow for differently sized user windows.
# Right, left, top, bottom and padding, respectively.
rmargin = 10
lmargin = 10
tmargin = 4
bmargin = 4
pmargin = 1

# The popup window to display retrieved information in. The window is
# created with the 'window' function.
popup = make_window(sizeY - tmargin - bmargin, sizeX - rmargin - lmargin, tmargin, lmargin)
wbkgd(popup, COLOR_PAIR(1))
box(popup)
popup_panel = new_panel(popup)

try:
    # If the user is specifying the '-n' flag, run Pokemon.name
    if args.name:
        Pokemon.name(args.name)

    # If the user is specifying the '-t' flag, run Pokemon.type
    if args.type:
        Pokemon.type(args.type)

# Present an error message if the Pokemon name doesn't match anything
# from the PokeAPI
except json.decoder.JSONDecodeError:
    print("Oops! Something went wrong!"
          "Make sure the Pokemon name or type"
          "you tried to enter was spelled correctly!")

# Drawing the background
update_panels()
doupdate()

# Two counters for the upcoming while-loop
key = 0
i = 1

# Allowing the use of the keypad
keypad(background, True)

# Unknown error cover-up!
try:
    # Every time a key is pressed, increment 'i' by 1
    while key != KEY_END:
        i = i + 1
        tast = wgetch(background)
        try:
            # If 'i' is 2, clear the screen and present the ASCII art
            if i == 2:
                wclear(background)
                wrefresh(background)
                update_panels()
                doupdate()
                Pokemon.art(args.name)

        # Additional error message, as it wouldn't present unless both were present
        except json.decoder.JSONDecodeError:
            print("\nOops! Something went wrong!\n"
                  "Make sure the Pokemon name or type \n"
                  "you tried to enter was spelled correctly!")

        # Exit the loop if i is 3
        if i == 3:
            break

# Running the '-t' flag raised an unknown attribute error, which is
# bypassed with this workaround.
except AttributeError:
    pass

# Clearing the screen and exiting the program.
wclear(background)
wrefresh(background)
endwin()

print("Exiting......\n")
