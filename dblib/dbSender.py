import multiprocessing.connection

SIZE = 128

class Sender:
    def __init__(self,node,time,sigstr,mac,host='gouda.bucknell.edu',port=10000):
        self.node = str(node)
        self.time = str(time)
        self.sigstr = str(sigstr)
        self.mac = str(mac)
        self.host = host
        self.port = port

    def send():
        sock = multiprocessing.connection.Client((self.host,self.port))
        data = self.node+','+self.time+','+self.sigstr+','+self.mac
        sock.send(data)
        s.close()
