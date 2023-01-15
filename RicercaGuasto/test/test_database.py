import unittest
from src.database.postgres import Database
from src.guasti.guasto import Guasto
from src.manutentori.manutentore import Manutentore


def stampa_avvio_test(stringa):
    print("------------------------------------------------------------------------")
    print(stringa)
    print("------------------------------------------------------------------------\n")


class TestDatabase(unittest.TestCase):
    """
    Classe di test per il database, i test non vengono eseguiti sul database del main program
    per evitare di sporcarlo con tuple inesistenti o di resettarlo e perdere i dati al suo interno,
    ma su un database di prova, creato nel medesimo modo del main database
    """

    def test_1connessione(self):
        """
        Il database non viene creato, quindi deve esistere
        """
        stampa_avvio_test("connessione")
        Db = Database("pgsql_test.ini")
        Db.conn.close()


    def test_2reset(self):
        """
        Test di reset database
        Dopo il reset mi aspetto di trovare la tabella dei manutentori con un solo elemento
        ovvero il caporeparto, e la tabella dei guasti vuota
        """
        stampa_avvio_test("reset")
        Db = Database("pgsql_test.ini")
        Db.reset_db()

        # Dopo l'operazione di reset, all'interno del database devono esserci due tabelle
        # una contenente i guasti (vuota) e una con un solo elemento che è il caporeparto

        self.assertTrue(Db.is_presente("caporeparto"))

        # Verifico che ci sia un solo manutentore dopo il reset, ovvero il caporeparto
        lista_manutentori = []
        query_manutentori = "SELECT * FROM Manutentori "
        Db.curr.execute(query_manutentori)
        for elementi in Db.curr:
            nome, password = elementi[0], elementi[1]
            m = Manutentore(nome,password)
            lista_manutentori.append(m)
        self.assertEqual(len(lista_manutentori),1)

        # Verifico che non ci sia nulla nella tabella dei guasti
        query_guasti = "SELECT * FROM Guasti"
        self.assertEqual(len(Db.curr.fetchall()),0)
        Db.conn.close()


    def test_3insert_ok_manutentore(self):
        """
        Metodo che uso per verificare il corretto inserimento di alcuni manutentori di prova
        all'interno del database
        """
        stampa_avvio_test("test di inserimento manutentori corretto")
        Db = Database("pgsql_test.ini")
        manutentori = [Manutentore("AndreaB", "andrea123"),Manutentore("RiccardoB","riccardo123"),
                       Manutentore("FrancescoB","francesco123"), Manutentore("AndreaT", "andreat123")]
        for manutentore in manutentori:
            Db.add_manutentore(manutentore)

        query_manutentori = "SELECT * FROM Manutentori "
        Db.curr.execute(query_manutentori)

        # Mi aspetto di avere esattamente CINQUE manutentori, i QUATTRO appena inseriti e il caporeparto
        self.assertEqual(len(Db.curr.fetchall()),5)
        Db.conn.close()



    def test_4insert_wrong_manutentore(self):
        """
        Metodo che uso per verificare di non poter inserire due manutentori con lo stesso nome all'interno
        del database
        """
        stampa_avvio_test("test di inserimento manutentori errato")
        Db = Database("pgsql_test.ini")
        mwrong = Manutentore("AndreaB", "password")
        Db.add_manutentore(mwrong)
        query_manutentori = "SELECT * FROM Manutentori "
        Db.curr.execute(query_manutentori)

        # Essendoci 5 manutentori prima di tentare l'inserimento, mi aspetto di averne ancora 5
        self.assertEqual(len(Db.curr.fetchall()), 5)
        Db.conn.close()



    def test_5modifica_password(self):
        """
        Test per verificare la correttezza della modifica password da parte di un manutentore
        Dopo aver modificato la propria password, le modifiche devono essere applicate anche sul DB
        """

        stampa_avvio_test("test di modifica password manutentore")
        Db = Database("pgsql_test.ini")

        m1 = Manutentore("AndreaB", "andrea123")
        if Db.ok_manutentore(m1):
            m1.password = "ciao"
        Db.modifica_password(m1)

        m2 = Db.ok_manutentore(m1)
        self.assertEqual(m2.password, "ciao")
        Db.conn.close()



    def test_6insert_ok_guasto(self):
        """
        Metodo che uso per verificare il corretto inserimento di un set di guasti di prova
        all'interno del database
        """
        stampa_avvio_test("test di inserimento guasti corretto")
        Db = Database("pgsql_test.ini")

        g1 = Guasto("2023-01-05 17:58:09.588134", "notte", "presse", "AndreaB","pressa 11 in emergenza", "sostituiti contatti NC pulsantiera operatore", "si")
        g2 = Guasto("2023-01-05 17:59:09.588134", "notte", "scelte", "AndreaB","scatto termico giostra lina 25", "sostituiti cavi alimentazione ed ethercat spintore ingresso ", "si")
        g3 = Guasto("2023-01-05 18:00:09.588134", "mattina", "forni", "AndreaB", "allarme encoder traino 3 forno 22","sostituito riduttore" ,"si")
        g4 = Guasto("2023-01-05 18:01:09.588134", "notte", "smalterie", "AndreaB", "macchina di carico lina 13 in emergenza","sostituito micro fune secondo traino", "si")
        Db.add_guasto(g1)
        Db.add_guasto(g2)
        Db.add_guasto(g3)
        Db.add_guasto(g4)
        query_guasto = "SELECT * FROM Guasti"
        Db.curr.execute(query_guasto)

        # mi aspetto di avere esattamente unn guasto
        self.assertEqual(len(Db.curr.fetchall()),4)
        Db.conn.close()


    def test_8ricerca(self):
        """
        Metodo che uso per verificare la correttezza della funzione di ricerca
        all'interno del database con un set di query di prova
        :return:
        """
        print("sono il test di ricerca guasti")
        Db = Database("pgsql_test.ini")

        # Mi aspetto di avere QUATTRO risultati
        risultati = []

        Db.query_guasto(1,"","","",risultati)
        for risultato in risultati:
            for elemento in risultato:
                print(elemento)
        self.assertEqual(len(risultati),4)

        # Mi aspetto di avere due risultati
        risultati.clear()
        Db.query_guasto(2,"","","emergenza",risultati)
        self.assertEqual(len(risultati),2)

        # Mi aspetto di avere 1 risultato
        risultati.clear()
        Db.query_guasto(3,"","presse","emergenza",risultati)
        self.assertEqual(len(risultati),1)

        # Mi aspetto di avere un risultato
        risultati.clear()
        Db.query_guasto(4, "notte","scelte", "scatto termico",risultati)
        self.assertEqual(len(risultati),1)

        Db.conn.close()


if __name__ =="__main__":
    unittest.main()