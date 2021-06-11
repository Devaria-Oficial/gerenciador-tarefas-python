from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from controllers.LoginController import login_controller
from controllers.LoginController import api as ns_login
from controllers.UsuarioController import usuario_controller
from controllers.UsuarioController import api as ns_usuario

import config

app = Flask(__name__)

CORS(app)

api = Api(app,
          version='1.0',
          title='Gerenciador de Tarefas',
          description='Aplicação para gerenciar tarefas - Devaria 2021',
          doc='/docs')

def register_blueprints():
    app.register_blueprint(login_controller, url_prefix=config.API_BASE_URL)
    app.register_blueprint(usuario_controller, url_prefix=config.API_BASE_URL+'/usuario')

def add_namespaces():
    api.add_namespace(ns_login, path=config.API_BASE_URL)
    api.add_namespace(ns_usuario, path=config.API_BASE_URL+'/usuario')

if __name__ == '__main__':
    register_blueprints()
    add_namespaces()

    app.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)