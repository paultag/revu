# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

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

    def do_log(self, line):
        subprocess.call([
            'git', '-C', self.repo.path,
            'log', '--graph', '--oneline',
            "{}...pr/{}".format(self.review.pr.base.ref, self.review.pr.number),
        ])

    def do_comments(self, line):
        for comment in self.review.comments():
            print(comment)

    def do_comment(self, line):
        self.review.comment(line)

    def do_skip(self, line):
        return True

    def do_EOF(self, line):
        print("")
        raise StopIteration("Stawp")

    do_exit = do_EOF
