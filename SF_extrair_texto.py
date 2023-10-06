import requests
import asyncio
from bs4 import BeautifulSoup
import re
from SF_AI import chatgpt
from SF_Info_User import *
import logging
from SF_prompts import noticias_maior, artigo_atual_maior, artigo_atemporal_maior

# Configurar o logger
logging.basicConfig(filename='SF_extrair_texto_erros.log', level=logging.ERROR)


        
def acessar_links(link):
    conteudos = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'

    # Configurar o cabeçalho User-Agent
    headers = {'User-Agent': user_agent}

    # Padrões de palavras-chave para encontrar a classe ou o texto
    k = 0

    
    try:
        if 'news.google' in link:
            response_google_news = requests.get(link, headers=headers, timeout=30)
            response_google_news.raise_for_status()  # Verifica se a solicitação foi bem-sucedida

            # Analisa o HTML da página
            soup_1 = BeautifulSoup(response_google_news.text, 'html.parser')
            # Encontre o elemento que contém o link do site verdadeiro
            elemnt = soup_1.find('a', {'jsname': 'tljFtd'})

            # Verifique se o elemento foi encontrado
            if elemnt:
                # Extraia o link do atributo "href"
                link = elemnt.get('href')
        
        response = requests.get(link, headers=headers, timeout=30)
        response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida

        # Analisa o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontre todos os elementos cujas classes contenham as palavras desejadas
        content_elements = soup.find_all(class_=re.compile(r'(content|conteudo|article|artigo)', re.I))

        if content_elements:
            # Combine o texto desses elementos em uma única string
            conteudo_artigo = '\n'.join(element.get_text() for element in content_elements)

            if conteudos:
                # Verifique se o conteúdo começa com o que já está na lista
                if conteudo_artigo.startswith(conteudos[-1]['conteudo']):
                    
                    # Remove a parte repetida do conteúdo
                    conteudo_artigo = conteudo_artigo[len(conteudos[-1]['conteudo']):].strip()

            

            #if not conteudo_existente:
            conteudos.append({
                'link': link,
                'conteudo': conteudo_artigo
            })
        else:
            logging.error(f"Nenhum elemento com as classes desejadas em {link}")


    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar o link {link}: {e}")
    except Exception as e:
        logging.error(f"Erro ao processar o link {link}: {e}")

    return conteudos


