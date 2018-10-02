from flask import Flask, jsonify, make_response, request, abort
from pymongo import MongoClient
from project import config
import string , random

app = Flask(__name__)



client = MongoClient(config.MONGO_URI)
mydb = client[config.MONGO_DATABASE_NAME]


def slug_generator(size=7, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"status": "failed",
                                  'message': 'bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
  "status": "failed",
  "message": "not found"
}), 404)


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
    try:
        slug = data['slug']
    except:
        slug = slug_generator()
    Newrecord = {

        "slug": slug,
        "ios": data['ios'],
        "android": data['android'],
        "web": data['web']
    }
    try:
        mydb.shortlink.insert(Newrecord)
    except:
        abort(400)
    del Newrecord['_id']

    return jsonify({"status": "successful",
                    "slug": slug,
                    "message": "created successfully"}),201




@app.route('/shortlinks/<link_slug>', methods=['PUT'])
def update_link(link_slug):

    links = [slug for slug in mydb.shortlink.find({"slug": link_slug})]

    if not request.json:
        abort(400)
    if len(links) == 0:
        return abort(404)


    data = request.get_json()

    if 'android' in data and 'fallback' in data['android']:
        mydb.shortlinks.update({'slug':link_slug}, {'$set':{'android.fallback':data['android']['fallback']}})
    elif'android' in data and 'primay' in data['android']:
        mydb.shortlinks.update({'slug': link_slug}, {'$set': {'android.primary': data['android']['primary']}})


    if 'ios' in data and 'fallback' in data['ios']:
        mydb.shortlinks.update({'slug':link_slug}, {'$set':{'ios.fallback':data['ios']['fallback']}})
    elif 'ios' in data and 'primay' in data['ios']:
        mydb.shortlinks.update({'slug': link_slug}, {'$set': {'ios.primary': data['ios']['primary']}})


    if 'web' in data:
        mydb.shortlinks.update({'slug': link_slug}, {'$set': {'web': data['web']}})


    return jsonify({
    "status": "successful",
    "message": "updated successfully"}),201







if __name__ == '__main__':
    app.run(debug=True)