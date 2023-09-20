from SF_Noticias import *
from SF_LOG import *
import os
import time

log_nome = 'log.json'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
log_caminho = os.path.join(diretorio_atual, log_nome)

def Lista_Noticias(qntmax=10, assunto="", tempo="1d", provedores=""):
    qntmax = int(qntmax)
    Noticias = news_list_mother(qntmax=qntmax, assunto=assunto, tempo=tempo, provedores=provedores)
    Log_Load = list(log(log_caminho))
    Noticias_Filter = atualizar_lista(Noticias, Log_Load)
    print(Noticias_Filter)
    return Noticias, Noticias_Filter

if __name__ == "__main__":
    texto1, texto2 = Lista_Noticias()
    print(texto1)