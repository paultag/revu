import cmd


class RevuREPL(cmd.Cmd):

    def __init__(self, repo):
        self.repo = repo
        super(RevuREPL, self).__init__()

    @property
    def prompt(self):
        return "({}) λ ".format(self.repo.name)

    def do_hello(self, line):
        print("Hello!")

    def do_EOF(self, line):
        return True
