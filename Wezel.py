from Interface import Interface
from SygnalZwotny import SygnalZwotny
from Krolestwo import Krolestwo

class Wezel:
    """Class Wezel
    """
    # Attributes:
    numerId = None  # (int) 
    stan = None  # (str) 
    czasSamoNaprawy = None  # (float) 
    sasiedziednieWezly = None  # (list) 
    otrzymaneSygnaly = None  # (list) 
    krolestwo = None  # (Krolestwo) 
    ostatniaDiagnoza = None  # (time) 
    
    # Operations
    def diagnozuj(self):
        """function diagnozuj
        
        returns str
        """
        return None # should raise NotImplementedError()
    
    def wyslijPolecenie(self, numerIdWezla):
        """function wyslijPolecenie
        
        numerIdWezla: int
        
        returns list
        """
        return None # should raise NotImplementedError()
    

