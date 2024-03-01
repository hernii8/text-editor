from abc import ABC, abstractmethod


class TextInterface(ABC):
    @abstractmethod
    def handle_input(self):
        pass
