import readline
import cmd


class Session:
    def __init__(self, projects):
        self.projects = projects

    def pulls(self):
        for repo, path in self.projects:
            yield from self._project_pulls(repo, path)

    def _project_pulls(self, repo, path):
        gq = GithubQueue()
        for changeset in gq.pulls([repo]):
            yield Review(path, changeset)


class SessionREPL(cmd.Cmd):
    def __init__(self, projects):
        self.projects = projects
        self.session = Session(self.projects)
        super(SessionREPL, self).__init__()

    def do_EOF(self, line):
        return True
