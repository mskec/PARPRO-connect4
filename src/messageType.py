

class MessageType():
    BOARD_DATA, TASK_REQUEST, TASK_DATA, TASK_RESULT, WAIT, STOP = range(6)

    """ BOARD_DATA: {type, board} """
    """ TASK_REQUEST: {type} """
    """ TASK_DATA: {type, task} """
    """ TASK_RESULT: {type, task, result} """
    """ WAIT: {type} """
    """ STOP: {type} """
