class Guasto:
    
    def __init__(self, data, turno, reparto, manutentore, descrizione_problema, risoluzione, isrisolto):
        self._data = data
        self._turno = turno
        self._reparto = reparto
        self._manutentore = manutentore
        self._descrizione_problema = descrizione_problema
        self._risoluzione = risoluzione
        self._isrisolto = isrisolto


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self, turno):
        if turno.lower() in ("mattina", "pomeriggio", "notte"):
            self._turno = turno
        else:
            print("turno errato")

    @property
    def reparto(self):
        return self._reparto

    @reparto.setter
    def reparto(self, reparto):
        if reparto.lower() in ('mulini', 'presse', 'smalterie', 'forni', 'squadrature', 'scelte', 'lgv'):
            self._reparto = reparto
        else:
            print("reparto errato")

    @property
    def manutentore(self):
        return self._manutentore

    @manutentore.setter
    def manutentore(self, manutentore):
        self._manutentore = manutentore

    @property
    def descrizione_problema(self):
        return self._descrizione_problema

    @descrizione_problema.setter
    def descrizione_problema(self, descrizione_problema):
        if descrizione_problema != "":
            self._descrizione_problema = descrizione_problema
        else: print("descrizione problema vuoto")

    @property
    def risoluzione(self):
        return self._risoluzione

    @risoluzione.setter
    def risoluzione(self, risoluzione):
        if risoluzione != "":
            self._risoluzione = risoluzione

    @property
    def isrisolto(self):
        return self._isrisolto

    @isrisolto.setter
    def isrisolto(self,isrisolto):
        self._isrisolto = isrisolto



    def controlla_attributi(self):
        """
        Metodo che controlla che tutti gli attributi di un guasto siano esistenti e verosimili
        :return:
        """
        if self.data and self.turno and self.reparto and self.manutentore and self.descrizione_problema and self.risoluzione and self.isrisolto:
            if self.turno.lower() not in ("mattina", "pomeriggio", "notte"):
                print("Turno errato")
                return False
            elif self.reparto.lower() not in ("mulini", "presse", "smalterie", "forni", "squadrature", "scelte", "lgv", "generale"):
                print("reparto errato")
                return False
            else: return True
        else:
            print("mancano gli attributi")
            return False