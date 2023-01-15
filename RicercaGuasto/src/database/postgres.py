import psycopg2
from src.database.dbconfig import config
from src.manutentori.manutentore import Caporeparto
from src.tool.Utility import find_path
from src.tool.Utility import replace


def connect(str):
    conn = None
    try:
        params = config(find_path(str))
        conn = psycopg2.connect(**params)
        curr = conn.cursor()
        return conn, curr
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


class Database:
    """
    ALL'INTERNO DI QUESSTA CLASSE SONO IMPLEMENTANTI I METODI
    PER INTERAGIRE IN SQL CON IL DATABASE RELAZIONALE Guasti
    CONTENENTE LE TABELLE Manutentori E Guasti
    """

    def __init__(self, str):
        self.conn, self.curr = connect(str)
        # Se nella tabella dei manutentori non è presente la tupla del caporeparto
        # creo un oggetto di tipo caporeparto e lo salvo
        if not self.is_presente("caporeparto"):
            C = Caporeparto()
            C.AggiungiManutentore(C.nome, C.password, self)

    # ------------------------------------------------------------------------------------- #
    def is_presente(self, Nome):
        """
        Metodo che verifica che un manutentore non sia presente all'interno del Db,
        utile per controllare l'unicità della chiave della tabella manutentore senza
        far terminare il programma quando provo a inserirne uno esistente
        :param Nome: nome del manutenotre da verificare
        :return: True se Nome è presente nella tabella Manutentori, False altrimenti
        """
        self.curr.execute("SELECT Manutentori.nome FROM Manutentori;")
        nomi = [list[0] for list in self.curr.fetchall()]
        for nome in nomi:
            nome = replace(nome)
            if nome == Nome: return True
        return False
    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def ok_manutentore(self, manutentore):
        """
        Metodo che verifica che un manutentore sia presente e che la password sia corretta
        :param manutentore: Manutentore del quale voglio verificare la presenza e la validità
        della password
        :return: il manutentore se presente, None altrimenti
        """
        self.curr.execute("SELECT * FROM Manutentori;")
        for manutentori in self.curr:
            nome, password = manutentori[0], manutentori[1]
            if nome == manutentore.nome and password == manutentore.password:
                return manutentore
        return None
    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def reset_db(self):
        """
        Metodo per resettare il database
        """

        # Cancello le tabelle
        self.curr.execute("DROP TABLE IF EXISTS Manutentori CASCADE;")
        self.curr.execute("DROP TABLE IF EXISTS Guasti CASCADE;")

        # Creo le tabelle
        self.curr.execute("""CREATE TABLE Manutentori(
                        nome VARCHAR(25) PRIMARY KEY,
                        password VARCHAR(25) ); """)

        self.curr.execute("""CREATE TABLE Guasti (
                        data TIMESTAMP,
                        turno VARCHAR(15),
                        reparto VARCHAR(20),
                        nome VARCHAR(25),
                        descrizione_problema VARCHAR (250),
                        risoluzione VARCHAR(250),
                        risolto VARCHAR(6),
                        PRIMARY KEY (data,nome),
                        FOREIGN KEY(nome) REFERENCES Manutentori); """)
        # per la data MM/DD/YYYY HH12
        # creo un oggetto di tipo Caporeparto e lo inserisco nel database
        C = Caporeparto()
        C.AggiungiManutentore(C.nome, C.password, self)

        # salvo le modifice
        self.conn.commit()

    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def add_manutentore(self, manutentore):
        """
        Metodo che aggiunge un manutentore al Database, dopo aver verificato che non sia presente
        :param manutentore: Manutentore da aggiungere
        :return: True se l'inserimento va a buon fine, False altrimenti
        """
        if not self.is_presente(manutentore.nome):
            self.curr.execute("INSERT INTO manutentori (nome, password)  VALUES (%s, %s)",
                              (manutentore._nome, manutentore._password))
            self.conn.commit()
            return True
        return False

    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def modifica_password(self, manutentore):
        """
        Metodo che modifica la password del manutentore
        :param manutentore: Manutentore del quale modificare la password
        :return: True se la modifica va a buon fine, False altrimenti
        """
        self.curr.execute("UPDATE Manutentori SET password = (%s) WHERE nome = (%s)",
                          (manutentore.password, manutentore.nome))
        self.conn.commit()

    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def add_guasto(self, g):
        """
        Metodo per inserire un guasto all'interno del database
        :param guasto: guasto da inserire
        """
        self.curr.execute("""INSERT INTO Guasti 
        (data, turno, reparto,nome,descrizione_problema,risoluzione,risolto) 
        VALUES (%s, %s,%s,%s,%s,%s,%s)""", (
        g.data, g.turno, g.reparto, g.manutentore, g.descrizione_problema, g.risoluzione, g.isrisolto))
        self.conn.commit()
    # ------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------- #
    def query_guasto(self, tipo, turno, reparto, descrizione, risultati):
        """
        Metodo per cercare all'interno del database, in base al parametro tipo modifico
        la query per cercare o meno nel turno, nel reparto e nella descrizione
        :param tipo: valore intero che indica il tipo di query da andare a eseguire
        :param turno: turno nel quale cercare il guasto
        :param reparto: reparto nel quale cercare il guasto
        :param descrizione: descrizione del problema da cercare
        :param risultati: lista di risultati che viene modificata
        :return:
        """

        # Tutti i guasti
        if tipo == 1:
            self.curr.execute("SELECT * FROM Guasti")

        # descrizione
        if tipo == 2:
            self.curr.execute('SELECT * FROM Guasti WHERE descrizione_problema LIKE %(descrizione)s',{'descrizione': '%{}%'.format(descrizione)})

        # reparto e descrizione
        if tipo == 3:
            self.curr.execute('SELECT * FROM Guasti WHERE reparto = %(reparto)s AND descrizione_problema LIKE %(descrizione)s',
                              {'reparto':'{}'.format(reparto),'descrizione': '%{}%'.format(descrizione)})

        # turno, reparto e descrizione
        if tipo == 4:
            self.curr.execute(
                'SELECT * FROM Guasti WHERE turno = %(turno)s AND reparto = %(reparto)s AND descrizione_problema LIKE %(descrizione)s',
                {'turno':'{}'.format(turno), 'reparto': '{}'.format(reparto), 'descrizione': '%{}%'.format(descrizione)})

        # +++ -------------------------------------------------------------------- +++ #
        # Per visualizzare i risultati in formato tabellare occorre fornire
        # i risultati in una lista di liste, ad esempio
        # [
        # [data1, turno1, reparto1, manutentore1,descrizione1,risoluzione1,risolto1]
        # [data2, turno2, reparto2, manutentore2,descrizione2,risoluzione2,risolto2]
        # ........ ]
        # Quindi per ogni risultato creo una lista e la aggiungo alla lista principale
        # Che risulta modificata dopo l'esecuzione della query
        # +++ -------------------------------------------------------------------- +++ #
        for guasti in self.curr:
            g = []
            for i in range(0,7):
                g.append(guasti[i])
            risultati.append(g)
    # ------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    print("\n\nIo sono il modulo Database \nPer eseguire il programma python3 main.py")