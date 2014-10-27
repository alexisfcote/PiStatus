# coding=UTF-8
import requests
import bs4
import os
import time

consommationpath = os.path.join("/tmp/", "consommation.txt")
USER = "VLCNOAEC"


def main():
    response = requests.get(
        "https://extranet.videotron.com/services/secur/extranet/tpia/Usage.do?lang=FRENCH&compteInternet=" + USER)
    # on va chercher le HTML de la page avec request
    soup = bs4.BeautifulSoup(response.text)
    # on le lit avec bs4
    tables = soup.table
    a = tables.tr.table.tr.table.table.table.table.tr.next_sibling.next_sibling.next_sibling.next_sibling.td.next_siblings
    # on sort du tableau le chiffre de consommation voulue en Go
    try:
        consom = float(list(a)[11].string)
    except (ValueError):
        print "Pas un nombre valide"
        consom = float('nan')
    except:
        raise

    print("Vous avez consommé %f go") % consom
    # on enregistre dans un fichier
    f = open(consommationpath, "wb")
    f.write(str(consom))
    f.close()


def readConsom(maxConsom=150):
    try:
        f = open(consommationpath, "rb")
    except(IOError):
        main()
        f = open(consommationpath, "rb")
    except:
        raise
    # if the file is older than a day, refresh it
    filetime = os.path.getmtime(consommationpath)
    if not (filetime > (time.time() - 3600 * 24)):
        f.close()
        main()
        f = open(consommationpath, "rb")
    consom = float(f.readline())
    f.close()
    return (consom / maxConsom, time.ctime(filetime))


if __name__ == '__main__':
    main()
