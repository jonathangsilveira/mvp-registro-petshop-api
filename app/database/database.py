from sqlalchemy_utils import database_exists, create_database
import os

db_path = "app/database"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/petshop.sqlite3' % db_path

# cria o banco se ele não existir 
if not database_exists(db_url):
    create_database(db_url) 
