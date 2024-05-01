import unittest
import os
from unittest.mock import patch, MagicMock
from auxiliars import convert_to_valid_folder_name
from oauth import authenticate_gdrive, create_new_folder_and_get_id, upload_drive_folder, upload_file_to_drive
from scrapping import download_images_from_google
from google.oauth2.credentials import Credentials

class TestDownloadImages(unittest.TestCase):
    def setUp(self):
        # Define los parámetros de prueba
        self.search_query = "cats"
        self.destination_folder = "images"
        self.number_of_images = 5

        # Llama a la función que quieres probar
        download_images_from_google(self.search_query, self.destination_folder, self.number_of_images)

    def test_folder_created(self):
        # Verifica si la carpeta de destino se creó correctamente
        self.assertTrue(os.path.exists(self.destination_folder))

    def test_images_downloaded(self):
        # Verifica si se descargaron las imágenes correctamente
        files = os.listdir(self.destination_folder)
        self.assertEqual(len(files), self.number_of_images)
        for i in range(1, self.number_of_images + 1):
            self.assertIn(f"{self.search_query}_{i}.jpg", files)

class TestGoogleDriveFunctions(unittest.TestCase):
    def test_authenticate_gdrive(self):
        # Call function
        creds = authenticate_gdrive()
        # Assertions
        self.assertIsInstance(creds, Credentials)

    def test_create_new_folder_and_get_id(self):
        # Call function
        folder_id = create_new_folder_and_get_id('TestFolder', authenticate_gdrive())

        # Assertions
        self.assertIsInstance(folder_id, str)

    def test_upload_drive_folder(self):

        search_query = "nubes"
        local_images_folder_path = convert_to_valid_folder_name(search_query)
        destination_folder = local_images_folder_path
        number_of_images = 10
        download_images_from_google(search_query, destination_folder, number_of_images)#getting images
        creds = authenticate_gdrive()
        id_folder_drive_to_upload = create_new_folder_and_get_id(local_images_folder_path,creds)

        #Call function
        result = upload_drive_folder(local_images_folder_path,id_folder_drive_to_upload,creds)

        # Assertions
        self.assertIsInstance(result, str)



if __name__ == '__main__':
    unittest.main()