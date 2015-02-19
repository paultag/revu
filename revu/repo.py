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


class Repo(object):

    def is_clean(self):
        """
        Is this method clean (ready to be used to do PR review; no unstaged
        changes)
        """
        raise NotImplementedError("Implement me")

    def restore(self):
        raise NotImplementedError("Implement me")

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


class Review(object):

    def comment(self):
        """
        Dispatch a comment to this review submitter
        """
        raise NotImplementedError("Implement me")

    def diff(self):
        """
        View the changeset
        """
        raise NotImplementedError("Implement me")

    def merge(self):
        """
        Preform the merge
        """
        raise NotImplementedError("Implement me")

    def push(self):
        """
        Do the push
        """
        raise NotImplementedError("Implement me")
