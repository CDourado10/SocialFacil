# Use a imagem Python oficial como base
FROM python:3.11.5

# Atualize o sistema e instale as dependências
RUN apt-get update && apt-get install -y \
    tesseract-ocr tesseract-ocr-por \
    libgl1-mesa-glx \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /SocialFacil

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt ./

# Instale as dependências
RUN pip install -r requirements.txt