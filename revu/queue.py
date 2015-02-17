from sh import git
import sh

import os
import shutil
import tempfile
import contextlib
import configparser


class Queue:
    pass


class Project:
    def __init__(self, name, repo, path):
        self.name = name
        self.repo = repo
        self.path = path

    @classmethod
    def from_config(cls, path):
        config = configparser.ConfigParser()
        config.read([os.path.expanduser(path)])
        for section, name in ((config[x], x) for x in config.sections()):
            yield Project(name=name, **section)


class PullRequest:  # Implied this is a Git repo
    def __init__(self, number, title, body, origin, oref, remote, rref):
        self.number = number
        self.title = title
        self.body = body
        self.origin = origin
        self.oref = oref
        self.remote = remote
        self.rref = rref

    def __str__(self):
        return "<PullRequest: {remote}/{rref} -> {origin}/{oref}".format(
            **self.__dict__
        )


class Review:
    def __init__(self, repo, pullrequest):
        self.pr = pullrequest
        self.repo = repo
        self._git = None

    def log(self, message):
        print(message)

    def checkout(self):
        self.log("Cloning origin; please wait")

        self._git = git.bake(C=self.repo)
        self._git.checkout(self.pr.oref)

        self.log("Pulling down PR {number}".format(number=self.pr.number))
        # This is where we get GitHub specific; please fix this
        # for future review plugins.
        self._git.fetch(
            "origin",
            "refs/pull/{number}/head:pr/{number}".format(number=self.pr.number))

        self.log("Checking out")
        self._git.checkout("pr/{number}".format(number=self.pr.number))
        self.log("Merging root ref in")
        conflict = False

        try:
            self._git.merge(self.pr.oref)
        except sh.ErrorReturnCode as e:
            self.log("Merge conflict! Yikes!")
            self.log(e.stdout.decode('utf-8'))
            conflict = True

        return conflict

    def merge(self):
        self.log("Checking out origin ref")
        self._git.checkout(self.pr.oref)
        self.log("Merging in the PR branch")
        self._git.merge("pr/{number}".format(number=self.pr.number))
        self.log("Done.")

    def push(self):
        self._git.push("origin", self.pr.oref)

    def comment(self, message):
        issue = self.pr._repo.issue(self.pr._pr.number)
        comment = issue.create_comment(message)
