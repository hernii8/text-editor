from unittest.mock import mock_open
from src.editor import Cursor, Editor


def test_from_file(monkeypatch):
    """Given a file, the editor should be initialized with its contents"""
    mocked_file_content = """Line 1
                             Line 2"""
    monkeypatch.setattr("builtins.open", mock_open(read_data=mocked_file_content))
    editor_text = Editor().from_file("").text
    assert "\n".join(editor_text) == mocked_file_content


def test_append():
    """When appending a character, it should add it to the right of the cursor"""
    editor = Editor()
    editor.append("a")
    assert editor.text == ["a"]
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 1


def test_cursor_right():
    """When moving the cursor right, it should advance one position to the right"""
    editor = Editor(text=["a"], cursor=Cursor(line=0, char=0))
    editor.cursor_right()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 1


def test_cursor_right_with_no_more_text():
    """When moving the cursor right and there is no more text, it should stay in the same position"""
    editor = Editor(
        text=["".join(["a" for _ in range(50)])],
        cursor=Cursor(line=0, char=50),
        max_line_length=50,
    )
    editor.cursor_right()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 50


def test_cursor_right_newline():
    """When moving the cursor right at the end of a line, it should move to the beginning of next line"""
    editor = Editor(
        text=["".join(["a" for _ in range(50)]), ""],
        cursor=Cursor(line=0, char=50),
        max_line_length=50,
    )
    editor.cursor_right()
    assert editor.cursor["line"] == 1 and editor.cursor["char"] == 0


def test_cursor_left():
    """When moving the cursor left, it should back one position to the left"""
    editor = Editor(text=["a"], cursor=Cursor(line=0, char=1))
    editor.cursor_left()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 0


def test_cursor_left_with_no_previous_text():
    """When moving the cursor left at the beginning of the text, it should not move"""
    editor = Editor(
        text=[""],
        cursor=Cursor(line=0, char=0),
        max_line_length=50,
    )
    editor.cursor_left()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 0


def test_cursor_left_with_lines_before():
    """When moving the cursor left just before a previous line, it should go to the end of the previous line"""
    editor = Editor(
        text=["".join(["a" for _ in range(50)]), ""],
        cursor=Cursor(line=1, char=0),
        max_line_length=50,
    )
    editor.cursor_left()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 50


def test_delete_first_character():
    """When deleting the first character of the editor nothing should happen"""
    editor = Editor(text=[""], cursor=Cursor(line=0, char=0))
    editor.delete()
    assert editor.text[0] == ""


def test_delete_on_the_middle():
    """When the cursor is on the middle of a sentence, the deletion should be made on that position"""
    editor = Editor(text=["abc"], cursor=Cursor(line=0, char=2))
    editor.delete()
    assert editor.text[0] == "ac"


def test_delete():
    """When deleting, it should remove the character before the cursor"""
    editor = Editor(text=["a"], cursor=Cursor(line=0, char=1))
    editor.delete()
    assert editor.text == [""]
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 0


def test_append_newline():
    """When there is no more space in the current line,
    it should create a new line and append the next character there"""
    editor = Editor(
        text=["".join(["a" for _ in range(50)])],
        cursor=Cursor(line=0, char=50),
        max_line_length=50,
    )
    editor.append("a")
    assert len(editor.text[0]) == 50
    assert editor.text[1] == "a"
    assert editor.cursor["line"] == 1 and editor.cursor["char"] == 1


def test_append_newline_from_middle():
    """When the cursor is in the middle of the line it should carry the rest of the text to the next line"""
    editor = Editor(text=["aaa"], cursor=Cursor(line=0, char=1))
    editor.add_line()
    assert editor.text[0] == "a"
    assert editor.text[1] == "aa"


def test_delete_line():
    """When deleting the last character of a line, it should delete the line and move the cursor to the last
    character of the previous line"""
    editor = Editor(text=["aaa", ""], cursor=Cursor(line=1, char=0))
    editor.delete()
    assert len(editor.text) == 1
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 3


def test_move_cursor_up():
    """When moving the cursor up between lines with the same size, it should situate the cursor
    in the upper line on the same character position"""
    editor = Editor(text=["aaa", "aaa"], cursor=Cursor(line=1, char=0))
    editor.cursor_up()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 0


def test_move_cursor_up_with_less_text():
    """When moving the cursor up to a line with less text, it should situate the cursor
    at the end of the line. Then when moving it again to a line with the same size as the first
    one, it should remember the position that it had on the first one and situate the cursor there"""
    editor = Editor(text=["aaa", "a", "aaa"], cursor=Cursor(line=2, char=3))
    editor.cursor_up()
    assert editor.cursor["line"] == 1 and editor.cursor["char"] == 1


def test_move_cursor_up_remembering_position():
    """When moving the cursor up twice, having in the middle a shorter line, it should remember the
    character position of the first line and situate the cursor there again in the last one"""
    editor = Editor(text=["aaa", "a", "aaa"], cursor=Cursor(line=2, char=3))
    editor.cursor_up()
    editor.cursor_up()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 3


def test_move_cursor_down():
    """When moving the cursor down between lines with the same size, it should situate the cursor
    in the lower line on the same character position"""
    editor = Editor(text=["aaa", "aaa"], cursor=Cursor(line=0, char=0))
    editor.cursor_down()
    assert editor.cursor["line"] == 1 and editor.cursor["char"] == 0


def test_move_cursor_down_with_less_text():
    """When moving the cursor down to a line with less text, it should situate the cursor at the end
    of the next line"""
    editor = Editor(text=["aaa", "a", "aaa"], cursor=Cursor(line=0, char=3))
    editor.cursor_down()
    assert editor.cursor["line"] == 1 and editor.cursor["char"] == 1


def test_move_cursor_down_remembering_position():
    """When moving the cursor down twice, having in the middle a shorter line, it should remember the
    character position of the first line and situate the cursor there again in the last one"""
    editor = Editor(text=["aaa", "a", "aaa"], cursor=Cursor(line=0, char=3))
    editor.cursor_down()
    editor.cursor_down()
    assert editor.cursor["line"] == 2 and editor.cursor["char"] == 3


def test_cursor_down_on_last_line():
    """When moving the cursor down in the last line it should nothing happen"""
    editor = Editor(text=[""], cursor=Cursor(line=0, char=0))
    editor.cursor_down()
    assert editor.cursor["line"] == 0 and editor.cursor["char"] == 0


def test_cut_text():
    """When cutting text it should remove the entire line and store it"""
    editor = Editor(text=["abc", "def"], cursor=Cursor(line=1, char=0))
    editor.cut()
    assert editor.copied == "def"


def test_paste_text():
    """It should paste the stored text in the current cursor position"""
    editor = Editor(text=["abc", "def"], cursor=Cursor(line=1, char=0))
    editor.cut()
    editor.paste()
    assert editor.text[0] == "abcdef"


# test cut first line
# test break word on appending
# test break word on deleting
