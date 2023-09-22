from datetime import datetime as dt
from datetime import timedelta
from PIL import Image
import os
from icrawler.builtin import GoogleImageCrawler
import pytesseract
import cv2
from unidecode import unidecode
from SF_Imagem_Download import *
from SF_Imagem_Escrever import *
import re
import urllib.parse
import unidecode
from SF_Imagem_Corte import *

def buscar_imagem_por_descricao(titulo, descricao, imagens_baixadas, pastaimagem, startin=0):
    save_dir = f'{pastaimagem}/{descricao}/'
    print(save_dir)
    
    max_imagens = 5
    
    baixar_imagem = imagem_download(titulo, max_imagens, save_dir, startin=startin)

    melhores_imagens = []
    
    for root, _, files in os.walk(save_dir):
        for image_filename in files:
            #print(image_filename)
            image_path = os.path.join(root, image_filename)
            print('image_path', image_path)
            if image_filename not in imagens_baixadas and has_text(image_path):
                imagens_baixadas.add(image_filename)
                melhores_imagens.append(image_path)

    print('melhores_imagens', len(melhores_imagens))
    print('melhores_imagens', melhores_imagens)

    if melhores_imagens:
        # Ordena as imagens pela qualidade de pixels (largura x altura)
        melhores_imagens.sort(key=lambda img_path: -os.path.getsize(img_path))
        return melhores_imagens[0]
                    
    return None  # Retorna None se nenhuma imagem sem texto for encontrada

def has_text(image_path):
    try:
        # Abre a imagem com o OpenCV
        image_cv = cv2.imread(image_path)
        # Converte a imagem para tons de cinza
        gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        
        # Aplica a limiarização (binarização) para destacar o texto
        _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Converte a imagem binarizada de volta para o formato PIL
        image_pil = Image.fromarray(binary_image)
        
        # Extrai o texto usando o pytesseract
        text = pytesseract.image_to_string(image_pil)
        
        return len(text.strip()) == 0
    except Exception as e:
        print("Error:", e)
        return False

def converter_para_png(caminho_imagem):
    try:
        # Abrir a imagem
        imagem = Image.open(caminho_imagem)

        # Extrair o nome do arquivo e o diretório
        nome_arquivo, extensao = os.path.splitext(os.path.basename(caminho_imagem))
        
        # Novo nome do arquivo com a extensão .png
        novo_nome = nome_arquivo + '.png'

        # Caminho para o novo arquivo
        novo_caminho = os.path.join(os.path.dirname(caminho_imagem), novo_nome)

        # Salvar a imagem no formato PNG com o novo nome
        imagem.save(novo_caminho, 'PNG')

        # Fechar a imagem original
        imagem.close()

        return novo_caminho
    except Exception as e:
        return str(e)

def convert_png_to_jpeg(png_path, jpeg_path):
    try:
        img = Image.open(png_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(jpeg_path, format='JPEG', quality=85)
        print(f"Imagem convertida com sucesso: {jpeg_path}")
        return jpeg_path
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")
        return None

def colocarmodelo(imagepath, modelpath):
    img = Image.open(imagepath)
    img_modelo = Image.open(modelpath)
    largura, altura = img_modelo.size
    cropped_img = img.resize((largura, altura), Image.LANCZOS)

    imagem_final = Image.new('RGBA', (largura, altura))
    imagem_final.paste(cropped_img, (0, 0))
    imagem_final.paste(img_modelo, (0, 0), img_modelo)

    imagem_final.save(imagepath, 'PNG')
    

def imagebuilder(titulo, pesquisargoogle, pastaimagem, modelomarca):
    descricao_UTF8 = unidecode.unidecode(titulo)
    descricao_UTF8 = re.sub(r'[^a-zA-Z0-9]', '', descricao_UTF8)
    imagens_baixadas = set()
    startin = 0
    while True:
        image_path = buscar_imagem_por_descricao(pesquisargoogle, descricao_UTF8, imagens_baixadas, pastaimagem, startin=startin)
        if image_path is None:
            print("Nenhuma Imagem sem Texto encontrada")
            startin += 5
        elif image_path:
            print("Imagem sem texto encontrada:", image_path)
            break
    imagem_cortada = crop_to_square(0.25, converter_para_png(image_path), f"{pastaimagem}/{descricao_UTF8}/imagem_cortada.png", fill_color="#212121")
    print(imagem_cortada)
    colocarmodelo(imagem_cortada, modelomarca)
    imagem_legenda = escreverimagem(titulo, imagem_cortada, maiusculo=False, nomesaida=f"Imagem com legenda", output_dir=f"{pastaimagem}/{descricao_UTF8}", modelo_imagem='lateral esquerdo')
    # Substitua com o caminho da imagem PNG de entrada e o caminho para salvar a imagem JPEG de saída
    jpeg_output_path = f'{pastaimagem}/{descricao_UTF8}/Instagram_Tratado.jpg'
    imagem_post = convert_png_to_jpeg(imagem_legenda, jpeg_output_path)
    return imagem_post
        



if __name__ == "__main__":
    # Exemplo de uso da função imagebuilder
    titulo = "Conheça Yoda, o cão de 4 anos que capturou brasileiro fugitivo nos EUA"
    pastaimagem = "C:/IAEficaz/myenv/CJ/CJ/"
    modelomarca = "C:/IAEficaz/myenv/CJ/CJ/modelo connectjus.png"
    print(imagebuilder(titulo, titulo, pastaimagem, modelomarca))



