import g4f
from bardapi import Bard, BardCookies
from unidecode import unidecode


cookie_dict = {
        "__Secure-1PSID": "awire-HTm04Q42Qcf-lWmw8wTGftPgNMHoxpMXk17iGJGA7PZb-fzTIibNz0m4m4SnJL8A.",
        "__Secure-1PSIDTS": "sidts-CjIBSAxbGQMk9o4iGpBGR5MqLm3WMzJ3uOnhUT8SgiCPq4P09ty9S7tlsOMifIxSFJp96RAA"
    }

bard = BardCookies(cookie_dict=cookie_dict)

def chatgpt(prompt):
    # Automatic selection of provider
    provedores = [g4f.Provider.Ails, g4f.Provider.DeepAi]
    # streamed completion
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=provedores[1],
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )

    return response

def bard_chamada(prompt):
    
    resposta_bard_G = bard.get_answer(prompt)
    conteudo_G = resposta_bard_G['content']

    return conteudo_G