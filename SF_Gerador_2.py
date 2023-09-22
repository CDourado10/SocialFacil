from SF_Noticias import *
from SF_LOG import *
from SF_AI import  *
from SF_Tratamento_INFO import *
from SF_Imagem_Builder import *
from SF_FakeNews import *
import time
import os
import shutil

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

pasta_imagem_nome = "Imagens"
arquivo_modelo_nome = "modelo_connectjus.png"
log_nome = 'log.json'



Pasta = os.path.join(diretorio_atual, pasta_imagem_nome)
Modelo = os.path.join(diretorio_atual, arquivo_modelo_nome)
log_caminho = os.path.join(diretorio_atual, log_nome)


def limpar_itens_do_diretorio():
    try:
        # Lista todos os itens no diretório
        itens = os.listdir(Pasta)
        
        # Itera sobre os itens e os exclui individualmente
        for item in itens:
            item_path = os.path.join(Pasta, item)
            if os.path.isfile(item_path):
                # Exclui arquivos
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Exclui subdiretórios e seu conteúdo recursivamente
                shutil.rmtree(item_path)
    except Exception as e:
        print(f"Erro ao remover conteúdo de '{Pasta}': {str(e)}")

def GerarNoticia(noticia, listadenoticia):
    print("Limpando diretório de imagens")
    limpar_itens_do_diretorio()
    print("Extraindo texto da notícia original")
    Provedor, Noticia_Texto = get_news_by_title_and_provider(noticia, listadenoticia)
    BardPrompt = (f"{Noticia_Texto}\n\n"
        "Resuma essa notícia para um post de um portal de notícias de Direito do Instagram, seguindo o modelo:\n"
        "Título: [Aqui você fará um novo título para a notícia]\n"
        "Área: [Aqui você especificará qual área do Direito a notícia se relaciona]\n"
        "Texto: [Aqui você irá resumir a notícia em 3 parágrafos]\n"
        "Fonte: [Aqui você colocar o nome do Portal de notícias onde você tirou a informação]\n"
        "Hashtags: [Aqui você colocar as #]\n"
        "Imagem: [Imagem do post]")
    tentativas = 0
    noticiavalidada = False
    while tentativas < 11:
        print(f"Tentativa de geração de notícia: {tentativas}")
        NoticiaCriada = bard_chamada(BardPrompt)
        if "TÍTULO" in NoticiaCriada.upper() or "TITULO" in NoticiaCriada.upper():
            NoticiaFormatadaInput = NoticiaCriada.replace("*", "")
            NoticiaFormatada = parse_texto(NoticiaFormatadaInput)
            chaves = list(NoticiaFormatada.keys())
            #VerificarPrompt = f"Output: Apenas VERDADEIRO ou FALSO. Nada mais. Input: Todas as notícias em %POST% são verdadeiras, levando em conta %NOTICIA_REFERENCIA%?. \n\n %NOTICIA_REFERENCIA%: {Noticia_Texto}\n\n%POST% {NoticiaFormatada['texto']}"
            #VerificarNoticia = chatgpt(VerificarPrompt)
            VerificarNoticia = is_TrueNews(f"{NoticiaFormatada[chaves[0]]}\n\n{NoticiaFormatada[chaves[2]]}\n\n{NoticiaFormatada[chaves[4]]}")
            #if "VERDADEIRO" in VerificarNoticia.upper():
            if VerificarNoticia == True:
                noticiavalidada = True
                print("Notícia aprovada")
                break
            else:
                tentativas += 1
                print("Notícia reprovada")
    if noticiavalidada != True:
        return None

    print("Produzindo imagem")
    Imagemloc = imagebuilder(NoticiaFormatada[chaves[0]], noticia ,Pasta, Modelo)

    print("Adicionando ao Log")
    add_to_log(noticia, log_caminho)
    NoticiaFormatada[chaves[4]] = NoticiaFormatada[chaves[4]].replace('\n', '')
    TextoPost = f"{NoticiaFormatada[chaves[0]]}\n\n{NoticiaFormatada[chaves[2]]}\n\n{NoticiaFormatada[chaves[4]]}\n\nFonte: {Provedor}"
    print("Retornando")
    return(TextoPost, Imagemloc)

