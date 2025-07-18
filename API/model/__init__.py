from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, CheckConstraint, event, DateTime
import os
from datetime import datetime


# importando os elementos definidos no modelo
from model.base import Base
from model.preprocessador import PreProcessador
from model.avaliador import Avaliador
from model.modelo import Model
from model.pipeline import Pipeline
from model.usuario import Usuario
from model.label_encoder import Label
from model.carregador import Carregador


db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Habilita os CHECK CONSTRAINTS no SQLite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # Ativa constraints como CHECK e FOREIGN KEY
    cursor.close()

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)
session = Session()

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
    Base.metadata.create_all(engine)