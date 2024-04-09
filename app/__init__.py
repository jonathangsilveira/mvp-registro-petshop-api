from .schema.servicos import *
from .schema.agendamento_servicos import *
from .schema.erro import *

from .controller import *

controller_servico: ServicoController = ServicoController()
controller_agendamento: AgendamentoServicoController = AgendamentoServicoController()