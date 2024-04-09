from datetime import datetime
from typing import Optional

from app.database import Session

from app.entity import ServicoEntity, AgendamentoServicoEntity

from app.schema.agendamento_servicos import NovoAgendamentoServicoSchema, AlterarAgendamentoServicoSchema, AgendamentoServicoSchema

from .excecoes import AgendamentoNaoEncontradoException, ExclusaoAgendamentoForaDoHorarioPermitidoException

from .extensoes_data import para_data_hora_servidor, alterar_data_hora_inicio, alterar_data_hora_fim, formatar_data_hora_servidor, para_data_servidor

PRAZO_EXCLUSAO_EM_HORAS = 4

class AgendamentoServicoController:
    """
    Acessa as entidades para fornecer os dados para as rotas de agendamento de serviços.
    """

    def agendar_servico(self, schema: NovoAgendamentoServicoSchema) -> None:
        """
        Agenda um serviço para um cliente e seu pet.
        """
        session = Session()
        data_agendamento = para_data_hora_servidor(schema.data_agendamento)
        agendamento = AgendamentoServicoEntity(data_agendamento=data_agendamento, nome_cliente=schema.nome_cliente, 
                                               nome_pet=schema.nome_pet, valor_servico=schema.valor_servico, 
                                               servico_id=schema.servico_id, eh_cancelado=schema.cancelado)
        session.add(agendamento)
        session.commit()
        session.close() 

    def alterar_agendamento_servico(self, schema: AlterarAgendamentoServicoSchema) -> None:
        """
        Altera um registro de agendamento de serviço.
        """
        session = Session()
        data_agendamento = para_data_hora_servidor(schema.data_agendamento)
        agendamento: Optional[AgendamentoServicoEntity] = session.get(AgendamentoServicoEntity, schema.id)
        if not agendamento:
            raise AgendamentoNaoEncontradoException('Agendamento não encontrado!')
        agendamento.data_agendamento = data_agendamento
        agendamento.eh_cancelado = schema.cancelado
        agendamento.nome_cliente = schema.nome_cliente
        agendamento.nome_pet = schema.nome_pet
        agendamento.servico_id = schema.servico_id
        agendamento.valor_servico = schema.valor_servico
        session.commit()
        session.close()

    def excluir_agendamento_servico(self, id: int) -> None:
        """
        Exclui o agendamento de serviço da base de dados
        """
        session = Session()
        agendamento: Optional[AgendamentoServicoEntity] = session.get(AgendamentoServicoEntity, id)
        if not agendamento:
            session.close()
            raise AgendamentoNaoEncontradoException('Agendamento não encontrado!')
        if self.__eh_exclusao_fora_do_prazo__(agendamento.data_agendamento): 
            session.close()
            raise ExclusaoAgendamentoForaDoHorarioPermitidoException('Não é possível excluir agendamento!')
        session.delete(agendamento)
        session.commit()
        session.close()

    def buscar_agendamentos_por_data(self, data_agendamento_inicio: str, 
                                     data_agendamento_fim: str) -> list[AgendamentoServicoSchema]:
        """
        Busca os agendamentos dado argumentos de pesquisa.

        Arguments:
            data_agendamento_inicio: Data de agendamento início.
            data_agendamento_fim: Data de agendamento.
        """

        data_hora_agendamento_inicio = alterar_data_hora_inicio(para_data_servidor(data_agendamento_inicio))
        data_hora_agendamento_fim = alterar_data_hora_fim(para_data_servidor(data_agendamento_fim))
        session = Session()
        agendamentos = session.query(AgendamentoServicoEntity). \
            filter(AgendamentoServicoEntity.data_agendamento >= data_hora_agendamento_inicio, 
                   AgendamentoServicoEntity.data_agendamento <= data_hora_agendamento_fim). \
            all()
        
        schemas = [self.__mapear_entity_para_schema__(agendamento) for agendamento in agendamentos]
        session.close()
        return schemas

    def buscar_agendamento_por_id(self, id: int) -> AgendamentoServicoSchema:
        """
        Retorna o agendamento pelo seu id ou None caso não encontre.
        """
        session = Session()
        agendamento: Optional[AgendamentoServicoEntity] = session.get(AgendamentoServicoEntity, id)
        if not agendamento:
            session.close()
            raise AgendamentoNaoEncontradoException('Agendamento não encontrado!')
        
        schema = self.__mapear_entity_para_schema__(agendamento)
        session.close()
        return schema
    
    def __eh_exclusao_fora_do_prazo__(self, data_agendamento: datetime) -> bool:
        """
        Valida se é permitido exclusão do agendamento do serviço.
        """
        duracao = datetime.now() - data_agendamento
        duracao_em_seg = duracao.total_seconds()
        duracao_em_horas = divmod(duracao_em_seg, 3600)[0]
        return duracao_em_horas < PRAZO_EXCLUSAO_EM_HORAS
    
    def __mapear_entity_para_schema__(self, agendamento: AgendamentoServicoEntity) -> AgendamentoServicoSchema:
        """
        Mapeia instancia de 'AgendamentoServicoEntity' para 'AgendamentoServicoSchema'.
        """
        data_agendamento = formatar_data_hora_servidor(agendamento.data_agendamento)
        data_inclusao = formatar_data_hora_servidor(agendamento.data_inclusao)
        return AgendamentoServicoSchema(id=agendamento.id, data_agendamento=data_agendamento, 
                                        nome_cliente=agendamento.nome_cliente, nome_pet=agendamento.nome_pet, 
                                        valor_servico=agendamento.valor_servico, servico_id=agendamento.servico_id, 
                                        servico_titulo='', cancelado=agendamento.eh_cancelado, 
                                        data_inclusao=data_inclusao)