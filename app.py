  
from flask import Flask, render_template,session, request, Response, url_for, redirect
from flask_restful import Resource, Api, reqparse, fields, marshal
import sqlite3

DATABASE = '/db/thesisManage'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def base():
    return render_template('base.html') #loads base for now to be changes


if __name__ == '__main__':
    app.run(use_reloader=False, debug=True)





