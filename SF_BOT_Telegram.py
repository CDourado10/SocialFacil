import telebot
from SF_Gerador_1 import *
from SF_Gerador_2 import *
from SF_Insta_Post import *
from SF_Telegram_Functions import *
from telebot import types
from SF_Info_User import *


info_users = informacoes_usuario()

# Substitua pelo seu token de acesso real
TOKEN = "6301103903:AAF-0JD9SpgYTLFU1Vze1Gqt64G7PJ8ZPxc"

# Substitua pelo seu ID de usuário
SEU_ID_USUARIO = 1636508473

# Configurar o bot do Telegram
bot = telebot.TeleBot(TOKEN)

# Configurar os horários das postagens
HORARIOS_POSTAGENS = ['08:00', '12:00', '18:00']


# Estado para controlar a postagem
post_state = {}


# Esta função obtém o nome do usuário com base no ID do Telegram
def get_user_name(user_id):
    user = bot.get_chat(user_id)
    return user.first_name if user.first_name else "Usuário"


# Função para criar um teclado inline com os botões desejados
def generate_inline_keyboard(button_options):
    markup = types.InlineKeyboardMarkup()
    for option in button_options:
        if "callback" in option:
            # Se a opção possui a chave "callback", é um botão de callback para função
            button = types.InlineKeyboardButton(option["text"], callback_data=option["callback"])
        elif "url" in option:
            # Se a opção possui a chave "url", é um botão de URL para uma página web
            button = types.InlineKeyboardButton(option["text"], url=option["url"])
        markup.add(button)
    return markup




# Lidar com o comando /start
# Função para buscar informações do usuário
def get_user_info(conn, user_id):
    try:
        return buscar_informacoes_usuario(conn, user_id)
    except sqlite3.Error as e:
        print(f"Erro ao buscar informações do usuário: {e}")
        return None

# Função para buscar informações das páginas do Instagram
def get_instagram_pages(conn, usuario_id):
    try:
        pages_info = buscar_informacoes_paginas(conn, usuario_id)
        return [page for page in pages_info if not page["postagem_automática"]]
    except sqlite3.Error as e:
        print(f"Erro ao buscar informações das páginas do Instagram: {e}")
        return []

# Função para criar a mensagem de boas-vindas com botões
def create_welcome_message(nome_usuario, pages_to_post, status):
    message_text = f"Bem-vindo de volta, {nome_usuario}! 😊\n"
    buttons = []

    if status:
        if pages_to_post:
            message_text += "Selecione as páginas para postar:\n"

            for page in pages_to_post:
                page_name = page.get("nome_pagina", "Página sem nome")
                button_text = f"{page_name}"
                callback_data = f"post_page_{page['id']}"
                buttons.append({"text": button_text, "callback": callback_data})
        else:
            renew_button = {"text": "Renovar Plano", "url": "URL_DA_PAGINA_DE_RENOVACAO_DE_PLANO"}
            buttons.append(renew_button)
            message_text += "Percebemos que seu plano está inativo. 😔\nPara renovar seu plano, clique no botão 'Renovar Plano'.\n"

    buttons.append({"text": "Configurações", "callback": "settings"})
    return message_text, buttons

# Função principal para enviar mensagem de boas-vindas
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    user_id = message.chat.id
    conn = conectar_banco()
    
    if conn:
        try:
            user_info = get_user_info(conn, user_id)

            if user_info:
                nome_usuario = user_info["nome"]
                status = user_info["status"]
                usuario_id = user_info['id']

                pages_to_post = get_instagram_pages(conn, usuario_id)

                message_text, buttons = create_welcome_message(nome_usuario, pages_to_post, status)

                bot.send_message(user_id, message_text, reply_markup=generate_inline_keyboard(buttons))
            else:
                user_name = get_user_name(user_id)
                message_text = f"Olá, {user_name}! 👋 Bem-vindo à SocialFácil - a sua solução de automação para postagens em redes sociais!\nEstou aqui para ajudar você a simplificar o processo de gerenciamento das suas redes sociais. 🚀\nVamos começar a tornar suas postagens nas redes sociais mais eficientes e eficazes! 💪\n"
                create_account_button = {"text": "Crie sua conta", "url": "https://www.socialfacil.com.br/accounts/register"}
                bot.send_message(user_id, message_text, reply_markup=generate_inline_keyboard([create_account_button]))
        except Exception as e:
            print(f"Erro ao processar o comando /start: {e}")
        finally:
            conn.close()


@bot.message_handler(commands=["cancel"])
def cancel_action(message):
    user_id = message.chat.id
    if user_id in post_state:
        post_state.pop(user_id, None)
        bot.send_message(user_id, "A ação atual foi cancelada. Você está de volta ao início.")
    else:
        bot.send_message(user_id, "Nenhuma ação para cancelar.")

