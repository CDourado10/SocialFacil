import telebot
from SF_Gerador_1 import *
from SF_Gerador_2 import *
from SF_Insta_Post import *
from SF_Telegram_Functions import *
from telebot.types import *

# Substitua pelo seu token de acesso real
TOKEN = "6632901248:AAGCaSyfP5GsYas23Dt7aXvuhVOXY28y9n4"

# Substitua pelo seu ID de usuário
SEU_ID_USUARIO = 1636508473

# Configurar o bot do Telegram
bot = telebot.TeleBot(TOKEN)

# Configurar os horários das postagens
HORARIOS_POSTAGENS = ['08:00', '12:00', '18:00']

# Estado para controlar a postagem
post_state = {}

# Lidar com o comando /start
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Olá! Este é um bot para uso interno do ConnectJus.")

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
    if message.chat.id == SEU_ID_USUARIO:
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

# Iniciar o bot
while True:
    try:
        bot.polling()
    except:
        print("Error")