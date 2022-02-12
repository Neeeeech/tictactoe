import pyglet

class TicTacToe:
    def __init__(self, board_len, win_len, window_len):
        """initializes tic tac toe board, with board length, length of chain needed to win & window size"""
        self.board_size = board_len
        self.win_len = win_len
        self.batch = pyglet.graphics.Batch()

        # draws the grid of right size and adds it to self.batch
        self.background = []
        window_min, window_max = window_len * 0.05, window_len * 0.95
        grid_width = (window_max - window_min) / board_len
        for i in range(window_len + 1):
            coord = window_min + i * grid_width
            self.background.append(pyglet.shapes.Line(coord, window_min, coord, window_max,
                                                      width=2, color=(245, 245, 245), batch=self.batch))
            self.background.append(pyglet.shapes.Line(window_min, coord, window_max, coord,
                                                      width=2, color=(245, 245, 245), batch=self.batch))


if __name__ == '__main__':
    game = TicTacToe(10, 3, 600)
    win = pyglet.window.Window(600, 600)

    @win.event()
    def on_draw():
        win.clear()
        game.batch.draw()

    pyglet.app.run()
