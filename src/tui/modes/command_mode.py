from dataclasses import dataclass
from src.editor import Editor
from src.interfaces.keys import Key
from src.interfaces.mode import Mode


@dataclass(frozen=True)
class TextUserInterfaceCommandMode(Mode):
    editor: Editor
    is_active: bool = True

    def key_action(self, key: int):
        if key == Key.ESC.value:
            raise StopIteration
        if key == Key.LEFT.value:
            self.editor.cursor_left()
        elif key == Key.RIGHT.value:
            self.editor.cursor_right()
        elif key == Key.UP.value:
            self.editor.cursor_up()
        elif key == Key.DOWN.value:
            self.editor.cursor_down()
        if key == ord("a"):
            object.__setattr__(self, "is_active", False)
        if key == ord("s"):
            self.editor.save()
        if key == ord("x"):
            self.editor.cut()
        if key == ord("p"):
            self.editor.paste()
