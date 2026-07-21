from collections import deque


class TaskQueue:

    def __init__(self):

        self.tasks = deque()

    def add(self, name, func, *args, **kwargs):

        self.tasks.append({

            "name": name,

            "func": func,

            "args": args,

            "kwargs": kwargs

        })

    def next(self):

        return self.tasks.popleft()

    def empty(self):

        return len(self.tasks) == 0

    def size(self):

        return len(self.tasks)

    def clear(self):

        self.tasks.clear()