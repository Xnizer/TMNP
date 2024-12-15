from ctypes import WinDLL, Structure, byref
from ctypes.wintypes import _COORD, _SMALL_RECT, DWORD, WORD, BOOL
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


kernel32 = WinDLL("Kernel32")


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
stdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)
stdout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_title(title):
    return kernel32.SetConsoleTitleW(title)


def set_cursor_visibility(visible):
    cursor_info = _CONSOLE_CURSOR_INFO()
    kernel32.GetConsoleCursorInfo(stdout, byref(cursor_info))
    cursor_info.bVisible = visible
    kernel32.SetConsoleCursorInfo(stdout, byref(cursor_info))


def set_cursor_position(position):
    kernel32.SetConsoleCursorPosition(stdout, _COORD(*position))


def get_screen_buffer_info():
    buffer_info = _CONSOLE_SCREEN_BUFFER_INFO()
    kernel32.GetConsoleScreenBufferInfo(stdout, byref(buffer_info))
    return buffer_info


def write(string):
    lpNumberOfCharsWritten = DWORD(0)
    kernel32.WriteConsoleW(stdout, string, len(string), byref(lpNumberOfCharsWritten))
    return lpNumberOfCharsWritten.value


def read():
    if kbhit():
        return getch()
    else:
        return None