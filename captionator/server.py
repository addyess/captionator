import json
import pathlib
from bottle import Bottle, run, request, redirect, response, static_file
from bottle import jinja2_view as view
from bottle import TEMPLATE_PATH

from captionator.db import DB


VIEW_PATH = pathlib.Path(__file__).parent / "views"
IMG_PATH = VIEW_PATH / "img"
JS_PATH = VIEW_PATH / "js"
TEMPLATE_PATH.insert(0, VIEW_PATH)


class WebUX:
    def __init__(self, config):
        self._app = Bottle()
        self._config = config
        self._route()

    def _route(self):
        self._app.route('/', method='GET', callback=self._root)
        self._app.route('/img/<filename>', callback=self._static_img)
        self._app.route('/js/<filename>', callback=self._static_js)
        self._app.route('/captions.json', method='GET', callback=self._captions)
        self._app.route('/view/<id:int>', method='GET', callback=self._view)
        self._app.route('/add', method='GET', callback=self._add)
        self._app.route('/add', method='POST', callback=self._add_json)
        self._app.route('/update/<id:int>', method='GET', callback=self._update)
        self._app.route('/update/<id:int>', method='POST', callback=self._update_json)

    def _static_img(self, filename):
        return static_file(filename, root=IMG_PATH)

    def _static_js(self, filename):
        return static_file(filename, root=JS_PATH)

    @view('root.j2')
    def _root(self):
        return dict()

    @view('add.j2')
    def _add(self):
        return dict()

    @view('view.j2')
    def _view(self, id):
        db = DB(self._config)
        captions = db.captions(views=("text",), filters={"id": id})
        if len(captions) == 1:
            return captions[0]
        redirect("/")

    @view('update.j2')
    def _update(self, id):
        db = DB(self._config)
        captions = db.captions(filters={"id": id})
        if len(captions) == 1:
            return captions[0]
        redirect("/")

    def _captions(self):
        db = DB(self._config)
        return json.dumps(db.captions(views=('name', 'id', 'location')))

    def _update_json(self, id):
        if request.json:
            db = DB(self._config)
            db.set_captions(id, request.json)
            return {"status": "updated", "id": id}
        response.status = 400
        return response

    def _add_json(self):
        if request.json:
            db = DB(self._config)
            id = db.create_captions(request.json)
            return {"status": "updated", "id": id}
        response.status = 400
        return response

    def main(self):
        run(self._app, host='0.0.0.0', port=self._config.http_port)
