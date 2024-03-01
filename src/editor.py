from __future__ import annotations
import os
from typing import List, TypedDict
from dataclasses import dataclass

MAX_LINE_LENGTH = 400


class Cursor(TypedDict):
    line: int = 0
    char: int = 0
    last_horizontal_ref: int = 0


@dataclass
class Editor:
    __text: List[str]
    __cursor: Cursor
    __max_line_length: int
    __file_path: str

    def __init__(
        self,
        text: List[str] = [""],
        cursor: Cursor = {"line": 0, "char": 0, "last_horizontal_ref": 0},
        max_line_length=MAX_LINE_LENGTH,
        file_path="",
    ):
        self.__text = text
        self.__cursor = cursor
        if "last_horizontal_ref" not in cursor:
            self.__cursor["last_horizontal_ref"] = cursor["char"]
        self.__max_line_length = max_line_length
        self.__file_path = file_path

    @property
    def text(self) -> List[str]:
        return self.__text

    @property
    def cursor(self) -> Cursor:
        return self.__cursor

    @property
    def max_line_length(self) -> Cursor:
        return self.__max_line_length

    @property
    def file_path(self) -> str:
        return self.__file_path

    def from_file(self, path: str) -> Editor:
        self.__file_path = path
        try:
            with open(path + ".tmp", "x+") as file:
                self.__text = file.read().split("\n")
                return self
        except FileNotFoundError:
            open(path, "x")
            with open(path + ".tmp", "x+") as file:
                self.__text = file.read().split("\n")
                return self
        except PermissionError:
            print(f"Error: Permission denied to access file '{path}'.")
        except Exception as e:
            raise e

    def save(self):
        try:
            with open(self.__file_path, "w") as file:
                file.write("\n".join(self.text))
        except FileNotFoundError:
            print(f"Error: File '{self.__file_path}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to access file '{self.__file_path}'.")
        except Exception as e:
            raise e

    def exit(self):
        os.remove(self.__file_path + ".tmp")

    def append(self, character):
        if len(self.__get_current_line_text()) >= self.max_line_length:
            self.add_line()
        self.__set_current_line_text(
            self.__get_current_line_text()[0 : self.cursor["char"]]
            + character
            + self.__get_current_line_text()[self.cursor["char"] :]
        )
        self.cursor_right()

    def delete(self):
        if len(self.__get_current_line_text()) > 0:
            self.__set_current_line_text(
                self.__get_current_line_text()[0 : self.cursor["char"] - 1]
                + self.__get_current_line_text()[self.cursor["char"] :]
            )
            self.cursor_left()
        else:
            if self.cursor["line"] > 0:
                self.__remove_line()

    def cursor_right(self):
        is_cursor_at_end = self.cursor["char"] >= len(self.__get_current_line_text())
        are_more_lines = self.cursor["line"] < len(self.text) - 1
        if is_cursor_at_end:
            if are_more_lines:
                self.__move_cursor(self.cursor["line"] + 1, 0, True)
        else:
            self.__move_cursor(self.cursor["line"], self.cursor["char"] + 1, True)

    def cursor_left(self):
        is_cursor_at_beggining = self.cursor["char"] <= 0
        is_first_line = self.cursor["line"] == 0
        if is_cursor_at_beggining:
            if not is_first_line:
                self.__move_cursor(
                    self.cursor["line"] - 1,
                    len(self.text[self.cursor["line"] - 1]),
                    True,
                )
        else:
            self.__move_cursor(self.cursor["line"], self.cursor["char"] - 1, True)

    def cursor_up(self):
        is_first_line = self.cursor["line"] == 0
        if not is_first_line:
            is_next_line_longer_than_last_ref = (
                len(self.__get_line_text_at(self.cursor["line"] - 1))
                >= self.cursor["last_horizontal_ref"]
            )
            if is_next_line_longer_than_last_ref:
                self.__move_cursor(
                    self.cursor["line"] - 1, self.cursor["last_horizontal_ref"], False
                )
            else:
                self.__move_cursor(
                    self.cursor["line"] - 1,
                    len(self.__get_line_text_at(self.cursor["line"] - 1)),
                    False,
                )

    def cursor_down(self):
        is_not_last_line = self.cursor["line"] < len(self.text) - 1

        if is_not_last_line:
            is_next_line_longest_than_last_ref = (
                len(self.__get_line_text_at(self.cursor["line"] + 1))
                >= self.cursor["last_horizontal_ref"]
            )
            if is_next_line_longest_than_last_ref:
                self.__move_cursor(
                    self.cursor["line"] + 1, self.cursor["last_horizontal_ref"], False
                )
            else:
                self.__move_cursor(
                    self.cursor["line"] + 1,
                    len(self.__get_line_text_at(self.cursor["line"] + 1)),
                    False,
                )

    def add_line(self):
        lines_before = self.text[0 : self.cursor["line"] + 1]
        lines_after = self.text[self.cursor["line"] + 1 :]
        characters_after_cursor = self.text[self.cursor["line"]][self.cursor["char"] :]
        if len(characters_after_cursor) > 0:
            characters_before_cursor = lines_before[-1][: -len(characters_after_cursor)]
            lines_before[-1] = characters_before_cursor
        new_line = [characters_after_cursor]
        self.__text = lines_before + new_line + lines_after
        self.__move_cursor(self.cursor["line"] + 1, 0, True)

    def __move_cursor(self, line: int, char: int, update_ref=False):
        self.cursor["line"] = line
        self.cursor["char"] = char
        if update_ref:
            self.cursor["last_horizontal_ref"] = char

    def __remove_line(self):
        lines_before = self.text[0 : self.cursor["line"]]
        lines_after = self.text[self.cursor["line"] + 1 :]
        previous_line_index = self.cursor["line"] - 1

        self.__text = lines_before + lines_after
        self.__move_cursor(
            previous_line_index, len(self.text[previous_line_index]), True
        )

    def __get_current_line_text(self):
        return self.__get_line_text_at(self.cursor["line"])

    def __get_line_text_at(self, i: int):
        return self.text[i]

    def __set_current_line_text(self, text: str):
        self.text[self.cursor["line"]] = text
