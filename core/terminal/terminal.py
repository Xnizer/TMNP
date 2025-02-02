import sys

if sys.platform == "win32":
    from ._windows import WindowsTerminalWrapper as TerminalWrapper
else:
    from ._unix import UnixTerminal as TerminalWrapper

from data import Point


class Terminal:
    def __init__(self):
        self.__terminal = TerminalWrapper()
        self.__size = self.__terminal.size()
        self.__buffer = self.__create_buffer(self.__size.size)


    def print(self, x: int, y: int, line: str):
        buffer_width = self.__size.rows
        buffer_height = self.__size.columns
        line_length = len(line)
        
        # Ignore lines that are outside the buffer
        if y < 0 or y > buffer_height:
            return
                
        # Ignore characters that are outside the buffer
        if x < 0:
            line = line[abs(x):]
            line_length = len(line)
            x = 0
            
        overdraw = (x + line_length) - buffer_width
        
        if overdraw > 0:
            line_length -= overdraw
            line = line[:line_length]
            
        # Copy line to the buffer
        line_start = y * buffer_width + x
        line_end = line_start + line_length
        self.__buffer[line_start : line_end] = line


    def clear_buffer(self, fill = ' '):
        # 'fill' must be 1 character
        if not isinstance(fill ,str) or len(fill) != 1:
            fill = ' '
            
        # Fill the frame buffer
        empty_line = fill * self.__size.rows
        for y in range(self.__size.columns):
            self.print(0, y, empty_line)


    def clear_screen(self, fill = ' '):
        # 'fill' must be 1 character
        if not isinstance(fill ,str) or len(fill) != 1:
            fill = ' '

        # Fill the entire screen buffer
        self.__terminal.clear(fill)


    def update_screen(self):
        # Resize buffer when window size changes.
        # Resizing deletes the current buffer, resulting in 1 empty frame
        size = self.__terminal.size()
        if size.rows != self.__size.rows or size.columns != self.__size.columns:
            self.__size = self.__terminal.size()
            self.__buffer = self.__create_buffer(self.__size.size)
            self.clear_screen()

        # Copy buffer content to a string
        width = self.__size.rows
        height = self.__size.columns
        frame = '\n'.join([''.join(self.__buffer[line * width : line * width + width]) for line in range(height)])

        # Print to screen
        self.__terminal.write(0, 0, frame)
        
        
    def next_keypress(self):
       return self.__terminal.read() 
    
    
    def get_size(self):
        return Point(self.__size.rows, self.__size.columns)
        

    def __create_buffer(self, size):
        return [' '] * size