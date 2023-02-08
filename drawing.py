

def draw_box(position, size, terminal):
    # Border pieces
    top_left_corner = '╔'
    top_right_corner = '╗'
    bot_left_corner = '╚'
    bot_right_corner = '╝'
    horizontal_line = '═'
    vertical_line = '║'
    # Draw top line
    top_line = top_left_corner + \
        (horizontal_line * (size.X - 1)) + top_right_corner
    terminal.print(
        position.X,
        position.Y,
        top_line)
    # Draw bottom line
    bot_line = bot_left_corner + \
        (horizontal_line * (size.X - 1)) + bot_right_corner
    terminal.print(
        position.X,
        position.Y + size.Y,
        bot_line)
    # Draw side lines
    for i in range(1, size.Y):
        terminal.print(position.X, position.Y + i, vertical_line)
        terminal.print(position.X + size.X, position.Y + i, vertical_line)


def draw_snake_game(game, position, scale, terminal):
    size = game.get_size() * scale
    empty_line = ' ' * size.X  # TODO: cache

    # Clear game area
    for y in range(size.Y):
        terminal.print(position.X, y + position.Y, empty_line)

    # Draw snake
    for piece in game.get_snake():
        piece_position = piece * scale + position
        terminal.print(piece_position.X, piece_position.Y, '██')

    # Draw food
    food_position = game.get_food() * scale + position
    terminal.print(food_position.X, food_position.Y, '██')
