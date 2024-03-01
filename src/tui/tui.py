from src.editor import Editor
from src.interfaces.mode import Mode
from src.logger import FileLogger
from src.interfaces.text_interface import TextInterface
import curses
import os
from src.tui.modes.command_mode import TextUserInterfaceCommandMode
from src.tui.modes.typing_mode import TextUserInterfaceTypingMode

COLOR_AQUAMARINE = 300


class TextUserInterface(TextInterface):
    def __init__(self, editor: Editor, logger: FileLogger, command_mode: bool = False):
        self.__editor = editor
        self.__logger = logger
        self.__active_mode: Mode = TextUserInterfaceTypingMode(editor=editor)
        self.__init_window()
        self.__update()

    @property
    def window(self):
        return self.__window

    @property
    def editor(self):
        return self.__editor

    @property
    def active_mode(self):
        return self.__active_mode

    @active_mode.setter
    def active_mode(self, value):
        self.__active_mode = value

    def handle_input(self):
        try:
            key = self.window.getch()
            self.active_mode.key_action(key)
            if not self.active_mode.is_active:
                self.switch_modes()

            self.__update(
                color=COLOR_AQUAMARINE
                if isinstance(self.active_mode, TextUserInterfaceCommandMode)
                else 0
            )
        except Exception as e:
            self.__exit()
            raise e

    def __update(self, color=0):
        self.window.clear()
        self.window.addstr("\n".join(self.editor.text), curses.color_pair(color))
        self.window.move(self.editor.cursor["line"], self.editor.cursor["char"])
        self.window.refresh()

    def __init_window(self):
        os.environ.setdefault("ESCDELAY", "25")
        self.__window = curses.initscr()
        self.__window.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def __exit(self):
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()

    def switch_modes(self):
        self.active_mode = (
            TextUserInterfaceTypingMode(editor=self.__editor)
            if isinstance(self.active_mode, TextUserInterfaceCommandMode)
            else TextUserInterfaceCommandMode(editor=self.__editor)
        )
