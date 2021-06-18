import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_restx import Namespace, Resource

from dtos.ErroDTO import ErroDTO
from dtos.SucessoDTO import SucessoDTO
from services.TarefaService import TarefaService
from utils import Decorators
from utils.Validacao import validar_data

tarefa_controller = Blueprint('tarefa_controller', __name__)

api = Namespace('Tarefa')

@api.route('', methods=['POST', 'GET'])
@api.route('/<idTarefa>', methods=['DELETE', 'PUT'])
class TarefaController(Resource):
    @Decorators.token_required
    def post(usuario, controller):
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

            if not "dataPrevistaConclusao" in body:
                erros.append("Campo 'dataPrevistaConclusao' é obrigatório.")
            elif not validar_data(body['dataPrevistaConclusao']):
                erros.append("Campo 'dataPrevistaConclusao' inválido, formato deve ser 'yyyy-mm-dd'")
            elif validar_data(body['dataPrevistaConclusao']) < datetime.now():
                erros.append("Data de previsão não pode ser menor que a data de hoje.")

            if erros:
                return Response(
                    json.dumps(ErroDTO(400, erros).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            tarefa_criada = TarefaService().criar_tarefa(body['nome'], body['dataPrevistaConclusao'], None, usuario.id)

            if not tarefa_criada:
                return Response(
                    json.dumps(ErroDTO(400, "Já existe uma tarefa cadastrada com esse nome.").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(tarefa_criada.to_dict()),
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

    @Decorators.token_required
    def delete(usuario, controller, idTarefa):
        try:
            if not TarefaService().filter_by_id(idTarefa):
                return Response(
                    json.dumps(ErroDTO(400, "Tarefa não encontrada").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            tarefa_deletada = TarefaService().deletar_tarefa(usuario.id, idTarefa)

            if not tarefa_deletada:
                return Response(
                    json.dumps(ErroDTO(400, "Não foi possível realizar sua requisição, favor tentar novamente").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(SucessoDTO(200, "Tarefa deletada com sucesso.").__dict__),
                status=200,
                mimetype='application/json'
            )
        except Exception:
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível realizar sua requisição, tente novamente.").__dict__),
                status=500,
                mimetype='application/json'
            )

    @Decorators.token_required
    def put(usuario, controller, idTarefa):
        try:
            if not TarefaService().filter_by_id(idTarefa):
                return Response(
                    json.dumps(ErroDTO(400, "Tarefa não encontrada").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            body = request.get_json()

            erros = []

            if not body:
                return Response(
                    json.dumps(ErroDTO(400, "Body da requisição está vazio.").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            if not 'nome' in body and not 'dataConclusao' in body and not 'dataPrevistaConclusao' in body:
                erros.append("Favor enviar os dados que deseja atualizar.")

            if 'dataConclusao' in body and not validar_data(body['dataConclusao']):
                erros.append("Campo 'dataConclusao' inválido, formato deve ser 'yyyy-mm-dd'.")

            if 'dataPrevistaConclusao' in body and not validar_data(body['dataPrevistaConclusao']):
                erros.append("Campo 'dataPrevistaConclusao' inválido, formato deve ser 'yyyy-mm-dd'.")

            if 'nome' in body:
                tarefa_encontrada = TarefaService().filter_by_nome(body['nome'], usuario.id)

                if tarefa_encontrada:
                    erros.append("Já existe uma tarefa cadastrada com esse nome.")

            if erros:
                return Response(
                    json.dumps(ErroDTO(400, erros).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            tarefa_encontrada = TarefaService().filter_by_id(idTarefa)

            if 'nome' in body:
                tarefa_encontrada.nome = body['nome']

            if 'dataConclusao' in body:
                tarefa_encontrada.dataConclusao = body['dataConclusao']

            if 'dataPrevistaConclusao' in body:
                tarefa_encontrada.dataPrevistaConclusao = body['dataPrevistaConclusao']

            tarefa_atualizada = TarefaService().atualizar_tarefa(usuario.id, tarefa_encontrada)

            if not tarefa_atualizada:
                return Response(
                    json.dumps(ErroDTO(400, "Não foi possível realizar sua requisição, favor tentar novamente").__dict__),
                    status=400,
                    mimetype='application/json'
                )

            return Response(
                json.dumps(SucessoDTO(200, "Tarefa atualizada com sucesso.").__dict__),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(e)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível realizar sua requisição, tente novamente.").__dict__),
                status=500,
                mimetype='application/json'
            )

    @Decorators.token_required
    def get(usuario, controller):
        try:
            erros = []

            if 'periodoDe' in request.args and not validar_data(request.args.get('periodoDe')):
                erros.append("Campo 'periodoDe' está inválido, formato deve ser 'yyyy-mm-dd'")

            if 'periodoAte' in request.args and not validar_data(request.args.get('periodoAte')):
                erros.append("Campo 'periodoAte' está inválido, formato deve ser 'yyyy-mm-dd'")

            if 'status' in request.args \
                    and not request.args.get('status') == '0' \
                    and not request.args.get('status') == '1' \
                    and not request.args.get('status') == '2':
                erros.append("Campo 'status' com opção inválida. Favor informar um status 0, 1 ou 2.")

            if erros:
                return Response(
                    json.dumps(ErroDTO(400, erros).__dict__),
                    status=400,
                    mimetype='application/json'
                )

            periodoDe = request.args.get('periodoDe')
            periodoAte = request.args.get('periodoAte')
            status = request.args.get('status') if request.args.get('status') else '0'

            tarefas = TarefaService().filter(usuario.id, periodoDe, periodoAte, status)

            return Response(
                json.dumps([ob.to_dict() for ob in tarefas]),
                status=200,
                mimetype='application/json'
            )

        except Exception as e:
            print(e)
            return Response(
                json.dumps(ErroDTO(500, "Não foi possível realizar sua requisição, tente novamente.").__dict__),
                status=500,
                mimetype='application/json'
            )