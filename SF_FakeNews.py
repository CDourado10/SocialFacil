import requests
import json

def request_fakenews(texto):
    # URL da solicitação POST
    url = "http://nilc-fakenews.herokuapp.com/ajax/check_web/"

    # Dados para enviar na solicitação POST
    data = {
        "text": texto,
        "model": "unigramas"  # Você pode ajustar o valor do modelo conforme necessário
    }

    # Cabeçalhos da solicitação
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": str(len(data)),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "csrftoken=K6F3j5BcHaKbl3ltjdl6A2NLhFJyHNiB62Cm1sJACeBzLJWfPdxNKKDB1HxNKqoN",
        "Host": "nilc-fakenews.herokuapp.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
        "X-Csrftoken": "K6F3j5BcHaKbl3ltjdl6A2NLhFJyHNiB62Cm1sJACeBzLJWfPdxNKKDB1HxNKqoN",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # Envia a solicitação POST
        response = requests.post(url, data=data, headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            return response.text  # Retorna a resposta do servidor
        else:
            return f"Erro na solicitação: Código de status {response.status_code}"
    except Exception as e:
        return f"Erro na solicitação: {str(e)}"

def is_TrueNews(texto):
    resposta = json.loads(request_fakenews(texto))
    if "result" in resposta:
        if resposta["result"] == "REAL":
            return True
        else:
            return False
    else:
        return resposta


if __name__ == "__main__":
# Exemplo de uso da função
    texto_da_noticia = """Era uma vez, em um Brasil fictício onde a política tomava rumos inesperados, que o ex-presidente Luiz Inácio Lula da Silva e o ex-presidente Jair Bolsonaro, dois políticos que representavam espectros políticos opostos, surpreenderam o país ao anunciarem um evento inusitado: um casamento de Natal no mês de janeiro.

A notícia da união de Lula e Bolsonaro pegou a todos de surpresa, mas a explicação era mais simples do que se poderia imaginar. Os ex-presidentes decidiram deixar para trás suas rivalidades políticas e optaram por uma aliança pessoal. Eles se conheceram melhor durante uma conferência internacional sobre mudanças climáticas e descobriram que tinham muito em comum, além das diferenças ideológicas que os separavam.

O casamento aconteceria no dia 25 de janeiro, uma data que combinava elementos do Natal e do aniversário de ambos, criando assim um simbolismo especial. A cerimônia aconteceu em um sítio tranquilo no interior do Brasil, longe dos holofotes da mídia, com a presença apenas de familiares e amigos próximos.

O casamento foi uma celebração de amor, amizade e reconciliação. Durante a cerimônia, Lula e Bolsonaro trocaram votos emocionantes, prometendo apoiar e cuidar um do outro pelo resto de suas vidas. Eles também destacaram a importância de deixar de lado as diferenças políticas em prol do bem-estar do país.

Após a cerimônia, Lula e Bolsonaro se tornaram um exemplo de como a política não deveria dividir as pessoas a ponto de impedir a construção de pontes e relacionamentos saudáveis. Eles continuaram a se envolver em causas sociais, trabalhando juntos em projetos de educação, saúde e meio ambiente, unindo suas experiências e conhecimentos para fazer a diferença.

Essa história improvável de um casamento de Natal em janeiro entre Lula e Bolsonaro lembra a todos que, mesmo nas circunstâncias mais inesperadas, o entendimento mútuo e a amizade podem superar as barreiras políticas e unir as pessoas em busca de um Brasil melhor."""

    resultado = is_TrueNews(texto_da_noticia)
    print(888)
    print("Resultado da verificação:", resultado)
