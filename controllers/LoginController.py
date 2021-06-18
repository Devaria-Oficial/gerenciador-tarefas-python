from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields
from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioLoginDTO
from services import JWTService
from services.UsuarioService import UsuarioService

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

            erros = []

            if not body:
                return Response(
                    json.dumps(ErroDTO(400, "Body da requisição está vazio.").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            if not "login" in body:
                erros.append("Campo 'login' é obrigatório.")

            if not "senha" in body:
                erros.append("Campo 'senha' é obrigatório.")

            if erros:
                return Response(
                    json.dumps(ErroDTO(400, erros).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            usuario_encontrado = UsuarioService().login(body["login"], body["senha"])

            if usuario_encontrado:
                token = JWTService.gerar_token(usuario_encontrado.id)

                return Response(
                    json.dumps(UsuarioLoginDTO(usuario_encontrado.nome, usuario_encontrado.email, token).__dict__),
                    status=200,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(ErroDTO(401, "Usuário ou Senha incorretos, favor tentar novamente.").__dict__),
                status=401,
                mimetype='application/json')
        except Exception as e:
            print(e)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível efetuar o login, tente novamente.").__dict__),
                status=500,
                mimetype='application/json'
            )
