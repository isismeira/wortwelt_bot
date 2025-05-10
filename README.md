# 🤖 Wortwelt Bot - O chatbot de atendimento automático

Um bot para telegram voltado para o **atendimento rápido e automatizado** de clientes de uma escola de idiomas. O bot, além de **fornecer informações de forma interativa** sobre preços, turmas, intercâmbio e bolsas , **realiza agendamento inteligente** de testes de nivelamento e aulas experimentais. Sinta-se livre para se basear no *WortWelt Bot* para **automatizar o atendimento do seu negócio!**

<img src="wortweltbot.gif">

##  🚀 Tecnologias utilizadas

-   **Python** – Linguagem principal do projeto.
-   **requests** – Para fazer requisições HTTP à API do Telegram.
-   **time** – Para adicionar pausas no loop principal do bot.
-   **json** – Para manipulação de arquivos JSON (armazenamento de agendamentos e outras informações).
-   **datetime** – Para manipular datas e horários (agendamentos e verificações de formato).
-   **os** – Para manipulação de variáveis de ambiente e arquivos.
-   **dotenv (`python-dotenv`)** – Para carregar variáveis de ambiente a partir do arquivo `.env` (armazenamento seguro de credenciais)

## ⚙️ Funcionalidades
-   Envio de mensagens automáticas com opções interativas para o usuário.
-   Uso de **arquivos JSON** para armazenar agendamentos.
-   Suporte a **agendamento de aulas experimentais e testes de nivelamento**.
-   Manipulação de **imagens** para ilustrar respostas no Telegram.
