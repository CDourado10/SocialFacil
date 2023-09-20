from selenium import webdriver
import requests
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from unidecode import unidecode
import urllib.parse


from unidecode import unidecode

def imagem_download(keysearch, totalimagens, output_directory, headless=True, startin=0):
    # Pasta de OutPUT
    key = urllib.parse.quote(keysearch)
    # Verifica se o diretório de saída existe; se não, cria-o
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Configuração do Selenium e do navegador
    if headless == True:
        options = webdriver.EdgeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)
    else:
        driver = webdriver.Edge()
      # Certifique-se de ter o ChromeDriver instalado e no PATH


    search_url = f"https://www.google.com/search?sca_esv=561360965&sxsrf=AB5stBizZ3_oufvDAKHyt0ER-JlBefTwjQ:1693421944312&q={key}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwiu7MeriIWBAxWWvJUCHZJ_BjoQ0pQJegQIDRAB&biw=1865&bih=961&dpr=1"

    # Abrir a página de pesquisa de imagens do Google
    driver.get(search_url)
    imgsbaixadas = 0
    position = 0
    # Encontrar e clicar nas imagens e depois baixar
    while imgsbaixadas < totalimagens and position < 4*totalimagens:
        position += 1
        try:
            if position+startin > 3: 
                parte = 3 
            else: 
                parte = 2
            image_xpath = f"/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{position+startin}]/a[1]/div[1]"
            image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, image_xpath)))
            #image = driver.find_element("xpath", image_xpath)
            image.click()

            # Esperar um pouco para a imagem carregar
            time.sleep(2)
            
            download_xpath = f"/html/body/div[2]/c-wiz/div[3]/div[{parte}]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]"
            #download_image = driver.find_element("xpath", download_xpath)
            download_image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, download_xpath)))
            image_link = download_image.get_attribute("src")
            print(f"Link da imagem {position}: {image_link}")
            output_filename = f"{output_directory}i{imgsbaixadas}.jpg"
            response = requests.get(image_link)
            if response.status_code == 200:
                with open(output_filename, "wb") as f:
                    f.write(response.content)
                print("Download concluído.")
                imgsbaixadas += 1
            else:
                print("Erro ao fazer o download da imagem.")
            
            # Aqui você pode adicionar o código para baixar a imagem usando a URL obtida

        except Exception as e:
            print(f"Erro ao obter a imagem {position}: {e}")

        # Fechar o navegador
    driver.quit()

    