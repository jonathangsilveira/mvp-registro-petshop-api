from datetime import datetime
from typing import Optional

from app.database import Session

from app.entity import ServicoEntity, AgendamentoServicoEntity

from app.schema.agendamento_servicos import NovoAgendamentoServicoSchema, AlterarAgendamentoServicoSchema, AgendamentoServicoSchema

from .excecoes import AgendamentoNaoEncontradoException, ExclusaoAgendamentoForaDoHorarioPermitidoException

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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
        data_agendamento = datetime.strptime(schema.data_agendamento, DATETIME_FORMAT)
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
        data_agendamento = datetime.strftime(schema.data_agendamento, DATETIME_FORMAT)
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

    def buscar_agendamentos_por_data(self, data_agendamento: str) -> list[AgendamentoServicoSchema]:
        """
        Busca os agendamentos dado argumentos de pesquisa.

        Arguments:
            data_agendamento: Data de agendamento.
        """
        pass

    def buscar_agendamentos_por_cliente(self, nome_cliente: str) -> list[AgendamentoServicoSchema]:
        """
        Busca os agendamentos dado argumentos de pesquisa.

        Arguments:
            nome_cliente: Nome do cliente.
        """
        pass

    def buscar_agendamentos_por_pet(self, nome_pet: str) -> list[AgendamentoServicoSchema]:
        """
        Busca os agendamentos dado argumentos de pesquisa.

        Arguments:
            nome_pet: Nome do pet.
        """
        pass

    def buscar_agendamento_por_id(self, id: int) -> AgendamentoServicoSchema:
        """
        Retorna o agendamento pelo seu id ou None caso não encontre.
        """
        session = Session()
        agendamento: Optional[AgendamentoServicoEntity] = session.get(AgendamentoServicoEntity, id)
        if not agendamento:
            session.close()
            raise AgendamentoNaoEncontradoException('Agendamento não encontrado!')
        data_agendamento = datetime.strftime(agendamento.data_agendamento, DATETIME_FORMAT)
        data_inclusao = datetime.strftime(agendamento.data_inclusao, DATETIME_FORMAT)
        schema = AgendamentoServicoSchema(id=agendamento.id, data_agendamento=data_agendamento, 
                                          nome_cliente=agendamento.nome_cliente, nome_pet=agendamento.nome_pet, 
                                          valor_servico=agendamento.valor_servico, servico_id=agendamento.servico_id, 
                                          servico_titulo='', cancelado=agendamento.eh_cancelado, 
                                          data_inclusao=data_inclusao)
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

