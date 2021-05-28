from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields
from dtos.UsuarioDTO import ErroDTO

import json

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
                return Response(json.dumps(ErroDTO("Parâmetros de entrada inválidos", 400).__dict__), status=400, mimetype='application/json')

            return Response("Login autenticado com sucesso", status=200, mimetype='application/json')
        except Exception as e:
            return Response(json.dumps(ErroDTO("Não foi possível efetuar o login, tente novamente", 500).__dict__), status=500, mimetype='application/json')
