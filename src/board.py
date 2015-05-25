

class BoardTag:
    EMPTY, CPU, HUMAN = ['_', 'c', 'h']


class Board():
    COLUMN_NUMBER = 7
    INIT_ROW_NUMBER = 6

    # Initial Board is 6 rows and 7 columns
    def __init__(self):
        self._board = []
        for i in xrange(Board.INIT_ROW_NUMBER):
            self._add_row()

    def _add_row(self):
        self._board.append([BoardTag.EMPTY] * Board.COLUMN_NUMBER)

    @staticmethod
    def _check_column_access(column, raise_exception=True):
        if column < 0 or column >= Board.COLUMN_NUMBER:
            if raise_exception:
                raise ValueError('Column %d must be between [0, %d]'.format(column, Board.COLUMN_NUMBER))
            else:
                return False
        return True

    def _check_row_access(self, row, raise_exception=True):
        if row < 0 or row > len(self._board)-1:
            if raise_exception:
                raise ValueError('Row %d must be between [0, %d]'.format(row, len(self._board)-1))
            else:
                return False
        return True


    """ Public methods """
    def play_move(self, current_player_tag, column):
        self._check_column_access(column)

        # if last row is played, add another row
        if self._board[len(self._board)-1][column] != BoardTag.EMPTY:
            self._add_row()

        for board_row in self._board:
            if board_row[column] == BoardTag.EMPTY:
                board_row[column] = current_player_tag
                break

    def reverse_move(self, last_played_column):
        self._check_column_access(last_played_column)

        top_row_idx = self._get_top_row(last_played_column)
        if top_row_idx is None:
            raise AssertionError('Cannot reverse move on column %d'.format(last_played_column))

        # TODO remove row if possible
        self._board[top_row_idx][last_played_column] = BoardTag.EMPTY

    def check_if_finished(self, last_played_column):
        self._check_column_access(last_played_column)

        # Check if there is anything in last_column_move
        last_played_row = self._get_top_row(last_played_column)
        if last_played_row is None:
            return False, BoardTag.EMPTY

        last_player_tag = self._board[last_played_row][last_played_column]
        # Check all directions
        if Board._check4_in_list(self._get_row_tags(last_played_row, last_played_column), last_player_tag) is True or \
                Board._check4_in_list(self._get_column_tags(last_played_row, last_played_column), last_player_tag) is True or \
                Board._check4_in_list(self._get_diagonal_tags(last_played_row, last_played_column), last_player_tag) is True or \
                Board._check4_in_list(self._get_diagonal_tags(last_played_row, last_played_column, True), last_player_tag) is True:
            return True, last_player_tag
        else:
            return False, BoardTag.EMPTY

    def print_board(self):
        # Column numbers
        for i in xrange(Board.COLUMN_NUMBER):
            print (i+1),
        print

        # Separator row
        print '-' * (Board.COLUMN_NUMBER * 2 - 1)

        # Board
        for board_row in reversed(self._board):
            for column in board_row:
                print column,
            print

    """ Helper methods for board checking """
    def _get_row_tags(self, row, column):
        board_tags = []
        for i in xrange(column - 3, column + 4):
            if self._check_column_access(i, False):
                board_tags.append(self._board[row][i])
        return board_tags

    def _get_column_tags(self, row, column):
        board_tags = []
        for i in xrange(row - 3, row + 4):
            if self._check_row_access(i, False):
                board_tags.append(self._board[i][column])
        return board_tags

    def _get_diagonal_tags(self, row, column, right_diagonal=False):
        board_tags = []

        row_iter = [3, 2, 1, 0, -1, -2, -3]
        col_iter = [-3, -2, -1, 0, 1, 2, 3]

        if right_diagonal:
            row_iter = col_iter

        for i in xrange(len(row_iter)):
            row_i = row_iter[i] + row
            col_i = col_iter[i] + column
            if self._check_row_access(row_i, False) and self._check_column_access(col_i, False):
                board_tags.append(self._board[row_i][col_i])

        return board_tags

    def _get_top_row(self, column):
        for idx, board_row in enumerate(reversed(self._board)):
            if board_row[column] != BoardTag.EMPTY:
                return len(self._board) - idx - 1
        return None

    @staticmethod
    def _check4_in_list(tag_list, player_tag):
        # TODO use reduce
        count = 0
        for tag in tag_list:
            if count == 4:
                break
            if player_tag == tag:
                count += 1
            else:
                count = 0
        return count == 4
