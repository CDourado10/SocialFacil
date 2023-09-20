import json


def log (log_caminho):
    try:
        with open(log_caminho, 'r') as log_file:
            log_data = json.load(log_file)
    except FileNotFoundError:
        # Se o arquivo não existe, crie uma lista vazia
        print("Caminho do log inválido ou inexistente")
        log_data = []
    
    return log_data

def add_to_log(new_item, json_file_path):
    # Carrega a lista do JSON existente (se o arquivo existir)
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Se o arquivo não existir, crie uma lista vazia
        data = []

    # Verifica se a lista tem mais de 20 itens
    if len(data) >= 20:
        # Remove o primeiro item da lista
        data.pop(0)

    # Adiciona o novo item à lista
    data.append(new_item)

    # Salva a lista de volta no arquivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)