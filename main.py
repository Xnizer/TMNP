import drawing
from data import Point
from core.terminal.terminal import Terminal
from snake import SnakeGame, GameState
from time import sleep


def main():
    
    # TODO: show a start menu
    
    game = SnakeGame(Point(40, 20))
    terminal = Terminal()
    terminal.clear_screen()
    
    # game loop
    while game.get_state() == GameState.RUNNING:
        # -------------- update --------------- #
        player_input = terminal.next_keypress()
        if (player_input is not None):
            game.process_input(player_input.value)
        game.advance()
        
        # --------------- draw ---------------- #
        terminal.clear_buffer('─')
        
        game_scale = Point(2, 1)
        game_size = game.get_size()
        game_position = terminal.get_size() / Point(2, 2) - game_size * game_scale / Point(2, 2)
        drawing.draw_snake_game(game, game_position, game_scale, terminal)

        box_pos = game_position - Point(1, 1)
        box_dim = game_size * game_scale + Point(1, 1)
        drawing.draw_box(box_pos, box_dim, terminal)

        terminal.update_screen()
        
        # sleep until next frame
        sleep(1/12)

    terminal.clear_screen()
    
    # TODO: print game results
    

if __name__ == "__main__":
    main()