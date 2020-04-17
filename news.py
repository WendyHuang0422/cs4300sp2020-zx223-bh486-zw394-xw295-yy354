import pymongo
from pymongo import MongoClient
# connect = MongoClient()
client = pymongo.MongoClient('mongodb://alicia:alicia1@ds139944.mlab.com:39944/heroku_4pflvg1c')

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

# songs.insert_many(SEED_DATA)

query = {'song': 'One Sweet Day'}

# songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})

cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)

for doc in cursor:
    print ('In the %s, %s by %s topped the charts for %d straight weeks.' %
              (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))
  
    ### Since this is an example, we'll clean up after ourselves.

# db.drop_collection('songs')

    ### Only close the connection when your app is terminating

client.close()
# db = connect.news

# # creating or switching to demoCollection
# collection = db.demoCollection

# # first document
# document1 = {
#         "name":"John",
#         "age":24,
#         "location":"New York"
#         }
# #second document
# document2 = {
#         "name":"Sam",
#         "age":21,
#         "location":"Chicago"
#         }

# # Inserting both document one by one
# collection.insert_one(document1)
# collection.insert_one(document2)



# # # Printing the data inserted
# # cursor = collection.find()
# # for record in cursor:
# #     print(record)