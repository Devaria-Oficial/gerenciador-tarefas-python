from database.database import SessionLocal
from models.Tarefa import Tarefa

db = SessionLocal()

class TarefaService:
    def __init__(self):
        pass

    def filter(self, idUsuario, periodoDe, periodoAte, status):
        tarefas = db.query(Tarefa).filter(Tarefa.idUsuario == idUsuario)

        if status == '1':
            tarefas = tarefas.filter(Tarefa.dataConclusao == None)
        elif status == '2':
            tarefas = tarefas.filter(Tarefa.dataConclusao.isnot(None))

        if periodoDe:
            tarefas = tarefas.filter(Tarefa.dataPrevistaConclusao >= periodoDe)

        if periodoAte:
            tarefas = tarefas.filter(Tarefa.dataPrevistaConclusao <= periodoAte)

        return tarefas.all()

    def filter_by_id(self, id):
        return db.query(Tarefa).filter(Tarefa.id == id).first()

    def filter_by_nome(self, nome, idUsuario):
        return db.query(Tarefa).filter(Tarefa.nome == nome, Tarefa.idUsuario == idUsuario).first()

    def criar_tarefa(self, nome, dataPrevistaConclusao, dataConclusao, idUsuario):
        if self.filter_by_nome(nome, idUsuario):
            return None

        nova_tarefa = Tarefa(
            nome=nome,
            dataPrevistaConclusao=dataPrevistaConclusao,
            dataConclusao=dataConclusao,
            idUsuario=idUsuario
        )

        db.add(nova_tarefa)
        db.commit()

        return nova_tarefa

    def deletar_tarefa(self, idUsuario, id):
        tarefa_encontrada = self.filter_by_id(id)

        if not tarefa_encontrada.idUsuario == idUsuario:
            return None

        db.query(Tarefa).filter(Tarefa.id == id).delete()
        db.commit()

        return True

    def atualizar_tarefa(self, idUsuario, tarefa):
        tarefa_encontrada = self.filter_by_id(tarefa.id)

        if not tarefa_encontrada.idUsuario == idUsuario:
            return None

        db.commit()

        return True

