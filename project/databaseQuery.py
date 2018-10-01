from pymongo import MongoClient
from project import config
from mongoframes import *
import datetime

clint = MongoClient('mongodb://localhost:27017/')
mydb = clint[config.MONGO_DATABASE_NAME]

myrecord = {

      "slug": "s5G1f3",
      "ios": {
        "primary": "http://...",
        "fallback": "http://..."
      },
      "android": {
        "primary": "http://...",
        "fallback": "http://..."
      },
      "web": "http://..."

        }

if __name__ == '__main__':
    output = []
    for link in mydb.shortlink.find():
        links_data = {}
        links_data['slug'] = link['slug']
        links_data['ios'] = link['ios']
        links_data['android'] = link['android']
        links_data['web'] = link['web']
        output.append(links_data)

    print(link['ios']['primary'])
    #record_id = mydb.shortlink.insert(myrecord)
    #print(record_id)
    #print(mydb.get_collection())
