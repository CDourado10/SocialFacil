import requests
from bs4 import BeautifulSoup
from lxml import html
from SF_Noticias_GET import *
from SF_sites_dict import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def news_list_mother(qntmax=10, assunto="", tempo="1d", provedores="", user_atuacao=['Direito'], user_atuacao_especifica = ['Notícias']):
    # Obter informações dos sites
    sites = buscar_sites()
    
    # Coletar todos os provedores aceitos
    todos_provedores = [provedor for area in sites.values() for categoria in area.values() for provedor in categoria.keys()]
    provedoresaceitos = set(todos_provedores)
    
    # Filtrar os provedores com base na área de atuação geral do usuário
    if not provedores:
        if user_atuacao:
            provedores = set()
            for area in user_atuacao:
                provedores |= {provedor.upper() for provedor in provedoresaceitos if provedor in {provedor for categoria in sites.get(area, {}).values() for provedor in categoria.keys()}}
        else:
            provedores = set(provedor.upper() for provedor in provedoresaceitos)

        # Filtrar os provedores específicos da categoria 'user_atuacao_especifica' se especificado
        provedores_especificos = set()
        for area in user_atuacao_especifica:
            for area_geral in user_atuacao:
                provedores_especificos |= {provedor.upper() for provedor in provedoresaceitos if provedor in sites.get(area_geral, {}).get(area, {}).keys()} if user_atuacao_especifica else provedores
    
    else:
        provedores = set(provedor.upper() for provedor in provedores.split(", "))

    # Determinar quais provedores usar com base na área específica do usuário
    provedoressolicitados = [provedor for provedor in provedoresaceitos if provedor.upper() in provedores] if not user_atuacao_especifica else [provedor for provedor in provedoresaceitos if provedor.upper() in provedores_especificos]
    combined_news = []
    for provedor in provedoressolicitados:
        getfrom = get_from_google_news(provedor=provedor, qntmax=qntmax, assunto=assunto, tempo=tempo, sites=sites)
        for noticia in getfrom:
            combined_news.append(noticia)
    return combined_news

def get_g1_news(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_elements = soup.find_all('p', class_='content-text__container')

    g1_news = ""

    for news_element in news_elements:
        news_text = news_element.text.strip()
        # Substituir "\n" por espaço em branco
        news_text = news_text.replace("\n", " ")
        # Excluir mensagem indesejada
        if "✅Clique aqui para seguir o novo canal do g1"  in news_text or "⚠️O grupo antigo será desativado. Mesmo que você já faça parte da nossa comunidade, é preciso se inscrever novamente." in news_text:
            continue
        g1_news += news_text + " "

    return g1_news

def get_jota_news(link):
    response = requests.get(link)
    response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontre o elemento que contém o corpo da notícia (classe 'jota-article__content')
    news_element = soup.find('div', class_='jota-article__content')

    if news_element:
        # Filtrar todos os parágrafos, exceto aqueles com a classe 'jota-article__byline'
        paragraphs = [paragraph for paragraph in news_element.find_all('p') if 'jota-article__byline' not in paragraph.get('class', [])]
        jota_news = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
        # Substituir "\n" por espaço em branco
        jota_news = jota_news.replace("\n", " ")
        return jota_news

def get_senado_news(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_element = soup.find('div', id='textoMateria')
    if news_element:
        paragraphs = news_element.find_all('p')
        senado_news = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
        senado_news = senado_news.replace("\n", " ")
        return senado_news
    
def get_migalhas_news(link):
    response = requests.get(link)
    response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontre o elemento que contém o corpo da notícia com classes contendo "clearfix" e "leitura-materia-"
    news_element = soup.find(lambda tag: tag.name == 'div' and 'clearfix' in tag.get('class', []) and 'leitura-materia-' in ' '.join(tag.get('class', '')))

    if news_element:
        # Filtrar todos os parágrafos dentro do elemento 'news_element'
        paragraphs = [paragraph.text.strip() for paragraph in news_element.find_all('p')]
        migalhas_news = ' '.join(paragraphs)
        return migalhas_news

def get_stj_news(link):
    # Abrir a página no navegador
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
    options = webdriver.EdgeOptions()
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument("--headless=new")
    driver = webdriver.Edge(options=options)

    driver.get(link)

    # Esperar até que um elemento específico seja carregado (pode ser qualquer elemento na página)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pstj_tabContCentro"))
    )
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text_elements = soup.find_all(['p', 'h2'])  # Extrair parágrafos e títulos h2

    extracted_text = []
    for element in text_elements:
        # Se o elemento for um parágrafo, adicione seu texto
        if element.name == 'p':
            extracted_text.append(element.get_text())
        # Se o elemento for um título h2, adicione-o como um cabeçalho
        elif element.name == 'h2':
            extracted_text.append(element.text)
    
    # Junte todos os textos em uma única string, separados por espaço
    full_text = ' '.join(extracted_text)
    
    # Substitua quebras de linha por espaços em branco
    full_text = full_text.replace('\n', ' ')
    driver.quit()
    return full_text

    
def get_folha_news(link):
    response = requests.get(link)
    tree = html.fromstring(response.content)
    
    # Use XPath para localizar todos os parágrafos da notícia
    paragraphs = tree.xpath('//div[@class="c-news__body"]//p/text()')

    # Junte os parágrafos em uma única string, removendo espaços extras
    news_text = " ".join(paragraphs)

    # Remove o texto indesejado
    unwanted_text = "Receba no seu email as notícias sobre o cenário jurídico e conteúdos exclusivos: análise, dicas e eventos; exclusiva para assinantes. Carregando..."
    news_text = news_text.replace(unwanted_text, '')

    # Substitui sequências de "\n" por um único espaço
    news_text = ' '.join(news_text.split())

    return news_text.strip()

def get_news_by_title_and_provider(title, news_list):
    for news_title, provider, link in news_list:
        if title == news_title:
            if provider == 'Folha':
                texto = get_folha_news(link)
            elif provider == 'Senado':
                texto = get_senado_news(link)
            elif provider == 'G1':
                texto = get_g1_news(link)
            elif provider == 'Migalhas':
                texto = get_migalhas_news(link)
            elif provider == 'STJ':
                texto = get_stj_news(link)
            elif provider == 'JOTA':
                texto = get_jota_news(link)
            else:
                return "Provedor de notícias não reconhecido"
            return provider, texto
    return "Notícia não encontrada na lista"

def atualizar_lista(listanoticias, listajson):
    # Criar um conjunto dos títulos da listajson para verificação eficiente
    titulos_listajson = set(listajson)
    
    # Filtrar as tuplas da listanoticias cujo título não está presente na listajson
    #print(listanoticias)
    listanoticias_filtrada = [tupla for tupla in listanoticias if tupla[0] not in titulos_listajson]
    
    # Extrair os títulos da listanoticias filtrada
    titulos_filtrados = [tupla[0] for tupla in listanoticias_filtrada]
    
    return titulos_filtrados

if __name__ == "__main__":
    migalhas_link = 'https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2023/17092023-Interpretacoes-do-STJ-sobre-o-instituto-da-interdicao-.aspx'
    migalhas_news = get_stj_news(migalhas_link)
    noticias_combinadas = news_list_mother()
    print(noticias_combinadas)