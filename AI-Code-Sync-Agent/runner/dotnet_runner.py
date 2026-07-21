from runner.terminal import Terminal


class DotNetRunner:

    def __init__(self, project):

        self.terminal = Terminal(project)

    def restore(self):

        return self.terminal.run(
            "dotnet restore"
        )

    def build(self):

        return self.terminal.run(
            "dotnet build"
        )

    def run(self):

        return self.terminal.run(
            "dotnet run"
        )

    def test(self):

        return self.terminal.run(
            "dotnet test"
        )