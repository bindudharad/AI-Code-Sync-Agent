from git.git_manager import GitManager


class GitRollback:

    def __init__(self, project):

        self.git = GitManager(project)

    def last_commit(self):

        return self.git.run(

            "git reset --hard HEAD~1"

        )

    def discard_changes(self):

        return self.git.run(

            "git restore ."

        )