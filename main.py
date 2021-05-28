from flask import Flask
from flask_restx import Api

import config
from controllers.LoginController import login_controller
from controllers.LoginController import api as ns_login

app = Flask(__name__)

api = Api(app,
          version='1.0',
          title='Gerenciador de Tarefas',
          description='Aplicação para gerenciar tarefas - Devaria 2021',
          doc='/docs')

def register_blueprints():
    app.register_blueprint(login_controller, url_prefix=config.API_BASE_URL)

def add_namespaces():
    api.add_namespace(ns_login, path=config.API_BASE_URL)

if __name__ == '__main__':
    register_blueprints()
    add_namespaces()

    app.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)