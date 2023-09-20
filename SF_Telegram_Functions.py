from SF_Gerador_1 import *

def Prompt_Gerador1(prompt):
    parametros = {"qntmax": "5", "tempo": "", "provedores": "", "assunto": ""}
    filtro = prompt[6:]
    for x in range(len(filtro)):
        if filtro[x] == "=":
            for parametro in parametros.keys():
                if filtro[(x - len(parametro)):x].upper() == parametro.upper():
                    if filtro[x+1] == '"':
                        caracterstop = '"'
                        comeco = x + 2
                    else:
                        caracterstop = " "
                        comeco = x + 1
                    for y in range(comeco, len(filtro)):
                        if filtro[y] == caracterstop:
                            parametros[parametro] = filtro[comeco:y]
                            break
                        if  caracterstop == " " and y == (len(filtro) - 1):
                            parametros[parametro] = filtro[comeco:(y+1)]
    
    print(f'qntmax={parametros["qntmax"]}, assunto={parametros["assunto"]}, tempo={parametros["tempo"]}, provedores={parametros["provedores"]}')
    resultado = Lista_Noticias(qntmax=parametros["qntmax"], assunto=parametros["assunto"], tempo=parametros["tempo"], provedores=parametros["provedores"])
    return(resultado)