from datetime import datetime, date

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

def para_data_hora_servidor(data_string: str) -> datetime:
    """
    Converte data em string para datetime usado pelo server.
    """
    return datetime.strptime(data_string, DATETIME_FORMAT)

def formatar_data_hora_servidor(data_hora: datetime) -> str:
    """
    Converte data em string para datetime usado pelo server.
    """
    return datetime.strftime(data_hora, DATETIME_FORMAT)

def alterar_data_hora_fim(data_hora: datetime) -> datetime:
    """
    Altera o valor do tipo datetime para horas, minutos e segundos serem o maior como comparação.

    Ex.:
        data_hora_atual = datetime.now() # '2024-04-09 20:34:00'
        data_hora_atual.alterar_data_hora_fim() # '2024-04-09 23:59:59'
    """
    return data_hora.replace(hour=23, minute=59, second=59)

def alterar_data_hora_inicio(data_hora: datetime) -> datetime:
    """
    Altera o valor do tipo datetime para horas, minutos e segundos serem o menor como comparação.

    Ex.:
        data_hora_atual = datetime.now() # '2024-04-09 20:34:00'
        data_hora_atual.alterar_data_hora_fim() # '2024-04-09 00:00:00'
    """
    return data_hora.replace(hour=0, minute=0, second=0)

def para_data_servidor(data: str) -> datetime:
    return datetime.strptime(data, DATE_FORMAT)