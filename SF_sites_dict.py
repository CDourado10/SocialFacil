import json

def buscar_sites():
    lista_de_sites = {
        'noticias':{
            'sites':{
                'folha':{'site':'www1.folha.uol.com.br', 'srcset': 'UOL', 'confiabilidade': 7}, 
                'g1':{'site':'g1.globo.com', 'srcset': 'G1', 'confiabilidade': 7},
                'oglobo':{'site':'oglobo.globo.com', 'srcset': 'oglobo', 'confiabilidade': 7},
                'senado':{'site':'www12.senado.leg.br', 'srcset': 'senado', 'confiabilidade': 8},
                'stj':{'site':'stj.jus.br', 'srcset': 'stj.jus.br', 'confiabilidade': 8},
                'migalhas':{'site':'www.migalhas.com.br', 'srcset': 'Migalhas', 'confiabilidade': 6},
                'jota':{'site':'jota.info', 'srcset': 'JOTA', 'confiabilidade': 8},
                'cnn_brasil':{'site':'www.cnnbrasil.com.br', 'srcset': 'CNN Brasil', 'confiabilidade': 7},
                'valor_economico':{'site':'valor.globo.com', 'srcset': 'Valor Econômico', 'confiabilidade': 7},
                'epocanegocios':{'site':'epocanegocios.globo.com', 'srcset': 'epocanegocios', 'confiabilidade': 7},
                'terra':{'site':'www.terra.com.br', 'srcset': 'Terra', 'confiabilidade': 6},
                'valor_investe':{'site':'valorinveste.globo.com', 'srcset': 'Valor Investe', 'confiabilidade': 7},
                'infomoney':{'site':'www.infomoney.com.br', 'srcset': 'InfoMoney', 'confiabilidade': 6},
                'estadao':{'site':'www.estadao.com.br', 'srcset': 'estadao', 'confiabilidade': 7},
                'exame_noticias':{'site':'exame.com', 'srcset': 'Exame Notícias', 'confiabilidade': 6},
                'unesp':{'site':'jornal.unesp.br', 'srcset': 'unesp', 'confiabilidade': 8},
                'usp':{'site':'jornal.usp.br', 'srcset': 'usp', 'confiabilidade': 8},
                'uerj':{'site':'www.uerj.br/noticia', 'srcset': 'uerj', 'confiabilidade': 8},
                'ufrj':{'site':'conexao.ufrj.br', 'srcset': 'ufrj', 'confiabilidade': 8},
                'unb':{'site':'noticias.unb.br', 'srcset': 'unb', 'confiabilidade': 8},
                'harvard':{'site':'news.harvard.edu/gazette', 'srcset': 'harvard', 'confiabilidade': 10},
                'mit':{'site':'news.mit.edu', 'srcset': 'mit', 'confiabilidade': 10},
                'mitsloan':{'site':'mitsloan.mit.edu', 'srcset': 'mitsloan', 'confiabilidade': 10},
                'cornell':{'site':'news.cornell.edu', 'srcset': 'cornell', 'confiabilidade': 10},
                'nature':{'site':'www.nature.com/articles', 'srcset': 'nature', 'confiabilidade': 10}

            }
        },
        'famosos':{
            'sites':{
                'ofuximo': {'site': 'www.ofuxico.com.br', 'srcset': 'OFuxico', 'confiabilidade': 1},
                'area_vip': {'site': 'www.areavip.com.br', 'srcset': 'Área VIP', 'confiabilidade': 1},
                'r7.com': {'site': 'entretenimento.r7.com/famosos-e-tv', 'srcset': 'R7.com', 'confiabilidade': 2}
            }
        }
    }
            

    return lista_de_sites

def assuntos():
    lista_de_assuntos = {'inteligencia_artificial':{
                            'machine_learning': {
                                'Visão Computacional': {'revelancia': 9, 'publicado': None},
                                'Processamento de Linguagem Natural (NLP)': {'revelancia': 9, 'publicado': None},
                                'Recomendação de Conteúdo': {'revelancia': 8, 'publicado': None},
                                'Medicina e Saúde': {'revelancia': 9, 'publicado': None},
                                'Finanças': {'revelancia': 8, 'publicado': None},
                                'Indústria': {'revelancia': 7, 'publicado': None},
                                'Agricultura de Precisão': {'revelancia': 7, 'publicado': None},
                                'Mobilidade e Transporte': {'revelancia': 8, 'publicado': None},
                                'Educação': {'revelancia': 7, 'publicado': None},
                                'Segurança Cibernética': {'revelancia': 8, 'publicado': None}
                                },

                            'ciencia_de_dados':{ 
                                'Marketing Digital': {'revelancia': 8, 'publicado': None},
                                'Saúde e Medicina': {'revelancia': 9, 'publicado': None},
                                'Finanças': {'revelancia': 9, 'publicado': None},
                                'Educação': {'revelancia': 7, 'publicado': None},
                                'Recursos Humanos': {'revelancia': 6, 'publicado': None},
                                'Manufatura e Logística': {'revelancia': 8, 'publicado': None},
                                'Ciências Sociais': {'revelancia': 5, 'publicado': None},
                                'Meio Ambiente': {'revelancia': 7, 'publicado': None},
                                'Tecnologia da Informação': {'revelancia': 8, 'publicado': None},
                                'Esportes': {'revelancia': 6, 'publicado': None}
                                },
                            
                            'visao_computacional':{
                                'Veículos autônomos': {'revelancia': 10, 'publicado': None},
                                'Imagens médicas': {'revelancia': 9, 'publicado': None},
                                'Agricultura ': {'revelancia': 8, 'publicado': None},
                                'Reconhecimento facial': {'revelancia': 8, 'publicado': None},
                                'Entretenimento interativo': {'revelancia': 7, 'publicado': None},
                                'Fábricas': {'revelancia': 7, 'publicado': None},
                                'Rastreamento de pose humana': {'revelancia': 8, 'publicado': None},
                                'Gerenciamento de varejo': {'revelancia': 6, 'publicado': None},
                                'Rastreamento de pose humana': {'revelancia': 8, 'publicado': None},
                                'Segurança Pública': {'revelancia': 8, 'publicado': None}
                            }
                                
                        }
                    }  
    
    return lista_de_assuntos

def controle_post_user():
    post_user = {
        'id_usuario': 45,
        'id_pagina': 55,
        'area': 'inteligencia_artificial',
        'subarea': 'ciencia_de_dados',
        'categoria': 'Finanças',
        'link': 'https://www.sistemampa.com.br/colunistas-e-blogs/nord-research/financas-inteligencia-artificial-em-busca-do-calice-sagrado/',
        'horario': '16/07/2023 20:39'

    }

    return post_user

if __name__ == "__main__":
    sites = buscar_sites()
    print(sites)
    temas = assuntos()
    print(temas)