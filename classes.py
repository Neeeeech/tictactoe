import pyglet

class TicTacToe:
    X, O = 1, 2

    def __init__(self, board_len, win_len, window_len):
        """initializes tic tac toe board, with board length, length of chain needed to win & window size"""
        self.board = [[0]*board_len for _ in range(board_len)]
        self.board_len = board_len
        self.win_len = win_len
        self.turn = TicTacToe.X

        # initializes pyglet Batches
        self.batch = pyglet.graphics.Batch()
        self.markers = []

        # draws the grid of right size and adds it to self.batch
        self.background = []
        self.window_min, self.window_max = window_len * 0.05, window_len * 0.95
        self.grid_width = (self.window_max - self.window_min) / board_len
        self.line_width = 0.01 * self.grid_width
        for i in range(window_len + 1):
            coord = self.window_min + i * self.grid_width
            self.background.append(pyglet.shapes.Line(coord, self.window_min, coord, self.window_max,
                                                      width=self.line_width, color=(245, 245, 245), batch=self.batch))
            self.background.append(pyglet.shapes.Line(self.window_min, coord, self.window_max, coord,
                                                      width=self.line_width, color=(245, 245, 245), batch=self.batch))

    def __str__(self):
        """returns a print of the board"""
        horizontal_line = ("-" * (self.board_len * 4 + 1)) + "\n"
        string_to_print = horizontal_line
        for row in self.board:
            string_to_print += "|"
            for tile in row:
                if tile == TicTacToe.X:
                    string_to_print += " X "
                elif tile == TicTacToe.O:
                    string_to_print += " O "
                else:
                    string_to_print += "   "
                string_to_print += "|"
            string_to_print += "\n"
            string_to_print += horizontal_line
        return string_to_print

    def play_x(self, x_coord, y_coord):
        """plays an X at the given coords, given that it is X's turn, & adds an X to self.batch"""
        if self.turn == TicTacToe.X and self.board[y_coord][x_coord] == 0:
            # adds an X to the right spot on the board list
            self.board[y_coord][x_coord] = TicTacToe.X

            # draws an X at the appropriate place
            box_bottom_left_coord = (self.window_min + x_coord * self.grid_width,
                                     self.window_max - (y_coord + 1) * self.grid_width)
            self.markers.append(pyglet.shapes.Line(box_bottom_left_coord[0] + 0.15 * self.grid_width,
                                                   box_bottom_left_coord[1] + 0.15 * self.grid_width,
                                                   box_bottom_left_coord[0] + 0.85 * self.grid_width,
                                                   box_bottom_left_coord[1] + 0.85 * self.grid_width,
                                                   width=self.line_width, color=(245, 245, 245), batch=self.batch))
            self.markers.append(pyglet.shapes.Line(box_bottom_left_coord[0] + 0.15 * self.grid_width,
                                                   box_bottom_left_coord[1] + 0.85 * self.grid_width,
                                                   box_bottom_left_coord[0] + 0.85 * self.grid_width,
                                                   box_bottom_left_coord[1] + 0.15 * self.grid_width,
                                                   width=self.line_width, color=(245, 245, 245), batch=self.batch))

            # sets the turn to O
            self.turn = TicTacToe.O

    def play_o(self, x_coord, y_coord):
        """plays an O at the given coords, given that it is O's turn, & adds an O to self.batch"""
        if self.turn == TicTacToe.O and self.board[y_coord][x_coord] == 0:
            # adds an O to the right spot on the board list
            self.board[y_coord][x_coord] = TicTacToe.O

            # draws an O at the appropriate place
            self.markers.append(pyglet.shapes.Circle(self.window_min + (x_coord + 0.5) * self.grid_width,
                                                     self.window_max - (y_coord + 0.5) * self.grid_width,
                                                     0.36 * self.grid_width, color=(245, 245, 245), batch=self.batch))
            self.markers.append(pyglet.shapes.Circle(self.window_min + (x_coord + 0.5) * self.grid_width,
                                                     self.window_max - (y_coord + 0.5) * self.grid_width,
                                                     0.35 * self.grid_width, color=(0, 0, 0), batch=self.batch))

            # sets the turn to X
            self.turn = TicTacToe.X

    def play(self, x_coord, y_coord):
        """plays the right marker depending on the turn at the given coords"""
        if self.board[y_coord][x_coord] == 0:
            if self.turn == TicTacToe.X:
                self.play_x(x_coord, y_coord)
            else:
                self.play_o(x_coord, y_coord)

    def on_click(self, x, y):
        """plays a marker on click"""
        if self.window_min < x < self.window_max and self.window_min < y < self.window_max:
            x_coord = int((x - self.window_min) // self.grid_width)
            y_coord = int(self.board_len - 1 - ((y - self.window_min) // self.grid_width))
            self.play(x_coord, y_coord)
            print(self)


if __name__ == '__main__':
    game = TicTacToe(3, 3, 600)
    win = pyglet.window.Window(600, 600)
    game.play(0,9)
    game.play(1,1)
    print(game)

    @win.event()
    def on_draw():
        win.clear()
        game.batch.draw()

    @win.event()
    def on_mouse_press(x, y, button, modifiers):
        game.on_click(x, y)

    pyglet.app.run()