def extrair_texto(link, area, tema, subtema,  assunto):    
    # Chamada da função
    conteudos = acessar_links(link)
    

    # Agora, você tem uma lista de dicionários com os links e os conteúdos dos artigos
    for conteudo in conteudos:
        #conteudo['link']
        conteudo = conteudo['conteudo']
        #print(f"Conteúdo: {conteudo['conteudo']}\n")
        # Dividir o conteúdo com base em "subconteúdo"
        
        # Use uma expressão regular para encontrar o texto entre 4 ou mais quebras de linha antes e depois
        # Use uma expressão regular para encontrar todas as seções separadas por quebras de linha
        secoes = re.split(r'\n{5,}', conteudo)

        # Inicialize variáveis para rastrear a seção com o maior conteúdo
        maior_secao = ""
        maior_comprimento = 0

        # Itere pelas seções e encontre a seção com o maior conteúdo de texto
        for secao in secoes:
            # Remova espaços em branco e quebras de linha para calcular o comprimento do texto real
            comprimento_secao = len(secao.strip().replace("\n", ""))
            if comprimento_secao > maior_comprimento:
                maior_secao = secao
                maior_comprimento = comprimento_secao

        maior_secao = maior_secao.strip()

        # Divida o texto em linhas
        linhas = maior_secao.splitlines()
        
        linhas_grandes = {}
        # Verifique se cada linha tem mais de 100 caracteres
        for i, linha in enumerate(linhas):
            if len(linha) > 100:
                linhas_grandes[i] = linha
                #print(f"Linha {i}: {linha}")
                


        # Conjunto para rastrear as linhas já verificadas
        linhas_verificadas = set()
        # Variável para armazenar o texto entre as repetições
        texto_entre_repeticoes = ""

        # Flag para indicar se já passamos pela primeira repetição
        passou_pela_primeira_repeticao = False

        indice_segunda_repeticao = False

        # Verifique se há linhas grandes com conteúdo idêntico
        for i, linha1 in linhas_grandes.items():
            # Verifique se a linha já foi verificada
            if i not in linhas_verificadas:
                # Inicialize uma lista para armazenar as linhas com conteúdo idêntico
                linhas_com_mesmo_conteudo = [i]

                for j, linha2 in linhas_grandes.items():
                    if i != j and linha1 == linha2:
                        linhas_com_mesmo_conteudo.append(j)
                        linhas_verificadas.add(j)
                
                # Se houver mais de uma linha com o mesmo conteúdo, imprima
                if len(linhas_com_mesmo_conteudo) > 1:
                    #print(f"Linhas {', '.join(map(str, linhas_com_mesmo_conteudo))} têm o mesmo conteúdo: {linha1}")
                    # Armazene o texto entre as repetições, excluindo a partir da segunda repetição
                    if not passou_pela_primeira_repeticao:
                        indice_primeira_repeticao = min(linhas_com_mesmo_conteudo)
                        passou_pela_primeira_repeticao = True
                        #indice_segunda_repeticao = linhas_com_mesmo_conteudo[1]
                    else:
                        indice_segunda_repeticao = linhas_com_mesmo_conteudo[0]

        # Agora você tem o texto entre as repetições em texto_entre_repeticoes, excluindo a partir da segunda repetição
        if passou_pela_primeira_repeticao:
            texto_entre_repeticoes = "\n".join(linhas[indice_primeira_repeticao:indice_segunda_repeticao])
        else:
            texto_entre_repeticoes = linhas

    'noticias_maior(tema, texto, entonacao), artigo_atual_maior(entonacao, tema, subtema, texto), artigo_atemporal_maior(entonacao, tema, subtema, assunto)'
    if  area == 'noticias':
        prompt = f'Escreva um artigo grande para postagem em um blog sobre {tema}, cite a fonte da informação se houver, sobre o seguinte assunto:\n\n{texto_entre_repeticoes}'
    
    else:
        prompt = f'Escreva um artigo grande para postagem em um blog sobre {tema}, relacionando uma aplicação prática de {subtema} ao assunto central do seguinte texto:\n\n{texto_entre_repeticoes}'
    


    resumo_gpt = asyncio.run(chatgpt(prompt))

    return resumo_gpt

if __name__ == "__main__":
    #link = 'https://news.google.com/./articles/CBMikgFodHRwczovL3d3dzEuZm9saGEudW9sLmNvbS5ici9jb3RpZGlhbm8vMjAyMy8wOS9jb20tb25kYS1kZS1jYWxvci1tYWlvcmlhLWRhcy1jYXBpdGFpcy1kZXZlLXJlZ2lzdHJhci1tYWlzLWRlLTMwMGMtbmVzdGEtc2V4dGEtdmVqYS1wcmV2aXNhby5zaHRtbNIBlgFodHRwczovL3d3dzEuZm9saGEudW9sLmNvbS5ici9hbXAvY290aWRpYW5vLzIwMjMvMDkvY29tLW9uZGEtZGUtY2Fsb3ItbWFpb3JpYS1kYXMtY2FwaXRhaXMtZGV2ZS1yZWdpc3RyYXItbWFpcy1kZS0zMDBjLW5lc3RhLXNleHRhLXZlamEtcHJldmlzYW8uc2h0bWw?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    link = 'https://portaldobitcoin.uol.com.br/microstrategy-compra-mais-r-730-milhoes-em-bitcoin/'
    print(extrair_texto(link))