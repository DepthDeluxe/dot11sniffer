import zlib
import pickle as cPickle
import pymongo
import bson

class Compress:
    def __init__(self):
        self.client = pymongo.MongoClient("gouda.bucknell.edu")
        self.collection = self.client.cheddar.compress
        self.timedb = self.client.cheddar.times

    def upload(self,time,data):
        pickled = cPickle.dumps(data)
        compressed = zlib.compress(pickled,9)
        update = {}
        update['$set'] = {'data':bson.binary.Binary(compressed)}
        self.collection.update({'_id':time},update,upsert=True)

    def download(self,time):
        compressed = self.collection.find_one({'_id':time})['data']
        pickled = zlib.decompress(str(compressed))
        data = cPickle.loads(pickled)
        return {'_id':time,'data':data}

    def remove(self,time):
        self.timedb.delete_one({'_id':time})
