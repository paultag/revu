from .git import GitRepo
from ..repo import Review

import github3
import os


class GitHubReview(Review):
    def __init__(self, *, repo, pr):
        self.repo = repo
        self.pr = pr
        self.issue = repo.issue(pr.number)

    def summary(self):
        return """\
Pull Request: #{pr.number}
Assigned to:  {pr.assignee}
From:         @{pr.user.login}
Title:        {pr.title}
State:        {pr.state}
Comments:     {pr.review_comments_count}/{issue.comments}
URL:          {pr.html_url}

{pr.body}
        """.format(pr=self.pr, repo=self.repo, issue=self.issue)

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
        self.user = "paultag"  # XXX: Fix?
        self.github = github3.GitHub(self.user, self.get_key())
        self.github_repo = self.github.repository(*self.repo.split("/", 1))

    def get_key(self):
        key = os.environ.get("GITHUB_API_KEY", None)
        if key:
            return key
        try:
            with open(os.path.expanduser("~/.github.key"), 'r') as fd:
                key = fd.read().strip()
        except IOError:
            raise ValueError("No key defined")
        return key

    def reviews(self):
        for review in self.github_repo.iter_pulls():
            yield GitHubReview(pr=review, repo=self.github_repo)

    def review(self, review):
        pass
