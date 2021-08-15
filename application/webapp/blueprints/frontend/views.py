from flask import abort, render_template
from webapp.ext.database import instance

def index():
    return render_template("index.html")

def monitored():
    result = instance.db['monitored_animals'].find()
    return render_template("monitored.html", monitored_animals=result, title="Animais Monitorados")

def identified():
    result = instance.db['identified_animals'].find()
    return render_template("identified.html", identified_animals=result, title="Animais Identificados")

def not_identified():
    result = instance.db['identified_animals'].find()
    return render_template("notidentified.html", identified_animals=result, title="Animais não Identificados")

def notification():
    result = instance.db['notifications'].find()
    return render_template("notification.html", notifications=result, title="Notificações")
