from mpi4py import MPI
from board import Board
from board import BoardTag
from taskPool import TaskPool
from messageType import MessageType

comm = MPI.COMM_WORLD
comm_size = comm.Get_size()


class Master():

    def __init__(self):
        print 'Master: init'
        self._board = Board()
        self._taskPool = TaskPool()

    def work(self):
        print 'Master: work'

        while True:
            # TODO Start timing

            # Broadcast board data
            message = {'type': MessageType.BOARD_DATA, 'board': self._board}
            for x in xrange(1, comm_size):
                print 'Master: sends BOARD_DATA to %d' % x
                comm.send(message, dest=x)

            active_workers = comm_size - 1
            finished = False
            while not finished:
                print 'Master: waiting for DATA_REQUEST'
                # Send tasks upon request
                message_status = MPI.Status()
                message = comm.recv(source=MPI.ANY_SOURCE, status=message_status)
                message_source = message_status.Get_source()

                if message['type'] == MessageType.TASK_REQUEST:
                    print 'Master: receives TASK_REQUEST from %d' % message_source
                    task = self._taskPool.next_task()
                    if task is not None:
                        message = {'type': MessageType.TASK_DATA, 'task': task}
                        print 'Master: sends TASK_DATA to %d' % message_source
                        comm.send(message, dest=message_source)

                    else:
                        active_workers -= 1
                        if active_workers == 0:
                            finished = True
                            print 'Master: sends WAIT to %d' % message_source
                            comm.send({'type': MessageType.WAIT}, dest=message_source)

                elif message['type'] == MessageType.TASK_RESULT:
                    print 'Master: receives TASK_RESULT from %d' % message_source
                    self._taskPool.update_task(message['task'], message['result'])

            # All tasks finished

            column_quality = self._taskPool.calculate_quality()
            best_column_move = max(enumerate(column_quality), key=lambda x: x[1])[0]

            # TODO End timing

            # Print column quality
            for idx, quality in enumerate(column_quality):
                print 'Column %d quality: %f' % (idx+1, quality)
            print 'Best column move', best_column_move+1
            print

            self._board.play_move(BoardTag.CPU, best_column_move)
            self._board.print_board()

            # TODO check if CPU is the winner

            # TODO human move
            raw_input()
