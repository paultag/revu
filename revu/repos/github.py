from .git import GitRepo
from ..repo import Review

from sh import git
import github3
import os
import sh


class GitHubReview(Review):
    def __init__(self, *, repo, git, pr):
        self.repo = repo
        self.pr = pr
        self.git = git
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

{body}
        """.format(
            pr=self.pr,
            repo=self.repo,
            issue=self.issue,
            body="\n".join(self._display(self.issue.body, " |  ")))

    def comment(self, body):
        return self.issue.create_comment(body=body)

    def _display(self, text, indent, align=80):
        text = text.strip("\n")
        if len(text) < align:
            line = indent + text
            yield line
            return
        idex = text.find("\n", 0, align)
        if idex == -1:
            idex = align
        line = indent + text[:idex]
        yield line
        yield from self._display(text[idex:], indent, align=align)


    def comments(self):
        for comment in self.issue.iter_comments():
            yield """\
From: {comment.user.login} at {comment.updated_at:%Y-%m-%d %I:%M%p %z}

{body}
            """.format(
                comment=comment,
                issue=self.issue,
                body="\n".join(self._display(comment.body, " |  "))
            )

    def diff(self):
        diff = self.git.diff(self.pr.base.ref)
        return diff.patch

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
            yield GitHubReview(pr=review, git=self.git, repo=self.github_repo)

    def review(self, review):
        head = review.pr.head
        base = review.pr.base
        target = base.ref  # Great; we just need to do the checkout now.

        oname = 'refs/remotes/origin/{}'.format(target)
        oref = self.git.lookup_reference(oname)

        review.branch = "pr/{}".format(review.pr.number)

        try:
            rref = self.git.lookup_reference('refs/heads/{}'.format(
                review.branch
            ))
            self.git.checkout(oname)
            rref.delete()
        except KeyError:
            pass

        gc = git.bake(C=self.path)
        gc.fetch("origin", "refs/pull/{no}/head:{branch}".format(
            no=review.pr.number,
            branch=review.branch,
        ))
        rref = self.git.lookup_reference('refs/heads/{}'.format(
            review.branch
        ))

        self.git.checkout(rref)
        try:
            gc.merge(oname)
        except sh.ErrorReturnCode_1:
            return False
        return True
