from editor import Editor
from typing import Any
from text_interface import TextInterface
from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_BACKSPACE, KEY_UP, initscr

import re

KEY_ENTER = 10
KEY_ESC = 27


class TextUserInterface(TextInterface):
    __window: Any
    __editor: Editor

    def __init__(self, editor: Editor):
        self.__window = initscr()
        self.__window.keypad(True)
        self.__editor = editor

    @property
    def window(self):
        return self.__window

    @property
    def editor(self):
        return self.__editor

    def handle_input(self):
        key = self.get_input()
        if key == 0xB0:
            self.editor.save()
        if key == KEY_LEFT:
            self.editor.cursor_left()
        elif key == KEY_RIGHT:
            self.editor.cursor_right()
        elif key == KEY_UP:
            self.editor.cursor_up()
        elif key == KEY_DOWN:
            self.editor.cursor_down()
        elif key == KEY_BACKSPACE:
            self.editor.delete()
        elif key == KEY_ENTER:
            self.editor.add_line()
        elif key == KEY_ESC:
            return 0
        elif self.__is_printable(character := chr(key)):
            self.editor.append(character)
        self.update()
        return 1

    def update(self):
        self.window.clear()
        self.window.addstr("\n".join(self.editor.text))
        self.window.move(self.editor.cursor["line"], self.editor.cursor["char"])
        self.window.refresh()

    def get_input(self):
        return self.window.getch()

    def __is_printable(self, char):
        printable_characters = r"[^\x00-\x1F\x7F-\x9F]+"
        return re.match(printable_characters, char) is not None
