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
                    update_id = mensagem['update_id']
                    chat_id = mensagem['message']['from']['id']

                    # Verificar se a mensagem tem 'text' (para evitar erros com stickers, áudios etc.)
                    if 'text' not in mensagem['message']:
                        continue 

                    texto_mensagem = mensagem['message']['text']
                    eh_primeira_mensagem = mensagem['message']['message_id'] == 1

                    resposta = self.criar_resposta(texto_mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    # Obtendo as mensagens
    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return resultado.json()

    # Formulando uma resposta ao usuário
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem or mensagem.lower() == 'voltar':
            return f'''Olá, bem-vindo(a) ao atendimento da Escola de Alemão WortWelt! 
Digite o número da informação que gostaria de obter:{os.linesep}
1 - Sobre nossa escola{os.linesep}
2 - Turmas e Nivelamento{os.linesep}
3 - Preços e descontos{os.linesep}
4 - Programa de Intercâmbio{os.linesep}
5 - Agendamentos'''

        if mensagem == '1':
            return f'''Bem-vindo à nossa escola de alemão! 
Oferecemos cursos para todos os níveis, com aulas em grupo ou individuais.{os.linesep}
Nossa metodologia é imersiva, com situações reais do cotidiano e professores nativos para melhorar a pronúncia e naturalidade da comunicação.'''

        if mensagem == '2':
            return f'''Temos turmas para iniciantes, intermediários e avançados. Também oferecemos aulas individuais em horários personalizados. Para saber seu nível, realizamos um nivelamento gratuito.{os.linesep}
- Digite 'turmas' para a consultar as turmas e seus horário.{os.linesep}
- Digite 'individual' para consultar os professores disponíveis para te ensinarem de forma particular.{os.linesep}
- Digite 'nivelamento' para o encaminharmos ao agendamento da sua prova de nivelamento.{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' '''
        if mensagem.lower() == 'turmas':
                return f"Termos turmas terça, quarta e quinta"
        if mensagem.lower() == 'individual':
                return f"Os professores Bob e Patrick estão disponiveis para dar aulas particulares"
        if mensagem.lower() == 'nivelamento':
                return f"Temos provas de nivelamento aos sábados"


        if mensagem == '3':
            return f'''Nossos cursos variam de acordo com a carga horária e modalidade. Oferecemos algumas bolsas e descontos.{os.linesep}
-  Digite "preços" para receber uma tabela com os preços referentes a cada curso.{os.linesep}
-  Digite "descontos" para saber mais sobre nossa política de descontos{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' '''

        if mensagem == '4':
            return f'''Temos parcerias com escolas na Alemanha para intercâmbio.{os.linesep}
- Digite "intercâmbio" para receber mais informações sobre os destinos, o tempo de duração do programa e preços{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' '''

        if mensagem == '5':
            return f'''Você pode agendar aulas, testes de nivelamento e atendimentos personalizados pelo nosso site ou WhatsApp.{os.linesep}
Qual serviço deseja agendar?'''

        return "Desculpe, não entendi. Digite 'voltar' para voltar ao menu principal e ver as opções."

    # Respondendo o usuário
    def responder(self, resposta, chat_id):
        link_de_envio = f"{self.url_base}sendMessage"
        params = {
             "chat_id": chat_id,
             "text": resposta}
        requests.get(link_de_envio, params=params)  

bot = TelegramBot()
bot.Iniciar()