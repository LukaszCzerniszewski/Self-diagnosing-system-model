from Sygnaly import Sygnal
from datetime import datetime
from Zdarzenie import Zdarzenie
from Wezel import Wezel, Address
import copy
import time, sys
class Interface:
    """Class Interface
    """
    # Attributes:
    listaWezlow = []  # (list) 
    zaplanowaneZdarzenia = []  # (lista)
    
    def __init__(self) -> None:
        self.momentStart = time.time() 
    
    # Operations
    def dodajWezel(self,wezel):
        self.listaWezlow.append(wezel)
        
    
    def usunWezel(self,wezel):
        self.listaWezlow.remove(wezel)

    def przygotujKolejki(self):
        for we in self.listaWezlow:
            for sa in we.sasiedziednieWezly:
                kolejkaWezla = None
                numerIdWezla = sa
                for m in self.listaWezlow:
                   
                    if m.numerId == sa:
                        kolejkaWezla = m.quote
                        index = we.sasiedziednieWezly.index(sa)
                        we.sasiedziednieWezly[index] = Address(numerIdWezla, kolejkaWezla )
                       
                        break
    


                


    def start(self):

        self.przygotujKolejki()
        self.momentStart = time.time()
        symulacjaTrwa = True
     
        while symulacjaTrwa :
            if len(self.zaplanowaneZdarzenia)==0:
                break
            if time.time() - self.momentStart >= self.zaplanowaneZdarzenia[0].czas and len(self.zaplanowaneZdarzenia)!=0:
           
                if self.zaplanowaneZdarzenia[0].idWezla != 0:
                    for wezel in self.listaWezlow:
                        if wezel.numerId != self.zaplanowaneZdarzenia[0].idWezla:
                            pass
                        
                        elif self.zaplanowaneZdarzenia[0].dzialanie == "start":
                            
                            wezel.start()

                        elif self.zaplanowaneZdarzenia[0].dzialanie == "wznow":
                            
                            wezel.symluj()    
                            
                            

                        elif self.zaplanowaneZdarzenia[0].dzialanie == "sendMesseng":
                            
                            wezel.sendMesseng(copy.copy(self.zaplanowaneZdarzenia[0]).dane.doKogo ,self.zaplanowaneZdarzenia[0].dane.typ, self.zaplanowaneZdarzenia[0].dane.tresc,[self.zaplanowaneZdarzenia[0].dane.doKogo])
                            
                            self.zaplanowaneZdarzenia[0].dzialanie += " " + str(self.zaplanowaneZdarzenia[0].dane.typ) + " " + str(self.zaplanowaneZdarzenia[0].dane.tresc)
                            
                           
                        elif self.zaplanowaneZdarzenia[0].dzialanie == "reakcjaNaSygnal":
                            
                            wezel.reakcjaNaSygnal(self.zaplanowaneZdarzenia[0].dane)

                        
                        
                elif self.zaplanowaneZdarzenia[0].idWezla == 0:
                   
                    for wezel in self.listaWezlow:
                        if self.zaplanowaneZdarzenia[0].dzialanie == "start":
                            wezel.start()

                        elif self.zaplanowaneZdarzenia[0].dzialanie == "koniec symulacji":
                            symulacjaTrwa=False
                         
                             
                
                #Na koniec usuwa zdarzenie z listy
                self.zaplanowaneZdarzenia.remove(self.zaplanowaneZdarzenia[0])
                        
                     
            else:
                time.sleep(2.00)
        
        return None


                



                    

    
    def test1(self):
        self.dodajWezel(Wezel(1,3.00,[2,3]))
        self.dodajWezel(Wezel(2,3.00,[1,3]))
        self.dodajWezel(Wezel(3,3.00,[2,1]))

        self.zaplanujZdarzenie(Zdarzenie(1,"start",0.00,None))
        self.zaplanujZdarzenie(Zdarzenie(2,"start",3.00,None))
        self.zaplanujZdarzenie(Zdarzenie(3,"start",4.00,None))

   
    
        sygnal1 = Sygnal(1,2,"Wiadomosc",None,"Wiadomosc testowa numer 1")
        self.zaplanujZdarzenie(Zdarzenie(1,"sendMesseng",30.00,sygnal1))

        sygnal2 = Sygnal(1,3,"Wiadomosc",None,"Wiadomosc testowa numer 2")
        self.zaplanujZdarzenie(Zdarzenie(1,"sendMesseng",60.00,sygnal2))

        sygnal3 = Sygnal(1,1,"Zdarzenie",[],"Zatrzymanie")
        self.zaplanujZdarzenie(Zdarzenie(1,"reakcjaNaSygnal",80.00,sygnal3))

        self.zaplanujZdarzenie(Zdarzenie(1,"wznow",200.00,None))


        sygnal4 = Sygnal(2,2,"Zdarzenie",[],"Zatrzymanie")
        self.zaplanujZdarzenie(Zdarzenie(2,"reakcjaNaSygnal",290.00,sygnal4))





        #self.zaplanujZdarzenie(Zdarzenie(0,"Koniec",2200.00,None))

        self.start()




        sys.exit()
        return 1 # should raise NotImplementedError()
    
    def rysujSiec(self):
        """function rysujSiec
        
        returns 
        """
        return None # should raise NotImplementedError()

    
    def zaplanujZdarzenie(self, zdarzenie):
        #Wezly maja numery id  1 - xxx
        #Jesli numer idWezla == 0 to dotyczy calej sieci
        self.zaplanowaneZdarzenia.append(zdarzenie)




if __name__ == '__main__':
    nowyInterface = Interface()
    wynik = nowyInterface.test1()
    sys.exit()
    print("Wynik")

