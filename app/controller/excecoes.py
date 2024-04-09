
class AgendamentoNaoEncontradoException(BaseException):
    """
    Exceção lançada quando agendamento não foi encontrado na base.
    """

class ExclusaoAgendamentoForaDoHorarioPermitidoException(BaseException):
    """
    Exceção lançada quando agendamento há tentativa de excluir registro antes do período válido (4h)
    """