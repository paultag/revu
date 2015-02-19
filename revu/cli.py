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

import configparser
import sys
import os

from revu.repos.github import GitHubRepo
from revu.sessions.tmux import TmuxSession
from revu.repl import RevuREPL


def main():
    def _(project):
        config = configparser.ConfigParser()
        config.read([os.path.expanduser(os.path.expanduser("~/.revu.conf"))])
        pdict = config[project]

        repo = GitHubRepo(name=project, **pdict)
        if not repo.is_clean():
            print("Yikes! The repo at {path} isn't clean for review.")
            print("Please stash any changes and push up unpushed work.")
            return

        tmux = TmuxSession("revu")
        for review in repo.reviews():
            repl = RevuREPL(review=review, repo=repo, session=tmux)
            if not repo.review(review):
                print("merging went poorly; please resolve merge conflict")
            try:
                repl.cmdloop()
            except StopIteration:
                break
        # repo.restore()

    return _(*sys.argv[1:])
