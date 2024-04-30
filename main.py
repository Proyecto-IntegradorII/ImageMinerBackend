from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import zipfile
from plyer import notification  # For sending desktop notifications
from oauth import oauth_and_upload

def descargar_imagenes_google(busqueda, carpeta_destino, cantidad=100):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={busqueda}&tbm=isch")
    time.sleep(3)
    
    elem = driver.find_element(By.TAG_NAME, "body")
    for i in range(30):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    images = driver.find_elements(By.TAG_NAME, 'img')
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    count = 0
    for i, image in enumerate(images):
        if count < cantidad:
            width = driver.execute_script("return arguments[0].naturalWidth", image)
            height = driver.execute_script("return arguments[0].naturalHeight", image)
            if width > 100 and height > 100:
                src = image.get_attribute('src')
                try:
                    if src and src.startswith('http'):
                        response = requests.get(src)
                        file_path = os.path.join(carpeta_destino, f"{busqueda}_{count+1}.jpg")
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        count += 1
                except Exception as e:
                    print(f"Could not download image {i+1}: {e}")
        else:
            break

    driver.quit()

# Example usage
search_query = "cute cats"
destination_folder = "cat_images"
download_count = 100
descargar_imagenes_google(search_query, destination_folder, download_count)

# log to google drive and upload it to a folder
folder_id = '126bk1h19PGTUVov2qz17ywff1Ld1OPH_'  # Make sure to replace this with your actual folder ID
image_folder_path = 'cat_images'
oauth_and_upload(folder_id,image_folder_path)