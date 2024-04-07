from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .database.database import db_url
from .entity.entities import BaseEntity, ServicoEntity
from .schema.servicos import *
from .schema.erro import *

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

BaseEntity.metadata.create_all(engine)