from data import Point
from winconsole import set_cursor_position, set_cursor_visibility, get_screen_buffer_info, write, read


class Terminal:
    def __init__(self):
        self.__size = self.__native_window_size()
        self.__buffer = self.__create_buffer(self.__size)


    def print(self, x: int, y: int, line: str):
        buffer_width = self.__size.X
        buffer_height = self.__size.Y
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
        empty_line = fill * self.__size.X
        for y in range(self.__size.Y):
            self.print(0, y, empty_line)


    def clear_screen(self, fill = ' '):
        # 'fill' must be 1 character
        if not isinstance(fill ,str) or len(fill) != 1:
            fill = ' '
            
        # Fill the entire screen buffer
        buffer_size = self.__native_buffer_size()
        set_cursor_position((0, 0))
        write(fill * (buffer_size.X * buffer_size.Y))
        set_cursor_position((0, 0))


    def update_screen(self):
        # Resize buffer when window size changes.
        # Resizing deletes the current buffer, resulting in 1 empty frame
        if self.__native_window_size() != self.__size:
            self.__size = self.__native_window_size()
            self.__buffer = self.__create_buffer(self.__size)
            self.clear_screen()

        # Copy buffer content to a string
        w = self.__size.X
        h = self.__size.Y
        frame = '\n'.join([''.join(self.__buffer[l * w : l * w + w]) for l in range(h)])

        # Print to screen
        set_cursor_visibility(False)
        set_cursor_position((0, 0))
        write(frame)
        set_cursor_position((0, 0))
        
        
    def next_keypress(self):
        key = read()

        if key is None:
            return None

        if key == b'\xe0' or key == b'\x00': # Special function key
            
            key = read() # Get the actual keycode

            if key == b'H': # Up arrow
                return 'up'
            elif key == b'P': # Down arrow
                return 'down'
            elif key == b'K': # Left arrow
                return 'left'
            elif key == b'M': # Right arrow
                return 'right'
            else:
                return None # TODO: handle more keys
        else:
            return None # TODO: handle more keys
        
    
    def get_size(self):
        return self.__size
        

    def __native_window_size(self):
        rect = get_screen_buffer_info().srWindow
        return Point(rect.Right, rect.Bottom)


    def __native_buffer_size(self):
        size = get_screen_buffer_info().dwSize
        return Point(size.X, size.Y)


    def __create_buffer(self, size):
        # TODO: consider using an array or a string instead of a list
        return [' '] * (size.X * size.Y)