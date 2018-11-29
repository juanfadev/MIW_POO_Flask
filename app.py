from flask import Flask, abort, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def page_not_found(error):
    return f'Error, recurso no encontrado: {error}', 404


@app.route('/')
def default_entities():
    return get_default_entities()


@app.route('/LandmarksOrHistoricalBuildings')
def all_landmarks():
    return get_all_landmarks()


@app.route('/LandmarksOrHistoricalBuildings/<int:entity_id>', methods=['GET', 'PUT', 'DELETE'])
def landmarks(entity_id):
    if request.method == 'POST':
        create_landmark(request.get_json())
    elif request.method == 'GET':
        landmark = get_landmark(entity_id)
    elif request.method == 'PUT':
        update_landmark(entity_id, request.get_json())
    elif request.method == 'DELETE':
        landmark = get_landmark(entity_id)
        if not remove_landmark(entity_id):
            abort(401)
    else:
        abort(401)
        return "Not valid method"

    if landmark.validate():
        return send_response(landmark)
    else:
        abort(401)
        return "Not valid"


@app.route('/Places/<int:entity_id>')
def places(entity_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        place = get_place(entity_id)
    elif request.method == 'PUT':
        update_place(entity_id, request.get_json())
    elif request.method == 'DELETE':
        pass
    else:
        return "Not valid method"

    if place.validate():
        return send_response(place)
    else:
        return "Not valid"


def get_landmark(entity_id):
    f = open(f'./landmarks/{entity_id}.json', 'r', encoding='utf-8')
    obj = json.load(f)
    return Landmark(obj)


def remove_landmark(entity_id):
    if os.path.exists(f'./landmarks/{entity_id}.json'):
        os.remove(f'./landmarks/{entity_id}.json')
        return True
    else:
        print("The file does not exist")
        return False


def update_landmark(entity_id, json_file):
    f = open(f'./landmarks/{entity_id}.json', 'w', encoding='utf-8')
    landmark = Landmark(json_file)
    if landmark.validate():
        json.dump(landmark, f, ensure_ascii=False)
    return landmark.toJSON()


def get_all_landmarks():
    landmarks_dir = os.listdir('./landmarks/')
    landmarks_arr = []
    for file in landmarks_dir:
        entity_id = os.path.splitext(file)[0]
        landmarks_arr.append(get_landmark(entity_id))
    return json.dumps(landmarks_arr, default=lambda x: x.__dict__)


def create_landmark(json_file):
    landmarks_dir = os.listdir('./landmarks/')
    last_file = os.path.splitext(landmarks_dir[0])[0]
    entity_id = last_file + 1
    landmark = Landmark(json_file)
    if landmark.validate():
        f = open(f'./landmarks/{entity_id}.json', 'w', encoding='utf-8')
        json.dump(landmark, f, ensure_ascii=False)
    return landmark.toJSON()


# Places
def get_place(entity_id):
    f = open(f'./places/{entity_id}.json', 'r', encoding='utf-8')
    obj = json.load(f)
    return Place(obj)


def update_place(entity_id, json_file):
    f = open(f'./landmarks/{entity_id}.json', 'w', encoding='utf-8')
    place = Place(json_file)
    if place.validate():
        json.dump(place, f, ensure_ascii=False)
    return place.to_json()


# Common functions
def send_response(response):
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    if best == 'application/json':
        return response.toJSON()
    else:
        return response.to_html()


def get_default_entities():
    f = open('./entities/entities.json', 'r', encoding='utf-8')
    return json.dumps(json.load(f))


class Landmark:
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.convert_json(d)

    def convert_json(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = Landmark(value)
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def validate(self):
        if getattr(self, "@context") == "http://schema.org/" and getattr(self,
                                                                         "@type") == "LandmarksOrHistoricalBuildings":
            return True
        else:
            return False

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)


class Place(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.convert_json(d)

    def convert_json(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = Place(value)
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def validate(self):
        if getattr(self, "@context") == "http://schema.org/" and getattr(self, "@type") == "Place":
            return True
        else:
            return False

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__)


if __name__ == '__main__':
    app.run()
