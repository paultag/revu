from revu.session import SessionREPL
from revu.queue import Project

session = SessionREPL([
    Project("fnord", "paultag/fnord", "/home/tag/dev/local/fnord"),
])
session.cmdloop()
