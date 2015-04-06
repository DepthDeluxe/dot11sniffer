import pymongo
import socket
from multiprocessing import Process,Queue

SIZE = 128

def recv_data(socket,queue):
    client,addr = socket.accept()
    data = client.recv(SIZE)
    queue.put(data)
    client.close()

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
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    q = Queue()
    while True: 
        p = Process(target=recv_data, args=(sock,q))
        p.start()
        if (q.qsize() == 100):
            p = Process(target=db_send,args=(db,q))
            p.start()

server('',10000)
