import json
from functools import wraps

import jwt
from flask import request, Response

import config
from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioBaseDTO
from services import JWTService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers

        if not 'Authorization' in headers:
            return Response(
                json.dumps(ErroDTO("É necessário um token para essa requisição.", 400).__dict__),
                status=400,
                mimetype='application/json'
            )

        try:
            #Pegar Token no Header
            token = str(headers['Authorization']).replace('Bearer ', '')

            user_id = JWTService.decodificar_token(token)

            usuario_atual = UsuarioBaseDTO("Admin", config.LOGIN_TESTE)

        except jwt.ExpiredSignatureError:
            return Response(
                json.dumps(ErroDTO("Token expirado.", 401).__dict__),
                status=401,
                mimetype='application/json'
            )
        except jwt.InvalidTokenError:
            return Response(
                json.dumps(ErroDTO("Token inválido.", 401).__dict__),
                status=401,
                mimetype='application/json'
            )
        except Exception:
            return Response(
                json.dumps(ErroDTO("Erro inesperado no servidor, favor tentar novamente", 500).__dict__),
                status=500,
                mimetype='application/json'
            )

        return f(usuario_atual, *args, **kwargs)

    return decorated

