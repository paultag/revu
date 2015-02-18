import subprocess
import tempfile
import cmd


class RevuREPL(cmd.Cmd):

    def __init__(self, *, repo, review, session):
        self.repo = repo
        self.session = session
        self.review = review
        super(RevuREPL, self).__init__()

    @property
    def intro(self):
        self.session.review(self.repo.path)
        return self.review.summary()

    @property
    def prompt(self):
        return "({}) λ ".format(self.repo.name)

    def do_diff(self, line):
        with tempfile.NamedTemporaryFile(suffix='task') as temp:
            with open(temp.name, 'w') as fd:
                fd.write(self.review.diff())
            subprocess.call(['vimdiff', temp.name])

    def do_comment(self, line):
        self.review.comment(line)

    def do_skip(self, line):
        return True

    def do_EOF(self, line):
        return True
