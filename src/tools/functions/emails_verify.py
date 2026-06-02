import json
import datetime
import os
from src.utils.resilience import CircuitBreaker

breaker = CircuitBreaker(failure_threshold= 3, recovery_timeout=10)

emails_verify_function = {
    "name": "emails_verify",
    "description": "Busca e lista os e-mails recebidos pelo usuário em um intervalo de dias recente. Use esta ferramenta sempre que o usuário perguntar se recebeu novas mensagens, quiser um resumo dos últimos e-mails ou pedir para verificar a caixa de entrada.",
    "parameters": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "O número de dias retroativos a partir de hoje para buscar os e-mails. Por exemplo: 1 para e-mails de hoje/últimas 24h, 7 para a última semana.",
            },
        },
        "required": ["days"],
    },
}

@breaker
def emails_verify(days: int):
    abs_working_dir = os.path.abspath('./src/db/aurinko_dummy_response.json')
    with open(abs_working_dir, 'r', encoding='utf-8') as file:
        emails = json.load(file)
    current_date =  "2026-05-29"
    windows_date = datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=days)
    last_emails = [
        email for email in emails["records"]
        if  datetime.datetime.strptime(email["receivedDate"].split('T')[0], "%Y-%m-%d") >= windows_date
    ]

    return last_emails

def get_functions_declarations():
    return [emails_verify_function]