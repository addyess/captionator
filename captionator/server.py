import pathlib
from bottle import Bottle, run, request, redirect, response
from bottle import jinja2_view as view
from bottle import TEMPLATE_PATH

TEMPLATE_PATH.insert(0, pathlib.Path(__file__).parent / "views")


class WebUX:
    def __init__(self, db, config):
        self._app = Bottle()
        self._config = config
        self._db = db
        self._route()

    def _route(self):
        self._app.route('/', method='GET', callback=self._root)
        self._app.route('/update', method='POST', callback=self._update)

    @view('root.j2')
    def _root(self):
        return dict(
            available_captions=self._db.captions()
        )

    def _update(self):
        try:
            user_req = request.json
        except:
            response.status = 400
            return
        return {}

    def main(self):
        run(self._app, host='0.0.0.0', port=self._config.http_port)
