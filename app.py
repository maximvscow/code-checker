from flask import Flask, jsonify, request, abort
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required
from config import Config
import json, base64, subprocess, sys, time, datetime
import timeit
import time


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)


# Роут для получения токена (регистрация)


@app.route('/register', methods=['POST'])
def register():
    params = request.get_json(force=True)
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def logon():
    params = request.get_json(force=True)
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


@app.route('/chek', methods=['GET', 'POST'])  # Роут для запуска тестируемого кода из JSON с параметром base64str
@jwt_required()
def get_code():                               # Для запуска необходимо создать venv2
    try:
        req = base64.b64decode(request.json["base64str"])
        with open('test.py', 'w') as f:
            f.write(req.decode("UTF-8"))
        start = time.time()
        execute = subprocess.Popen(["venv2/Scripts/python.exe", "test.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time_taken = (time.time() - start)
        outs, errs = execute.communicate()
        outs = outs.decode('UTF-8')
        errs = errs.decode('UTF-8')
        result = {
            'output': outs,
            'errors': errs,
            'time_taken': time_taken
        }
        execute.terminate()
        return jsonify(result)
    except Exception as e:
        abort(500)


@app.errorhandler(500)
def err_handler(e):
    err_msg = {
        'type': 'error',
        'msg': 'Sorry, unexpected error'
    }
    return err_msg


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == "__main__":
    app.run(debug=False)
