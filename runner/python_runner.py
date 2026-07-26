from runner.terminal import Terminal


class PythonRunner:

    def __init__(self, project):

        self.terminal = Terminal(project)

    def install(self):

        return self.terminal.run(
            "pip install -r requirements.txt"
        )

    def run(self):

        return self.terminal.run(
            "python main.py"
        )

    def test(self):

        return self.terminal.run(
            "pytest"
        )