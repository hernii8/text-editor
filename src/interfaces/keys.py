from enum import Enum
import curses


class Key(Enum):
    ENTER = 10
    ESC = 27
    SAVE = 186
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    BACKSPACE = curses.KEY_BACKSPACE
