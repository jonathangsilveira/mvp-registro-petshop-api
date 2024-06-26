from datetime import datetime
from typing import Optional

from app.database import Session

from app.entity import ServicoEntity, AgendamentoServicoEntity

from app.schema.agendamento_servicos import NovoAgendamentoServicoSchema, CancelarAgendamentoServicoSchema, AgendamentoServicoSchema

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

    def cancelar_agendamento_servico(self, id: int) -> None:
        """
        Altera um registro de agendamento de serviço atribuindo flag de cancelado.
        """
        session = Session()
        agendamento: Optional[AgendamentoServicoEntity] = session.get(AgendamentoServicoEntity, id)
        if not agendamento:
            raise AgendamentoNaoEncontradoException('Agendamento não encontrado!')
        agendamento.eh_cancelado = True
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
            order_by(AgendamentoServicoEntity.data_agendamento). \
            all()
        
        schemas = [self.__mapear_entity_para_schema__(agendamento, self.__buscar_titulo_servico__(agendamento.servico_id)) for agendamento in agendamentos]
        session.close()
        return schemas

    def __eh_exclusao_fora_do_prazo__(self, data_agendamento: datetime) -> bool:
        """
        Valida se é permitido exclusão do agendamento do serviço.
        """
        now = datetime.now()
        if now > data_agendamento:
            return True
        duracao = now - data_agendamento
        duracao_em_seg = duracao.total_seconds()
        duracao_em_horas = divmod(duracao_em_seg, 3600)[0]
        return abs(duracao_em_horas) < PRAZO_EXCLUSAO_EM_HORAS
    
    def __mapear_entity_para_schema__(self, agendamento: AgendamentoServicoEntity, servico_titulo: str = '') -> AgendamentoServicoSchema:
        """
        Mapeia instancia de 'AgendamentoServicoEntity' para 'AgendamentoServicoSchema'.
        """
        data_agendamento = formatar_data_hora_servidor(agendamento.data_agendamento)
        data_inclusao = formatar_data_hora_servidor(agendamento.data_inclusao)
        return AgendamentoServicoSchema(id=agendamento.id, data_agendamento=data_agendamento, 
                                        nome_cliente=agendamento.nome_cliente, nome_pet=agendamento.nome_pet, 
                                        valor_servico=agendamento.valor_servico, servico_id=agendamento.servico_id, 
                                        servico_titulo=servico_titulo, cancelado=agendamento.eh_cancelado, 
                                        data_inclusao=data_inclusao)
    
    def __buscar_titulo_servico__(self, servico_id: int) -> str:
        """
        Busca título do serviço pelo seu id.
        """
        session = Session()
        servico: Optional[ServicoEntity] = session.get(ServicoEntity, servico_id)
        if not servico:
            session.close()
            return ''
        servico_titulo = servico.titulo
        session.close()
        return servico_titulo