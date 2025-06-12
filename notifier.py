# Este arquivo é o nosso serviço de mensagens.
# Sua única responsabilidade é se comunicar com a API do Telegram para enviar uma notificação.

import requests
import os
from dotenv import load_dotenv
# --- Configuração do Notificador ---
# Seus dados de acesso ao bot do Telegram.
# Lembre-se de manter seu token em segredo.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """Envia uma mensagem formatada para o seu chat do Telegram."""

    # 1. Monta a URL de destino da API do Telegram.
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # 2. Monta o "pacote" de dados (payload) com as informações da mensagem.
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, # Para quem enviar.
        "text": message, # O conteúdo da mensagem.
        "parse_mode": "Markdown" # Permite usar formatação como *negrito* e [links](url).
    }
    
    # 3. Tenta enviar a mensagem, com tratamento de erros de conexão.
    try:
        response = requests.post(url, json=payload)
        # Se o status não for 200 (OK), imprime o erro que o Telegram retornou.
        if response.status_code != 200:
            print(f"ERRO ao notificar no Telegram: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERRO de conexão com o Telegram: {e}")


# --- Bloco de Teste ---
# Este bloco só é executado quando rodamos o arquivo diretamente com "python notifier.py".
# Ele não é executado quando outro arquivo (como o robo_caçador) importa a função.
if __name__ == "__main__":
    print("Executando teste de notificação...")
    send_telegram_message("🤖 *Teste Final!* Se você recebeu esta mensagem, seu notificador está 100% funcional!")
    print("Comando de teste finalizado.")