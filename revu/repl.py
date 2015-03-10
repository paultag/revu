# Copyright (c) 2015 Paul Tagliamonte <paultag@debian.org>
#
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
        """
        Show a diff of the Pull Request, and open it with vim.
        """
        with tempfile.NamedTemporaryFile(suffix='.revu.diff') as temp:
            with open(temp.name, 'w') as fd:
                fd.write(self.review.diff())
            subprocess.call(['vimdiff', temp.name])

    def do_log(self, line):
        """
        Show the git log. More exactly, show the log in a graphical
        format that's kinda fun.
        """
        subprocess.call([
            'git', '-C', self.repo.path,
            'log', '--graph', '--oneline',
            "{}...pr/{}".format(self.review.pr.base.ref, self.review.pr.number),
        ])

    def do_comments(self, line):
        """
        Show pull request comments.
        """
        for comment in self.review.comments():
            print(comment)

    def do_comment(self, line):
        """
        Write a new comment.
        """
        if line.strip() != "":
            self.review.comment(line)
            return

        with tempfile.NamedTemporaryFile(suffix='.revu.md') as temp:
            subprocess.call(['vim', temp.name])
            with open(temp.name, 'r') as fd:
                self.review.comment(fd.read())


    def do_merge(self, line):
        """
        Merge the pull request into the target branch
        """
        self.review.merge()

    def do_push(self, line):
        """
        Push the target branch to the remote.
        """
        self.review.push()
        return True

    def do_skip(self, line):
        """
        Skip the branch.
        """
        return True

    def do_EOF(self, line):
        print("")
        raise StopIteration("Stawp")

    do_exit = do_EOF
    do_s = do_skip
    do_c = do_comment
    do_d = do_diff
    do_l = do_log
