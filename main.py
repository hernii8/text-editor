from sys import argv
from src.editor import Editor
from src.tui import TextUserInterface


def main():
    file_path = argv[1]
    editor = Editor().from_file(file_path)
    interface = TextUserInterface(editor=editor)
    return_status = 1
    while return_status == 1:
        return_status = interface.handle_input()


if __name__ == "__main__":
    main()
