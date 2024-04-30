from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import zipfile
from plyer import notification  # For sending desktop notifications
from oauth import upload_drive_folder
from auxiliars import convert_to_valid_folder_name


def download_images_from_google(search_query, destination_folder, number_of_images):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch")
    time.sleep(3)
    
    elem = driver.find_element(By.TAG_NAME, "body")
    for i in range(30):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    images = driver.find_elements(By.TAG_NAME, 'img')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    count = 0
    for i, image in enumerate(images):
        if count < number_of_images:
            width = driver.execute_script("return arguments[0].naturalWidth", image)
            height = driver.execute_script("return arguments[0].naturalHeight", image)
            if width > 100 and height > 100:
                src = image.get_attribute('src')
                try:
                    if src and src.startswith('http'):
                        response = requests.get(src)
                        file_path = os.path.join(destination_folder, f"{search_query}_{count+1}.jpg")
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        count += 1
                except Exception as e:
                    print(f"Could not download image {i+1}: {e}")
        else:
            break

    driver.quit()

# Example usage
#search_query = "pandas"
#destination_folder = convert_to_valid_folder_name(search_query)
#number_of_images = 100
#download_images_from_google(search_query, destination_folder, number_of_images)