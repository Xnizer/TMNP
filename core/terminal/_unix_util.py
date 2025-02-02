from ._wrapper import KeyboardKey


def parse_input_buffer(buffer: bytes) -> tuple[KeyboardKey | None, int]:
    if not buffer:
        return (None, 0)

    # Enter
    if buffer[0] == 13:
        return (KeyboardKey.ENTER, 1)
    
    # ESC
    if buffer[0] == 0x1b:
        return _parse_escape_sequence(buffer)

    # TODO: handle more keys
    
    return (None, 1)


def _parse_escape_sequence(buffer: bytes) -> tuple[KeyboardKey | None, int]:
    # ESC
    if len(buffer) == 1:
        return (KeyboardKey.ESC, 1)
    
    # CSI sequence (ESC [ ...)
    if buffer[1] == 0x5b:  # [
        return _parse_csi_sequence(buffer)
    
    # ESC+X sequences
    return (None, 2)


def _parse_csi_sequence(buffer: bytes) -> tuple[KeyboardKey | None, int]:
    if len(buffer) < 3:
        return (None, 0)  # Wait for more data
    
    match buffer[2]:
        case 0x41: return (KeyboardKey.UP, 3) # A
        case 0x42: return (KeyboardKey.DOWN, 3) # B
        case 0x44: return (KeyboardKey.LEFT, 3) # C
        case 0x43: return (KeyboardKey.RIGHT, 3) # D
    
    # Handle longer CSI sequences by finding terminator
    # CSI sequences end with ~ or A-Za-z
    for i in range(2, min(len(buffer), 16)):
        if 0x40 <= buffer[i] <= 0x7E:  # ASCII @ to ~
            return (None, i + 1)  # Consume entire sequence
    
    # If no terminator found, wait for more data
    return (None, 0)