from datetime import datetime
import PySimpleGUI as sg
from src.guasti.guasto import Guasto
from src.manutentori.manutentore import Caporeparto, Manutentore
from src.tool.Utility import find_path


class gui:
    def __init__(self, tipo, manutentore, db, risultati=None):
        self.tipo = tipo
        self.manutentore = manutentore
        self.db = db
        self.headings = ["Data", "Turno","Reparto","Manutentore","Descrizione","Risoluzione","Risolto"]
        self.risultati = risultati
        self.window = self.make_window()

    def make_window(self, risultati=None):
        """Metodo che utilizzo per risolvere il problema di PySimleGui che non permette
        di riutilizzare lo stesso layout più volte, la finestra la creo con un layout definito
        come variabile locale di questa funzione, così posso riusalra varie volte"""

        # --------------------------------------------------- #
        # Finestra Iniziale
        # --------------------------------------------------- #
        if self.tipo == "Welcome":
            layout_welcome = [[sg.Image(filename=find_path("logo.png"))],
                              [sg.Text("Effettuare il login ", font=22)],
                              [sg.Text("Username", font=16), sg.InputText(size=(65, 2), font=16), ],
                              [sg.Text("Password", font=16), sg.InputText(size=(65, 2), font=16, password_char='*')],
                              [sg.Button("Login", font=16)]
                              ]
            return sg.Window("RicercaGuasto",layout_welcome,element_justification ='l', size=(740,480))

        # --------------------------------------------------- #
        # Finestra dopo aver fatto il login come caporeparto
        # --------------------------------------------------- #
        if self.tipo == "Caporeparto":
            layout_caporeparto = [[sg.Image(filename=find_path("logo.png"))],
                                  [sg.Text("Inserire un nuovo guasto                  ", font=16),sg.Button("Guasto", font=16)],
                                  [sg.Text("Ricerca tra i vecchi guasti               ", font=16),sg.Button("Ricerca", font=16)],
                                  [sg.Text("Inserisci un nuovo manutentore            ", font=16),sg.Button("Inserisci Manutentore", font=16)],
                                  [sg.Text("Modificare la propria password            ", font=16),sg.Button("Modifica Password", font=16)],
                                  [sg.Text("Modificare la password altrui             ", font=16),sg.Button("Modifica", font=16)],
                                  [sg.Text("Logout                                    ", font=16),sg.Button("Logout", font=16)]
                                  ]
            return sg.Window("RicercaGuasto",layout_caporeparto,element_justification ='l', size=(740,480))

        # --------------------------------------------------- #
        # Finestra dopo aver fatto il login come manutentore
        # --------------------------------------------------- #
        if self.tipo == "UtenteLoggato":
            layout_loggato = [[sg.Image(filename=find_path("logo.png"))],
                              [sg.Text("Inserire un nuovo guasto                 ", font=16),sg.Button("Guasto", font=16)],
                              [sg.Text("Ricerca tra i vecchi guasti              ", font=16),sg.Button("Ricerca", font=16)],
                              [sg.Text("Cambia password                          ", font=16),sg.Button("Modifica Password", font=16)],
                              [sg.Text("Logout                                           ", font=16),sg.Button("Logout", font=16)]
                              ]
            return sg.Window("RicercaGuasto",layout_loggato,element_justification ='l', size=(740,480))

        # --------------------------------------------------- #
        # Finestra nella quale inserire i nuovi guasti
        # --------------------------------------------------- #
        if self.tipo == "Aggiungi":
            layout_insert = [[sg.Image(filename=find_path("logo.png"))],
                             [sg.Text("Turno                ", font=16),sg.OptionMenu(('Mattina', 'Pomeriggio', 'Notte'), size=(12, 3))],
                             [sg.Text("Reparto del guasto   ", font=16), sg.OptionMenu(('Mulini', 'Presse', 'Smalterie', 'Forni', 'Squadrature', 'Scelte', 'Generale'),size=(12, 3))],
                             [sg.Text("Descrizione Problema ", font=16),sg.InputText(size=(65, 2), font=16, do_not_clear=False)],
                             [sg.Text("Risoluzione Problema ", font=16),sg.InputText(size=(65, 2), font=16, do_not_clear=False)],
                             [sg.Text("Problema risolto?    ", font=16),sg.OptionMenu(("Si", "No", "Forse"), size=(2, 2))],
                             [sg.Text("                                    "), sg.Button("Inserisci Guasto", font=16)],
                             [sg.Button("Logout", font=16),sg.Button("Indietro", font=16)]
                             ]
            return sg.Window("Aggiunta guasti", layout_insert,element_justification ='l', size=(740,480))

        # --------------------------------------------------- #
        # Finestra nella quale inserire i campi del quale effettuare la ricerca
        # --------------------------------------------------- #
        if self.tipo == "Ricerca":
            layout_ricerca = [[sg.Image(filename=find_path("logo.png"))],
                              [sg.Text("Turno                ", font=16),sg.OptionMenu(('Tutti','Mattina', 'Pomeriggio', 'Notte'), size=(12, 3))],
                              [sg.Text("Reparto del guasto   ", font=16), sg.OptionMenu(('Tutti','Mulini', 'Presse', 'Smalterie', 'Forni', 'Squadrature', 'Scelte', 'LGV', 'Generale'),size=(12, 3))],
                              [sg.Text("Ricerca della descrizione ", font=16),sg.InputText(size=(65, 2), font=16, do_not_clear=False)],
                              [sg.Text("                                                                     "), sg.Button("Cerca", font=16)],
                              [sg.Text("Indietro                                 ", font=16),sg.Button("Indietro", font=16)],
                              [sg.Text("Logout                                   ", font=16),sg.Button("Logout", font=16)]
                              ]
            return sg.Window("Ricerca guasti", layout_ricerca,element_justification ='l', size=(740,480))

        # --------------------------------------------------- #
        # Finestra di modifica password
        # --------------------------------------------------- #
        if self.tipo == "UtModificaPassword":
            layout_modifica = [[sg.Image(filename=find_path("logo.png"))],
                               [sg.Text("Nuova password ", font=16), sg.InputText(size=(45, 2), font=16, password_char='*')],
                               [sg.Text("Conferma password ", font=16), sg.InputText(size=(45, 2), font=16,password_char='*')],
                               [sg.Button("Cambia", font=16),sg.Button("Indietro", font=16)],
                               ]
            return sg.Window("Ricerca guasti", layout_modifica, element_justification='l', size=(740, 480))

        if self.tipo == "Aggiungi Manutentore":
            layout_aggiungi = [[sg.Image(filename=find_path("logo.png"))],
                               [sg.Text("Nome            ", font=16), sg.InputText(size=(45, 2), font=16)],
                               [sg.Text("Password        ", font=16), sg.InputText(size=(45, 2), font=16,password_char='*')],
                               [sg.Button("Aggiungi",font=16), sg.Button("Indietro", font=16)],
                               ]
            return sg.Window("Ricerca guasti",layout_aggiungi,element_justification='l', size=(740, 480))

        # --------------------------------------------------- #
        # Finestra dove mostro i risultati della ricerca
        # --------------------------------------------------- #
        if self.tipo == "Mostra":
            layout_mostra = [[sg.Image(filename=find_path("logo.png"))],
                             [sg.Table(values=self.risultati,
                                       headings=self.headings,
                                       max_col_width=35,
                                       auto_size_columns=True,
                                       alternating_row_color="DeepSkyBlue3",
                                       display_row_numbers=True,
                                       justification='right',
                                       num_rows=5,
                                       key='-TABLE-',
                                       vertical_scroll_only=False,
                                       row_height=35)],
                             [sg.Button("OK",font=16)]]
            return sg.Window("Risultati ricerca", layout_mostra, element_justification='l', size=(740, 480))

