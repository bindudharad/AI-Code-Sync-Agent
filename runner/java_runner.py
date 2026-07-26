from runner.terminal import Terminal


class JavaRunner:

    def __init__(self, project):

        self.terminal = Terminal(project)

    def build(self):

        return self.terminal.run(
            "mvn clean install"
        )

    def run(self):

        return self.terminal.run(
            "mvn spring-boot:run"
        )

    def test(self):

        return self.terminal.run(
            "mvn test"
        )