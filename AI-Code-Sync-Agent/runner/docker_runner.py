from runner.terminal import Terminal


class DockerRunner:

    def __init__(self, project):

        self.terminal = Terminal(project)

    def build(self):

        return self.terminal.run(
            "docker compose build"
        )

    def up(self):

        return self.terminal.run(
            "docker compose up"
        )

    def down(self):

        return self.terminal.run(
            "docker compose down"
        )