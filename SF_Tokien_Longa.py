import requests

# Defina as informações necessárias
graph_api_version = "v18.0"
app_id = "1293119424742546"
app_secret = "870b528712e08c7271b37f481004b6b3"
your_access_token = "EAASYFdP2xJIBOzMN2dcZAbPX3JpmgYQ4D5j0ZBIpUZCywmZBhZAAJxk9vk1xPzmScwoo9YxoaNdeYD8nnF76jFlW8RmOw3ZBxWreDs3T0sYZAKkhp9TwXfLPa7C0mZCAjGR8KmnyYx6JnCTbSDvwGYZARSLJOdAY0xeZBAy3hTrwyNFlhvqixC2lVZAnnvKYsvq9wjO6fMOVxkyzPgrHCEcKdnguSuaZBgRV1YwZD"

# Construa a URL da solicitação
url = f"https://graph.facebook.com/{graph_api_version}/oauth/access_token"

# Crie os parâmetros da solicitação
params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": your_access_token
}

# Faça a solicitação GET usando a biblioteca requests
response = requests.get(url, params=params)

# Verifique a resposta
if response.status_code == 200:
    print("Solicitação bem-sucedida!")
    print("Resposta:")
    print(response.json())
else:
    print(f"Erro na solicitação. Código de status: {response.status_code}")
    print("Resposta:")
    print(response.text)
