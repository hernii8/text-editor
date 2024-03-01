from abc import ABC, abstractmethod

from src.editor import Editor


class Mode(ABC):
    editor: Editor
    is_active: bool

    @abstractmethod
    def key_action(self, key: int):
        pass
