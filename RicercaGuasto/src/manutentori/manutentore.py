# -------------------------------------------------------------#
"""Classe che descrive unn manutentore. In particolare di un manutentore
mi interesse memorizzare nome e password"""
class Manutentore():
    def __init__(self, nome, password):
        self._nome = nome
        self._password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, nuova_password):
        if nuova_password != "" and nuova_password != self._password:
            self._password = nuova_password
            return True
        else:
            print("impossibile cambiare la password")
            return False

    @property
    def nome(self):
        return self._nome


    def AggiuniGuasto(self, g, Db):
        """
        Metodo per aggiungere un guasto al database
        :param g: guasto
        :param Db: database
        :return: True se l'inserimento va a buon fine, False altrimenti
        """
        if g.controlla_attributi():
            Db.add_guasto(g)
            return True
        else: return False

    def RicercaGuasti(self,Db):
        """
        Metodo per cercare tra i vecchi guasti all'interno del database
        :param Db:
        :return:
        """
        pass
# -------------------------------------------------------------#


# -------------------------------------------------------------#
class Caporeparto(Manutentore):
    """
    La classe Caporeparto eredita i metodi della classe Manutentore, ma
    """

    def __init__(self):
        self._nome = "caporeparto"
        self._password = "capo123"

    # Il caporeparto può modificare la password degli altri manutentori
    def ModificaPasswordAltrui(self, manutentore, Db):
        manutentore.password = "1234"
        Db.modifica_password(manutentore)

    def AggiungiManutentore(self, user, password, Db):
        nuovo_manutentore = Manutentore(user, password)
        Db.add_manutentore(nuovo_manutentore)
        return nuovo_manutentore

# -------------------------------------------------------------#


# -------------------------------------------------------------#
if __name__ == '__main__':
    print("Io sono il modulo manutentore \nPer eseguire il programma python3 main.py")
# -------------------------------------------------------------#
