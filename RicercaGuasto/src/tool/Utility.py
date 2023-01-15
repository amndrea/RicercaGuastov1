import os

def replace(stringa):
    stringa = stringa.replace("[", "")
    stringa = stringa.replace("]"," ")
    stringa = stringa.replace(",","")
    stringa = stringa.replace(" ","")
    stringa = stringa.replace("(","")
    stringa = stringa.replace(")","")
    return stringa

def find_path(stinga):
    """
    Metodo che a partire dal path del file attuale ritorna il path del file di configurazione del database
    :return: path del file di configurazione del database
    """
    s = (os.path.realpath(__file__))
    i = s.find('\\src')
    s = s[0:i]+'\\data\\'+stinga
    return s


if __name__ == '__main__':
    find_path()
