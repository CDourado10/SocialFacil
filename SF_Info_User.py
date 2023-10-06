# -*- coding: utf-8 -*-
import psycopg2
from SF_Exception import *
from SF_sites_dict import *
from datetime import datetime
from psycopg2 import sql
from psycopg2 import errorcodes
import logging

# Configurar o logger
logging.basicConfig(filename='SF_extrair_texto_erros.log', level=logging.ERROR)

def informacoes_usuario():

    info_users = {
        1:{
            'nome': 'Astolfo',
            'sobrenome': 'Da Silva Pinto',
            'email': 'AstolfOTerrorDelas@OPica.com',
            'id_telegram': 1234567890,
            'status': False,
            'periodo_teste': False,
            'pagamento_pendente': True,
            'redes_sociais': {
                'informacoes_pagina':{
                    1:{
                        'rede_social': 'instagram',
                        'status': False,
                        'postagem_automatica': False,
                        'id_instagram_business_account': 1234567890,
                        'token_de_acesso': '',
                        'nome_pagina': 'DR. Astolfo',
                        'area_geral': ['medicina'],
                        'area_especifica': ['clinico_geral'],
                        'quantidade_posts_diarios': int(),
                        'horario_posts': ['09:00', '16:00', '21:00'],
                        'horario_agendado': []
                    }
                }
            }
        },  

        2:{
            'nome': 'Caleb',
            'sobrenome': 'Vasconcelos Dourado Jordao',
            'email': 'calebdourado@gmail.com',
            'id_telegram': 1636508473,
            'status': True,
            'periodo_teste': False,
            'pagamento_pendente': False,
            'redes_sociais': {
                'informacoes_pagina':{
                    1:{
                        'rede_social': 'instagram',
                        'status': True,
                        'postagem_automatica': True,
                        'id_instagram_business_account': 17841461813950424,
                        'token_de_acesso':'EAAL1JC8i6IgBOZCk8BdGbl3wZAyU5B33dwxK1vD3C5qIXCWztF7I4RRMqLNtZAVrWMZCSrL45gNORSAGZAVAmidwqThomGAYSniZAe6sQyZBMuDfWS6U1yhPat58BlGMiAe4Qp1qxx7EeiLqFTt3ls8ZCVYAsy4ETZAYnDjNO3CTXoNBEcv4841LZCO1ZBa',
                        'nome_pagina': 'iaeficaz',
                        'area_geral': ['inteligencia_artificial'],
                        'area_especifica': ['noticias'],
                        'quantidade_posts_diarios': 3,
                        'horario_posts': ['09:00', '16:00', '21:00'],
                        'horario_agendado': []
                    },
                    2:{
                        'rede_social': 'instagram',
                        'status': True,
                        'postagem_automatica': False,
                        'id_instagram_business_account': int(),
                        'token_de_acesso': '',
                        'nome_pagina': 'canto.da.fofoca',
                        'area_geral': ['famosos'],
                        'area_especifica': [],
                        'quantidade_posts_diarios': 3,
                        'horario_posts': ['09:00', '16:00', '21:00'],
                        'horario_agendado': []
                    },
                    3:{
                        'rede_social': 'instagram',
                        'status': True,
                        'postagem_automatica': False,
                        'id_instagram_business_account': int(),
                        'token_de_acesso': '',
                        'nome_pagina': 'beleza.no.ponto',
                        'area_geral': ['estetica'],
                        'area_especifica': [],
                        'quantidade_posts_diarios': 3,
                        'horario_posts': ['09:00', '16:00', '21:00'],
                        'horario_agendado': []
                    },
                    4:{
                        'rede_social': 'instagram',
                        'status': True,
                        'postagem_automatica': False,
                        'id_instagram_business_account': int(),
                        'token_de_acesso': '',
                        'nome_pagina': 'crypto.news.br',
                        'area_geral': ['criptomoedas'],
                        'area_especifica': ['noticias'],
                        'quantidade_posts_diarios': 3,
                        'horario_posts': ['09:00', '16:00', '21:00'],
                        'horario_agendado': []
                    }
                }
            }
        }
    }    

    return info_users