# Obtenha as notícias uma vez no manipulador de comandos /post
@bot.message_handler(commands=["post"])
def post_news(message):
    user_id = message.chat.id
    authorized_users = informacoes_usuario()  # Obter a lista de usuários com informações
    
    # Verificar se o user_id está presente nas informações de algum usuário autorizado
    for user_info in authorized_users.values():
        if 'ID_Telegram' in user_info and user_info['ID_Telegram'] == user_id:
            if user_info['Status']:
                try:
                    noticias, noticias_filter = Prompt_Gerador1(message.text)
                    post_state[message.chat.id] = {"step": 1, "selected_news": None, "noticias_filter": noticias_filter, "noticias": noticias}
                    message_text = "Selecione uma notícia para postar:\n"
                    for i, noticia in enumerate(noticias_filter, start=1):
                        message_text += f"{i}. {noticia}\n"
                    bot.send_message(message.chat.id, message_text)
                except Exception as e:
                    bot.send_message(message.chat.id, f"Ocorreu um erro durante a execução do comando: {str(e)}")
                    post_state.pop(message.chat.id, None)
            else:
                bot.send_message(message.chat.id, "Desculpe, você não tem permissão para usar este bot.")


# Lidar com mensagens de texto durante a postagem (step 1 e 2)
@bot.message_handler(func=lambda message: message.chat.id in post_state and post_state[message.chat.id]["step"] in [1, 2])
def handle_selected_news(message):
    if message.text.isdigit():
        selected_news_index = int(message.text) - 1
        noticias_filter = post_state[message.chat.id]["noticias_filter"]
        if 0 <= selected_news_index < len(noticias_filter):
            post_state[message.chat.id]["selected_news"] = noticias_filter[selected_news_index]
            post_state[message.chat.id]["step"] = 2
            bot.send_message(message.chat.id, "Aguarde enquanto geramos a notícia...")
            try:
                selected_news = post_state[message.chat.id]["selected_news"]
                noticias = post_state[message.chat.id]["noticias"]
                resultado = GerarNoticia(selected_news, noticias)
                if resultado is not None and len(resultado) == 2:
                    text, image_path = resultado
                    # Salvando as variáveis text e image_path
                    post_state[message.chat.id]["text"] = text
                    post_state[message.chat.id]["image_path"] = image_path
                    bot.send_message(message.chat.id, text)
                    with open(image_path, 'rb') as image_file:
                        bot.send_photo(message.chat.id, image_file)
                    bot.send_message(message.chat.id, "Digite 1 para para postar ou 2 para cancelar.")
                    post_state[message.chat.id]["step"] = 3
                else:
                    bot.send_message(message.chat.id, "Houve um problema na notícia escolhida. Postagem cancelada.")
                    post_state.pop(message.chat.id, None)
            except Exception as e:
                bot.send_message(message.chat.id, f"Ocorreu um erro durante a geração da notícia: {str(e)}")
                post_state.pop(message.chat.id, None)
        else:
            bot.send_message(message.chat.id, "Número de notícia inválido. Por favor, escolha uma notícia válida.")
    else:
        bot.send_message(message.chat.id, "Por favor, escolha um número de notícia válido.")

# Manipulador de confirmação (step 3)
@bot.message_handler(func=lambda message: message.chat.id in post_state and post_state[message.chat.id]["step"] == 3)
def handle_confirmation(message):
    if message.text == "1":
        try:
            selected_news = post_state[message.chat.id]["selected_news"]
            noticias = post_state[message.chat.id]["noticias"]
            text = post_state[message.chat.id]["text"]
            image_path = post_state[message.chat.id]["image_path"]
            
            bot.send_message(message.chat.id, "Postagem confirmada.")
            
            # Execute a função InstaUpload com os parâmetros corretos
            InstaUpload(image_path, text)

            # Limpe o estado do usuário
            post_state.pop(message.chat.id, None)
        except Exception as e:
            bot.send_message(message.chat.id, f"Ocorreu um erro durante a postagem no Instagram: {str(e)}")
            post_state.pop(message.chat.id, None)
    elif message.text == "2":
        bot.send_message(message.chat.id, "Postagem cancelada.")
        post_state.pop(message.chat.id, None)
    else:
        # Adicione o teclado personalizado novamente
        bot.send_message(message.chat.id, "Por favor, escolha uma opção válida: Confirmar ou Cancelar.")

# Manipulador de Comando /auto
@bot.message_handler(commands=["auto"])
def auto_post(message):
    if message.chat.id == SEU_ID_USUARIO:  # Verifica se o usuário é autorizado a usar o comando
        try:
            
            # Substitua esta linha pela lógica real para escolher o conteúdo da postagem automaticamente.
            # selected_news = noticias[0]  # Supondo que a primeira notícia seja escolhida automaticamente
            
            # Aqui você pode gerar o texto e a imagem da postagem com base na notícia selecionada
            # Substitua esta linha pela lógica real de geração de postagem.
            # text, image_path = GerarNoticia(selected_news, noticias)
            
            # Simulando a postagem (substitua esta parte pela lógica de postagem real)
            text = "Texto da postagem automática"
            image_path = "caminho/para/imagem.jpg"
            
            bot.send_message(message.chat.id, "Aguarde enquanto geramos a notícia automática...")
            
            # Simulando o envio da postagem (substitua esta parte pela lógica de postagem real)
            bot.send_message(message.chat.id, text)
            with open(image_path, 'rb') as image_file:
                bot.send_photo(message.chat.id, image_file)
            
            # Mensagem de confirmação
            bot.send_message(message.chat.id, "Postagem automática concluída.")
            
        except Exception as e:
            bot.send_message(message.chat.id, f"Ocorreu um erro durante a postagem automática: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Desculpe, você não tem permissão para usar este bot.")



# Iniciar o bot
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Error: {str(e)}")