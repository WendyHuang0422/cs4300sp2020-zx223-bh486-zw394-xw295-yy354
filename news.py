import flask_pymongo
from flask_pymongo import MongoClient
# connect = MongoClient()
client = flask_pymongo.MongoClient(
    'mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')

SEED_DATA = [
    {
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    },
    {
        'decade': '1980s',
        'artist': 'Olivia Newton-John',
        'song': 'Physical',
        'weeksAtOne': 10
    },
    {
        'decade': '1990s',
        'artist': 'Mariah Carey',
        'song': 'One Sweet Day',
        'weeksAtOne': 16
    }
]

db = client.get_default_database()

songs = db['songs']

songs.insert_many(SEED_DATA)

query = {'song': 'One Sweet Day'}

songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})

cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)

for doc in cursor:
    print('In the %s, %s by %s topped the charts for %d straight weeks.' %
          (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))


client.close()
