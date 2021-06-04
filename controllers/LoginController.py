from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

import config
from dtos.ErroDTO import ErroDTO

import json

from dtos.UsuarioDTO import UsuarioLoginDTO
from services import JWTService

login_controller = Blueprint('login_controller', __name__)

api = Namespace('Login', description='Realizar login na aplicação')

login_fields = api.model('LoginDTO', {
    'login': fields.String,
    'senha': fields.String
})

user_fields = api.model('UsuarioDTO', {
    'name': fields.String,
    'email': fields.String,
    'token': fields.String,
})

@api.route('/login', methods=['POST'])
class Login(Resource):
    @api.doc(responses={200: 'Login realizado com sucesso.'})
    @api.doc(responses={400: "Parâmetros de entrada inválidos."})
    @api.doc(responses={500: "Não foi possível efetuar o login, tente novamente"})
    @api.response(200, 'Success', user_fields)
    @api.expect(login_fields)
    def post(self):
        try:
            body = request.get_json()

            if not body or "login" not in body or "senha" not in body:
                return Response(
                    json.dumps(ErroDTO("Parâmetros de entrada inválidos.", 400).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            if body["login"] == config.LOGIN_TESTE and body["senha"] == config.SENHA_TESTE:
                id_usuario = 1

                token = JWTService.gerar_token(id_usuario)

                return Response(
                    json.dumps(UsuarioLoginDTO("Admin", config.LOGIN_TESTE, token).__dict__),
                    status=200,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(ErroDTO("Usuário ou Senha incorretos, favor tentar novamente.", 401).__dict__),
                status=401,
                mimetype='application/json')
        except Exception:
            return Response(
                json.dumps(ErroDTO("Não foi possível efetuar o login, tente novamente.", 500).__dict__),
                status=500,
                mimetype='application/json'
            )
