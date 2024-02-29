from abc import ABC, abstractmethod
from typing import Tuple
from editor import Editor


class TextInterface(ABC):
    __editor: Editor

    @abstractmethod
    def __init__(self, editor: Editor):
        pass

    @abstractmethod
    def update(self, text: str, cursor_coordinates: Tuple[int, int]):
        pass

    @abstractmethod
    def get_char(self):
        pass
