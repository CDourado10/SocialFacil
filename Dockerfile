# Use a imagem Python oficial como base
FROM python:latest

# Atualize o sistema
RUN apt-get update && apt-get upgrade -y

# Instale o Tesseract OCR (Linux)
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y tesseract-ocr-por

# Defina o diretório de trabalho
WORKDIR /SocialFacil

# Copie os arquivos do projeto para o contêiner
COPY ./Bot\Telegram\* ./

# Instale as dependências
RUN pip install -r requirements.txt

# Configure o comando de entrada
CMD ["python", "SocialFacil.py"]
