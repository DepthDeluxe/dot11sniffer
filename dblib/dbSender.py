import multiprocessing.connection

SIZE = 128

class Sender:
    def __init__(self,host='gouda.bucknell.edu',port=10000):
        self.host = host
        self.port = port
        self.data = ""

    def send():
        sock = multiprocessing.connection.Client((self.host,self.port))
        sock.send(self.data)
        s.close()

    def add(mac,node,time,sigstr):
        if len(self.data) == 0:
            self.data = self.data+str(node)+','+str(time)+','+str(sigstr)+
                ','+str(mac)
        else:
            self.data = self.data+','+str(node)+','+str(time)+','+str(sigstr)+
                ','+str(mac)
