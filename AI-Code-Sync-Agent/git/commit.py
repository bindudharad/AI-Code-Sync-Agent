from git.git_manager import GitManager


class GitCommit:

    def __init__(self, project):

        self.git = GitManager(project)

    def commit(self, message):

        self.git.add_all()

        return self.git.run(

            f'git commit -m "{message}"'

        )