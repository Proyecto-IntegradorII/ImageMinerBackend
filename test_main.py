import unittest
import os
from unittest.mock import patch, MagicMock
from oauth import authenticate_gdrive, create_new_folder_and_get_id, upload_drive_folder, upload_file_to_drive
from scrapping import download_images_from_google

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
    @patch('scrapping.build')
    def test_authenticate_gdrive(self, mock_build):
        # Mock build function to return MagicMock
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Call function
        creds = authenticate_gdrive()

        # Assertions
        self.assertIsInstance(creds, MagicMock)
        mock_build.assert_called_with('drive', 'v3', credentials=None)

    @patch('scrapping.build')
    def test_upload_file_to_drive(self, mock_build):
        # Mock build function to return MagicMock
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Call function
        upload_file_to_drive('test.jpg', '/path/to/test.jpg', 'folder_id', MagicMock())

        # Assertions
        mock_service.files.return_value.create.assert_called_once()

    @patch('scrapping.build')
    def test_create_new_folder_and_get_id(self, mock_build):
        # Mock build function to return MagicMock
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Call function
        folder_id = create_new_folder_and_get_id('TestFolder', MagicMock())

        # Assertions
        self.assertIsInstance(folder_id, str)
        mock_service.files.return_value.create.assert_called_once()

    @patch('scrapping.upload_file_to_drive')
    def test_upload_drive_folder(self, mock_upload_file):
        # Mock upload_file_to_drive function
        mock_upload_file.return_value = 'file_id'

        # Call function
        result = upload_drive_folder('/path/to/local/folder', 'folder_id', MagicMock())

        # Assertions
        self.assertEqual(result, 'folder_id')
        mock_upload_file.assert_called()


if __name__ == '__main__':
    unittest.main()