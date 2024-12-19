from ._windows_api import (
    set_cursor_position, 
    set_cursor_visibility, 
    get_screen_buffer_info, 
    fill_console_output_characters, 
    fill_console_output_attribute, 
    write_console, 
    read
)
from ._wrapper import TerminalWrapperBase, KeyboardKey, TerminalSize

class WindowsTerminalWrapper(TerminalWrapperBase):
    def size(self) -> TerminalSize:
        size = get_screen_buffer_info().dwSize
        return TerminalSize(size.X, size.Y)
    

    def write(self, row: int, col: int, text: str):
        set_cursor_position((row, col))
        write_console(str)
    

    def clear(self, fill: str = ' '):
        fill_console_output_characters(fill)
        fill_console_output_attribute()
        set_cursor_position(0, 0)
    

    def read(self) -> KeyboardKey | None:
        key = read()

        if key is None:
            return None
        
        if key == b'\xe0' or key == b'\x00': # Special function key
            
            key = read() # Get the actual keycode

            if key == b'H': # Up arrow
                return KeyboardKey.UP
            elif key == b'P': # Down arrow
                return KeyboardKey.DOWN
            elif key == b'K': # Left arrow
                return KeyboardKey.LEFT
            elif key == b'M': # Right arrow
                return KeyboardKey.UP
            else:
                return None # TODO: handle more special function keys
        else:
            return None # TODO: handle more keys