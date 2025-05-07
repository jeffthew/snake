from enum import Enum

class CursorState(Enum):
    CURSOR_PLAY = 0
    CURSOR_CREDITS = 1
    CURSOR_QUIT = 2

class DisplayState(Enum):
    MAIN_MENU_DISPLAY = 100
    CREDITS_DISPLAY = 101
    GAME_OVER_DISPLAY = 102

class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
