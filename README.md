# SocialFacil - Automação de Postagens para Redes Sociais

## Descrição do Projeto

O SocialFacil é uma solução automatizada para criação e gerenciamento de conteúdo para redes sociais. O sistema utiliza inteligência artificial para gerar postagens relevantes e personalizadas com base em notícias atuais, adaptando o conteúdo para diferentes áreas de atuação e necessidades específicas dos usuários.

## Principais Funcionalidades

- **Bot do Telegram**: Interface principal para interação com o usuário
- **Geração Automática de Conteúdo**: Criação de textos para postagens usando IA
- **Geração de Imagens**: Criação automática de imagens para acompanhar as postagens
- **Verificação de Fake News**: Sistema para validar a veracidade das notícias
- **Postagem Automática**: Agendamento e publicação automática em redes sociais
- **Personalização por Área**: Conteúdo adaptado para diferentes áreas de atuação

## Estrutura do Projeto

### Arquivos Principais

- **SF_BOT_Telegram.py**: Bot do Telegram para interação com usuários
- **SF_AI.py**: Integração com serviços de IA (ChatGPT, Bard, Bing)
- **SF_Gerador_1.py**: Obtenção de notícias e filtragem inicial
- **SF_Gerador_2.py**: Geração de conteúdo para postagens
- **SF_Noticias.py**: Coleta de notícias de diferentes fontes
- **SF_Imagem_Builder.py**: Criação de imagens para postagens
- **SF_FakeNews.py**: Verificação da veracidade das notícias
- **SF_Info_User.py**: Gerenciamento de informações dos usuários
- **SF_Insta_Post.py**: Publicação de conteúdo no Instagram

### Módulos Auxiliares

- **SF_Imagem_Download.py**: Download de imagens para postagens
- **SF_Imagem_Corte.py**: Recorte e ajuste de imagens
- **SF_Imagem_Escrever.py**: Adição de texto às imagens
- **SF_LOG.py**: Sistema de registro de atividades
- **SF_Exception.py**: Tratamento de exceções
- **SF_sites_dict.py**: Dicionário de sites e fontes de notícias
- **SF_Noticias_GET.py**: Obtenção de notícias de fontes específicas

## Fluxo de Funcionamento

1. O usuário interage com o bot do Telegram
2. O sistema busca notícias relevantes para a área de atuação do usuário
3. A IA gera conteúdo personalizado com base nas notícias
4. O sistema verifica a veracidade das informações
5. Uma imagem é gerada para acompanhar o texto
6. O conteúdo é enviado para aprovação do usuário ou postado automaticamente
7. As informações são registradas para evitar repetição de conteúdo

## Requisitos do Sistema

O projeto utiliza diversas bibliotecas Python, incluindo:

- telebot (API do Telegram)
- g4f, bardapi (APIs de IA)
- requests, beautifulsoup4 (Web scraping)
- PIL, opencv-python (Processamento de imagens)
- psycopg2 (Banco de dados PostgreSQL)
- selenium (Automação de navegador)

Para instalar todas as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

1. Configure o token do bot do Telegram em SF_BOT_Telegram.py
2. Configure as credenciais do banco de dados em SF_Info_User.py
3. Configure os tokens de acesso das APIs de IA em SF_AI.py
4. Configure os tokens de acesso do Instagram em SF_Info_User.py

## Uso

Para iniciar o bot do Telegram:

```bash
python SF_BOT_Telegram.py
```

## Estrutura do Banco de Dados

O sistema utiliza um banco de dados PostgreSQL com as seguintes tabelas:

- **usuarios**: Informações dos usuários
- **informacoes_pagina**: Configurações das páginas de redes sociais
- **provedor_sites**: Informações sobre fontes de notícias
- **assuntos**: Áreas e subáreas para categorização de conteúdo

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
