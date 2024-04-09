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
        controller_servico.adicionar_servico(schema=form)
        
        return {}, 200
    except IntegrityError as cause:
        erro = ErroSchema()
        erro.mensagem = f'Serviço "{form.titulo}" já cadastrado!'
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
    try:
        servicos_ativos = controller_servico.recuperar_servicos_ativos()
        return apresentar_servicos_ativos(servicos_ativos), 200
    except Exception as cause:
        erro = ErroSchema()
        erro.mensagem = 'Erro ao listar serviços ativos!'
        print(f'{erro.mensagem}: {cause}')
        return apresentar_erro(erro), 400
    
@app.post('/api/agendamento_servico/novo', tags=[], 
          responses={200: {}, 400: ErroSchema, 409: ErroSchema})
def novo_agendamento(form: NovoAgendamentoServicoSchema):
    """
    Registra um novo agendamento de serviço.
    """
    try:
        controller_agendamento.agendar_servico(form)
        return {}, 200
    except IntegrityError:
        mensagem_erro = f'Já existe um agendamento para esta data e horário: {form.data_agendamento}'
        schema = ErroSchema(mensagem=mensagem_erro)
        return apresentar_erro(schema), 409
    except Exception as erro:
        print(erro)
        mensagem_erro = f'Erro ao agendar serviço para a data {form.data_agendamento}!'
        schema = ErroSchema(mensagem=mensagem_erro)
        return apresentar_erro(schema), 400
    
@app.delete('/api/agendamento_servico', tags=[], 
            responses={200: {}, 400: ErroSchema})
def excluir_agendamento(form: ExcluirAgendamentoServicoSchema):
    """
    """
    try:
        controller_agendamento.excluir_agendamento_servico(form.id)
        return {}, 200
    except Exception as erro:
        print(erro)
        schema = ErroSchema(mensagem=f'Erro ao excluir agendamento de serviço!')
        return apresentar_erro(schema), 400