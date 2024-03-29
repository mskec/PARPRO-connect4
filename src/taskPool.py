

class TaskPool():

    def __init__(self):
        self._tasks = {}

        for x in xrange(0, 7):
            for y in xrange(0, 7):
                self._tasks[(x, y)] = None

    def next_task(self):
        for task_key, task_value in self._tasks.iteritems():
            if task_value is None:
                self._tasks[task_key] = True
                return task_key
        return None

    def update_task(self, task, value):
        self._tasks[task] = value

    def calculate_quality(self):
        quality = [0] * 7
        for task_key, task_value in self._tasks.iteritems():
            quality[task_key[0]] += task_value
        return map(lambda x: x / 7.0, quality)
