from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

SQLALCHEMY_DATABASE_URI = f'mysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

engine.execute(f'CREATE DATABASE IF NOT EXISTS {config.MYSQL_DATABASE}')
engine.execute(f'USE {config.MYSQL_DATABASE}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

metadata = MetaData()
