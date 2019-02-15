# Innstaller UniCurses fra: https://sourceforge.net/projects/pyunicurses/
# Last ned pdcurses.dll, putt den i katalogen til programmet ditt (prosjektfil.py)-katalogen
# Ikke bland 64bit python med 32bit dll.
# Start programmet fra powershell, cmd, bash eller lignende
from unicurses import *
import textwrap

# init
stdscr = initscr()  # initializes the standard screen
start_color()

# tastatur
noecho()  # Skru av at man ser hvilket tegn som er trykket
cbreak()  # Gets raw key inputs but allows CRTL+C to work
keypad(stdscr, True)  # Get arrow keys etc.

# fargepar
init_pair(1, COLOR_RED, COLOR_BLACK)
init_pair(2, COLOR_WHITE, COLOR_BLUE)
init_pair(3, COLOR_RED, COLOR_GREEN)


# høyde, bredde, x, y
def lagVindu(y, x, startx, starty, tittel):
    lokalt = newwin(y, x, startx, starty)
    box(lokalt, 0, 0)
    # mvwaddch(lokalt, 2, 0, ACS_LTEE)
    # mvwhline(lokalt, 2, 1, ACS_HLINE, x - 2)
    # mvwaddch(lokalt, 2, x - 1, ACS_RTEE)
    mvwaddstr(lokalt, y - 2, 1, "Size: %dx%d" % (x, y), A_NORMAL)
    mvwaddstr(lokalt, 1, 1, "[*] %s" % tittel, A_NORMAL)

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

bakgrunn = lagVindu(storrelseY, storrelseX, 0, 0, "Unicurses-program")
box(bakgrunn)  # , 0,0)
bakgrunnPanel = new_panel(bakgrunn)

# Lorem-tekst, testtekst fra typografi
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

# marginer
hmargin = 40
vmargin = 40
tmargin = 4
bmargin = 4
# padding-margin
pmargin = 1

poppopp = lagVindu(storrelseY - tmargin - bmargin, storrelseX - hmargin - vmargin, tmargin, vmargin, "Lorem Ipsum")
wbkgd(poppopp, COLOR_PAIR(2))
box(poppopp)
poppoppPanel = new_panel(poppopp)

vinduTekst(poppopp, 1, 3, storrelseX - hmargin - vmargin - pmargin * 2, lorem)

# Sett på farger, fargepar nummer 4
wattron(bakgrunn, COLOR_PAIR(3))

# move cursor, spesifiser window, legg til string til vinduet
# mv           w                  addstr
mvwaddstr(bakgrunn, 1, 1, "Dette programmet er et test-program.", A_BOLD)

wattroff(bakgrunn, COLOR_PAIR(3))

mvwaddstr(bakgrunn, storrelseY - 2, 1, "Avslutt programmet med bruk av END-tasten", A_BOLD)

# Tegn vinduet bakgrunn
update_panels()
doupdate()

tast = 0
i = 1
storrelse = getmaxyx(stdscr)

keypad(bakgrunn, True)

while (tast != KEY_END):
    i = i + 1
    wattron(bakgrunn, COLOR_PAIR(i - 1))
    mvwaddstr(bakgrunn, i, 1, "Teller!", COLOR_PAIR(i) | A_NORMAL)
    tast = wgetch(bakgrunn)
    if (i == 5):
        break

# Rydde opp på skjermen!
wclear(bakgrunn)
wrefresh(bakgrunn)
endwin()

print("Dette var alt!\n")
