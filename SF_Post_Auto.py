#from SF_Gerador_1 import Lista_Noticias
from SF_Gerador_2 import GerarNoticia
from SF_Insta_Post import *
from SF_Telegram_Functions import *
from SF_Info_User import *
from SF_extrair_texto import extrair_texto
from datetime import datetime, timedelta


def buscar_ids_usuarios_com_status_true(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE status = 1")
        ids_usuarios = cursor.fetchall()
        return [id[0] for id in ids_usuarios]  # Extrai apenas os IDs
    except psycopg2.Error as e:
        print(f"Erro ao buscar IDs de usuários com status True: {e}")
        return []


# Função para buscar informações de páginas de Instagram relacionadas a um usuário com critérios específicos
def buscar_paginas_usuario_com_critérios(conn, usuario_id):
    try:
        hora_atual = datetime.now().time()
        cursor = conn.cursor()
        cursor.execute("SELECT id_instagram_business_account, token_de_acesso, nome_pagina, area_geral, area_especifica, quantidade_posts_diarios, horario_posts FROM informacoes_pagina WHERE usuario_id = ? AND status = 1 AND postagem_automática = 1", (usuario_id,))

        pages_data = cursor.fetchall()
        pages_info = []
        for page_data in pages_data:
            page_info = {
                'id_instagram_business_account': page_data[0],
                'token_de_acesso': page_data[1],
                'nome_pagina': page_data[2],
                'area_geral': page_data[3],
                'area_especifica': page_data[4],
                'quantidade_posts_diarios': page_data[5],
                'horario_posts': page_data[6].split(',') if page_data[6] else None
            }
            pages_info.append(page_info)
        return pages_info
    except psycopg2.Error as e:
        print(f"Erro ao buscar páginas de Instagram para o usuário com critérios: {e}")
        return []

# Chamada da função para buscar informações de páginas de Instagram relacionadas a todos os usuários com critérios
with conectar_banco() as conn:
    usuarios_com_critérios = buscar_ids_usuarios_com_status_true(conn)
    for user_info in usuarios_com_critérios:
        # Obtém informações das páginas de Instagram relacionadas ao usuário
        pages_info = buscar_paginas_usuario_com_critérios(conn, user_info)
        
        print(pages_info)
        # Faça o que desejar com as informações de cada usuário e suas páginas de Instagram relacionadas


def criar_conteudo(conn, pages_info, texto):
    # Suponha que 'informacoes_pagina' seja a lista com informações de todas as páginas
    for pagina_info in pages_info:
        # Obtenha as informações relevantes da página
        id_instagram = pagina_info['id_instagram_business_account']
        token_acesso = pagina_info['token_de_acesso']
        nome_pagina = pagina_info['nome_pagina']
        area_geral = pagina_info['area']
        area_especifica = pagina_info['subarea']
        quantidade_posts = pagina_info['quantidade_posts_diarios']
        horario_posts = pagina_info['horario_posts']
        fez_postagem = pagina_info.get('fez_postagem', False)  # Adicione a chave 'fez_postagem' se ainda não existir
        
        sites = buscar_informacoes_provedor_sites(conn)
        

        assuntos_info = buscar_assuntos(conn)


        # Obtenha a hora atual
        hora_atual = datetime.now().time()
        
        # Encontre o próximo horário de postagem
        proximo_horario_postagem = None
        for horario_planejado in horario_posts:
            horario_planejado = datetime.strptime(horario_planejado, '%H:%M').time()
            if horario_planejado > hora_atual:
                proximo_horario_postagem = horario_planejado
                break
        
        # Se o próximo horário de postagem for encontrado e a postagem já foi feita, marque como Falso
        if proximo_horario_postagem is not None and fez_postagem and hora_atual >= proximo_horario_postagem:
            pagina_info['fez_postagem'] = False

        # Verifique se o usuário ainda não fez a postagem e a hora atual está dentro do intervalo de 2 horas antes do horário planejado
        if not fez_postagem:
            for horario_planejado in horario_posts:
                # Verifique se a hora atual está dentro do intervalo de 2 horas antes do horário planejado até o próprio horário planejado
                #hora_planejada = datetime.datetime.strptime(horario_planejado, '%H:%M')
                # Converter horários planejados em objetos de tempo
                hora_planejada = [datetime.strptime(horario, '%H:%M').time() for horario in horario_posts]
                # Obter o horário mais próximo
                #hora_planejada = min(hora_planejada, key=lambda x: abs(datetime.combine(datetime.date(1, 1, 1), x) - datetime.combine(datetime.date(1, 1, 1), hora_atual)))
                # Obter o horário mais próximo
                hora_proxima = min(hora_planejada, key=lambda x: abs(datetime.combine(datetime.today(), x) - datetime.combine(datetime.today(), hora_atual)))

                hora_proxima = datetime.now().replace(
                    hour=hora_proxima.hour, minute=hora_proxima.minute, second=0, microsecond=0
                )

                hora_atual_calc = datetime.now().replace(
                    hour=hora_atual.hour, minute=hora_atual.minute, second=0, microsecond=0
                )

                # Calculando a hora inicial (2 horas antes do horário planejado)
                hora_postagem_inicial = hora_proxima - timedelta(hours=2)

                if hora_postagem_inicial <= hora_atual_calc <= hora_proxima:
                    # Realize a postagem automática para esse usuário
                    #realizar_postagem(pagina_info)  # Substitua isso pela função real de postagem
                    for provedor in sites['nome_site']:
                        resultado = get_from_google_news(provedor, assunto, sites)
                    

                    # Marque o usuário como tendo feito a postagem para evitar postagens repetidas
                    pagina_info['fez_postagem'] = True
                    print(pagina_info)
                    break  # Saia do loop de horários

    
    return conteudo


    '''noticias, noticias_filter = Prompt_Gerador1('auto')
    message_text = "Selecione só e somente só a notícia que você acredita que trará mais engajamento para uma página no instagram de  para postar:\n\n"
    for i, noticia in enumerate(noticias_filter, start=1):
                    message_text += f"{i}. {noticia}\n"'''

