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
    def write_processed_block(self, timeblock, data):
        dbObj = {}
        dbObj['_id'] = timeblock
        dbObj['data'] = data
        self.processedCollection.insert(dbObj)

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
