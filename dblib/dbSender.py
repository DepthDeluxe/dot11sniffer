import multiprocessing.connection

class Sender:
    def __init__(self,host='gouda.bucknell.edu',port=10000):
        self.host = host
        self.port = port
        self.data = ""

    def send(self):
        sock = multiprocessing.connection.Client((self.host,self.port))
        sock.send(self.data)
        sock.close()

    def add(self,mac,node,time,sigstr):
        if len(self.data) == 0:
            self.data = self.data+str(node)+','+str(time)+','+str(sigstr)+','+str(mac)
        else:
            self.data = self.data+','+str(node)+','+str(time)+','+str(sigstr)+','+str(mac)

    def clear(self):
        self.data = ''
