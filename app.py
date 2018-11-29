from flask import Flask, abort, request
import json
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/LandmarksOrHistoricalBuildings/<int:entity_id>', methods=['GET', 'PUT', 'DELETE'])
def landmarks(entity_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        landmark = get_landmark(entity_id)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        landmark = get_landmark(entity_id)
        if not remove_landmark(entity_id):
            abort(401)
    else:
        return "Not valid method"

    if landmark.validate():
        return landmark.to_json()
    else:
        return "Not valid"


@app.route('/Places/<int:entity_id>')
def places(entity_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        place = get_place(entity_id)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return "Not valid method"

    if place.validate():
        return place.to_json()
    else:
        return "Not valid"


def get_landmark(entity_id):
    f = open(f'./landmarks/{entity_id}.json', 'r')
    obj = json.load(f)
    return Landmark(obj)


def remove_landmark(entity_id):
    if os.path.exists(f'./landmarks/{entity_id}.json'):
        os.remove(f'./landmarks/{entity_id}.json')
        return True
    else:
        print("The file does not exist")
        return False


def get_place(entity_id):
    f = open(f'./places/{entity_id}.json', 'r')
    obj = json.load(f)
    return Place(obj)


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

    def to_json(self):
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
