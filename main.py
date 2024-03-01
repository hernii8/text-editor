from sys import argv
from src.editor import Editor
from src.logger import FileLogger
from src.tui.tui import TextUserInterface
import traceback


def main():
    if len(argv) == 1:
        raise Exception("You must specify a file")
    file_path = argv[1]
    logger = FileLogger()
    editor = Editor().from_file(file_path)
    interface = TextUserInterface(editor=editor, logger=logger)
    while True:
        try:
            interface.handle_input()
        except StopIteration:
            editor.save()
            break
        except Exception as e:
            editor.save()
            raise e


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
