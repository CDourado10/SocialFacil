import requests
from bs4 import BeautifulSoup
from lxml import html
import urllib.parse
from SF_sites_dict import *


def get_from_google_news(provedor="Folha", qntmax=10, assunto="", tempo="1d", sites={}):

    # Verificar se o provedor existe nos sites
    provedor_info = None
    for area in sites.values():
        for categoria in area.values():
            if provedor in categoria:
                provedor_info = categoria[provedor]
                break
        if provedor_info:
            break
    
    if provedor_info:
        # Extrair as informações de site e srcset
        site = provedor_info['site']
        srcset = provedor_info['srcset']

    parametros = f"{site if site else ''}{f' {assunto}' if assunto != '' else ''}{f' when:{tempo}' if tempo != '' else ''}"
    parametros = urllib.parse.quote(parametros)
    link = f"https://news.google.com/search?q={parametros}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
    # Faça a solicitação HTTP
    response = requests.get(link)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Parse o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')
        root = html.fromstring(response.text)

        # Inicialize uma lista para armazenar as tuplas (título, provedor, link)
        resultados = []

        # Itere sobre os elementos com base na condição
        for noticia in range(1, qntmax + 1):
            img_element = root.xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[{noticia}]/div/article/div[1]/img[1]')
            try:
                if srcset in html.tostring(img_element[0], encoding="utf-8").decode("utf-8"):
                    titulo_element = root.xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[{noticia}]/div/article/h3/a/text()')
                    link_element = root.xpath(f'/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[{noticia}]/div/article/h3/a/@href')
                    # Pegue o título
                    if titulo_element:
                        titulo = titulo_element[0]
                    else:
                        continue
                    # Pegue o link
                    if link_element:
                        link = f"https://news.google.com/{link_element[0]}"
                    else:
                        continue
                    # Adicione a tupla à lista de resultados
                    resultados.append((titulo, provedor, link))
            except:
                continue
        # Retorne a lista de resultados
        return resultados

    else:
        print('Falha na solicitação HTTP.')

def get_from_senado(qntmax=10):
    senado_url = "https://www12.senado.leg.br/noticias/ultimas"
    response = requests.get(senado_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_elements = soup.find_all('li')

    senado_news = []

    for news_element in news_elements:
        if len(senado_news) >= qntmax:
            break  # Parar após encontrar 10 notícias
        title_element = news_element.find('span', class_='eta normalis-xs')
        link_element = news_element.find('a', href=True)

        if title_element and link_element:
            title = title_element.text.strip()
            link = link_element['href']
            senado_news.append((title, 'Senado', f"https://www12.senado.leg.br{link}"))

    return senado_news



if __name__ == "__main__":
    resultados = get_from_google_news(provedor="JOTA", qntmax=10, assunto="", tempo="")
    for resultado in resultados:
        print(resultado)


