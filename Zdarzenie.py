
from Sygnaly import Sygnal
class Zdarzenie:
    """Class Zdarzenie
    """
    # Attributes:
    idWezla = None  # (int) 
    dzialanie = None  # (str) 
    czas = None  # (time)
    dane = None 

    def __init__(self,idWezla ,dzialanie ,czas, dane) -> None:
        self.idWezla=idWezla
        self.dzialanie =dzialanie
        self.czas  = czas
        self.dane = dane
    


