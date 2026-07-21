from runner.terminal import Terminal


class NodeRunner:

    def __init__(self, project):

        self.terminal = Terminal(project)

    def install(self):

        print("Installing npm packages...")

        return self.terminal.run(
            "npm install"
        )

    def build(self):

        print("Building project...")

        return self.terminal.run(
            "npm run build"
        )

    def start(self):

        print("Starting project...")

        return self.terminal.run(
            "npm run dev"
        )

    def test(self):

        return self.terminal.run(
            "npm test"
        )