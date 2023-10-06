
class prompts():
    def __init__(self, id_user, id_pagina, id_site, id_assuntos, entonacao):
      self.user = id_user
      self.pagina = id_pagina
      self.site = id_site
      self.assunto = id_assuntos
      self.entonacao = entonacao

    def noticias_maior(tema, texto, entonacao):
        prompt = f'''
        Escreva um artigo grande com entonação {entonacao} para publicação em um blog de {tema}, 
        cite a fonte da informação se houver, sobre o seguinte texto:\n\n{texto}
        '''
        return prompt
    
    def artigo_atual_maior(entonacao, tema, subtema, texto):
        prompt = f'''
        Escreva um artigo grande com entonação {entonacao} para postagem em um blog de {tema}, 
        relacionando uma aplicação prática de {subtema} ao assunto central do seguinte texto:\n\n{texto}
        '''
        return prompt

    def artigo_atemporal_maior(entonacao, tema, subtema, assunto):
        prompt = f'''
        Escreva um texto grande com entonação {entonacao} para postagem em um blog de {tema}.\n
        O texto deve falar sobre como {subtema} pode ser aplicado em {assunto}.\n
        Cite pelo menos três exemplos detalhados de uso prático ou possíveis usos práticos dessa aplicação.
        '''
        return prompt
    
    def verificar_titulos(tema, titulos, n_titulos=25):
        prompt = f'''
        Retorne só e somente só os números que correspondam aos {n_titulos} titulos, 
        com maior proximidade do tema {tema}, em ordem de maior relação.\n\nTítulos:\n{titulos}
        '''
        return prompt
    
    def verificar_titulos_auto(tema, titulos):
        prompt = f'''
        Retorne só e somente só o número que corresponda ao titulo com maior relação com o tema {tema}.\n\n
        Títulos:\n{titulos}
        '''
        return prompt
    
    def titulo_imagem(tema, texto):
        prompt = f'''
        Escreva só e somente só o título para colocar em uma imagem que servirá de post para uma página no 
        instagram sobre {tema}.\nUtilize o conteúdo do post para se inspirar em um título que capte a atenção 
        do não seguidor.\nO título deve ser curto e relacionar a dor/prazer comum de uma pessoa.\n\nConteúdo 
        do post:\n{texto}
        '''
        return prompt
    
    def noticia(titulo, texto, entonacao, tema):
        prompt = f'''
        Título notícia de referência: {titulo}\n\nTexto da notícia de referencia: {texto}\n\n
        Faça dessa notícia um post para o Instagram com uma entonação {entonacao} de um portal de notícias 
        de {tema}.\n Siga o modelo:\n
        Título: [Aqui você fará um novo título para a notícia]\n
        Área: [Aqui você especificará qual área de {tema} a notícia se relaciona]\n
        Texto: [Aqui você irá resumir a notícia em 3 parágrafos. Evite fazer falsas conclusões. 
        Cite a fonte caso haja. Faça um CTA persuasivo]\n
        Hashtags: [Aqui você irá colocar as #]\n
        Imagem: [Aqui você irá colocar um título para inserir na imagem]
        '''
        return prompt
    
    def artigo_atual(titulo, texto, entonacao, tema):
        prompt = f'''
        Título notícia de referência: {titulo}\n\nTexto da notícia de referencia: {texto}\n\n
        Escreva um artigo com uma entonação {entonacao} relacionando o assunto princial da notícia inserida 
        ao tema {tema}.\n
        Demonstre de maneira prática como o {tema} pode ser aplicado para contribuir com o assunto principal 
        da notícia inserida
        \n Siga o modelo:\n
        Título: [Aqui você fará um título para o artigo]\n
        Área: [Aqui você especificará qual área de {tema} a notícia se relaciona]\n
        Texto: [Aqui você irá resumir, em 3 parágrafos, como o {tema} pode contribuir de maneira prática com 
        a notícia. Evite fazer falsas conclusões. 
        Cite a fonte caso haja. Faça um CTA persuasivo]\n
        Hashtags: [Aqui você irá colocar as #]\n
        Imagem: [Aqui você irá colocar um título para inserir na imagem]
        '''
        return prompt

titulo = 'asdfkjdf'
texto = 'asdlkfjaslkdjfa   aosdjf ojwoiej rioo o jeor woiejro qwoeirj ooqwe oiwe oirjoiwqe ro'
tema = 'diereito'
self = 'a'
asdf = prompts.verificar_titulos(tema, titulo, 10)

print(asdf)
    

            