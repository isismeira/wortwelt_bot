import os
import requests
import time
import json
from dotenv import load_dotenv

# Carregando as variáveis do .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TelegramBot:
    # Inicializando a classe
    def __init__(self):
        self.url_base = f'https://api.telegram.org/bot{TOKEN}/'

    # Inicializando o bot
    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            mensagens = atualizacao.get('result', [])

            if mensagens:
                for mensagem in mensagens:
                    if "message" in mensagem:
                        chat_id = mensagem['message']['from']['id']

                        if 'text' not in mensagem['message']:
                            continue 

                        texto_mensagem = mensagem['message']['text']
                        eh_primeira_mensagem = mensagem['message']['message_id'] == 1

                        resposta, botoes = self.criar_resposta(texto_mensagem, eh_primeira_mensagem)
                        self.responder(resposta, chat_id, botoes)

                    elif "callback_query" in mensagem:  
                        self.processar_callback(mensagem["callback_query"])

                    update_id = mensagem['update_id']

            time.sleep(1)

    # Obtendo as mensagens digitadas pelo cliente
    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'

        resposta = requests.get(link_requisicao)
        return resposta.json()
    
    # Formulando uma resposta baseado no que foi escrito
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        botoes = None

        if eh_primeira_mensagem or mensagem.lower() == 'voltar':
            return f'''Olá 👋 , bem-vindo(a) ao atendimento da <b>Escola de Alemão WortWelt</b>! 
Digite o número da informação que gostaria de obter:{os.linesep}
1 - Turmas e Nivelamento{os.linesep}
2 - Preços e descontos{os.linesep}
3 - Programa de Intercâmbio{os.linesep}
4 - Agendamentos''', botoes

        if mensagem == '1':
            return f'''Temos turmas para iniciantes, intermediários e avançados. Também oferecemos aulas individuais em horários personalizados. Para saber seu nível, realizamos um nivelamento gratuito.{os.linesep}
- Digite 'turmas' para a consultar as turmas e seus horários.{os.linesep}
- Digite 'individual' para consultar os professores disponíveis para te ensinarem de forma particular.{os.linesep}
- Digite 'nivelamento' para o encaminharmos ao agendamento da sua prova de nivelamento.{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes
        
        # Sub-opções da primeira informação
        if mensagem.lower() == 'turmas':
            return f"Temos turmas terça, quarta e quinta", botoes
        if mensagem.lower() == 'individual':
            return f"Os professores Bob e Patrick estão disponíveis para dar aulas particulares", botoes
        if mensagem.lower() == 'nivelamento':
            return f"Temos provas de nivelamento aos sábados", botoes

        if mensagem == '2':
            return f'''Nossos cursos variam de acordo com a carga horária e modalidade. Oferecemos algumas bolsas e descontos.{os.linesep}
- Digite "preços" para receber uma tabela com os preços referentes a cada curso.{os.linesep}
- Digite "descontos" para saber mais sobre nossa política de descontos{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes
        
        if mensagem.lower() == 'precos' or mensagem.lower() == 'preços':
            return f'''Essa é a nossa tabela de preços.''', botoes
        if mensagem.lower() == 'descontos':
            return f'''Essa é nossa política de descontos.''', botoes

        if mensagem == '3':
            return f'''Temos parcerias com escolas na Alemanha para intercâmbio.{os.linesep}
Para receber mais informações sobre os destinos, o tempo de duração do programa e preços, escolha um dos destinos de interesse: {os.linesep}
- Digite "Berlim" para receber informações sobre o intercâmbio em Berlim.{os.linesep}
- Digite "Munique" para receber informações sobre o intercâmbio em Munique{os.linesep}
- Digite "Zurique" para receber informações sobre o intercâmbio em Zurique{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes
        
        if mensagem.lower() == 'berlim':
            return f'''Informações sobre o intercâmbio em Berlim''', botoes
        if mensagem.lower() == 'munique':
            return f'''Informações sobre o intercâmbio em Munique''', botoes
        if mensagem.lower() == 'zurique':
            return f'''Informações sobre o intercâmbio em Zurique''', botoes

        if mensagem == '4':
            resposta = '''Você pode agendar aulas, testes de nivelamento e atendimentos personalizados pelo nosso site ou WhatsApp.  
Escolha uma das opções abaixo:'''

            botoes = {
                "inline_keyboard": [
                    [{"text": "📅 Agendar aula experimental", "callback_data": "agendar_aula"}],
                    [{"text": "📖 Agendar teste de Nivelamento", "callback_data": "teste_nivelamento"}],
                    [{"text": "📞 Atendimento via WhatsApp", "url": "https://wa.me/seunumero"}]
                ]
            }

            return resposta, botoes
        
        return "Desculpe, não entendi. Digite 'voltar' para voltar ao menu principal e ver as opções.", botoes

    # Processa o callback após o clique dos botões (processo ocorre somente no caso de clique na mensagem 4)
    def processar_callback(self, callback_query):
        chat_id = callback_query["message"]["chat"]["id"]
        dados = callback_query["data"]

        if dados == "agendar_aula":
            self.responder("Ótimo! Para agendar uma aula, acesse nosso site ou envie uma mensagem.", chat_id)
        elif dados == "teste_nivelamento":
            self.responder("Podemos agendar seu teste de nivelamento. Entre em contato conosco!", chat_id)

    # Responde o cliente        
    def responder(self, resposta, chat_id, botoes=None):
        link_de_envio = f"{self.url_base}sendMessage"
        params = {
            "chat_id": chat_id,
            "text": resposta,
            "parse_mode": "HTML",
        }

        if botoes:
            params["reply_markup"] = json.dumps(botoes)

        requests.get(link_de_envio, params=params)

bot = TelegramBot()
bot.Iniciar()
