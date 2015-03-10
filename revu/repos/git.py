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

from revu.repo import Repo, Review
from pygit2 import Repository

import os


class GitRepo(Repo):

    def __init__(self, *, path):
        os.environ["REVU_GIT_PATH"] = path
        self.path = path
        self.git = Repository('{}/.git'.format(self.path))

    def is_clean(self):
        diff = self.git.diff()
        patch = diff.patch
        return patch is None

    def review(self, review):
        """
        Apply and checkout the review.
        """
        raise NotImplementedError("Implement me")

    def reviews(self):
        """
        Iterate over open reviews for this repo.
        """
        raise NotImplementedError("Implement me")

    def end(self):
        self.git.checkout("refs/heads/master")  # XXX: Fix this.
