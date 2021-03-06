import pymongo
import datetime
import time
import math

'''
    time is "day/month/year H:M", nodepos is list with node
    positions
'''

class DBFinder:
    def __init__(self):
        # initialize client in the constructor so the connection stays alive
        self.client = pymongo.MongoClient("gouda.bucknell.edu")
        self.db = self.client.cheddar
        self.collection = self.db.times
        self.processedCollection = self.db.processed_data

    '''
        Gets list of all IDs in the raw collection
    '''
    def findIds(self):
        resList = []
        responses = self.collection.find({}, {"_id": 1})
        for response in responses:
            resList.append(response["_id"])

        return resList

    '''
        Gets list of all IDs in the processed collection
    '''
    def findProcessedIds(self):
        resList = []
        responses = self.processedCollection.find({}, {"_id": 1})
        for response in responses:
            resList.append(response["_id"])

        return resList


    #Do not use find_mac, it is incomplete
    '''
        find a mac address based on a time
    '''
    def find_mac(self, mac, curTime):
        epoch = datetime.datetime.utcfromtimestamp(0)
        current = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M')
        time = (current - epoch).total_seconds()/600

        data = self.collection.find_one({"_id":curTime})['data']
        #doesnt work, we have a list of dictionaries not a dictionary
        data = {k:v for (k,v) in data.iteritems() if mac in k}
        return data

    '''
        Pulls a timeblock from the collection
    '''
    def pull(self, timeblock=math.floor(time.time() / 600)):
        return self.collection.find_one({"_id":timeblock})['data']

    '''
        Sets the number of unique nodes in a timeblock region
    '''
    def set_num_unique(self, timeblock, val):
        updateObj = {}
        updateObj['$set'] = {'uniq': val}
        self.collection.update_one({'_id': timeblock}, updateObj)

    '''
        Writes one whole processed data chunk to the database
    '''
    def write_processed_block(self, timeblock, data, uniq):
        dbObj = {}
        dbObj['_id'] = timeblock
        dbObj['data'] = data
        dbObj['uniq'] = uniq
        self.processedCollection.insert(dbObj)

    def pull_processed_block(self, timeblock):
        points = []
        obj = self.processedCollection.find_one({"_id":timeblock})
        for pt in obj['data']:
            points.append(pt)

        return points

    def pull_processed_uniq(self, timeblock):
        obj = self.processedCollection.find_one({"_id":timeblock})
        return obj['uniq']

#time is "month/day/year,H:M"
def pull(self,curTime):
        epoch = datetime.datetime.utcfromtimestamp(0)
        current = datetime.datetime.strptime(time,'%m/%d/%Y,%H:%M')
        curTime = ((current - epoch).total_seconds() + 14400)/600 #14400 accounts for eastern timezone

        client = pymongo.MongoClient()
        db = client.cheddar
        col = db.times
        data = col.find_one({"_id":curTime})['data']
        return data
