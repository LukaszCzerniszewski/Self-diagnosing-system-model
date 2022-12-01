import pickle
import time


class Sygnal:
    def __init__(self,odKogo,doKogo, typ, trasa,tresc) -> None:
        self.odKogo = odKogo
        self.doKogo = doKogo
        self.typ = typ
        self.trasa=trasa
        self.tresc = tresc
        self.id = str(time.time())
    def __bytes__(self):
        return pickle.dumps(self)

    def loads(bytes):
        return pickle.loads(bytes)