import pyglet

def const_gen(const):
    """generates a generator that spits out a constant"""
    while True:
        yield const

def left_iter(marker_coord, min_coord):
    """generates a generator that counts leftwards to just before the min_coord"""
    for i in range(marker_coord - 1, min_coord, -1):
        yield i

def right_iter(marker_coord, max_coord):
    """generates a generator that counts rightwards to just before the max_coord"""
    for i in range(marker_coord + 1, max_coord):
        yield i

def count_continuous(board, marker, x_iter, y_iter):
    """iterates through x_iter and y_iter for coordinates to count the continuous chain of the same marker along line"""
    counter = 0
    try:
        while True:
            # checks the next coordinate for if it's the right marker. otherwise breaks out of loop.
            if board[next(y_iter)][next(x_iter)] == marker:
                counter += 1
            else:
                break
    except StopIteration:
        return counter
    return counter

def check_win(board, board_len, win_len, x_marker, y_marker):
    """for given board and most recently placed marker, see if it has caused a win"""
    marker = board[y_marker][x_marker]
    horizontal_counter, vertical_counter, diag1_counter, diag2_counter = 1, 1, 1, 1

    # saves the bounds for easy reference later
    x_min = -1 if -1 > x_marker - win_len else x_marker - win_len
    x_max = board_len if board_len < x_marker + win_len else x_marker + win_len
    y_min = -1 if -1 > y_marker - win_len else y_marker - win_len
    y_max = board_len if board_len < y_marker + win_len else y_marker + win_len

    # left, right. returns true if horizontally won
    horizontal_counter += count_continuous(board, marker, left_iter(x_marker, x_min), const_gen(y_marker))
    horizontal_counter += count_continuous(board, marker, right_iter(x_marker, x_max), const_gen(y_marker))
    if horizontal_counter >= win_len:
        return True

    # up, down. returns true if vertically won
    vertical_counter += count_continuous(board, marker, const_gen(x_marker), left_iter(y_marker, y_min))
    vertical_counter += count_continuous(board, marker, const_gen(x_marker), right_iter(y_marker, y_max))
    if vertical_counter >= win_len:
        return True

    # diag1 - bottom left to top right.
    diag1_counter += count_continuous(board, marker, left_iter(x_marker, x_min), right_iter(y_marker, y_max))
    diag1_counter += count_continuous(board, marker, right_iter(x_marker, x_max), left_iter(y_marker, y_min))
    if diag1_counter >= win_len:
        return True

    # diag2 - top left to bottom right.
    diag2_counter += count_continuous(board, marker, left_iter(x_marker, x_min), left_iter(y_marker, y_min))
    diag2_counter += count_continuous(board, marker, right_iter(x_marker, x_max), right_iter(y_marker, y_max))
    if diag2_counter >= win_len:
        return True

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
        if check_win(self.board, self.board_len, self.win_len, x_coord, y_coord):
            print('\n\nWIN!!!!!!!!!!\n\n')

    def on_click(self, x, y):
        """plays a marker on click"""
        if self.window_min < x < self.window_max and self.window_min < y < self.window_max:
            x_coord = int((x - self.window_min) // self.grid_width)
            y_coord = int(self.board_len - 1 - ((y - self.window_min) // self.grid_width))
            self.play(x_coord, y_coord)


if __name__ == '__main__':
    game = TicTacToe(3, 3, 600)
    win = pyglet.window.Window(600, 600)
    print(game)

    @win.event()
    def on_draw():
        win.clear()
        game.batch.draw()

    @win.event()
    def on_mouse_press(x, y, button, modifiers):
        game.on_click(x, y)

    pyglet.app.run()
