from revu.queues.github import GithubQueue
from revu.queue import Review

import readline
import cmd


class Session:
    def __init__(self, projects):
        self.projects = projects
        self.project_map = {x.name: x for x in self.projects}

    def get(self, project):
        return self.project_map[project]

    def pulls(self, project):
        if isinstance(project, str):
            project = self.project_map[project]

        gq = GithubQueue()
        for changeset in gq.pulls([project.repo]):
            yield Review(project.path, changeset)


class TmuxController:
    def __init__(self, session_name):
        self.session_name = session_name


class SessionREPL(cmd.Cmd):
    def __init__(self, projects):
        self.projects = projects
        self.session = Session(self.projects)
        self.review = None
        self.project = None
        self.prs = []

        super(SessionREPL, self).__init__()

    @property
    def prompt(self):
        ps1 = ""

        if self.project:
            ps1 += "({}) ".format(self.project.repo)

        if self.review:
            ps1 += "#{} ".format(self.review.pr.number)

        ps1 += "λ "
        return ps1

    def do_workon(self, line):
        self.project = self.session.get(line)

    do_w = do_workon

    def do_prs(self, line):
        if self.project is None:
            print("Please select a project with `workon` first.")
            return
        self.prs = list(self.session.pulls(self.project))

        print("Open Pull Requests")
        print("==================")
        for i, pr in enumerate(self.prs):
            print("{}) - GH #{pr.number} - {pr.title}".format(i, pr=pr.pr))

    def do_review(self, line):
        self.review = self.prs[int(line)]
        mc = self.review.checkout()
        if mc:
            print("Euch, there was a merge conflict.")
        print("Ready for human intervention. - {}".format(self.review.repo))

    do_r = do_review

    def do_comment(self, line):
        if self.review is None:
            print("Need to be on a review")
            return
        self.review.comment(line)

    def do_list(self, line):
        print("Known projects")
        print("==============")
        for project in self.projects:
            print("{project.name}".format(project=project))
        print("")

    do_l = do_list

    def do_EOF(self, line):
        return True
