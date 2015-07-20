from flask import render_template, redirect, url_for, flash, request
from subprocess import call, check_output
from os import system

from app import app
from models import User
import transcodeDaemon
import db_consommation

transmissionUser = "transmission-daemon"


@app.route("/")
@app.route("/index")
def main():
    a = check_output(["ps", "-e", "-o", "pid,comm"])
    isopen = 'transmission-da' in a
    if isopen:
        string = "running"
        value = 1
    else:
        string = "not running"
        value = 0

    isopen = 'minidlna' in a
    if isopen:
        string_minidlna = "running"
        value_minidlna = 1
    else:
        string_minidlna = "not running"
        value_minidlna = 0

    # Transcode status
    trans_status = transcode_status()

    # Consommation ratio
    for u in User.query.all():
        db_consommation.update_user(u)


    templatedata = {
        'isOpen': string,
        'isOpenBool': value,
        's_minidlna': string_minidlna,
        'v_minidlna': value_minidlna,
        'trans_status': trans_status,
        'users': User.query.all(),
    }
    return render_template('status.html', **templatedata)


@app.route("/open/")
def open_transmission():
    #system("su -c " + transmissionUser + " -s /bin/sh transmission")
    call(["service", "transmission-daemon", "start"])
    flash("transimission daemon started")
    return redirect(url_for('main'))


@app.route("/close/")
def close():
    call(["service", "transmission-daemon", "stop"])
    flash("transmission daemon stopped")
    return redirect(url_for('main'))


@app.route("/start_minidlna/")
def start_minidlna():
    call(["service", "minidlna", "start"])
    flash("minidlna started")
    return redirect(url_for('main'))


@app.route("/stop_minidlna/")
def stop_minidlna():
    call(["service", "minidlna", "stop"])
    flash("minidlna stopped")
    return redirect(url_for('main'))


@app.route("/scan_minidlna/")
def scan_minidlna():
    call(["minidlna", "-R", "-p", "8200"])
    flash("minidlna searching for new files")
    return redirect(url_for('main'))


def transcode_status(cmd="status"):
    return transcodeDaemon.client(cmd)


@app.route("/transcode_startconversion")
def transcode_startconversion():
    msg = transcode_status("startconversion")
    flash(msg)
    return redirect(url_for('main'))

@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    Vuser=request.form['videotronuser']
    consom=int(request.form['consomax'])
    db_consommation.new_user(Vuser, consom)
    flash("added user " + Vuser)
    return redirect(url_for('main'))

@app.route("/del_user/<user>", methods=['POST', 'GET'])
def del_user(user):
    user_to_del = User.query.filter_by(videotron_username=user).first()
    db_consommation.del_user(user_to_del)
    flash("deleted user " + user)
    return redirect(url_for('main'))




@app.errorhandler(404)
def error404(error):
    return "error" + str(error.code), error.code
