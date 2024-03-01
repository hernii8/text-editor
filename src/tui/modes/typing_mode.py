from dataclasses import dataclass
from src.editor import Editor
from src.interfaces.keys import Key
from src.interfaces.mode import Mode
import re


@dataclass(frozen=True)
class TextUserInterfaceTypingMode(Mode):
    editor: Editor
    is_active: bool = True

    def key_action(self, key: int):
        if key == Key.ESC.value:
            object.__setattr__(self, "is_active", False)
        if key == Key.LEFT.value:
            self.editor.cursor_left()
        elif key == Key.RIGHT.value:
            self.editor.cursor_right()
        elif key == Key.UP.value:
            self.editor.cursor_up()
        elif key == Key.DOWN.value:
            self.editor.cursor_down()
        elif key == Key.BACKSPACE.value:
            self.editor.delete()
        elif key == Key.ENTER.value:
            self.editor.add_line()
        elif self.__is_printable(character := chr(key)):
            self.editor.append(character)

    def __is_printable(self, char):
        printable_characters = r"[^\x00-\x1F\x7F-\x9F]+"
        return re.match(printable_characters, char) is not None
