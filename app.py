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


@app.route('/Places', methods=['GET', 'POST'])
def all_places():
    if request.method == 'POST':
        place = create_place(request.get_json())
        if place.validate():
            return send_response(place)
    elif request.method == 'GET':
        return get_all_places()
    else:
        abort(401)
        return "Not valid method"


@app.route('/LandmarksOrHistoricalBuildings', methods=['GET', 'POST'])
def all_landmarks():
    if request.method == 'POST':
        landmark = create_landmark(request.get_json())
        if landmark.validate():
            return send_response(landmark)
    elif request.method == 'GET':
        return get_all_landmarks()
    else:
        abort(401)
        return "Not valid method"


@app.route('/LandmarksOrHistoricalBuildings/<int:entity_id>', methods=['GET', 'PUT', 'DELETE'])
def landmarks(entity_id):
    if request.method == 'GET':
        landmark = get_landmark(entity_id)
    elif request.method == 'PUT':
        landmark = update_landmark(entity_id, request.get_json())
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


@app.route('/Places/<int:entity_id>', methods=['GET', 'PUT', 'DELETE'])
def places(entity_id):
    if request.method == 'GET':
        place = get_place(entity_id)
    elif request.method == 'PUT':
        place = update_place(entity_id, request.get_json())
    elif request.method == 'DELETE':
        place = get_place(entity_id)
        if not remove_landmark(entity_id):
            abort(401)
    else:
        abort(401)
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
        json.dump(landmark.toJSON(), f, ensure_ascii=False)
    return landmark


def get_all_landmarks():
    landmarks_dir = sorted(os.listdir('./landmarks/'))
    landmarks_arr = []
    for file in landmarks_dir:
        entity_id = os.path.splitext(file)[0]
        landmarks_arr.append(get_landmark(entity_id))
    return json.dumps(landmarks_arr, default=lambda x: x.__dict__)


def create_landmark(json_file):
    landmarks_dir = sorted(os.listdir('./landmarks/'))
    landmarks_dir.reverse()
    last_file = os.path.splitext(landmarks_dir[0])[0]
    entity_id = int(last_file) + 1
    landmark = Landmark(json_file)
    if landmark.validate():
        f = open(f'./landmarks/{entity_id}.json', 'w', encoding='utf-8')
        json.dump(landmark, f, ensure_ascii=False, default=lambda x: x.__dict__)
    return landmark


# Places
def get_place(entity_id):
    f = open(f'./places/{entity_id}.json', 'r', encoding='utf-8')
    obj = json.load(f)
    return Place(obj)


def update_place(entity_id, json_file):
    f = open(f'./places/{entity_id}.json', 'w', encoding='utf-8')
    place = Place(json_file)
    if place.validate():
        json.dump(place, f, ensure_ascii=False)
    return place


def remove_place(entity_id):
    if os.path.exists(f'./places/{entity_id}.json'):
        os.remove(f'./places/{entity_id}.json')
        return True
    else:
        print("The file does not exist")
        return False


def get_all_places():
    places_dir = sorted(os.listdir('./places/'))
    places_arr = []
    for file in places_dir:
        entity_id = os.path.splitext(file)[0]
        places_arr.append(get_place(entity_id))
    return json.dumps(places_arr, default=lambda x: x.__dict__)


def create_place(json_file):
    places_dir = sorted(os.listdir('./places/'))
    places_dir.reverse()
    last_file = os.path.splitext(places_dir[0])[0]
    entity_id = int(last_file) + 1
    place = Place(json_file)
    if place.validate():
        f = open(f'./places/{entity_id}.json', 'w', encoding='utf-8')
        json.dump(place, f, ensure_ascii=False, default=lambda x: x.__dict__)
    return place


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

    def to_html(self):
        return f'<!DOCTYPE html> <html> <head> <meta charset="utf-8" /> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <title>Landmark {self.name}</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <script type="application/ld+json"> {self.toJSON()} </script> </head> <body> <h1>Place: {self.name}</h1> <h2>Description:</h2> <p>{self.description}</p> <p>{self}</p> <h2>Address:</h2> <ul> <li> Locality: {self.address.addressLocality} </li> <li> Region: {self.address.addressRegion} </li> <li> Country: {self.address.addressCountry} </li> </ul> <img src="{self.photo}" alt="{self.name} photo" /> <a href="{self.mainEntityOfPage}">Main URL</a> </body> </html>'


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

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)

    def to_html(self):
        return f'<!DOCTYPE html> <html> <head> <meta charset="utf-8" /> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <title>Place {self.name}</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <script type="application/ld+json"> {self.toJSON()} </script> </head> <body> <h1>Place: {self.name}</h1> <h2>Description:</h2> <p>{self.description}</p>  <h2>Address:</h2> <ul> <li> Locality: {self.address.addressLocality} </li> <li> Region: {self.address.addressRegion} </li> <li> Country: {self.address.addressCountry} </li> </ul> <img src="{self.photo}" alt="{self.name} photo" /> <a href="{self.mainEntityOfPage}">Main URL</a> </body> </html>'


if __name__ == '__main__':
    app.run()
