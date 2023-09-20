from imgur_uploader import *

# Configure o cliente do Imgur com seu client_id e client_secret
uploader = ImgurClient(client_id="65e21235564102c", client_secret="131e60768f3c04e9b1fc107c7bbda6499c3bd852")

def Imgur_upload(image_path):
    result = uploader.upload_from_path(image_path)
    return result["link"]

