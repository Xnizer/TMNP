import os
import termios
import tty

from ._unix_util import parse_input_buffer
from ._wrapper import TerminalWrapperBase, TerminalSize, KeyboardKey


class UnixTerminal(TerminalWrapperBase):
    def __init__(self):
        self.__read_fd = os.open('/dev/tty', os.O_RDONLY | os.O_NONBLOCK)
        self.__write_fd = os.open('/dev/tty', os.O_WRONLY)
        self._input_buffer = b''
        
        # Save original terminal settings
        self.__original_attrs = termios.tcgetattr(self.__read_fd)
        tty.setcbreak(self.__read_fd, termios.TCSANOW)
        

    def size(self) -> TerminalSize:
        ts = os.get_terminal_size(self.__write_fd)
        return TerminalSize(ts.columns, ts.lines)


    def write(self, row: int, col: int, text: str):
        output = f"\033[{row+1};{col+1}H{text}"
        os.write(self.__write_fd, output.encode())


    def clear(self, fill: str = ' '):
        # TODO: implement character fill
        os.write(self.__write_fd, b"\033[2J")


    def cursor(self, visible: bool):
        if visible:
            os.write(self.__write_fd, b"\x1b[?25h")
        else:
            os.write(self.__write_fd, b"\x1b[?25l")


    def read(self) -> KeyboardKey | None:
        try:
            new_bytes = os.read(self.__read_fd, 1024)
            self._input_buffer += new_bytes
        except BlockingIOError:
            pass

        if not self._input_buffer:
            return None

        key, consumed_bytes = parse_input_buffer(self._input_buffer)
        if consumed_bytes > 0:
            self._input_buffer = self._input_buffer[consumed_bytes:]
            return key

        return None


    def __del__(self):
        # Restore original terminal settings
        termios.tcsetattr(self.__read_fd, termios.TCSANOW, self.__original_attrs)

        os.close(self.__read_fd)
        os.close(self.__write_fd)
        del self.__read_fd
        del self.__write_fd