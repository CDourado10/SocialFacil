import requests
from imgur_uploader import *



def InstaUpload(image_path, LEGENDA, ID_instagram_business_account, ACCESS_TOKEN):
    #Fazendo upload ao Imgur
    uploader = ImgurClient(client_id="65e21235564102c", client_secret="131e60768f3c04e9b1fc107c7bbda6499c3bd852")
    result = uploader.upload_from_path(image_path)
    
    URL_IMAGE = result["link"]

    url = f"https://graph.facebook.com/v18.0/{ID_instagram_business_account}/media"

    # Crie os parâmetros da solicitação
    params = {
        "image_url": URL_IMAGE,
        "caption": LEGENDA,
        "access_token": ACCESS_TOKEN
    }

    # Faça a solicitação POST usando a biblioteca requests
    response = requests.post(url, params=params)

    # Verifique a resposta
    if response.status_code == 200:
        # Extrai o ID da resposta JSON
        response_data = response.json()
        creation_id = response_data.get("id")
        
        # Agora você pode usar o creation_id na segunda solicitação
        # Construa a URL da segunda solicitação
        url_publish = f"https://graph.facebook.com/v18.0/{ID_instagram_business_account}/media_publish"
        
        # Crie os parâmetros da segunda solicitação
        params_publish = {
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN
        }
        
        # Faça a segunda solicitação POST
        response_publish = requests.post(url_publish, params=params_publish)
        
        # Verifique a resposta da segunda solicitação
        if response_publish.status_code == 200:
            print("Segunda solicitação bem-sucedida!")
            print("Resposta:")
            print(response_publish.json())
        else:
            print(f"Erro na segunda solicitação. Código de status: {response_publish.status_code}")
            print("Resposta:")
            print(response_publish.text)
    else:
        print(f"Erro na primeira solicitação. Código de status: {response.status_code}")
        print("Resposta:")
        print(response.text)
