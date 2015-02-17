from revu.session import SessionREPL
from revu.queue import Project


def main():
    session = SessionREPL(list(Project.from_config("~/.revu.conf")))
    session.cmdloop()
