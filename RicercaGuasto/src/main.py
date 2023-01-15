from database.postgres import Database
from src.gui.gui import app

if __name__ == '__main__':
    Db = Database("pgsql.ini")
    App = app(None,Db)