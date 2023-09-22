import re
from unidecode import unidecode


def parse_texto(texto):
    padrao = r'([^\n:]+):(.*?)(?=\n\w+:|$)'
    resultados = re.findall(padrao, texto, re.DOTALL)

    parsed_data = {}
    for chave, valor in resultados:
        chave_normalizada = unidecode(chave.strip().lower())
        valor_normalizado = valor.strip()
        parsed_data[chave_normalizada] = valor_normalizado

    return parsed_data