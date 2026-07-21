from automation.task_queue import TaskQueue


class Workflow:

    def __init__(self):
        self.queue = TaskQueue()

    def add_task(self, name, func, *args, **kwargs):
        self.queue.add(name, func, *args, **kwargs)

    def run(self):
        print("========== WORKFLOW START ==========")

        while not self.queue.empty():

            task = self.queue.next()

            print(f"Running : {task['name']}")

            try:
                task["func"](*task["args"], **task["kwargs"])
                print("Success\n")

            except Exception as e:
                print(f"Failed : {e}\n")

        print("=========== WORKFLOW END ===========")