import cmd


class RevuREPL(cmd.Cmd):

    def __init__(self, repo):
        self.repo = repo
        self.reviews = repo.reviews()
        super(RevuREPL, self).__init__()

    @property
    def prompt(self):
        return "({}) λ ".format(self.repo.name)

    def do_next(self, line):
        try:
            review = next(self.reviews)
        except StopIteration:
            return True
        print(review.summary())

    def do_EOF(self, line):
        return True
