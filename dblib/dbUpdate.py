import pymongo
import multiprocessing
import multiprocessing.connection
import time

SIZE = 128

def recv_data(sock,dataQueue,cQueue):
    connect = sock.accept()
    cQueue.put("listen")
    data = connect.recv()
    dataQueue.put(data)
    connect.close()

def db_send(database,queue):
    t = int(time.time())
    doc = int(t/600)   
    new_posts = {'_id':doc}
    for i in range(len(queue.qsize())):
        data = queue.get()
        data = data.split(',')
        for j in range(0,len(data)-4,4):
            new_posts.update({data[j+3]:{'node':data[0],'time':data[j+1],'sigstr':data[j+2]}})

##        dic = {'node':temp[0],'time':temp[1],'sigstr':temp[2],'mac':temp[3]}
##        new_posts.append(dic)
    
##    posts.insert_many(new_posts)
    collection = database.times
    collection.insert(new_posts)

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
            p = multiprocessing.Process(target=recv_data, args=(sock,dq,cq))
            p.start()
##        if (dq.qsize() == 100):
        if time.time()%600 == 0:
            p = multiprocessing.Process(target=db_send,args=(db,dq))
            p.start()
##            pass

server('',10000)

