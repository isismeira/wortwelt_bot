import os
import requests
import time
import json
from dotenv import load_dotenv

# Carregando as variáveis do .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Caminhos das imagens armazenadas localmente
IMAGENS = {
    "turmas": "imagens/turmas.jpeg",
    "precos": "imagens/precos.jpeg",
    "berlim": "imagens/berlim.jpg",
    "munique": "imagens/munique.jpg",
    "zurique": "imagens/zurique.jpg"
}

class TelegramBot:
    def __init__(self):
        self.url_base = f'https://api.telegram.org/bot{TOKEN}/'

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

                        resposta, botoes, imagem = self.criar_resposta(texto_mensagem, eh_primeira_mensagem)
                        self.responder(resposta, chat_id, botoes, imagem)

                    elif "callback_query" in mensagem:  
                        self.processar_callback(mensagem["callback_query"])

                    update_id = mensagem['update_id']

            time.sleep(1)

    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'

        try:
            resposta = requests.get(link_requisicao)
            return resposta.json()
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {}

    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        botoes = None
        imagem = None  

        if eh_primeira_mensagem or mensagem.lower() == 'voltar':
            return f'''Olá 👋 , bem-vindo(a) ao atendimento da <b>Escola de Alemão WortWelt</b>! 
Digite o número da informação que gostaria de obter:{os.linesep}
1 - Turmas e nivelamento 👥{os.linesep}
2 - Preços e descontos 💵{os.linesep}
3 - Programa de intercâmbio ✈️{os.linesep}
4 - Agendamentos 📆''', botoes, imagem

        if mensagem == '1':
            return f'''Temos turmas para <em>iniciantes, intermediários e avançados</em>. Também oferecemos <em>aulas individuais</em> em horários personalizados. Para saber seu nível, realizamos um <em>nivelamento gratuito</em>. {os.linesep}
- Digite <b>'turmas'</b> para a consultar as turmas e seus horários. 👥{os.linesep}
- Digite <b>'individual'</b> para saber mais sobre as aulas particulares. 👤{os.linesep}
- Digite <b>'nivelamento'</b> para ter mais informações sobre a prova de nivelamento. 〽️{os.linesep}
   ↪️ Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes, imagem
        
        if mensagem.lower() == 'turmas':
            return f'''Veja a seguir nossa tabela com nossas turmas e seus horarios. {os.linesep}
Gostaria de consultar nossos <em>preços</em>? Digite <b>'preços'</b>💲''', botoes, IMAGENS["turmas"]
        if mensagem.lower() == 'individual':
            return f'''Temos professores nativos com horários flexíveis para dar aula. Você pode escolher entre ter aulas <em>presenciais</em> ou <em>online</em>.{os.linesep}
 Gostaria de consultar nossos <em>preços</em>? Digite <b>'preços'</b>💲''', botoes, None
        if mensagem.lower() == 'nivelamento':
            return f'''Para nivelar nossos futuros alunos na categoria correta, temos uma prova de nivelamento, que consiste em uma <em>prova objetiva</em> e um <em>teste de conversação</em> com um de nossos professores.{os.linesep}
Gostaria de <em>agendar</em> um teste de nivelamento? Digite <b>'agendamento'</b> 🕑''', botoes, None

        if mensagem == '2':
            return f'''Nossos cursos variam de acordo com a carga horária e modalidade. Oferecemos algumas <em>bolsas</em> e <em>descontos</em>.{os.linesep}
