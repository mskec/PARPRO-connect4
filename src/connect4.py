from mpi4py import MPI

from master import Master
from worker import Worker


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
processor_name = MPI.Get_processor_name()

DEPTH = 7
MASTER_DEPTH = 2
WORKER_DEPTH = DEPTH - MASTER_DEPTH

if __name__ == '__main__':
    print 'hello %d on %s' % (rank, processor_name)
    comm.Barrier()

    if rank == 0:
        master = Master()
        master.work()
    else:
        worker = Worker(WORKER_DEPTH)
        worker.work()
