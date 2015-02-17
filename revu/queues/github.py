import os
import github3
from ..queue import Queue, PullRequest


class GithubQueue(Queue):
    def __init__(self):
        self._github = github3.GitHub("paultag", self.get_key())  # Erm.

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

    def _get_pr(self, user, repo):
        repo = self._github.repository(user, repo)
        requests = repo.iter_pulls()
        for request in requests:
            yield (request, repo)

    def _get_prs(self, repos):
        for repo in repos:
            yield from self._get_pr(*repo.split("/", 1))

    def pulls(self, repos):
        for pr, repo in self._get_prs(repos):

            remote = "git://github.com/{}/{}.git".format(*pr.head.repo)
            origin = "git://github.com/{}/{}.git".format(*pr.base.repo)

            npr = PullRequest(
                pr.number, pr.title, pr.body,
                origin,
                pr.base.ref,
                remote,
                pr.head.ref)

            npr._pr = pr
            npr._repo = repo  # XXX: Subclass
            yield npr
