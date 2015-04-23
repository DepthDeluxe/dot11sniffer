import zlib
import cPickle
import pymongo
import time

client = pymongo.MongoClient("gouda.bucknell.edu")
db = client.cheddar
collection = db.times

count = 0

while(True):
    if count < collection.count():                                  #check if there is more data left
        query = collection.find(snapshot=True).sort('_id',1)
        #first = collection.find().sort("_id",1)[0]["_id"]  #get id of first element
        #data = collection.find({"_id":first+count})['data']         #get data from first+count elements
        while(count < query.count()-1):
            data = query[count]['data']
            pickled = cPickle.dumps(data)
            compressed = zlib.compress(pickled,9)
            update = {}
            update['$set'] = {'data':compressed}
            collection.update_one({'_id':query[count]['_id']},update)
            count += 1
    else:
        time.sleep(300)


