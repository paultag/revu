from revu.session import SessionREPL

session = SessionREPL([("paultag/fnord", "/home/tag/dev/local/fnord")])
session.cmdloop()
