from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, Response, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

from app import *

info = Info(title="MVP Registro Petshop API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

servico_tag = Tag(name='Serviço', description='Adição e visualização de serviços à base.')
servico_ativo_tag = Tag(name='Serviços Ativo', description='Exibição de serviços ativos.')

@app.route('/api')
def documentation():
    """Redireciona para visualização do estilo de documentação Swagger.
    """
    return redirect('/openapi/swagger')

@app.post('/api/servico', tags=[servico_tag], 
          responses={200: {}, 400: ErroSchema, 409: ErroSchema})
def adicionar_servico(form: NovoServicoSchema):
    """
    Adicionar um novo serviço na base de dados.
    """
    try:
        servico = ServicoEntity(titulo=form.titulo, preco_unitario=form.preco_unitario, 
                               eh_ativo=form.eh_ativo)
        session = Session()
        session.add(servico)
        session.commit()
        session.close()
        
        return {}, 200
    except IntegrityError as cause:
        erro = ErroSchema()
        erro.mensagem = f'Serviço "{servico.titulo}" já cadastrado!'
        print(f'{erro.mensagem}: {cause}')
        return apresentar_erro(erro), 409
    except Exception as cause:
        erro = ErroSchema()
        erro.mensagem = 'Erro ao adicionar novo serviço!'
        print(f'{erro.mensagem}: {cause}')
        return apresentar_erro(erro), 400
    
@app.get('/api/servico', tags=[servico_ativo_tag], 
         responses={200: ServicosAtivosViewSchema, 400: ErroSchema})
def listar_servicos_ativos():
    """
    Lista os serviços com status ativo na base de dados.
    """
    try:
        session = Session()
        servicos = session.query(ServicoEntity).filter(ServicoEntity.eh_ativo == True).all()
        servicos_ativos: list[ServicoAtivoSchema] = []
        for servico in servicos:
            servico_ativo = ServicoAtivoSchema(id=servico.id, titulo=servico.titulo, 
                                               preco_unitario=servico.preco_unitario)
            servicos_ativos.append(servico_ativo)
        
        session.close()
        return apresentar_servicos_ativos(servicos_ativos), 200
    except Exception as cause:
        erro = ErroSchema()
        erro.mensagem = 'Erro ao listar serviços ativos!'
        print(f'{erro.mensagem}: {cause}')
        return apresentar_erro(erro), 400