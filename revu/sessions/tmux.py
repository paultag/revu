# Copyright (c) 2015 Paul Tagliamonte <paultag@debian.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

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
