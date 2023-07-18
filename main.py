from PIL import Image, ImageFilter, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_captcha_text(location, size, driver):
    png = driver.get_screenshot_as_png()  # Hace una captura de pantalla

    im = Image.open(BytesIO(png))  # usa PIL para abrir la imagen en memoria

    left = location['x']
    top = location['y'] + 100  # Desplaza la captura 100 píxeles hacia abajo
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] + 100  # Desplaza la captura 100 píxeles hacia abajo

    im = im.crop((left, top, right, bottom))  # define la ubicación y el tamaño del captcha en la captura de pantalla
    im.save('captcha.png')  # guarda la imagen del captcha

    img = Image.open('captcha.png')  # Abre la imagen 
    img = img.convert('L')  # La convierte a escala de grises
    img = img.filter(ImageFilter.MedianFilter())  # Aplica un filtro de media para reducir el ruido
    enhancer = ImageEnhance.Contrast(img)  # Incrementa el contraste
    img = enhancer.enhance(2)

    # Usa Tesseract para hacer OCR en la imagen
    text = pytesseract.image_to_string(img)
    
    return text

def main():
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service)

    driver.get('https://zefoy.com')

    time.sleep(5)  # Espera para que la página se cargue completamente

    captcha_element = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/form/div/div/img")
    
    # Desplaza la página hasta el elemento captcha
    driver.execute_script("arguments[0].scrollIntoView();", captcha_element)

    # Espera un momento para que el scroll se complete
    time.sleep(2)

    location = captcha_element.location
    size = captcha_element.size

    text = get_captcha_text(location, size, driver)
    print("Captcha text: ", text)  # Imprime el texto del captcha

    time.sleep(2)

    # Aquí se ingresa el texto del captcha en el formulario y se envia
    captcha_input_field = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/form/div/div/div/input")
    captcha_input_field.send_keys(text)  # Escribe el texto del captcha en el campo de texto

    time.sleep(5)

    send_views_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button")
    send_views_button.click() 

    print("Se ha pulsado el botón de enviar vistas")

    time.sleep(5)

    enter_video_url_field = driver.find_element(By.XPATH, "/html/body/div[10]/div/form/div/input")
    enter_video_url_field.send_keys("https://vm.tiktok.com/ZGJVdcb4e/")
    enter_video_url_field.submit()  # Ingresa la URL del video  

    print("Se ha ingresado la URL del video")

    time.sleep(2)

    sending_views_button = driver.find_element(By.XPATH, "/html/body/div[10]/div/div/div[1]/div/form/button")
    sending_views_button.click()  # Envía las vistas

    print("Se ha pulsado el botón de enviar vistas")

    

if __name__ == "__main__":
    main()