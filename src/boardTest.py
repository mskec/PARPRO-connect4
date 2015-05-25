import unittest

from board import Board
from board import BoardTag


class BoardTest(unittest.TestCase):

    def setUp(self):
        self._board = Board()

    def test__get_top_row(self):
        self._board.play_move(BoardTag.CPU, 0)
        self.assertEqual(self._board._get_top_row(0), 0)
        self._board.play_move(BoardTag.HUMAN, 0)
        self.assertEqual(self._board._get_top_row(0), 1)
        self.assertEqual(self._board._get_top_row(1), None)

    def test__check_column_access(self):
        self.assertTrue(self._board._check_column_access(0, False))
        self.assertTrue(self._board._check_column_access(6, False))
        self.assertFalse(self._board._check_column_access(-1, False))
        self.assertFalse(self._board._check_column_access(7, False))

    def test__check_row_access(self):
        self.assertTrue(self._board._check_row_access(0, False))
        self.assertTrue(self._board._check_row_access(5, False))
        self.assertFalse(self._board._check_row_access(-1, False))
        self.assertFalse(self._board._check_row_access(6, False))
        # Add moves to the same column to increase board row by 1
        for x in xrange(7):
            self._board.play_move(BoardTag.CPU, 0)
        self.assertTrue(self._board._check_row_access(6, False))

    def test_play_move(self):
        self._board.play_move(BoardTag.CPU, 0)
        self.assertEqual(self._board._board[0][0], BoardTag.CPU)
        self._board.play_move(BoardTag.HUMAN, 0)
        self.assertEqual(self._board._board[1][0], BoardTag.HUMAN)

    def test_reverse_move(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 1)
        self._board.play_move(BoardTag.CPU, 0)

        self._board.reverse_move(1)
        self.assertEqual(self._board._board[0][1], BoardTag.EMPTY)
        self.assertEqual(self._board._board[0][0], BoardTag.CPU)
        self.assertEqual(self._board._board[1][0], BoardTag.CPU)

        self._board.reverse_move(0)
        self.assertEqual(self._board._board[1][0], BoardTag.EMPTY)
        self.assertEqual(self._board._board[0][0], BoardTag.CPU)

    def test__get_row_tags_1(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 1)
        self._board.play_move(BoardTag.CPU, 2)
        self._board.play_move(BoardTag.CPU, 3)

        row_tags = self._board._get_row_tags(0, 0)
        self.assertSequenceEqual(row_tags, [BoardTag.CPU, BoardTag.HUMAN, BoardTag.CPU, BoardTag.CPU])

    def test__get_row_tags_2(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.CPU, 6)
        self._board.play_move(BoardTag.CPU, 3)

        row_tags = self._board._get_row_tags(0, 3)
        self.assertSequenceEqual(row_tags, [BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY,
                                            BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY,  BoardTag.CPU])

    def test__get_column_tags_1(self):
        self._board.play_move(BoardTag.CPU, 0)
        column_tags = self._board._get_column_tags(0, 0)
        self.assertSequenceEqual(column_tags, [BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.EMPTY])

    def test__get_column_tags_2(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 0)
        column_tags = self._board._get_column_tags(3, 0)
        self.assertSequenceEqual(column_tags, [BoardTag.CPU, BoardTag.HUMAN, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.EMPTY])

    def test__get_diagonal_tags_left_1(self):
        self._board.play_move(BoardTag.CPU, 6)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)

        left_diagonal_tags = self._board._get_diagonal_tags(0, 6)
        self.assertSequenceEqual(left_diagonal_tags, [BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.CPU])

    def test__get_diagonal_tags_left_2(self):
        self._board.play_move(BoardTag.CPU, 6)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)

        left_diagonal_tags = self._board._get_diagonal_tags(3, 3)
        self.assertSequenceEqual(left_diagonal_tags, [BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.CPU])

    def test__get_diagonal_tags_right_1(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)

        right_diagonal_tags = self._board._get_diagonal_tags(0, 0, True)
        self.assertSequenceEqual(right_diagonal_tags, [BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.CPU])

    def test__get_diagonal_tags_right_2(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.CPU, 3)

        right_diagonal_tags = self._board._get_diagonal_tags(3, 3, True)
        self.assertSequenceEqual(right_diagonal_tags, [BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY, BoardTag.CPU, BoardTag.EMPTY, BoardTag.EMPTY])

    def test__check4_in_row(self):
        test_row_1 = [BoardTag.CPU, BoardTag.CPU, BoardTag.CPU, BoardTag.CPU]
        self.assertTrue(Board._check4_in_list(test_row_1, BoardTag.CPU))

        test_row_2 = [BoardTag.EMPTY, BoardTag.CPU, BoardTag.CPU, BoardTag.CPU, BoardTag.CPU, BoardTag.EMPTY]
        self.assertTrue(Board._check4_in_list(test_row_2, BoardTag.CPU))

        test_row_3 = [BoardTag.CPU, BoardTag.CPU, BoardTag.EMPTY, BoardTag.CPU, BoardTag.CPU]
        self.assertFalse(Board._check4_in_list(test_row_3, BoardTag.CPU))

    def test_check_if_finished_row(self):
        self._board.play_move(BoardTag.CPU, 0)

        finished_1 = self._board.check_if_finished(0)
        self.assertFalse(finished_1[0])

        self._board.play_move(BoardTag.CPU, 1)
        self._board.play_move(BoardTag.CPU, 3)
        self._board.play_move(BoardTag.HUMAN, 1)
        self._board.play_move(BoardTag.CPU, 2)

        finished_2 = self._board.check_if_finished(2)
        self.assertTrue(finished_2[0])
        self.assertEqual(finished_2[1], BoardTag.CPU)

    def test_check_if_finished_column(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.CPU, 0)

        finished = self._board.check_if_finished(0)
        self.assertTrue(finished[0])
        self.assertEqual(finished[1], BoardTag.CPU)

    def test_check_if_finished_diagonal(self):
        self._board.play_move(BoardTag.CPU, 0)
        self._board.play_move(BoardTag.HUMAN, 1)
        self._board.play_move(BoardTag.CPU, 1)
        self._board.play_move(BoardTag.HUMAN, 2)
        self._board.play_move(BoardTag.HUMAN, 2)
        self._board.play_move(BoardTag.CPU, 2)

        finished_1 = self._board.check_if_finished(2)
        self.assertFalse(finished_1[0])

        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.HUMAN, 3)
        self._board.play_move(BoardTag.CPU, 3)

        finished_2 = self._board.check_if_finished(3)
        self.assertTrue(finished_2[0])
        self.assertEqual(finished_2[1], BoardTag.CPU)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BoardTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
