import tmuxp
from ..session import Session


class TmuxSession(Session):
    def __init__(self, session_name):
        self.session_name = session_name
        self.server = tmuxp.Server()
        try:
            self.session = self.server.new_session(
                session_name=self.session_name,
                kill_session=False,
                detatch=True,
            )
        except tmuxp.exc.TmuxSessionExists:
            self.session = self.server.findWhere({
                "session_name": session_name
            })

    def _clean(self):
        for window in self.session.windows:
            if window.get('window_name') == 'revu-review':
                window.kill_window()

    def review(self, path):
        self._clean()
        return self.session.new_window(
            window_name="revu-review",
            start_directory=path,
            attach=True)