# Conectar ao banco de dados ou criar um novo se não existir
conn = psycopg2.connect(
    dbname='socialfacil_dados',
    user='cdourado',
    password='guitarra10',
    host='localhost',
    port='5432'
)

#=============================================================================================================
# FUNÇÕES DE CRIAÇÃO DAS TABELAS

# Função para criar a tabela de usuários no banco de dados
def criar_tabela_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(30),
            sobrenome VARCHAR(100),
            email VARCHAR(100),
            id_telegram INTEGER,
            status BOOLEAN,
            periodo_teste BOOLEAN,
            pagamento_pendente BOOLEAN,
            redes_sociais INTEGER
        )
    ''')

    conn.commit()
    cursor.close()


def criar_tabela_informacoes_pagina(conn):
    cursor = conn.cursor()
    # Criar tabela de informações da página do Instagram
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS informacoes_pagina (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER,
        rede_social VARCHAR(20),
        status BOOLEAN,
        postagem_automatica BOOLEAN,
        id_instagram_business_account BIGINT,
        token_de_acesso VARCHAR(1000),
        nome_pagina VARCHAR(50),
        area VARCHAR(30)[],
        subarea VARCHAR(30)[],
        quantidade_posts_diarios INTEGER,
        horario_posts TIME[],
        horario_agendado TIMESTAMP[],
        entonacao VARCHAR(20)
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
''')
    # Salvar as alterações no banco de dados
    conn.commit()
    cursor.close()

