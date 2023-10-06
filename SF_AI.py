import g4f, asyncio
from bardapi import Bard, BardCookies
from unidecode import unidecode
import time
import asyncio
import logging

# Configurar o logger
logging.basicConfig(filename='SF_AI_erros.log', level=logging.ERROR)


async def bing_async(prompt):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 
    # Automatic selection of provider
    provedor = g4f.Provider.Bing
    # streamed completion
    #for provedor in provedores:
    try:
        response = await asyncio.wait_for(
                        asyncio.to_thread(
        g4f.ChatCompletion.create,
        model="gpt-3.5-turbo",
        provider= provedor, #provedor
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        ),
            timeout=60  # Tempo limite em segundos
        )
        if response is not None:
            return response
        
    except asyncio.TimeoutError:
        logging.error("Tempo limite de chamada excedido.")

    except Exception as e:
        logging.error("Erro ao chamar o bing na função g4f.ChatCompletion.create:", e)
        return None 


async def chatgpt_assyncio(prompt):
    # Automatic selection of provider
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    provedores = [
        g4f.Provider.Acytoo, g4f.Provider.Aichat, g4f.Provider.Ails, g4f.Provider.ChatBase, 
        g4f.Provider.ChatgptAi, g4f.Provider.You, g4f.Provider.Yqcloud
    ]

    max_tentativas = 5
    tentativas = 0

    while tentativas < max_tentativas:
        for provedor in provedores:
            try:
                response = await asyncio.wait_for(
                        asyncio.to_thread(
                    g4f.ChatCompletion.create,
                    model="gpt-3.5-turbo",
                    provider=provedor,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False,
                    ),
                 timeout=300  # Tempo limite em segundos
                )

                if response is not None:
                    return response

            except asyncio.TimeoutError:
                logging.error("Tempo limite de chamada excedido.")

            except Exception as e:
                logging.error(f"Erro ao chamar a função g4f.ChatCompletion.create com o provedor {provedor.__name__}: {e}")
                await asyncio.sleep(1)  # Aguarde um segundo antes de tentar o próximo provedor

        # Se nenhum provedor tiver sucesso, aguarde 1 minuto antes de tentar novamente
        tentativas += 1
        print(f"Tentativa {tentativas} de {max_tentativas}. Aguardando 1 minuto antes de tentar novamente.")
        await asyncio.sleep(60)

    print("Todos os provedores falharam após várias tentativas.")
    return None


async def bard_chamada(prompt):
    cookie_dict = {
        "__Secure-1PSID": "awire1qvsnyBJb9qYbUuqweAy_lqZITjirj5kL3HwdtMSmFh0XrTRb6MdNk2C3eqrF-Bcg.",
        "__Secure-1PSIDTS": "sidts-CjEB3e41hRibW6ZnpD1oOqqHh1IOm5sz7s3aIRHuuDTwKdl0-wGZI-qN77i9GVgx80FJEAA"
    }

    try:
        bard = BardCookies(cookie_dict=cookie_dict)
        
        resposta_bard_G = await asyncio.wait_for(
                        asyncio.to_thread(bard.get_answer, prompt
                ),
                 timeout=300)
        
        conteudo_G = resposta_bard_G['content']

        if conteudo_G is not None:
            return conteudo_G
        
    except asyncio.TimeoutError:
       logging.error("Tempo limite de chamada excedido.")

    except Exception as e:
        logging.error("Erro ao chamar o bard na função bard.get_answer:", e)
        return None 
    
async def chatgpt(prompt):
    result = await chatgpt_assyncio(prompt)
    return result

async def bard(prompt):
    result = await bard_chamada(prompt)
    return result

async def bing(prompt):
    result = await bing_async(prompt)
    return result

if __name__ == "__main__":
    #prompt = 'Fale detalhadamente sobre a teoria da relatividade'
    prompt = 'Escreva um texto para um post no instagram sobre inteligencia artificial, com um exemplo prático detalhado, para uma página de análise de dados'
    prompt2 = 'Escreva um texto para um post no instagram sobre inteligencia artificial, com um exemplo prático detalhado, para uma página de biologia'
    gpt = asyncio.run(chatgpt(prompt))
    print(gpt)
    #asyncio.run(run_all(prompt))