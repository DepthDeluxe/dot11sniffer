import pymongo
import multiprocessing
import multiprocessing.connection

SIZE = 128

def recv_data(sock,dataQueue,cQueue):
    connect = sock.accept()
    cQueue.put("listen")
    data = connect.recv()
    dataQueue.put(data)
    connect.close()

def db_send(database,queue):
    new_posts = []
    for i in range(100):
        temp = queue.get()
        temp = temp.split(',')
        dic = {'node':temp[0],'time':temp[1],'sigstr':temp[2],'mac':temp[3]}
        new_posts.append(dic)
    
    posts = database.posts
    posts.insert_many(new_posts)

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
        if (dq.qsize() == 100):
            p = multiprocessing.Process(target=db_send,args=(db,dq))
            p.start()
            pass

server('',10000)

