import pymongo
import datetime
import time

'''
    time is "day/month/year H:M", nodepos is list with node
    positions
'''

class Finder:
    def __init__(self,nodepos = [(0,0),(100,100),(50,50)]):
        self.nodepos = nodepos
        
    #Do not use find_mac, it is incomplete
    '''
        find a mac address based on a time
    '''
    def find_mac(self,mac,time):
        epoch = datetime.datetime.utcfromtimestamp(0)
        current = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M')
        time = (current - epoch).total_seconds()/600
        
        client = pymongo.MongoClient()
        db = client.cheddar
        col = db.times
        data = col.find_one({"_id":time})['data']
        #doesnt work, we have a list of dictionaries not a dictionary
        data = {k:v for (k,v) in data.iteritems() if mac in k}
        return data

    def pull(self):
        time = time.time()/600
        
        client = pymongo.MongoClient()
        db = client.cheddar
        col = db.times
        data = col.find_one({"_id":time})['data']
        return data

#time is "month/day/year,H:M"
def pull(self,time):
        epoch = datetime.datetime.utcfromtimestamp(0)
        current = datetime.datetime.strptime(time,'%m/%d/%Y,%H:%M')
        time = ((current - epoch).total_seconds() + 14400)/600 #14400 accounts for eastern timezone
        
        client = pymongo.MongoClient()
        db = client.cheddar
        col = db.times
        data = col.find_one({"_id":time})['data']
        return data