def criar_tabela_provedor_sites(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS provedor_sites (
            id SERIAL PRIMARY KEY,
            nome_site VARCHAR(25),
            site VARCHAR(60),
            srcset VARCHAR(25),
            confiabilidade INTEGER,
            area  VARCHAR(50)
            )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'provedor_sites' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'provedor_sites':", e)

def criar_tabela_assuntos(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assuntos (
        id SERIAL PRIMARY KEY,
        area VARCHAR(50),
        subarea VARCHAR(50),
        categoria VARCHAR(50),
        revelancia INTEGER,
        publicado TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'assuntos' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'assuntos':", e)

def criar_tabela_controle_post_user(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS controle_post_user (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        area VARCHAR(50),
        subarea VARCHAR(50),
        categoria VARCHAR(50),
        link VARCHAR(255),
        horario TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'controle_post_user' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'controle_post_user':", e)

def criar_tabela_info_post():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS info_post (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        titulo VARCHAR(50),
        texto VARCHAR(50),
        hashtag VARCHAR(50),
        imagem IMAGE,
        titulo_imagem TIMESTAMP,
        imagem_filtro IMAGE,
        video MP4,
        legenda_video,
        musica_video,
        edicao VARCHAR(50),
        data TIMESTAMP,
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'controle_post_user' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'controle_post_user':", e)

def criar_tabela_info_post():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS info_post (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        titulo VARCHAR(50),
        texto VARCHAR(50),
        hashtag VARCHAR(50),
        imagem IMAGE,
        titulo_imagem VARCHAR(50,
        imagem_filtro IMAGE,
        video VIDEO,
        legenda_video VARCHAR(5000),
        musica_video AUDIO,
        edicao VARCHAR(20)[],
        data TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'info_post' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'info_post':", e)


def criar_tabela_estatisticas_post():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas_post (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        id_post INTEGER REFERENCES info_post(id),
        curtir INTEGER,
        comentar INTEGER,
        compartlhar INTEGER,
        salvar INTEGER,
        data TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'estatisticas_post' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'estatisticas_post':", e)

def criar_tabela_estatisticas_pagina():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas_pagina (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        seguindo INTEGER,
        seguidor INTEGER,
        nao_seguidor INTEGER,
        alcance INTEGER,
        regioes VARCHAR(20)[],
        genero INTEGER,
        idade VARCHAR(20)[],
        data TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'estatisticas_pagina' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'estatisticas_pagina':", e)

def criar_tabela_estatisticas_gerais():
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas_gerais (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES usuarios(id),
        id_pagina INTEGER REFERENCES informacoes_pagina(id),
        seguindo INTEGER,
        seguidor INTEGER,
        nao_seguidor INTEGER,
        alcance INTEGER,
        regioes VARCHAR(20)[],
        genero INTEGER,
        idades VARCHAR(20)[],
        data TIMESTAMP
    )
    ''')
        conn.commit()
        cursor.close()
        print("Tabela 'estatisticas_gerais' criada com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao criar a tabela 'estatisticas_gerais':", e)


#=============================================================================================================
# FUNÇÕES PARA INSERIR DADOS NAS TABELAS

def inserir_usuario(conn, usuario):
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO usuarios (nome, sobrenome, email, id_telegram, status, periodo_teste, pagamento_pendente, redes_sociais)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    ''', (
        usuario['nome'],
        usuario['sobrenome'],
        usuario['email'],
        usuario['id_telegram'],
        usuario['status'],
        usuario['periodo_teste'],
        usuario['pagamento_pendente'],
        usuario['redes_sociais']
    ))
    conn.commit()
    usuario_id = cursor.fetchone()[0] # Pega o ID inserido com RETURNING
    cursor.close()
    return usuario_id



# Função para inserir dados na tabela redes_sociais
def inserir_dados_informacoes_pagina(conn, usuario_id, dados):
    cursor = conn.cursor()

    horario_posts = [datetime.strptime(horario, '%H:%M').time() for horario in dados['horario_posts']]
    horario_agendado = [datetime.strptime(horario, '%Y-%m-%d %H:%M') for horario in dados['horario_agendado']]

    cursor.execute(sql.SQL('''
    INSERT INTO informacoes_pagina (usuario_id, rede_social, status, postagem_automatica, id_instagram_business_account, token_de_acesso, nome_pagina, area_geral, area_especifica, quantidade_posts_diarios, horario_posts, horario_agendado, entonacao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''), (
        usuario_id,
        dados['status'],
        dados['rede_social'],
        dados['postagem_automatica'],
        dados['id_instagram_business_account'],
        dados['token_de_acesso'],
        dados['nome_pagina'],
        dados['area'],
        dados['subarea'],
        dados['quantidade_posts_diarios'],
        horario_posts,
        horario_agendado,
        dados['entonacao'],
        
    ))

    conn.commit()
    cursor.close()

def inserir_site(conn, site):
    try:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO provedor_sites (nome_site, site, srcset, confiabilidade, area)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        ''', (
            site['nome_site'],
            site['site'],
            site['srcset'],
            site['confiabilidade'],
            site['area']
        ))
        
        conn.commit()
        site_id = cursor.fetchone()[0]  # Pega o ID inserido com RETURNING
        cursor.close()
        return site_id
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir site:", e)


def inserir_assunto(conn, assunto):
    try:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO assuntos (area, subarea, categoria, revelancia, publicado)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        ''', (
            assunto['area'],
            assunto['subarea'],
            assunto['categoria'],
            assunto['revelancia'],
            assunto['publicado']
        ))
        
        conn.commit()
        assunto_id = cursor.fetchone()[0]  # Pega o ID inserido com RETURNING
        cursor.close()
        return assunto_id
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir assunto:", e)


def inserir_post_user(conn, post_user):
    try:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO controle_post_user (id_usuario, id_pagina, area, subarea, categoria, link, horario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        ''', (
            post_user['id_usuario'],
            post_user['id_pagina'],
            post_user['area'],
            post_user['subarea'],
            post_user['categoria'],
            post_user['link'],
            post_user['horario']
        ))
        
        conn.commit()
        post_user_id = cursor.fetchone()[0]  # Pega o ID inserido com RETURNING
        cursor.close()
        return post_user_id
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir informações na tabela 'controle_post_user':", e)




#=============================================================================================================
# FUNÇÕES PARA ATUALIZAR DADOS NAS TABELAS

def atualizar_usuario(conn, usuario_id, novos_dados):
    cursor = conn.cursor()

    # Verifique se o usuário existe com base no ID
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s", (usuario_id,))
    if cursor.fetchone()[0] == 0:
        raise UsuarioNaoEncontradoException(usuario_id)
    
    # Verifique se há pelo menos um campo em novos_dados
    if not any(field in novos_dados for field in ['nome', 'sobrenome', 'email', 'id_telegram', 'status', 'periodo_teste', 'pagamento_pendente', 'redes_sociais']):
        raise Exception(f"Nenhum campo de atualização fornecido pelo {usuario_id}")

    # Construa dinamicamente a parte SET da instrução UPDATE com base nos campos fornecidos em novos_dados
    update_set = []
    params = []

    if 'nome' in novos_dados:
        update_set.append('nome = %s')
        params.append(novos_dados['nome'])
    if 'sobrenome' in novos_dados:
        update_set.append('sobrenome = %s')
        params.append(novos_dados['sobrenome'])
    if 'email' in novos_dados:
        update_set.append('email = %s')
        params.append(novos_dados['email'])
    if 'id_telegram' in novos_dados:
        update_set.append('id_telegram = %s')
        params.append(novos_dados['id_telegram'])
    if 'status' in novos_dados:
        update_set.append('status = %s')
        params.append(novos_dados['status'])
    if 'periodo_teste' in novos_dados:
        update_set.append('periodo_teste = %s')
        params.append(novos_dados['periodo_teste'])
    if 'pagamento_pendente' in novos_dados:
        update_set.append('pagamento_pendente = %s')
        params.append(novos_dados['pagamento_pendente'])
    if 'redes_sociais' in novos_dados:
        update_set.append('redes_sociais = %s')
        params.append(novos_dados['redes_sociais'])

    # Execute a instrução UPDATE
    update_sql = f'''
    UPDATE usuarios
    SET {', '.join(update_set)}
    WHERE id = %s
    '''
    params.append(usuario_id)
    cursor.execute(update_sql, tuple(params))
    conn.commit()
    cursor.close()

def atualizar_informacoes_informacoes_pagina(conn, usuario_id, dados):
    cursor = conn.cursor()

    # Verifique se o usuário e as informações da rede social existem com base no ID do usuário
    cursor.execute("SELECT COUNT(*) FROM informacoes_pagina WHERE usuario_id = %s", (usuario_id,))
    if cursor.fetchone()[0] == 0:
        raise Exception(f"Informações de redes sociais não encontradas para o usuário {usuario_id}")

    # Construa dinamicamente a parte SET da instrução UPDATE com base nos campos fornecidos em dados
    update_set = []
    params = []

    if 'status' in dados:
        update_set.append('status = %s')
        params.append(dados['status'])
    if 'rede_social' in dados:
        update_set.append('rede_social = %s')
        params.append(dados['rede_social'])
    if 'postagem_automatica' in dados:
        update_set.append('postagem_automatica = %s')
        params.append(dados['postagem_automatica'])
    if 'id_instagram_business_account' in dados:
        update_set.append('id_instagram_business_account = %s')
        params.append(dados['id_instagram_business_account'])
    if 'token_de_acesso' in dados:
        update_set.append('token_de_acesso = %s')
        params.append(dados['token_de_acesso'])
    if 'nome_pagina' in dados:
        update_set.append('nome_pagina = %s')
        params.append(dados['nome_pagina'])
    if 'area' in dados:
        update_set.append('area = %s')
        params.append(dados['area'])
    if 'subarea' in dados:
        update_set.append('subarea = %s')
        params.append(dados['subarea'])
    if 'quantidade_posts_diarios' in dados:
        update_set.append('quantidade_posts_diarios = %s')
        params.append(dados['quantidade_posts_diarios']) 
    
    # Converter horario_posts de string para o tipo TIME
    if 'horario_posts' in dados:
        horario_posts = [datetime.strptime(horario, '%H:%M').time() for horario in dados['horario_posts']]
        update_set.append('horario_posts = %s')
        params.append(horario_posts)
    
    # Converter horario_agendado de string para o tipo TIMESTAMP
    if 'horario_agendado' in dados:
        horario_agendado = [datetime.strptime(horario, '%Y-%m-%d %H:%M') for horario in dados['horario_agendado']]
        update_set.append('horario_agendado = %s')
        params.append(horario_agendado)

    if 'entonacao' in dados:
        update_set.append('entonacao = %s')
        params.append(dados['entonacao'])

    # Execute a instrução UPDATE
    update_sql = f'''
    UPDATE informacoes_pagina
    SET {', '.join(update_set)}
    WHERE usuario_id = %s
    '''
    params.append(usuario_id)
    cursor.execute(update_sql, tuple(params))
    conn.commit()
    cursor.close()

def atualizar_site(conn, site_id, novos_dados):
    try:
        cursor = conn.cursor()

        # Verifique se o site existe com base no ID
        cursor.execute("SELECT COUNT(*) FROM provedor_sites WHERE id = %s", (site_id,))
        if cursor.fetchone()[0] == 0:
            raise SiteNaoEncontradoException(site_id)
        
        # Verifique se há pelo menos um campo em novos_dados
        if not any(field in novos_dados for field in ['nome_site', 'site', 'srcset', 'confiabilidade']):
            raise Exception(f"Nenhum campo de atualização fornecido para o site {site_id}")

        # Construa dinamicamente a parte SET da instrução UPDATE com base nos campos fornecidos em novos_dados
        update_set = []
        params = []

        if 'nome_site' in novos_dados:
            update_set.append('nome_site = %s')
            params.append(novos_dados['nome_site'])
        if 'site' in novos_dados:
            update_set.append('site = %s')
            params.append(novos_dados['site'])
        if 'srcset' in novos_dados:
            update_set.append('srcset = %s')
            params.append(novos_dados['srcset'])
        if 'confiabilidade' in novos_dados:
            update_set.append('confiabilidade = %s')
            params.append(novos_dados['confiabilidade'])
        if 'area' in novos_dados:
            update_set.append('area = %s')
            params.append(novos_dados['area'])

        # Execute a instrução UPDATE
        update_sql = f'''
        UPDATE provedor_sites
        SET {', '.join(update_set)}
        WHERE id = %s
        '''
        params.append(site_id)
        cursor.execute(update_sql, tuple(params))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao atualizar site:", e)

def atualizar_assunto(conn, assunto_id, novos_dados):
    try:
        cursor = conn.cursor()

        # Verifique se o assunto existe com base no ID
        cursor.execute("SELECT COUNT(*) FROM assuntos WHERE id = %s", (assunto_id,))
        if cursor.fetchone()[0] == 0:
            raise AssuntoNaoEncontradoException(assunto_id)
        
        # Verifique se há pelo menos um campo em novos_dados
        if not any(field in novos_dados for field in ['area', 'subarea', 'categoria', 'revelancia', 'publicado']):
            raise Exception(f"Nenhum campo de atualização fornecido para o assunto {assunto_id}")

        # Construa dinamicamente a parte SET da instrução UPDATE com base nos campos fornecidos em novos_dados
        update_set = []
        params = []

        if 'area' in novos_dados:
            update_set.append('area = %s')
            params.append(novos_dados['area'])
        if 'subarea' in novos_dados:
            update_set.append('subarea = %s')
            params.append(novos_dados['subarea'])
        if 'categoria' in novos_dados:
            update_set.append('categoria = %s')
            params.append(novos_dados['categoria'])
        if 'revelancia' in novos_dados:
            update_set.append('revelancia = %s')
            params.append(novos_dados['revelancia'])
        if 'publicado' in novos_dados:
            update_set.append('publicado = %s')
            params.append(novos_dados['publicado'])

        # Execute a instrução UPDATE
        update_sql = f'''
        UPDATE assuntos
        SET {', '.join(update_set)}
        WHERE id = %s
        '''
        params.append(assunto_id)
        cursor.execute(update_sql, tuple(params))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao atualizar assunto:", e)


def atualizar_controle_post_user(conn, usuario_id, pagina_id, dados):
    try:
        cursor = conn.cursor()

        # Verifique se o usuário e as informações da página existem com base nos IDs
        cursor.execute("SELECT COUNT(*) FROM controle_post_user WHERE id_usuario = %s AND id_pagina = %s", (usuario_id, pagina_id))
        if cursor.fetchone()[0] == 0:
            raise Exception(f"Dados de controle de postagem não encontrados para o usuário {usuario_id} e página {pagina_id}")

        # Construa dinamicamente a parte SET da instrução UPDATE com base nos campos fornecidos em dados
        update_set = []
        params = []

        if 'area' in dados:
            update_set.append('area = %s')
            params.append(dados['area'])
        if 'subarea' in dados:
            update_set.append('subarea = %s')
            params.append(dados['subarea'])
        if 'categoria' in dados:
            update_set.append('categoria = %s')
            params.append(dados['categoria'])
        if 'link' in dados:
            update_set.append('link = %s')
            params.append(dados['link'])
        if 'horario' in dados:
            # Converter horario de string para o tipo TIMESTAMP
            horario = datetime.strptime(dados['horario'], '%d/%m/%Y %H:%M')
            update_set.append('horario = %s')
            params.append(horario)

        # Execute a instrução UPDATE
        update_sql = f'''
        UPDATE controle_post_user
        SET {', '.join(update_set)}
        WHERE id_usuario = %s AND id_pagina = %s
        '''
        params.extend((usuario_id, pagina_id))
        cursor.execute(update_sql, tuple(params))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao atualizar dados de controle de postagem:", e)


#=============================================================================================================
# OUTRAS FUNÇÕES

def imprimir_informacoes_usuarios(conn):
    cursor = conn.cursor()

    # Consulta SQL para selecionar todos os usuários e suas informações
    cursor.execute('''
        SELECT u.id, u.nome, u.sobrenome, u.email, u.id_telegram, u.status, u.periodo_teste, u.pagamento_pendente, u.redes_sociais,
               ip.id, ip.rede_social, ip.status, ip.postagem_automatica, ip.id_instagram_business_account, ip.token_de_acesso, ip.nome_pagina, ip.area_geral,
               ip.area_especifica, ip.quantidade_posts_diarios, ip.horario_posts, ip.horario_agendado, ip.entonacao
        FROM usuarios u
        LEFT JOIN informacoes_pagina ip ON u.id = ip.usuario_id
        ORDER BY u.id, ip.id
    ''')

    # Recuperar todos os resultados da consulta
    resultados = cursor.fetchall()

    # Variável para rastrear o ID do usuário atual
    usuario_atual_id = None

    for row in resultados:
        usuario_id = row[0]
        if usuario_id != usuario_atual_id:
            # Nova entrada de usuário, imprima as informações do usuário
            if usuario_atual_id is not None:
                print("=" * 40)  # Linha de separação entre informações de usuários
                print(f"Informações do usuário com ID: {usuario_id}")
                print(f"Nome: {row[1]}")
                print(f"Sobrenome: {row[2]}")
                print(f"Email: {row[3]}")
                print(f"ID do Telegram: {row[4]}")
                print(f"Status: {'Ativo' if row[5] else 'Inativo'}")
                print(f"Período de teste: {'Sim' if row[6] else 'Não'}")
                print(f"Pagamento pendente: {'Sim' if row[7] else 'Não'}")
                print(f"Redes sociais: {row[8]}")
                usuario_atual_id = usuario_id

        # Imprima as informações da página, se disponíveis
        if row[9] is not None:
            print(f"Informações da Página com ID: {row[9]}")
            print(f"Rede social: {row[10]}")
            print(f"Status: {'Ativo' if row[11] else 'Inativo'}")
            print(f"Postagem automática: {'Ativo' if row[12] else 'Inativo'}")
            print(f"ID Instagram Business Account: {row[13]}")
            print(f"Token de Acesso: {row[14]}")
            print(f"Nome de Usuário: {row[15]}")
            print(f"Área Geral: {', '.join(row[16] if row[16] else 'N/A')}")
            print(f"Área Específica: {', '.join(row[17] if row[17] else 'N/A')}")
            print(f"Quantidade de Posts Diários: {row[18] if row[18] else 'N/A'}")
            print(f"Horário das Postagens: {row[19] if row[19] else 'N/A'}")
            print(f"Horário Agendado: {row[20] if row[20] else 'N/A'}")
            print(f"Entonacao do texto: {row[15]}")
    print("=" * 40)


def usuario_existe(conn, id_telegram):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id_telegram = %s", (id_telegram,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    except psycopg2.Error as e:
        print(f"Erro ao verificar se o usuário existe: {e}")
        return False

def pagina_existe(conn, rede_social, nome_pagina):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM informacoes_pagina WHERE rede_social = %s AND nome_pagina = %s", (rede_social, nome_pagina,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    except psycopg2.Error as e:
        print(f"Erro ao verificar se a página da rede social existe: {e}")
        return False

def conectar_banco():
    try:
        return psycopg2.connect(
            dbname='socialfacil_dados',
            user='cdourado',
            password='guitarra10',
            host='localhost',
            port='5432'
        )
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


#=============================================================================================================
# FUNÇÕES PARA BUSCAR DADOS NAS TABELAS


def buscar_informacoes_usuario(conn, id_telegram):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_telegram = %s", (id_telegram,))
        user_data = cursor.fetchone()
        if user_data:
            user_info = {
                'id': user_data[0],
                'nome': user_data[1],
                'sobrenome': user_data[2],
                'email': user_data[3],
                'id_telegram': user_data[4],
                'status': user_data[5],
                'periodo_teste': user_data[6],
                'pagamento_pendente': user_data[7],
                'redes_sociais': user_data[8]
            }
            cursor.close()
            return user_info
        else:
            cursor.close()
            return None
    except psycopg2.Error as e:
        print(f"Erro ao buscar informações do usuário: {e}")
        return None

def buscar_informacoes_pagina(conn, usuario_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM informacoes_pagina WHERE usuario_id = %s", (usuario_id,))
        redes_sociais_data = cursor.fetchall()
        redes_sociais_info = []

        for row in redes_sociais_data:
            info = {
                'id': row[0],
                'usuario_id': row[1],
                'rede_social': row[2],
                'status': row[3],
                'postagem_automatica': row[4],
                'id_instagram_business_account': row[5],
                'token_de_acesso': row[6],
                'nome_pagina': row[7],
                'area': row[8],
                'subarea': row[9],
                'quantidade_posts_diarios': row[10],
                'horario_posts': row[11],
                'horario_agendado': row[12],
                'entonacao': row[13]
            }
            redes_sociais_info.append(info)
        cursor.close()
        return redes_sociais_info
    except psycopg2.Error as e:
        print(f"Erro ao buscar informações de redes sociais: {e}")
        return None


def buscar_informacoes_provedor_sites(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM provedor_sites")
        sites = []

        for row in cursor.fetchall():
            site = {
                'id': row[0],
                'nome_site': row[1],
                'site': row[2],
                'srcset': row[3],
                'confiabilidade': row[4],
                'area': row[5]
            }
            sites.append(site)

        cursor.close()
        return sites
    except psycopg2.Error as e:
        print(f"Erro ao buscar informações do provedor de sites: {e}")
        return None
    
def buscar_assuntos(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assuntos")
        assuntos = cursor.fetchall()

        # Mapeie os resultados em uma lista de dicionários para facilitar o acesso aos dados
        assuntos_info = []
        for assunto in assuntos:
            assunto_info = {
                'id': assunto[0],
                'area': assunto[1],
                'subarea': assunto[2],
                'categoria': assunto[3],
                'revelancia': assunto[4],
                'publicado': assunto[5]
            }
            assuntos_info.append(assunto_info)

        cursor.close()
        return assuntos_info
    except psycopg2.Error as e:
        print(f"Erro ao buscar informações na tabela 'assuntos': {e}")
        return None


def buscar_informacoes_controle_post(conn, id_usuario, id_pagina):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM controle_post_user WHERE id_usuario = %s AND id_pagina = %s", (id_usuario, id_pagina))
        post_data = cursor.fetchone()
        if post_data:
            post_info = {
                'id_usuario': post_data[0],
                'id_pagina': post_data[1],
                'area': post_data[2],
                'subarea': post_data[3],
                'categoria': post_data[4],
                'link': post_data[5],
                'horario': post_data[6]
            }
            cursor.close()
            return post_info
        else:
            cursor.close()
            return None
    except psycopg2.Error as e:
        conn.rollback()  # Faça um rollback em caso de erro para evitar transações pendentes
        print(f"Erro ao buscar informações de controle de post: {e}")
        return None


def inserir_informacoes_usuarios_pagina(conn, info_users):
    cursor = conn.cursor()

    try:
        for usuario_id, usuario_data in info_users.items():
            # Inserir informações do usuário
            cursor.execute('''
                INSERT INTO usuarios (nome, sobrenome, email, id_telegram, status, periodo_teste, pagamento_pendente, redes_sociais)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                usuario_data['nome'],
                usuario_data['sobrenome'],
                usuario_data['email'],
                usuario_data['id_telegram'],
                usuario_data['status'],
                usuario_data['periodo_teste'],
                usuario_data['pagamento_pendente'],
                len(usuario_data['redes_sociais']['informacoes_pagina'].keys())  # Número de páginas de redes sociais
            ))
            usuario_id_inserido = cursor.fetchone()[0]  # Pega o ID inserido com RETURNING

            # Inserir informações das páginas de redes sociais
            for pagina_id, pagina_data in usuario_data['redes_sociais']['informacoes_pagina'].items():
                horario_posts = [datetime.strptime(horario, '%H:%M').time() for horario in pagina_data['horario_posts']]
                horario_agendado = [datetime.strptime(horario, '%Y-%m-%d %H:%M') for horario in pagina_data['horario_agendado']]

                cursor.execute(sql.SQL('''
                    INSERT INTO informacoes_pagina (usuario_id, rede_social, status, postagem_automatica, id_instagram_business_account, token_de_acesso, nome_pagina, area_geral, area_especifica, quantidade_posts_diarios, horario_posts, horario_agendado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''), (
                    usuario_id_inserido,
                    pagina_data['rede_social'],
                    pagina_data['status'],
                    pagina_data['postagem_automatica'],
                    pagina_data['id_instagram_business_account'],
                    pagina_data['token_de_acesso'],
                    pagina_data['nome_pagina'],
                    pagina_data['area'],
                    pagina_data['subarea'],
                    pagina_data['quantidade_posts_diarios'],
                    horario_posts,
                    horario_agendado,
                    pagina_data['entonacao']
                ))

        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        error_message = errorcodes.lookup(e.pgcode)
        conn.rollback()
        cursor.close()
        print(f"Erro do PostgreSQL: {error_message}")
        print("Detalhes do erro:", e)


if __name__ == '__main__':
    info_users = informacoes_usuario()
    # Criar as tabelas (se já não existirem)
    criar_tabela_usuarios(conn)
    criar_tabela_informacoes_pagina(conn)
    criar_tabela_provedor_sites(conn)
    criar_tabela_assuntos(conn)
    criar_tabela_controle_post_user(conn)

    inserir_informacoes_usuarios_pagina(conn, info_users)

    # Imprimir as informações dos usuários
    imprimir_informacoes_usuarios(conn)

    id_telegram = 1636508473
    user_info = buscar_informacoes_usuario(conn, id_telegram)
    print('user_info', user_info)

    lista_de_sites = buscar_sites()
    lista_de_assuntos = assuntos()

    # Loop para inserir sites
    for area in lista_de_sites:
        site = {}
        site['area'] = info['area']
        for provedor in lista_de_sites[area]['sites']:
            site['nome_site'] = provedor
            info = lista_de_sites['noticias']['sites'][provedor]
            site['site'] = info['site']
            site['srcset'] = info['srcset']
            site['confiabilidade'] = info['confiabilidade']
            site_id = inserir_site(conn, site)
            if site_id is not None:
                print(f"Site inserido com ID {site_id}")
            else:
                print("Erro ao inserir site")

    for geral in lista_de_assuntos['inteligencia_artificial']:
        assunto = {}
        assunto['area'] = 'inteligencia_artificial'
        assunto['subarea'] = geral
        for espessifico in lista_de_assuntos['inteligencia_artificial'][geral]:
            assunto['categoria'] = espessifico
            info = lista_de_assuntos['inteligencia_artificial'][geral][espessifico]
            assunto['revelancia'] = info['revelancia']
            assunto['publicado'] = info['publicado']
            assunto_id = inserir_assunto(conn, assunto)
    
    if assunto_id is not None:
        print(f"assunto inserido com ID {assunto_id}")
    else:
        print("Erro ao inserir assunto")

    conn.close()