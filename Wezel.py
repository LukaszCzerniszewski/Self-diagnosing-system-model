from Sygnaly import  Sygnal
from _thread import *
import threading
import time
import pickle
import sys
from queue import Queue
import copy
from datetime import datetime
class Address():
    def __init__(self, idWezla, quote ) -> None:
        self.idWezla = idWezla
        self.quote = quote 
class Wezel(threading.Thread):
    """Class Wezel
    """
    # Attributes:
    numerId = None  # (int) 
    stan = None  # (str) 
    czasSamoNaprawy = None  # (float) 
    sasiedziednieWezly = []  # (list) 
    otrzymaneSygnaly = [] # (list) 
    ostatniaDiagnoza = 0  # (time) 
    kordynator = 999999999999999999
    ostaniaElekcja = 0.00
 
   

    def __init__(self, numerId, czasSamoNaprawy, sasiedziednieWezly) -> None:
        threading.Thread.__init__(self)
        self.numerId = numerId
        self.czasSamoNaprawy = czasSamoNaprawy
        self.sasiedziednieWezly =   sasiedziednieWezly
        self.stan = "Brak awarii"
        self.quote = Queue(maxsize=1024)
        
       
       

    
    # Operations
    def diagnozuj(self):
        """function diagnozuj
        
        returns str
        """
        return self.stan # should raise NotImplementedError()
    
    def znajdzTrase(self, numerIdWezlaDoKogo):
        #Do implementacji
        trasa = []
        return trasa

    
    def reakcjaNaSygnal(self, sygnal):
        #print(sygnal.typ ," ",sygnal.tresc, flush=True)
        if sygnal.typ == "Zdarzenie":
       
            doZapisania = (str("[" + str(datetime.fromtimestamp((time.time())))+"] - Wezel: "+ str(self.numerId) + " - : " +str(sygnal.typ) + " -  " +str(sygnal.tresc) +"\n"))
            print(doZapisania, flush=True)
            
            if sygnal.tresc == "Zatrzymanie" or sygnal.tresc == "Fail-silent":
                self.stan = sygnal.tresc
                self.quote.maxsize=1
                

               # print("Wezel otrzymal zdarzenie ", sygnal.tresc, flush=True)  
             
            elif sygnal.tresc == "bizantyjska" :

                self.stan = sygnal.tresc
                print("Wezel otrzymal zdarzenie ", sygnal.tresc, flush=True)

            else:
                print("Wezel" , self.numerId," otrzymal niepoprawne zdarzenie", flush=True)
                return "error reakcjaNaSygnal -> typ == Zdarzenie"

        elif sygnal.typ == "Diagnozuj sie":

            #print(sygnal.typ ," ",sygnal.tresc)   
            if sygnal.tresc == "Przeprowadz testy" and time.time() - self.ostatniaDiagnoza > 20.00:
                #print(sygnal.typ ," ",sygnal.tresc)
                for nei in self.sasiedziednieWezly:

                    if sygnal.odKogo != nei.idWezla:
                        #nowySygnal.doKogo = nei.numerId
                        sygnal.trasa.append(self.numerId)
                        self.sendMesseng(nei.idWezla,"Diagnozuj sie","Przeprowadz testy",sygnal.trasa)
                


                self.ostatniaDiagnoza = time.time()
            
                sygnal.tresc = self.diagnozuj()
                sygnal.trasa.append(self.numerId)
           
        
                #Wyslanie odpowiedzi o stanie
                self.sendMesseng(sygnal.odKogo,sygnal.typ,sygnal.tresc,sygnal.trasa)
                
                return None
            elif sygnal.tresc == "Zatrzymanie" or sygnal.tresc == "Fail-silent" or sygnal.tresc == "bizantyjska" or sygnal.tresc == "Brak awari":
                
                if sygnal.doKogo == self.numerId:
                    dodaj = True
                   
                    for sy in self.otrzymaneSygnaly:
                        if sygnal.odKogo == sy.odKogo:
                            dodaj = False
                            break
                    #print(self.numerId,". Dodano stan wezla ", sygnal.odKogo, " = ", sygnal.tresc, flush= True )
                    
                    doZapisania = str("[" + str(datetime.fromtimestamp((time.time())))+"] - Wezel: "+str(self.numerId)+ " okreslil stan wezla: "+str(sygnal.odKogo) + " jako " + str(sygnal.tresc) + "\n")
                    print(doZapisania, flush = True)       
                    if dodaj == True:
                        self.otrzymaneSygnaly.append(copy.deepcopy(sygnal))
                else:
                    if self.numerId not in sygnal.trasa:
                        sygnal.trasa.append(self.numerId)
                        for nei in self.sasiedziednieWezly:
                            if nei.numerId not in sygnal.trasa:
                                self.sendMesseng(nei.numerId, "Diagnozuj sie", sygnal,sygnal.trasa)
                return None
        elif sygnal.typ == "Elekcja" :
            self.ostaniaElekcja = time.time()
    
            if sygnal.tresc[0] == "Podporzadkuj sie":
                if time.time() - self.ostaniaElekcja > 50.00:
                    self.kordynator = self.numerId
                    self.ostaniaElekcja=time.time()
               

                #print("sygnal.tresc[0] == "Podporzadkuj sie":",sygnal.tresc[1],  self.numerId, flush = True ) 
                if sygnal.tresc[1] < self.kordynator and  self.kordynator !=sygnal.tresc[1]:
                    #print("sygnal.tresc[1]< self.numerId",sygnal.tresc[1],"->",self.numerId,flush=True)
                    self.kordynator = copy.deepcopy(sygnal.tresc[1])
                    self.sendMesseng(sygnal.odKogo,"Elekcja",["Klaniam sie",self.numerId],[self.numerId])
                    self.algorytmElekcji()
                    self.ostatniaDiagnoza = time.time()
                    self.ostaniaElekcja=time.time()
                  
                    doZapisania = "[" + str(datetime.fromtimestamp(time.time()))+"] - Wezel: "+ str(self.numerId) + " ma nowego lidera : " +str(self.kordynator) +"\n"
                    print(doZapisania, flush=True)
                elif sygnal.tresc[1] >  self.numerId and  self.kordynator !=sygnal.tresc[1]:
                    #print("sygnal.tresc[1]> self.numerId",sygnal.tresc[1],"->",self.numerId,flush=True)
                    self.kordynator = copy.deepcopy(self.numerId)
                    self.sendMesseng(sygnal.odKogo,"Elekcja",["Podporzadkuj sie",self.kordynator],[self.numerId])
                    self.algorytmElekcji()
                    self.ostatniaDiagnoza = time.time()
                    self.ostaniaElekcja=time.time()
           
            
            else:
                return "error reakcjaNaSygnal -> typ == Diagnozuj sie"

        elif sygnal.typ == "Wiadomosc":
            doZapisania = "[" + str(datetime.fromtimestamp((time.time())))+"] - Wezel " + str(self.numerId) + " otrzymal wiadomosc od " + str(sygnal.odKogo) +" "+sygnal.tresc +"\n"
            print(doZapisania,flush=True)       
        return None



    def algorytmElekcji(self):
        #self.krolestwo = Krolestwo(self.numerId)
        #for x in self.sasiedziednieWezly:
            #self.sendMesseng(x.idWezla, "PodporzadkujSie",[self.krolestwo.koordynator,self.krolestwo.liczbaWasali])
        for x in self.sasiedziednieWezly:
            self.sendMesseng(x.idWezla,"Elekcja",["Podporzadkuj sie",self.kordynator],[self.numerId])

        return None

    def run(self):
        self.symluj()

    def symluj(self):
        self.stan = "Brak awari"
        self.quote.maxsize=1024

        
        doZapisania = (str("[" + str(datetime.fromtimestamp((time.time())))+"] - Wezel: "+str(self.numerId)+ " rozpoczal swoje dzialanie "+ "\n"))
        print(doZapisania, flush= True)
        
        while self.stan != "Zatrzymanie":
            if self.stan == "Zatrzymanie":
                break 
            #print("W wezle =",self.numerId ,"Lider = ", self.kordynator,flush=True)
            if time.time() - self.ostatniaDiagnoza > 30.00 and self.kordynator == self.numerId and self.quote.full()==False:
                print("[" + str(datetime.fromtimestamp((time.time())))+ "] - Wezel: "+str(self.numerId)+ " rozpoczyna procedure diagnozy, wezel okreslil swoj stan jako " + self.diagnozuj()+"\n",flush=True)
                self.otrzymaneSygnaly = []
                self.ostatniaDiagnoza = time.time()
                for x in self.sasiedziednieWezly:
                    self.sendMesseng(x.idWezla,"Diagnozuj sie","Przeprowadz testy",[])
               

            elif time.time() - self.ostatniaDiagnoza > 60.00:
                print("[" + str(datetime.fromtimestamp((time.time())))+ "] - Wezel: "+str(self.numerId)+ " rozpoczyna proces Elekcji\n",flush=True)
                self.kordynator = self.numerId
                self.ostaniaElekcja  = time.time()
                self.algorytmElekcji()
                #print("halo 1",flush=True)
                self.ostatniaDiagnoza = time.time()
            elif self.quote.empty() != True:
                data =  self.quote.get()
                self.reakcjaNaSygnal(data)
                #print(self.numerId,"Lider = ",self.kordynator)
            else:
                time.sleep(1)



                 
     
    
    def sendMesseng(self, numerIdWezlaDoKogo,typ, tresc,trasa ):
        
        #trasa = self.znajdzTrase(numerIdWezlaDoKogo)
        polecenie = Sygnal(self.numerId,numerIdWezlaDoKogo, typ, trasa , tresc)
        
        
        for ne in self.sasiedziednieWezly:
            if self.stan =="Zatrzymanie":
                break
            #print(ne.quote)
            if int(ne.idWezla) == int(numerIdWezlaDoKogo) and self.stan!="Zatrzymanie":
                #print("Widomosc do ", ne.idWezla, numerIdWezlaDoKogo,typ, flush=True)
                try:
                    if ne.quote.full() == False or ne.quote.maxsize != 1:
                        ne.quote.put(polecenie )
                    else:
                        print("[" + str(datetime.fromtimestamp((time.time())))+ "] - Wezel: "+str(self.numerId)+ " Okreslil stan wezla " + str(ne.idWezla) + " jako: Zatrzymanie\n",flush=True)
  

                except:
                    print("[" + str(datetime.fromtimestamp((time.time())))+ "] - Wezel: "+str(self.numerId)+ " Okreslil stan wezla " + str(ne.idWezla) + " jako: Zatrzymanie\n",flush=True)
                    polecenie.trasa = [ne.idWezla, self.numerId]
                    tresc = "Wezel " + str(self.numerId) + " okreslil stan Wezla " + str(ne.idWezla) + " jako Zatrzymanie"
                    self.sendMesseng(self.kordynator,  "Wiadomosc", tresc, polecenie.trasa)
                break
  
        
        

  

        



   
 
            

