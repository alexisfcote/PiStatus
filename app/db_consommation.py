# coding=UTF-8
import requests
import bs4
import datetime
from app import models, db


def fetch_consom(user):
    """
    :param user: Name of the videotron user
    :return: bandwidth used as int or nan if invalid
    """
    response = requests.get(
        "https://extranet.videotron.com/services/secur/extranet/tpia/Usage.do?lang=FRENCH&compteInternet=" + user)
    # on va chercher le HTML de la page avec request
    soup = bs4.BeautifulSoup(response.text)
    # on le lit avec bs4
    tables = soup.table
    a = tables.tr.table.tr.table.table.table.table.tr.next_sibling.next_sibling.next_sibling.next_sibling.td.next_siblings
    # on sort du tableau le chiffre de consommation voulue en Go
    try:
        consom = int(float(list(a)[11].string))
    except (ValueError):
        print "Pas un nombre valide"
        consom = int(-1)
    except:
        raise
    return consom


def update_user(dbuser, force=False):
    """ Update the database with new bandwidth data from website
    :param dbuser: userfrom the database
    :return: nothing
    :type dbuser: models.User
    """
    if (datetime.datetime.now() - dbuser.timestamp > datetime.timedelta(hours=4)
            or force or dbuser.bandwidth_used == -1):
        dbuser.bandwidth_used = fetch_consom(dbuser.videotron_username)
        dbuser.timestamp = datetime.datetime.now()
        db.session.commit()


def new_user(videotronuser, max_consom):
    """ Create a new user in the database
    :param videotronuser: videotron user code
    :param max_consom: maximum allowed consommation
    :return:
    """
    user = models.User(videotron_username=videotronuser, bandwidth_allowed=max_consom, bandwidth_used=0,
                       timestamp=datetime.datetime.now())
    db.session.add(user)
    db.session.commit()
    update_user(user, force=True)

def del_user(user):
    """ Delete a user from the database
    :param user: user to delete
    :return:
    """
    db.session.delete(user)
    db.session.commit()
