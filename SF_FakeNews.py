from requests_html import HTMLSession
from pyppeteer import launch
import asyncio

def is_TrueNews(texto):
    async def TrueFunction():
        url = 'http://nilc-fakenews.herokuapp.com/'
        # Inicializa uma sessão HTTP com requests-html
        session = HTMLSession()

        # Inicializa o navegador Chromium com pyppeteer
        browser = await launch()
        page = await browser.newPage()

        # Define as informações de cabeçalho e cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        # Define as opções do navegador, incluindo cabeçalho e cookies
        await page.setExtraHTTPHeaders(headers)

        # Vai para a página da web
        await page.goto(url)

        # Preenche o campo de texto com o texto da notícia
        await page.type('#news', texto)

        # Clica no botão de envio
        await page.click('#send')

        # Aguarda um tempo para a página processar
        await asyncio.sleep(5)

        # Obtém o resultado da página após o processamento
        resultado = await page.evaluate('document.querySelector("#answer").textContent')
        await browser.close()
        return(resultado)

    resultadoTrueFunction = asyncio.run(TrueFunction())
    if "VERDADEIRA" in resultadoTrueFunction.upper():
        return True
    else:
        return False
        # Fecha o navegador


if __name__ == "__main__":
# Exemplo de uso da função
    url_da_pagina = 'http://nilc-fakenews.herokuapp.com/'
    texto_da_noticia = """Era uma vez, em um Brasil fictício onde a política tomava rumos inesperados, que o ex-presidente Luiz Inácio Lula da Silva e o ex-presidente Jair Bolsonaro, dois políticos que representavam espectros políticos opostos, surpreenderam o país ao anunciarem um evento inusitado: um casamento de Natal no mês de janeiro.

A notícia da união de Lula e Bolsonaro pegou a todos de surpresa, mas a explicação era mais simples do que se poderia imaginar. Os ex-presidentes decidiram deixar para trás suas rivalidades políticas e optaram por uma aliança pessoal. Eles se conheceram melhor durante uma conferência internacional sobre mudanças climáticas e descobriram que tinham muito em comum, além das diferenças ideológicas que os separavam.

O casamento aconteceria no dia 25 de janeiro, uma data que combinava elementos do Natal e do aniversário de ambos, criando assim um simbolismo especial. A cerimônia aconteceu em um sítio tranquilo no interior do Brasil, longe dos holofotes da mídia, com a presença apenas de familiares e amigos próximos.

O casamento foi uma celebração de amor, amizade e reconciliação. Durante a cerimônia, Lula e Bolsonaro trocaram votos emocionantes, prometendo apoiar e cuidar um do outro pelo resto de suas vidas. Eles também destacaram a importância de deixar de lado as diferenças políticas em prol do bem-estar do país.

Após a cerimônia, Lula e Bolsonaro se tornaram um exemplo de como a política não deveria dividir as pessoas a ponto de impedir a construção de pontes e relacionamentos saudáveis. Eles continuaram a se envolver em causas sociais, trabalhando juntos em projetos de educação, saúde e meio ambiente, unindo suas experiências e conhecimentos para fazer a diferença.

Essa história improvável de um casamento de Natal em janeiro entre Lula e Bolsonaro lembra a todos que, mesmo nas circunstâncias mais inesperadas, o entendimento mútuo e a amizade podem superar as barreiras políticas e unir as pessoas em busca de um Brasil melhor."""

    resultado = is_TrueNews(texto_da_noticia)
    print(888)
    print("Resultado da verificação:", resultado)
