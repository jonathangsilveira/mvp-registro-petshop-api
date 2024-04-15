from app.database import Session

from app.entity import ServicoEntity

from app.schema.servicos import ServicoAtivoSchema

class ServicoController:
    """
    Acessa as entidades para fornecer os dados para as rotas de serviços.
    """

    def recuperar_servicos_ativos(self) -> list[ServicoAtivoSchema]:
        """
        Lista os serviços com status ativo na base de dados.
        """
        session = Session()
        servicos = session.query(ServicoEntity).filter(ServicoEntity.eh_ativo == True).all()
        servicos_ativos: list[ServicoAtivoSchema] = []
        for servico in servicos:
            servico_ativo = ServicoAtivoSchema(id=servico.id, titulo=servico.titulo, 
                                               preco_unitario=servico.preco_unitario)
            servicos_ativos.append(servico_ativo)
        
        session.close()
        return servicos_ativos