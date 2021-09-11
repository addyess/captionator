import json
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
        self._app.route('/captions.json', method='GET', callback=self._captions)
        self._app.route('/update/<id:int>', method='GET', callback=self._update)
        self._app.route('/update/<id:int>', method='POST', callback=self._update)

    @view('root.j2')
    def _root(self):
        return dict()

    def _captions(self):
        return json.dumps(self._db.captions(views=('name', 'id', 'location')))

    @view('update.j2')
    def _update(self, id):
        if request.forms:
            self._db.set_captions(id, request.forms)
        captions = self._db.captions(filters={"id": id})
        if len(captions) == 1:
            return captions[0]
        redirect("/")

    def main(self):
        run(self._app, host='0.0.0.0', port=self._config.http_port)
