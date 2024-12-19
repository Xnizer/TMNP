from ctypes import WinDLL, Structure, byref
from ctypes.wintypes import _COORD, _SMALL_RECT, DWORD, WORD, BOOL, ULONG, WCHAR
from msvcrt import kbhit, getch


class _CONSOLE_CURSOR_INFO(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('bVisible', BOOL)
    ]


class _CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ('dwSize', _COORD),
        ('dwCursorPosition', _COORD),
        ('wAttributes', WORD),
        ('srWindow', _SMALL_RECT),
        ('dwMaximumWindowSize', _COORD),
    ]


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11

kernel32 = WinDLL("Kernel32")
stdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)
stdout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_title(title: str):
    return kernel32.SetConsoleTitleW(title)


def set_cursor_visibility(visible: bool):
    cursor_info = _CONSOLE_CURSOR_INFO()
    kernel32.GetConsoleCursorInfo(stdout, byref(cursor_info))
    cursor_info.bVisible = visible
    kernel32.SetConsoleCursorInfo(stdout, byref(cursor_info))


def set_cursor_position(row: int, col: int):
    kernel32.SetConsoleCursorPosition(stdout, _COORD(row, col))


def get_screen_buffer_info():
    buffer_info = _CONSOLE_SCREEN_BUFFER_INFO()
    kernel32.GetConsoleScreenBufferInfo(stdout, byref(buffer_info))
    return buffer_info


def fill_console_output_characters(fill: str = ' '):
    buffer_info = get_screen_buffer_info()
    buffer_size = DWORD(buffer_info.dwSize.X * buffer_info.dwSize.Y)
    characters_written = ULONG(0) 
    kernel32.FillConsoleOutputCharacterW(STD_OUTPUT_HANDLE, WCHAR(fill), buffer_size, _COORD(0, 0), byref(characters_written))
    return characters_written.value


def fill_console_output_attribute():
    buffer_info = get_screen_buffer_info()
    buffer_size = DWORD(buffer_info.dwSize.X * buffer_info.dwSize.Y)
    characters_written = ULONG(0) 
    kernel32.FillConsoleOutputAttribute(STD_OUTPUT_HANDLE, buffer_info.wAttributes, buffer_size, _COORD(0, 0), byref(characters_written))
    return characters_written.value


def write_console(string: str):
    lpNumberOfCharsWritten = DWORD(0)
    kernel32.WriteConsoleW(stdout, string, len(string), byref(lpNumberOfCharsWritten))
    return lpNumberOfCharsWritten.value


def read():
    if kbhit():
        return getch()
    else:
        return None