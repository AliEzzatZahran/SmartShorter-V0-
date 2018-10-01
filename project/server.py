from flask import Flask, jsonify, make_response, request, abort
from pymongo import MongoClient
from project import config
import uuid

app = Flask(__name__)



client = MongoClient(config.MONGO_URI)
mydb = client[config.MONGO_DATABASE_NAME]


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'message': 'bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({}), 500)


@app.route('/shortlinks', methods=['GET'])
def get_shortlinks():
    output = []
    for link in mydb.shortlink.find():
        links_data = {}
        links_data['slug'] = link['slug']
        links_data['ios'] = link['ios']
        links_data['android'] = link['android']
        links_data['web'] = link['web']
        output.append(links_data)
    return jsonify('shortlinks', output)


@app.route('/shortlinks', methods=['POST'])
def create_shortlinks():
    if not request.json or 'ios' and 'android' and 'web' not in request.json:
        abort(400)
    data = request.json
    if not data['slug']:
        slug = str(uuid.uuid4())
    Newrecord = {

        "slug": slug,
        "ios": data['ios'],
        "android": data['android'],
        "web": data['web']
    }
    mydb.shortlink.insert(Newrecord)
    return jsonify({'shortlinks': Newrecord}), 201



if __name__ == '__main__':
    app.run(debug=True)