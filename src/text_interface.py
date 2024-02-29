from abc import ABC, abstractmethod
from typing import Tuple


class TextInterface(ABC):
    @abstractmethod
    def update(self, text: str, cursor_coordinates: Tuple[int, int]):
        pass

    @abstractmethod
    def get_char(self):
        pass
