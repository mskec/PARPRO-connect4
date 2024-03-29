from mpi4py import MPI

from board import Board
from board import BoardTag
from messageType import MessageType
from log import Log


comm = MPI.COMM_WORLD
rank = comm.Get_rank()


class Worker():

    def __init__(self, worker_depth):
        self._board = Board()       # This will be overwritten when BOARD_DATA is received
        self._worker_depth = worker_depth
        self._log = Log('Worker %d' % rank)
        self._log.debug('init')

    def work(self):
        self._log.debug('work')

        # Move cycle
        while True:
            message = comm.recv(source=0)

            if message['type'] == MessageType.BOARD_DATA:
                self._log.debug('receives BOARD_DATA')
                self._board = message['board']
            elif message['type'] == MessageType.STOP:
                self._log.debug('receives STOP')
                break

            # Start requesting tasks
            while self._request_task(): pass

    def _request_task(self):
        self._log.debug('sends TASK_REQUEST')
        message = {'type': MessageType.TASK_REQUEST}
        comm.send(message, dest=0)

        message = comm.recv(source=0)
        if message['type'] == MessageType.WAIT:
            self._log.debug('receives WAIT')
            return False

        task = message['task']
        self._log.debug('receives TASK_DATA {0}'.format(task))

        # CPU first move
        if self._play_cpu(task): return True

        # Human move
        if self._play_human(task): return True

        # Evaluate in depth
        result = self._evaluate(BoardTag.CPU, task[1], self._worker_depth)

        self._board.reverse_move(task[1])
        self._board.reverse_move(task[0])

        self._log.debug('sends TASK_RESULT')
        message = {'type': MessageType.TASK_RESULT, 'task': task, 'result': result}
        comm.send(message, dest=0)

        return True

    def _play_cpu(self, task):
        self._board.play_move(BoardTag.CPU, task[0])
        if self._board.check_if_finished(task[0])[0]:
            result = 1
            self._board.reverse_move(task[0])
            message = {'type': MessageType.TASK_RESULT, 'task': task, 'result': result}
            comm.send(message, dest=0)
            return True

    def _play_human(self, task):
        self._board.play_move(BoardTag.HUMAN, task[1])
        if self._board.check_if_finished(task[1])[0]:
            result = -1
            self._board.reverse_move(task[1])
            self._board.reverse_move(task[0])
            message = {'type': MessageType.TASK_RESULT, 'task': task, 'result': result}
            comm.send(message, dest=0)
            return True

    def _evaluate(self, current_player, last_played_column, depth):
        end_check = self._board.check_if_finished(last_played_column)
        if end_check[0]:
            return 1 if end_check[1] == BoardTag.CPU else -1

        if depth == 0: return 0

        total_result = 0.0
        all_child_loses = True
        all_child_wins = True
        for column in xrange(7):
            self._board.play_move(current_player, column)
            next_player = BoardTag.HUMAN if current_player == BoardTag.CPU else BoardTag.CPU
            result = self._evaluate(next_player, column, depth-1)
            self._board.reverse_move(column)

            if result > -1: all_child_loses = False
            if result != 1: all_child_wins = False
            if result == 1 and current_player == BoardTag.HUMAN: return 1   # if win is discovered before human turn
            if result == -1 and current_player == BoardTag.CPU: return -1   # if lost is discovered before cpu turn
            total_result += result

        return 1 if all_child_wins else -1 if all_child_loses else total_result / 7
