import os.path
from configparser import ConfigParser


def config(filename, section='postgresql'):
    file = os.path.realpath(__file__)
    # Creo il parser 
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        parametri = parser.items(section)
        for param in parametri:
            db[param[0]] = param[1]
    else:
        raise Exception('Sezione {0} non trovata in  {1} '.format(section, filename))
    return db
