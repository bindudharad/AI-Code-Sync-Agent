from git.git_manager import GitManager


class GitBranch:

    def __init__(self, project):

        self.git = GitManager(project)

    def list(self):

        return self.git.run(

            "git branch"

        )

    def create(self, name):

        return self.git.run(

            f"git checkout -b {name}"

        )

    def switch(self, name):

        return self.git.run(

            f"git checkout {name}"

        )

    def delete(self, name):

        return self.git.run(

            f"git branch -D {name}"

        )