from src.editor import Editor
from typing import Any
from src.logger import FileLogger
from src.text_interface import TextInterface
import curses
import re
import os

KEY_ENTER = 10
KEY_ESC = 27
KEY_SAVE = 186
COLOR_AQUAMARINE = 300
"""Command mode cuando se presione ESC, salir de el cuando se presione a
Last combination of characters se resetea cuando se haga alguna accion o sino
cuando pase 1 segundo sin haber escrito nada"""


class TextUserInterface(TextInterface):
    __window: Any
    __editor: Editor
    __command_mode: bool
    __logger: FileLogger

    def __init__(self, editor: Editor, logger: FileLogger, command_mode: bool = False):
        os.environ.setdefault("ESCDELAY", "25")
        self.__window = curses.initscr()
        self.__editor = editor
        self.__command_mode = command_mode
        self.__logger = logger
        self.__window.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.__update()

    @property
    def window(self):
        return self.__window

    @property
    def editor(self):
        return self.__editor

    @property
    def command_mode(self):
        return self.__command_mode

    def handle_input(self):
        key = self.__get_input()
        if self.command_mode:
            self.__command_mode_input(key)
        else:
            self.__regular_mode_input(key)

        if self.command_mode:
            self.__update(color=COLOR_AQUAMARINE)
        else:
            self.__update()

    def __command_mode_input(self, key):
        try:
            if key == KEY_ESC:
                raise StopIteration
            if key == curses.KEY_LEFT:
                self.editor.cursor_left()
            elif key == curses.KEY_RIGHT:
                self.editor.cursor_right()
            elif key == curses.KEY_UP:
                self.editor.cursor_up()
            elif key == curses.KEY_DOWN:
                self.editor.cursor_down()
            if key == ord("a"):
                self.__command_mode = False
            if key == ord("s"):
                self.editor.save()
            if key == ord("x"):
                self.editor.cut()
            if key == ord("p"):
                self.editor.paste()
        except Exception as e:
            self.__exit()
            raise e

    def __regular_mode_input(self, key):
        try:
            if key == KEY_ESC:
                self.__command_mode = True
            if key == curses.KEY_LEFT:
                self.editor.cursor_left()
            elif key == curses.KEY_RIGHT:
                self.editor.cursor_right()
            elif key == curses.KEY_UP:
                self.editor.cursor_up()
            elif key == curses.KEY_DOWN:
                self.editor.cursor_down()
            elif key == curses.KEY_BACKSPACE:
                self.editor.delete()
            elif key == KEY_ENTER:
                self.editor.add_line()
            elif self.__is_printable(character := chr(key)):
                self.editor.append(character)
        except Exception as e:
            self.__exit()
            raise e

    def __update(self, color=0):
        self.window.clear()
        self.window.addstr("\n".join(self.editor.text), curses.color_pair(color))
        self.window.move(self.editor.cursor["line"], self.editor.cursor["char"])
        self.window.refresh()

    def __get_input(self):
        return self.window.getch()

    def __is_printable(self, char):
        printable_characters = r"[^\x00-\x1F\x7F-\x9F]+"
        return re.match(printable_characters, char) is not None

    def __exit(self):
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()
