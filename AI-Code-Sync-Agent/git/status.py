from git.git_manager import GitManager


class GitStatus:

    def __init__(self, project):

        self.git = GitManager(project)

    def status(self):

        return self.git.run(

            "git status"

        )

    def log(self):

        return self.git.run(

            "git log --oneline"

        )

    def diff(self):

        return self.git.run(

            "git diff"

        )