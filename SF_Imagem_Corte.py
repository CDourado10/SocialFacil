from PIL import Image, ImageDraw, ImageColor
import cv2
import numpy as np

def detectpessoas(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    
    # Carregar o classificador pré-treinado para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detectar rostos na imagem
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))
    
    if len(faces) == 0:
        print("Nenhum rosto encontrado")
        return image.shape[1] // 2
    
    # Encontrar o maior rosto
    largest_face = max(faces, key=lambda x: x[2] * x[3])  # O maior rosto tem a maior área (largura x altura)
    
    # Calcular a área mínima que um rosto deve ter para ser considerado (80% do tamanho do maior rosto)
    min_face_area = 0.8 * (largest_face[2] * largest_face[3])
    
    # Inicializar variáveis para o rosto mais à direita
    rightmost_face = None
    rightmost_x = 0
    
    # Iterar pelos rostos detectados
    for (x, y, w, h) in faces:
        face_area = w * h
        # Verificar se o rosto tem pelo menos 80% do tamanho do maior rosto
        if face_area >= min_face_area:
            # Verificar se o rosto está à direita do rosto mais à direita até agora
            if x > rightmost_x:
                rightmost_face = (x, y, w, h)
                rightmost_x = x
    
    if rightmost_face is not None:
        # Coordenadas do retângulo do rosto mais à direita
        x, y, w, h = rightmost_face
        
        # Calcular o ponto médio (centro) do rosto mais à direita
        x_center = x + w // 2
        y_center = y + h // 2
        
        # Desenhar um ponto vermelho no centro do rosto mais à direita
        print(f"Rosto posição {x_center}")
        return x_center
    else:
        print("Nenhum rosto encontrado")
        return image.shape[1] // 2

def crop_to_square(posicaoobj, input_image_path, output_image_path, fill_color="#212121"):
    objetoprincipal = detectpessoas(input_image_path)
    # Abre a imagem de entrada
    img = Image.open(input_image_path)
    img = img.convert("RGB")

    # Obtém as dimensões da imagem
    width, height = img.size

    # Calcula as coordenadas de corte para tornar a imagem 1:1
    if width >= height:
        left = (objetoprincipal - height/2) - height*posicaoobj
        right = left + height
        top = 0
        bottom = height
    else:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = (height + width) / 2

    if right > width:
        right = width
        left = right - height

    # Realiza o corte
    img = img.crop((left, top, right, bottom))
    if left < 0:
        cor = Image.new("P", (1, 1))
        cor = Image.new("RGB", (1, 1), ImageColor.getcolor(fill_color, "RGB"))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, -left, img.height], fill=cor.getpixel((0, 0)))

    # Salva a imagem cortada
    img.save(output_image_path)
    img.close()
    return(output_image_path)








# Exemplo de uso
if __name__ == "__main__":
    input_image_path = "C:\\IAEficaz\\myenv\\CJ\\CJ\\ConhecaYodaocaode4anosquecapturoubrasileirofugitivonosEUA\\i4.png"
    output_image_path = "imagem_cortada.png"  # Substitua pelo caminho de saída desejado
    print(crop_to_square(0.25, input_image_path, output_image_path))
