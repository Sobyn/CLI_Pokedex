# Innstaller UniCurses fra: https://sourceforge.net/projects/pyunicurses/
# Last ned pdcurses.dll, putt den i katalogen til programmet ditt (prosjektfil.py)-katalogen
# Ikke bland 64bit python med 32bit dll.
# Start programmet fra powershell, cmd, bash eller lignende
from unicurses import *

stdscr = initscr()  # initializes the standard screen

# Skru på fargestøtte
start_color()

# Tastaturfjas
noecho()  # Skru av at man ser hvilket tegn som er trykket
cbreak()  # Gets raw key inputs but allows CRTL+C to work
keypad(stdscr, True)  # Get arrow keys etc.

# Bakgrunn,hvot på sort.
init_pair(1, COLOR_RED, COLOR_BLACK)

# Grå tekst på blått
init_pair(2, COLOR_WHITE, COLOR_BLUE)

# Rødt på grønt
init_pair(3, COLOR_RED, COLOR_GREEN)


# høyde, bredde, x, y
def lagVindu(y, x, startx, starty):
    lokalt = newwin(y, x, startx, starty)
    #box(lokalt, 0, 0)
    #mvwaddch(lokalt, 2, 0, ACS_LTEE)
    #mvwhline(lokalt, 2, 1, ACS_HLINE, x - 2)
    #mvwaddch(lokalt, 2, x - 1, ACS_RTEE)
    return lokalt


storrelse = getmaxyx(stdscr)

storrelseX = storrelse[1]
storrelseY = storrelse[0]

bakgrunn = lagVindu(storrelseY, storrelseX, 0, 0)
box(bakgrunn)  # , 0,0)
bakgrunnPanel = new_panel(bakgrunn)

poppopp = lagVindu(15, 50, storrelseY - 22, 3)
wbkgd(poppopp, COLOR_PAIR(2))
box(poppopp)
poppoppPanel = new_panel(poppopp)

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

print("Dette var alt......\n")
