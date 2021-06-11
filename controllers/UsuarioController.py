from flask import Blueprint, Response, request
from flask_restx import Namespace, Resource, fields
from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioCreateDTO
from services.UsuarioService import UsuarioService

import json

usuario_controller = Blueprint('usuario_controller', __name__)

api = Namespace('Usuário')

user_fields = api.model('UsuarioBaseDTO', {
    'nome': fields.String,
    'email': fields.String
})


@api.route('', methods=['POST'])
class UsuarioController(Resource):
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

            if not "nome" in body:
                erros.append("Campo 'nome' é obrigatório.")

            if not "email" in body:
                erros.append("Campo 'email' é obrigatório.")

            if not "senha" in body:
                erros.append("Campo 'senha' é obrigatório.")

            if erros:
                return Response(
                    json.dumps(ErroDTO(400, erros).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            usuario_criado = UsuarioService().criar_usuario(body['nome'], body['email'], body['senha'])

            if not usuario_criado:
                return Response(
                    json.dumps(ErroDTO(400, "E-mail já cadastrado no sistema.").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(UsuarioCreateDTO(usuario_criado.id, usuario_criado.nome, usuario_criado.email, usuario_criado.senha).__dict__),
                status=201,
                mimetype='application/json'
            )
        except Exception as e:
            print(e)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível realizar sua requisição, tente novamente.").__dict__),
                status=500,
                mimetype='application/json'
            )