- Digite <b>'preços'</b> para receber uma tabela com os preços referentes a cada curso. 💵{os.linesep}
- Digite <b>'descontos'</b> para saber mais sobre nossa política de descontos. 💰{os.linesep}
   ↪️ Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes, imagem

        if mensagem.lower() == 'precos' or mensagem.lower() == 'preços':
            return f'''Essa é a nossa tabela de preços:''', botoes, IMAGENS["precos"]
        if mensagem.lower() == 'descontos':
            return f'''Na nossa política de descontos depende do nivelamento do aluno: {os.linesep}
- ❗️ Recém Matriculado | 70% de desconto na primeira mensalidade.{os.linesep}
- 🟢 Nível iniciante(após primeiro mês de matrícula) | 20% de desconto na mensalidade.{os.linesep}
- 🟡 Nível Intermediário | 35% de desconto na mensalidade.{os.linesep}
- 🔴 Nível Avançado | 50% de desconto na mensalidade.{os.linesep}''', botoes, None

        if mensagem == '3':
            return f'''Temos parcerias com escolas na <em>Alemanha</em> e na <em>Suiça</em> para intercâmbio.{os.linesep}
Para receber mais informações sobre os destinos, o tempo de duração do programa e preços, escolha um dos destinos de interesse: {os.linesep}
- Digite "Berlim" para receber informações sobre o intercâmbio em Berlim. 🧱{os.linesep}
- Digite "Munique" para receber informações sobre o intercâmbio em Munique. 🏰{os.linesep}
- Digite "Zurique" para receber informações sobre o intercâmbio em Zurique. 🗻{os.linesep}
    Voltar - Para voltar ao menu principal digite 'voltar' ''', botoes, imagem

        if mensagem.lower() == 'berlim':
            return f'''📆 Duração: 3 meses (12 semanas) {os.linesep}
💰 Preço: €3.200 (inclui acomodação e curso) {os.linesep}
🎓 Descrição: {os.linesep}
Nosso programa em Berlim é ideal para quem deseja aprender alemão em um ambiente vibrante e culturalmente rico. As aulas acontecem em uma escola parceira no coração da cidade, com professores nativos e turmas reduzidas. {os.linesep}
{os.linesep}
🌍 O que está incluído? {os.linesep}
✅ Curso intensivo de alemão (20 horas/semana) {os.linesep}
✅ Acomodação em residência estudantil ou casa de família {os.linesep}
✅ Passeios guiados por pontos icônicos, como o Portão de Brandemburgo, a Ilha dos Museus e o Memorial do Muro de Berlim {os.linesep}
✅ Workshops de imersão cultural, incluindo culinária alemã e teatro interativo 
''', botoes, IMAGENS["berlim"]
        
        if mensagem.lower() == 'munique':
            return f'''📆 Duração: 1 mês (4 semanas)
💰 Preço: €2.500 (inclui curso, acomodação e passeios)
🎓 Descrição:
A capital da Baviera combina tradição e modernidade. Nosso programa em Munique oferece um aprendizado intensivo do idioma, aliado a experiências incríveis na cidade, famosa por sua cerveja e sua arquitetura histórica.

🌍 O que está incluído?
✅ Curso intensivo de alemão (25 horas/semana)
✅ Hospedagem em hostels premium ou casas de família
✅ Passeios guiados ao Palácio de Nymphenburg e à Marienplatz
✅ Excursão ao famoso Castelo de Neuschwanstein''', botoes, IMAGENS["munique"]
        
        if mensagem.lower() == 'zurique':
            return f'''📆 Duração: 2 meses (8 semanas)
💰 Preço: CHF 4.500 (inclui curso, acomodação e transporte público)
🎓 Descrição:
A Suíça é o destino perfeito para quem busca um aprendizado imersivo e uma qualidade de vida excepcional. O intercâmbio em Zurique oferece um ambiente acadêmico de excelência, aliado a experiências únicas na natureza e cultura suíça.

🌍 O que está incluído?
✅ Curso de alemão padrão ou business (15h/semana)
✅ Acomodação em flats estudantis no centro da cidade
✅ Passe gratuito para transporte público durante toda a estadia
✅ Visitas culturais ao Lago de Zurique, ao Museu Nacional Suíço e ao bairro medieval Niederdorf''', botoes, IMAGENS["zurique"]

        if mensagem == '4' or mensagem.lower()=='agendamento':
            resposta = '''Você pode agendar uma aula experimental ou seu teste de nivelamento e atendimentos personalizados pelo nosso site ou WhatsApp.  
Escolha uma das opções abaixo:'''

            botoes = {
                "inline_keyboard": [
                    [{"text": "🧑‍🏫 Agendar aula experimental", "callback_data": "agendar_aula"}],
                    [{"text": "📖 Agendar teste de nivelamento", "callback_data": "teste_nivelamento"}]
                ]
            }

            return resposta, botoes, imagem
        
        return "Desculpe, não entendi. Digite 'voltar' para voltar ao menu principal e ver as opções.", botoes, imagem

    def processar_callback(self, callback_query):
        chat_id = callback_query["message"]["chat"]["id"]
        dados = callback_query["data"]

        if dados == "agendar_aula":
            self.responder("Ótimo! Para agendar uma aula, acesse nosso site ou envie uma mensagem.", chat_id)
        elif dados == "teste_nivelamento":
            self.responder("Podemos agendar seu teste de nivelamento. Entre em contato conosco!", chat_id)

    def responder(self, resposta, chat_id, botoes=None, imagem=None):
        link_de_envio = f"{self.url_base}sendMessage"
        params = {
            "chat_id": chat_id,
            "text": resposta,
            "parse_mode": "HTML",
        }

        if botoes:
            params["reply_markup"] = json.dumps(botoes)

        requests.get(link_de_envio, params=params)

        if imagem:
            with open(imagem, 'rb') as foto:
                requests.post(f"{self.url_base}sendPhoto", data={"chat_id": chat_id}, files={"photo": foto})

bot = TelegramBot()
bot.Iniciar()
