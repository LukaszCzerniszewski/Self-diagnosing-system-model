from SygnalZwotny import SygnalZwotny
from Krolestwo import Krolestwo
import socket
from _thread import *
import threading
import time

class Wezel(threading.Thread):
    """Class Wezel
    """
    # Attributes:
    numerId = None  # (int) 
    stan = None  # (str) 
    czasSamoNaprawy = None  # (float) 
    sasiedziednieWezly = []  # (list) 
    otrzymaneSygnaly = None  # (list) 
    krolestwo = None  # (Krolestwo) 
    ostatniaDiagnoza = 0  # (time) 
    socketSerwer = None #int
    socketClient = None #int
    print_lock = threading.Lock() # 
    def __init__(self, numerId, czasSamoNaprawy, sasiedziednieWezly) -> None:
        threading.Thread.__init__(self)
        self.numerId = numerId
        self.czasSamoNaprawy = czasSamoNaprawy
        self.sasiedziednieWezly =   sasiedziednieWezly
        self.socketSerwer = 9000+self.numerId
       
       

    
    # Operations
    def diagnozuj(self):
        """function diagnozuj
        
        returns str
        """
        return self.stan # should raise NotImplementedError()
    
    def wyslijPolecenie(self, numerIdWezla):
        """function wyslijPolecenie
        
        numerIdWezla: int
        
        returns list
        """
        return None # should raise NotImplementedError()
    
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", self.socketSerwer))
        print("Wezel ",self.numerId," rozpoczal prace na sokecie ",self.socketSerwer, flush=True )
        s.listen(5)
        c, addr = s.accept()
        while   True: 
            # data received from client
            data = c.recv(1024)
            if not data:
                break
            c.sendall(data)
    
    def sendMesseng(self, soketAdresata, messang):
        host = '127.0.0.1'
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,soketAdresata))
        s.send(messang.encode('ascii'))
        data = s.recv(1024)
        s.close()
        print("Wezel ", self.numerId, " otrzymal odpowiedz", data)
        return data

        


if __name__ == '__main__':
    listaWezlow=[]
    listaWezlow.append(Wezel(1,3.00,[2,3]))
    listaWezlow.append(Wezel(2,3.00,[1,3]))
    listaWezlow.append(Wezel(3,3.00,[2,1]))
    
    listaWezlow[0].start()
    listaWezlow[1].start()
    listaWezlow[2].start()

    # listaWezlow[0].startWezel()
    # listaWezlow[1].startWezel()
    # listaWezlow[2].startWezel()

    time.sleep(1)
    listaWezlow[0].sendMesseng(listaWezlow[1].socketSerwer,'messengER')
    print("NO i to by byona tyle")


 
            

