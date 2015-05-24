from mpi4py import MPI
from board import Board
from board import BoardTag
from taskPool import TaskPool
from messageType import MessageType
from log import Log
import time

comm = MPI.COMM_WORLD
comm_size = comm.Get_size()


class Master():

    def __init__(self):
        self._board = Board()
        self._taskPool = TaskPool()
        self._log = Log('Master')
        self._log.debug('init')

    def work(self):
        self._log.debug('work')

        while True:
            self._taskPool = TaskPool()

            print 'CPU is thinking...'
            start_time = time.time()

            # Broadcast board data
            message = {'type': MessageType.BOARD_DATA, 'board': self._board}
            for x in xrange(1, comm_size):
                self._log.debug('BOARD_DATA to %d' % x)
                comm.send(message, dest=x)

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

            # All tasks finished

            column_quality = self._taskPool.calculate_quality()
            best_column_move = max(enumerate(column_quality), key=lambda x: x[1])[0]

            print 'Calculation done in:', (time.time() - start_time)
            print

            # Print column quality
            for idx, quality in enumerate(column_quality):
                print 'Column %d quality: %f' % (idx+1, quality)
            print 'Best column move', best_column_move+1
            print

            self._board.play_move(BoardTag.CPU, best_column_move)
            self._board.print_board()
            print

            # TODO check if CPU is the winner

            self._human_turn()
        # New cycle

    def _human_turn(self):
        # Take player move
        human_input = self._read_human_input()
        if human_input == 0:
            print 'Human gave up! CPU WINS!!!'

        # play
        self._board.play_move(BoardTag.HUMAN, human_input-1)
        self._board.print_board()
        print

        # eval
        # TODO result = self._check_game_end(player_input)

    @staticmethod
    def _read_human_input():
        while True:
            print 'Column:',
            human_input = raw_input()
            try:
                human_input = int(human_input)
                if human_input < 0 or human_input > 7:
                    raise ValueError()
                return human_input
            except ValueError:
                print 'Invalid input! Enter 1-7 for column or 0 for end'
