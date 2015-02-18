from revu.repo import Repo, Review
from pygit2 import Repository


class GitRepo(Repo):

    def __init__(self, *, path):
        self.path = path
        self.git_repo = Repository('{}/.git'.format(self.path))

    def is_clean(self):
        diff = self.git_repo.diff()
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
