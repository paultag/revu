from .git import GitRepo
from ..repo import Review


class GitHubReview(Review):

    def __init__(self, *, number):
        pass

    def comment(self):
        raise NotImplementedError("Implement me")

    def diff(self):
        raise NotImplementedError("Implement me")

    def merge(self):
        raise NotImplementedError("Implement me")

    def push(self):
        raise NotImplementedError("Implement me")


class GitHubRepo(GitRepo):

    def __init__(self, *, name, repo, path):
        super(GitHubRepo, self).__init__(path=path)
        self.repo = repo
        self.name = name

    def reviews(self):
        if False:
            yield

    def review(self, review):
        pass

