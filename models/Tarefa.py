from sqlalchemy import Column, Integer, String, Date, ForeignKey, inspect
from sqlalchemy_serializer import SerializerMixin

import config
from database.database import metadata, Base, engine


class Tarefa(Base, SerializerMixin):
    __tablename__ = 'tarefa'
    metadata

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200))
    dataPrevistaConclusao = Column(Date)
    dataConclusao = Column(Date)
    idUsuario = Column(Integer, ForeignKey('usuario.id'))

if not inspect(engine).has_table('tarefa', schema=config.MYSQL_DATABASE):
    Tarefa.__table__.create(engine)
