import time
from mpi4py import MPI

from board import Board
from board import BoardTag
from taskPool import TaskPool
from messageType import MessageType
from log import Log


comm = MPI.COMM_WORLD
comm_size = comm.Get_size()


class Master():

    def __init__(self, measuring):
        self._measuring = measuring
        self._board = Board()
        self._taskPool = TaskPool()
        self._log = Log('Master')
        self._log.debug('init')

    def work(self):
        self._log.debug('work')

        while self._move_cycle(): pass

        self._stop_workers()

    def _move_cycle(self):
            self._taskPool = TaskPool()

            self._print('CPU is thinking...')
            start_time = time.time()

            # Broadcast board data
            self._broadcast_board()

            # Send tasks to workers on request
            self._serve_tasks()

            column_quality = self._taskPool.calculate_quality()
            best_column_move = max(enumerate(column_quality), key=lambda x: x[1])[0]

            end_time = time.time() - start_time
            print (end_time if self._measuring else 'Thinking done in: %f\n' % end_time)

            # Print column quality
            for idx, quality in enumerate(column_quality):
                self._print('Column %d quality: %f' % (idx+1, quality))
            self._print('Best column move %d\n' % (best_column_move+1))

            # In case we are just measuring 1st move by CPU
            if self._measuring:
                self._stop_workers()
                return False

            self._board.play_move(BoardTag.CPU, best_column_move)
            self._board.print_board()
            self._print('')

            if self._board.check_if_finished(best_column_move)[0]:
                self._print_winner(BoardTag.CPU)
                return False

            human_column_move = self._human_turn()
            if human_column_move == -1: return False
            if self._board.check_if_finished(human_column_move)[0]:
                self._print_winner(BoardTag.HUMAN)
                return False

            return True

    def _broadcast_board(self):
        message = {'type': MessageType.BOARD_DATA, 'board': self._board}
        for x in xrange(1, comm_size):
            self._log.debug('BOARD_DATA to %d' % x)
            comm.send(message, dest=x)

    def _serve_tasks(self):
        active_workers = comm_size - 1
        finished = False
        while not finished:
            self._log.debug('waiting for DATA_REQUEST')
            # Send tasks upon request
            message_status = MPI.Status()
            message = comm.recv(source=MPI.ANY_SOURCE, status=message_status)
            message_source = message_status.Get_source()

            if message['type'] == MessageType.TASK_REQUEST:
                self._log.debug('receives TASK_REQUEST from %d' % message_source)
                task = self._taskPool.next_task()
                if task is not None:
                    message = {'type': MessageType.TASK_DATA, 'task': task}
                    self._log.debug('sends TASK_DATA to %d' % message_source)
                    comm.send(message, dest=message_source)

                else:
                    self._log.debug('sends WAIT to %d' % message_source)
                    comm.send({'type': MessageType.WAIT}, dest=message_source)
                    active_workers -= 1
                    if active_workers == 0:
                        finished = True

            elif message['type'] == MessageType.TASK_RESULT:
                self._log.debug('receives TASK_RESULT from %d' % message_source)
                self._taskPool.update_task(message['task'], message['result'])

    def _stop_workers(self):
        for x in xrange(1, comm_size):
            self._log.debug('STOP to %d' % x)
            comm.send({'type': MessageType.STOP}, dest=x)

    def _human_turn(self):
        # Take player move
        human_input = self._read_human_input()-1
        if human_input == -1:
            print 'Human gave up! CPU WINS!'
            return human_input

        # play
        self._board.play_move(BoardTag.HUMAN, human_input)
        self._board.print_board()
        print

        return human_input

    @staticmethod
    def _read_human_input():
        while True:
            print 'Human move:',
            human_input = raw_input()
            try:
                human_input = int(human_input)
                if human_input < 0 or human_input > 7:
                    raise ValueError()
                return human_input
            except ValueError:
                print 'Invalid input! Enter 1-7 for column or 0 for end'

    @staticmethod
    def _print_winner(player):
        player_label = 'CPU' if player == BoardTag.CPU else 'Human'
        print '%s won!' % player_label

    def _print(self, message):
        if not self._measuring:
            print message