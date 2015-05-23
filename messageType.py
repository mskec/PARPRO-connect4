class MessageType():
    BOARD_DATA, TASK_REQUEST, TASK_DATA, WAIT, TASK_RESULT = range(5)

    """ BOARD_DATA: {type, board} """
    """ TASK_REQUEST: {type} """
    """ TASK_DATA: {type, task} """
    """ WAIT: {type} """
    """ TASK_RESULT: {type, task, result} """
