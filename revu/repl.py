import subprocess
import tempfile
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
            self.review = next(self.reviews)
        except StopIteration:
            return True
        is_clean = self.repo.review(self.review)
        if not is_clean:
            print("merging went poorly; please resolve merge conflict")
        print(self.review.summary())

    def do_diff(self, line):
        if self.review is None:
            print("Take a review first, homie! (type `next`)")
            return

        with tempfile.NamedTemporaryFile(suffix='task') as temp:
            with open(temp.name, 'w') as fd:
                fd.write(self.review.diff())

            subprocess.call(['vimdiff', temp.name])

    def do_comment(self, line):
        if self.review is None:
            print("Take a review first, homie! (type `next`)")
            return
        self.review.comment(line)

    def do_EOF(self, line):
        return True
