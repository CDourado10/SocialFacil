import os
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from PIL import Image, ImageDraw, ImageFont


# Carregue o modelo do spaCy
nlp = spacy.load("pt_core_news_sm")

# Inicialize o SentimentIntensityAnalyzer do NLTK
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

def calcular_sentimento(palavra):
    sentiment_score = sia.polarity_scores(palavra)
    return sentiment_score['compound']


def calcular_polaridade(texto):
    blob = TextBlob(texto)
    polaridade = blob.sentiment.polarity
    return polaridade

endereço_fonte = "fonte"
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
endereço_fonte = os.path.join(diretorio_atual, endereço_fonte)

#EuclidFlexMedium
def escreverimagem(textodaimagem, caminho_imagem, fonte_maior=endereço_fonte+"\EuclidFlexBold.ttf", fonte_media=endereço_fonte+"\EuclidFlexMedium.ttf", maiusculo=True, nomesaida="Imagem com legenda", output_dir='', modelo_imagem = 'inferior'):
    # Dimensões da imagem
    largura_imagem = 1080
    altura_imagem = 1080

    if maiusculo:
        textodaimagem = textodaimagem.upper()

    # Configurações da legenda
    tamanho_texto = len(textodaimagem)
    tamfonte = int(abs(70 - (tamanho_texto/8)))
    fonte_maior = ImageFont.truetype(fonte_maior, tamfonte)
    fonte_media = ImageFont.truetype(fonte_media, tamfonte)

    palavras = textodaimagem.split()
    tamanho_palavras = [len(palavra) for palavra in palavras]
    maior_palavra = max(tamanho_palavras)

    if modelo_imagem == 'inferior':
        posicao_vertical = (altura_imagem - 350, altura_imagem - 75)
        posicao_horizontal = (50, largura_imagem - 65)
        cor_texto = (255, 255, 255)  # Cor branca

    elif modelo_imagem == 'lateral esquerdo':
        if maior_palavra < 15:
            posicao_vertical = (275, altura_imagem - 65)
            posicao_horizontal = (largura_imagem - 1000, largura_imagem - 625)
            cor_texto = (255, 255, 255)  # Cor branca
        else:
            posicao_vertical = (altura_imagem - 400, altura_imagem - 65)
            posicao_horizontal = (largura_imagem - 1000, largura_imagem - 500)
            cor_texto = (255, 255, 255)  # Cor branca
    

    # Criar uma imagem em branco
    imagem = Image.open(caminho_imagem)

    # Adicionar texto à imagem
    desenho = ImageDraw.Draw(imagem)
    area_paragrafo = (posicao_horizontal[0], posicao_vertical[0], posicao_horizontal[1], posicao_vertical[1])

    # Use spaCy para identificar substantivos e nomes próprios no título
    doc = nlp(textodaimagem)
    palavras_principais = set([token.text.upper() for token in doc if token.pos_ in ["NOUN"] or token.ent_type_ == "PERSON"])

    # Separe o texto em palavras
    palavras = textodaimagem.split()

    # Inicialize a lista de linhas de texto
    linhas_texto = []
    linha_atual = []

    for palavra in palavras:
        
        # Calcule a polaridade da palavra
        polaridade = calcular_polaridade(palavra)

        # Calcule o sentimento da palavra
        sentimento = calcular_sentimento(palavra)

        # Use a fonte Montserrat-SemiBold para palavras-chave
        fonte_usada = fonte_maior if (palavra.upper() in palavras_principais) or (palavra.upper() in {'IA', 'INTELIGENCIA', 'ARTIFICIAL'}) else fonte_media # and polaridade != 0 and sentimento != 0

        # Verifique se a palavra cabe na linha atual
        #largura_texto = desenho.textsize(" ".join(linha_atual + [palavra]), font=fonte_usada)[0]
        #bbox = desenho.textbbox((0, 0), textodaimagem, font=fonte_usada)
        bbox = desenho.textbbox((0, 0), " ".join(linha_atual + [palavra]), font=fonte_usada)
        largura_texto = bbox[2] - bbox[0]
        if largura_texto <= area_paragrafo[2] - area_paragrafo[0]:
            linha_atual.append(palavra)
        else:
            linhas_texto.append(linha_atual)
            linha_atual = [palavra]

    if linha_atual:
        linhas_texto.append(linha_atual)

    # Calcula o espaçamento uniforme entre as linhas de texto
    espacamento = (area_paragrafo[3] - area_paragrafo[1]) / (len(linhas_texto) + 10)

    espacamento_palavras = 15  # Defina o espaçamento entre as palavras aqui

    # Define a posição vertical inicial para o texto
    posicao_vertical_inicial = area_paragrafo[1] + int(area_paragrafo[1]/50)

    # Tamanho da imagem abaixo do qual a linha deve ser centralizada
    limiar_centralizacao = altura_imagem * 0.001  # Ajuste conforme necessário

    # Desenha as linhas de texto com espaçamento uniforme
    for linha in linhas_texto:
        
        # Calcule o espaçamento extra uniforme entre as palavras
        #espacamento_extra = (area_paragrafo[2] - area_paragrafo[0] - largura_texto) / (len(linha) - 1) if len(linha) > 1 else 0
        largura_texto = desenho.textbbox((0, 0), " ".join(linha), font=fonte_maior)[2] - desenho.textbbox((0, 0), " ".join(linha), font=fonte_maior)[0]
        #espacamento_palavras = (area_paragrafo[2] - area_paragrafo[0] - largura_texto) / (len(linha)) if len(linha) > 0 else 0

        # Centralize a linha se o tamanho for menor que o limiar
        if largura_texto < limiar_centralizacao:
            posicao_horizontal_atual = (area_paragrafo[0] + area_paragrafo[2]) / 2 - largura_texto / 2
        else:
            posicao_horizontal_atual = area_paragrafo[0]

        #posicao_horizontal_atual = area_paragrafo[0]
        for palavra in linha:
            # Use a fonte Montserrat-SemiBold para palavras-chave
            bbox = desenho.textbbox((0, 0), palavra, font=fonte_usada)
            largura_palavra = bbox[2] - bbox[0]
             # Calcule a polaridade da palavra
            polaridade = calcular_polaridade(palavra)

            # Calcule o sentimento da palavra
            sentimento = calcular_sentimento(palavra)

            # Use a fonte Montserrat-SemiBold para palavras-chave
            fonte_usada = fonte_maior if (palavra.upper() in palavras_principais) or (palavra.upper() in {'IA', 'INTELIGENCIA', 'ARTIFICIAL'}) else fonte_media
            #fonte_usada = fonte_maior if palavra.upper() in palavras_principais else fonte_media

            # Renderize cada palavra com a fonte apropriada
            desenho.text((posicao_horizontal_atual, posicao_vertical_inicial), palavra, font=fonte_usada, fill=cor_texto)
            # Atualize a posição horizontal
            posicao_horizontal_atual += largura_palavra + espacamento_palavras

        # Atualize a posição vertical
        posicao_vertical_inicial += tamfonte + int(espacamento/16)

    text_image_path = os.path.join(os.path.dirname(caminho_imagem), output_dir, 'corted_' + nomesaida)
    text_image_path += '.png'

    # Salvar a imagem com a legenda
    imagem.save(text_image_path)

    return text_image_path