if __name__ == "__main__":
    lista1 = [('Lula chega a Cuba para encontro com o grupo G77 e a China', 'G1', 'https://g1.globo.com/politica/noticia/2023/09/15/lula-chega-a-cuba-para-encontro-do-grupo-g77-e-a-china.ghtml'), ('Por que 40% dos brasileiros não confiam no que Lula diz?', 'Folha', 'https://www1.folha.uol.com.br/tv/2023/09/por-que-40-dos-brasileiros-nao-confiam-no-que-lula-diz.shtml'), ('Em sessão especial, profissionais de educação física defendem sua importância', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/em-sessao-especial-profissionais-de-educacao-fisica-defendem-sua-importancia'), ('Suspeito e 4 parentes são mortos horas após assassinato de PMs', 'G1', 'https://g1.globo.com/pe/pernambuco/noticia/2023/09/15/apos-morte-de-dois-pms-em-tiroteio-encapuzados-matam-suspeito-e-parentes-dele.ghtml'), ('Lula chega a Cuba e deve criticar embargo dos EUA contra a ilha\n        \nPresidente participa de cúpula do G77', 'Folha', 'https://www1.folha.uol.com.br/mundo/2023/09/lula-chega-a-cuba-e-deve-criticar-embargo-dos-eua-contra-a-ilha.shtml'), ('Vai à promulgação PEC que evita perda de nacionalidade brasileira', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/vai-a-promulgacao-pec-que-evita-perda-de-nacionalidade-brasileira'), ('Irmãos de suspeito executados filmaram ataque de encapuzado', 'G1', 'https://g1.globo.com/pe/pernambuco/noticia/2023/09/15/irmaos-sao-mortos-a-tiros-por-homens-encapuzados-uma-das-vitimas-transmitiu-ataque-ao-vivo-em-rede-social.ghtml'), ('Decreto de Lula no saneamento leva empresas municipais à Justiça', 'Folha', 'https://www1.folha.uol.com.br/mercado/2023/09/decreto-de-lula-no-saneamento-leva-empresas-municipais-a-justica.shtml'), ('Esperidião Amin pede sessão temática para discutir clima e desastres naturais', 'Senado', 'https://www12.senado.leg.br/noticias/audios/2023/09/esperidiao-amin-pede-sessao-tematica-para-discutir-clima-e-desastres-naturais'), ('Agente da PF e 4 suspeitos são mortos em operação em Salvador', 'G1', 'https://g1.globo.com/ba/bahia/noticia/2023/09/15/confronto-valeria-salvador.ghtml'), ('CNJ vê possível conluio no controle de valores pagos em acordos da Lava Jato', 'Folha', 'https://www1.folha.uol.com.br/poder/2023/09/cnj-afirma-que-houve-possivel-conluio-no-controle-de-valores-pagos-em-acordos-da-lava-jato.shtml'), ('Pacheco não garante aprovação de minirreforma eleitoral em duas semanas', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/pacheco-nao-garante-aprovacao-de-minirreforma-eleitoral-em-duas-semanas'), ('Preso, blogueiro condenado por bomba em aeroporto chega a Brasília', 'G1', 'https://g1.globo.com/df/distrito-federal/noticia/2023/09/15/blogueiro-condenado-por-ligacao-com-bomba-colocada-perto-do-aeroporto-e-transferido-para-brasilia.ghtml'), ("Advogado confunde 'O Pequeno Príncipe' com 'O Príncipe' em julgamento do 8/1", 'Folha', 'https://www1.folha.uol.com.br/poder/2023/09/advogado-confunde-o-pequeno-principe-com-o-principe-em-julgamento-do-81-entenda.shtml'), ('Estudo aponta que emendas de bancada se transformaram em individuais', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/estudo-aponta-que-emendas-de-bancada-se-transformaram-em-individuais'), ('Quer receber notícias no WhatsApp? Veja como seguir os Canais do g1', 'G1', 'https://g1.globo.com/tecnologia/noticia/2023/09/13/g1-canais-whatsapp.ghtml'), ('Liberação do aborto voltará à pauta do STF; veja como tema é encarado na América Latina\n        \nSupremo Tribunal Federal deve julgar em breve ação que pede descriminalização', 'Folha', 'https://www1.folha.uol.com.br/cotidiano/2023/09/liberacao-do-aborto-voltara-a-pauta-do-stf-veja-como-tema-e-encarado-na-america-latina.shtml'), ('Projeto que altera prazos da Lei da Ficha Limpa chega ao Senado', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/projeto-que-altera-prazos-da-lei-da-ficha-limpa-chega-ao-senado'), ('Compras de até US$ 50: Amazon e Shopee pedem isenção de imposto', 'G1', 'https://g1.globo.com/economia/noticia/2023/09/15/compras-internacionais-de-us-50-amazon-e-shopee-formalizam-pedido-de-adesao-ao-programa-da-receita.ghtml'), ('Livros com personagens quilombolas ajudam pequeno leitor a se identificar\n        \nAutores dão à nova geração referências que pessoas mais velhas não tiveram', 'Folha', 'https://www1.folha.uol.com.br/folhinha/2023/09/infancia-sem-estereotipos-dos-livros-quilombolas-ajuda-leitor-a-sentir-identificacao.shtml'), ('Regulamentação de apostas esportivas será analisada pelo Senado', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/regulamentacao-de-apostas-esportivas-sera-analisada-pelo-senado'), ('João de Deus é condenado de novo, e pena chega a 489 anos de prisão', 'G1', 'https://g1.globo.com/go/goias/noticia/2023/09/15/joao-de-deus-e-condenado-a-mais-de-118-anos-de-prisao-por-crimes-sexuais-condenacoes-somam-quase-500-anos.ghtml'), ('Mercado Livre e Amazon pedem para participar do Remessa Conforme\n        \nPrograma federal isenta de imposto de importação compras até US$ 50', 'Folha', 'https://www1.folha.uol.com.br/mercado/2023/09/mercado-livre-e-amazon-pedem-para-participar-do-remessa-conforme.shtml'), ('CPMI: relatora protocola pedido de acareação entre Bolsonaro e Mauro Cid', 'Senado', 'https://www12.senado.leg.br/noticias/videos/2023/09/cpmi-relatora-protocola-pedido-de-acareacao-entre-bolsonaro-e-mauro-cid'), ('Estudante de medicina vira réu por agressões ao ator Victor Meyniel', 'G1', 'https://g1.globo.com/rj/rio-de-janeiro/noticia/2023/09/15/estudante-de-medicina-vira-reu-por-agressoes-ao-ator-victor-meyniel.ghtml'), ('Foto de policiais ao lado de Danilo Cavalcante seria considerada irregular no Brasil\n        \nAgentes posaram com brasileiro que foi capturado após escapar de prisão', 'Folha', 'https://www1.folha.uol.com.br/cotidiano/2023/09/foto-de-policiais-ao-lado-de-danilo-cavalcante-seria-considerada-irregular-no-brasil.shtml'), ('IFI revê crescimento do PIB, mas alerta para riscos fiscais', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/ifi-reve-crescimento-do-pib-mas-alerta-para-riscos-fiscais'), ('Santos, na zona de rebaixamento, demite Diego Aguirre após cinco jogos\n        \nUruguaio é o oitavo nome descartado pelo presidente do clube paulista, Andres Rueda', 'Folha', 'https://www1.folha.uol.com.br/esporte/2023/09/santos-na-zona-de-rebaixamento-demite-aguirre-apos-cinco-jogos.shtml'), ('Dia do Cerrado: bioma está em modo sobrevivência', 'Senado', 'https://www12.senado.leg.br/noticias/infomaterias/2023/09/dia-do-cerrado-bioma-esta-em-modo-sobrevivencia'), ('Contas públicas: IFI alerta para risco de descumprimento da meta fiscal em 2024', 'Senado', 'https://www12.senado.leg.br/noticias/videos/2023/09/contas-publicas-ifi-alerta-para-risco-de-descumprimento-da-meta-fiscal-em-2024'), ('Pacheco descarta rapidez na votação da minirreforma eleitoral', 'Senado', 'https://www12.senado.leg.br/noticias/audios/2023/09/pacheco-descarta-rapidez-na-votacao-da-minirreforma-eleitoral'), ('Senado Aprova: reforço no Fundo para Calamidades é destaque', 'Senado', 'https://www12.senado.leg.br/noticias/videos/2023/09/senado-aprova-reforco-no-fundo-para-calamidades-e-destaque'), ('Compensação por perdas de ICMS de combustíveis será analisada pelo Senado', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/compensacao-por-perdas-de-icms-de-combustiveis-sera-analisada-pelo-senado'), ('CAS aprova aumento de penas para agressão a profissional de saúde em atendimento', 'Senado', 'https://www12.senado.leg.br/noticias/audios/2023/09/cas-aprova-aumento-de-penas-para-agressao-a-profissional-de-saude-em-atendimento'), ("Girão: matéria de revista desrespeita cristãos e reforça 'campanha antinatalista'", 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/girao-materia-de-revista-desrespeita-cristaos-e-reforca-campanha-antinatalista'), ('Comissão de Ciência e Tecnologia aprova incentivo a pesquisas com nanotecnologia', 'Senado', 'https://www12.senado.leg.br/noticias/audios/2023/09/comissao-de-ciencia-e-tecnologia-aprova-incentivo-a-pesquisas-com-nanotecnologia'), ('Relator de texto que limita juros do cartão, Rodrigo Cunha vê superendividamento', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/relator-de-texto-que-limita-juros-do-cartao-rodrigo-cunha-lamenta-o-superendividamento'), ('Lei concede auxílio-aluguel para mulher vítima de violência', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/lei-concede-auxilio-aluguel-para-mulher-vitima-de-violencia'), ('Servidores e empregados do Poder Executivo têm reajuste de 9%', 'Senado', 'https://www12.senado.leg.br/noticias/materias/2023/09/15/servidores-e-empregados-do-poder-executivo-tem-reajuste-de-9')]
    Noticia1 = 'Irmãos de suspeito executados filmaram ataque de encapuzado'
    print(GerarNoticia(Noticia1, lista1))