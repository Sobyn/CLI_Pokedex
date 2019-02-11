from unicurses import *

stdscr = initscr()                              # initializes the standard screen

addstr('Hello World!\n')
addch(ord('A') | A_BOLD)
addstr(' single bold letter\n')
attron(A_BOLD)                                  # Turns on attribute
addstr('\n\nBold string')
attroff(A_BOLD)
addstr("\nNot bold now")
mvaddch(7, 10, 66)                              # B at row 7, col 10
addstr(' - single letter at row 7, col 10')

start_color()
init_pair(1, COLOR_RED, COLOR_GREEN)            # Specifies foreground and background pair 1
init_pair(2, COLOR_YELLOW, COLOR_RED)

attron(COLOR_PAIR(1))
mvaddstr(15, 12, 'Red on green at row 15, col 12')
attroff(COLOR_PAIR(1))

attron(COLOR_PAIR(2))
addstr('\n\nYellow on red')
addstr('\n\nPress up arrow!')
attroff(COLOR_PAIR(2))

cbreak()                # Gets raw key inputs but allows CRTL+C to work
keypad(stdscr, True)    # Get arrow keys etc.
noecho()                # Do not display automatically characters for key presses
a = getch()             # Gets the key code
if a == KEY_UP:
    beep()
    clear()
    addstr('Beep! Any key to quit.')
a = getch()
