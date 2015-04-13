import pymongo
import multiprocessing
import multiprocessing.connection
import time

SIZE = 128
NUM_NODES = 3

def recv_data(sock,dataQueue,cQueue):
    connect = sock.accept()
    cQueue.put("listen")
    data = connect.recv()
    dataQueue.put(data)
    connect.close()
    print("received data")
    exit(0)

def db_send(database,queue):
    collection = database.times
    t = int(time.time())
    doc = int(t/600)   
    for i in range(queue.qsize()):
        data = queue.get()
        data = data.split(',')
        for j in range(0,len(data)-3,4):
            new_posts = {}
            new_posts.update({'data':{"mac":data[j+3],'node':int(data[0]),'time':int(data[j+1]),'sigstr':int(data[j+2])}})
            collection.update({'_id':doc},{"$push":new_posts},upsert=True)
##        dic = {'node':temp[0],'time':temp[1],'sigstr':temp[2],'mac':temp[3]}
##        new_posts.append(dic)
    
##    posts.insert_many(new_posts)

    print("sent")
    exit(0)

def server(host,port):
    client = pymongo.MongoClient()
    db = client.cheddar
    
    sock = multiprocessing.connection.Listener((host,port))
    dq = multiprocessing.Queue()
    cq = multiprocessing.Queue()
    cq.put("listen")
    while True:
        try:
            task = cq.get(True,1)
        except:
            task = "none"
        if task == "listen":
            print("spawning listening thread")
            p = multiprocessing.Process(target=recv_data, args=(sock,dq,cq))
            p.start()
##        if (dq.qsize() == 100):
        if dq.qsize() != 0:
            print("spawning sending thread")
            p = multiprocessing.Process(target=db_send,args=(db,dq))
            p.start()
##            pass

server('',10000)

