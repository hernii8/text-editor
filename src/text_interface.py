from abc import ABC
from typing import Tuple
from editor import Editor


class TextInterface(ABC):
    __editor: Editor

    def __init__(self, editor: Editor):
        pass

    def update(self, text: str, cursor_coordinates: Tuple[int, int]):
        pass

    def get_char(self):
        pass
