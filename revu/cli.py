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

        repl = RevuREPL(repo=repo, session=tmux)
        repl.cmdloop()

    return _(*sys.argv[1:])