def app(manutentore, Db):

    window = gui("Welcome",manutentore,Db)
    while True:
        event, values = window.window.read()

        if event == sg.WIN_CLOSED:
            Db.conn.close()
            break

        # -------------------------------------------------------------------#
        # TENTO DI FARE IL LOGIN COME UTENTE O COME CAPOREPARTO
        # -------------------------------------------------------------------#
        if event == "Login":
            (user, password) = values[1], values[2]

            # controllo che siano presenti entrambi i valori
            if user == "" or password == "":
                sg.Popup("Inserire tutte le credenziali")

            # Controllo che si stia facendo il login come caporeparto
            if user == "caporeparto":
                manutentore = Manutentore(user,password)
                if Db.ok_manutentore(manutentore):
                    manutentore = Caporeparto()
                    window2 = gui("Caporeparto",manutentore,Db)
                    window,window2 = window2,window
                    window2.window.close()
                else: sg.popup_error("Password caporeparto errata")

            # Controllo che il manutentore sia presente nel db
            else:
                manutentore = Manutentore(user,password)
                if Db.ok_manutentore(manutentore):
                    window2 = gui("UtenteLoggato",manutentore,Db)
                    window,window2 = window2,window
                    window2.window.close()
                else: sg.popup_error("Password manutentore errata")
            # -------------------------------------------------------------------#

        # -------------------------------------------------------------------#
        # TORNO ALLA PAGINA INIZIALE
        # -------------------------------------------------------------------#
        if event == "Logout":
            window2 = gui("Welcome",  None, Db)
            window,window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # PASSO ALLA FINESTRA DI RICERCA TRA I VECCHI GUASTI
        # -------------------------------------------------------------------#
        if event == "Ricerca" or event == "OK":
            window2 = gui("Ricerca",manutentore,Db)
            window,window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # PASSO ALLA FINESTRA PER INSERIRE UN NUOVO GUASTO
        # -------------------------------------------------------------------#
        if event == "Guasto":
            window2 = gui("Aggiungi", manutentore, Db)
            window, window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # LEGGO I VALORI DALLA GUI, CREO UN GUASTO E TENTO DI INSERIRLO NEL DB
        # -------------------------------------------------------------------#
        if event == "Inserisci Guasto":
            print("inserisci guasto")
            (turno, reparto, descrizione, risoluzione, risolto) = values[1], values[2], values[3], values[4], values[5]
            data = datetime.today()
            g = Guasto(data, turno, reparto,manutentore.nome, descrizione,risoluzione, risolto)
            print(g.__dict__)
            if g.controlla_attributi():
                print("sono qua")
                manutentore.AggiuniGuasto(g, Db)
                sg.Popup("Inserimento andato a buon fine")
            else:
                sg.Popup("Attributi guasto errati")
                print(g.__dict__)

        # -------------------------------------------------------------------#
        # Torno alla pagina precedente
        # -------------------------------------------------------------------#
        if event == "Indietro":
            if isinstance(manutentore,Caporeparto): window2 = gui("Caporeparto",manutentore,Db)
            else: window2 = gui("UtenteLoggato",manutentore,Db)
            window,window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # PASSO ALLA SCHERMATA DOVE INSERIRE UN NUOVO MANUTENTORE
        # -------------------------------------------------------------------#
        if event == "Inserisci Manutentore":
            window2 = gui("Aggiungi Manutentore",manutentore, Db)
            window,window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # CREO UN OGGETTO MANUTENTORE E CERCO DI INSERIRLO NEL DB
        # -------------------------------------------------------------------#
        if event == "Aggiungi":
            nome, password = values[1],values[2]
            if nome == "" or password == "":
                sg.popup_error("Inserire tutti i campi")
            else:
                if Db.is_presente(nome):
                    sg.popup_error("Manutentore gia presente")
                else:
                    manutentore.AggiungiManutentore(nome, password, Db)
                    sg.popup_ok("Inserimento avvenuto con successo")

        # -------------------------------------------------------------------#
        # PASSO ALLA SCHERMATA DI MODIFICA PASSWORD
        # -------------------------------------------------------------------#
        if event == "Modifica Password":
            window2 = gui("UtModificaPassword",manutentore,Db)
            window,window2 = window2,window
            window2.window.close()

        # -------------------------------------------------------------------#
        # MODIFICO LA PASSWORD DELL'UTENTE
        # -------------------------------------------------------------------#
        if event == "Cambia":
            password1, password2 = values[1],values[2]

            if password1 == "" or password == "":
                sg.popup_error("Inserire la password e la conferma")

            elif password1 != password2:
                sg.popup_error("Le password non corrispondono")

            else:
                manutentore.password = password1
                Db.modifica_password(manutentore)
                sg.popup_ok("Password modificata con successo")
        # -------------------------------------------------------------------#

        # -------------------------------------------------------------------#
        # FORMULO LA QUERY
        # -------------------------------------------------------------------#
        if event == "Cerca":
            turno,reparto,descrizione = values[1],values[2],values[3]
            risultati = []
            tipo = 0

            # Cerco tutti i guasti in tutti i repasti
            if turno == "Tutti" and reparto == "Tutti" and descrizione== "":
                tipo = 1

            # Cerco solo nella descrizione
            elif turno == "Tutti" and reparto == "Tutti" and descrizione != "":
                tipo = 2

            # Cerco nel reparto e nella descrizione
            elif turno == "Tutti" and reparto != "Tutti" and descrizione != "":
                tipo = 3

            # Cerco nel turno, nel reparto e nella descrizione
            elif turno != "Tutti" and reparto != "Tutti" and descrizione != "":
                tipo = 4

            if tipo == 0:
                sg.popup_error("configurazione errata, inserire la descrizione per la ricerca")
            else:
                Db.query_guasto(tipo,turno,reparto,descrizione,risultati)

            # Se ci sono risultati, cambio finestra per mosrtarli
            if len(risultati) != 0:
                window2 = gui("Mostra",manutentore,Db,risultati)
                window,window2 = window2,window
                window2.window.close()
            else: sg.popup("Non ci sono risultati per questa ricerca")
        # -------------------------------------------------------------------#

if __name__ == "__main__":
    print("Questo è il modulo gui, \nPer eseguire il programma \"python3 main.py\"")
