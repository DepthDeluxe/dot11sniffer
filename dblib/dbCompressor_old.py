import zlib
import cPickle
import pymongo
import time
import bson

client = pymongo.MongoClient("gouda.bucknell.edu")
db = client.cheddar
collection = db.times
testcol = db.compress

count = 0

while(True):
    size = collection.count();
    if count < size:                                  #check if there is more data left
        responses = collection.find({},{'_id':1})
        ids = []
        for i in responses:
        		ids.append(i['_id'])
        ids.sort()
        ids = ids[0:len(ids)-1]
        #first = collection.find().sort("_id",1)[0]["_id"]  				#get id of first element
        #data = collection.find({"_id":first+count})['data']        #get data from first+count elements
        while(count < len(ids)):
            data = collection.find_one({'_id':ids[count]})['data']
            pickled = cPickle.dumps(data)
            compressed = zlib.compress(pickled,9)
            update = {}
            update['$set'] = {'data':bson.binary.Binary(compressed)}
            testcol.update({'_id':ids[count]},update,upsert=True)
            print ("updating: " + str(ids[count]))
            count += 1
    else:
        time.sleep(300)


