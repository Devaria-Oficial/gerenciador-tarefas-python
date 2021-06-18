from functools import wraps
from flask import request, Response
from dtos.ErroDTO import ErroDTO
from services import JWTService
from services.UsuarioService import UsuarioService

import json
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers

        if not 'Authorization' in headers:
            return Response(
                json.dumps(ErroDTO(400, "É necessário um token para essa requisição.").__dict__),
                status=400,
                mimetype='application/json'
            )

        try:
            #Pegar Token no Header
            token = str(headers['Authorization']).replace('Bearer ', '')

            id_usuario = JWTService.decodificar_token(token)

            usuario_atual = UsuarioService().filter_by_id(id_usuario)

            if not usuario_atual:
                return Response(
                    json.dumps(ErroDTO(401, "Token inválido.").__dict__),
                    status=401,
                    mimetype='application/json'
                )

        except jwt.ExpiredSignatureError:
            return Response(
                json.dumps(ErroDTO(401, "Token expirado.").__dict__),
                status=401,
                mimetype='application/json'
            )
        except jwt.InvalidTokenError:
            return Response(
                json.dumps(ErroDTO(401, "Token inválido.").__dict__),
                status=401,
                mimetype='application/json'
            )
        except Exception:
            return Response(
                json.dumps(ErroDTO(500, "Erro inesperado no servidor, favor tentar novamente").__dict__),
                status=500,
                mimetype='application/json'
            )

        return f(usuario_atual, *args, **kwargs)

    return decorated

