import pymongo
import datetime

'''
    time is "day/month/year H:M", nodepos is list with node
    positions
'''

class Finder:
    def __init__(self,nodepos = [(0,0),(100,100),(50,50)]):
        self.nodepos = nodepos
'''
    find a mac address based on a time
'''

    def find(self,mac,time):
        epoch = datetime.datetime.utcfromtimestamp(0)
        current = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M')
        time = (current - epoch).total_seconds()
        
        client = pymongo.MongoClient()
        db = client.cheddar
        collection = db.times
