from sys import argv
from src.editor import Editor
from src.tui import TextUserInterface


def main():
    file_path = argv[1]
    editor = Editor().from_file(file_path)
    interface = TextUserInterface(editor=editor)
    while True:
        try:
            interface.handle_input()
        except StopIteration:
            editor.save()
            editor.exit()
            break
        except Exception as e:
            editor.save()
            editor.exit()
            raise e


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
