from datetime import datetime
from unittest.mock import patch

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.test import TestCase

from flickrapp.utils.file_utils import MinioUploader, upload_file


class FileUtilTest(TestCase):
    def test_upload_file_returns_location(self):
        title = 'TestTitle'
        dt_now = datetime.now()
        timestamp = dt_now.timestamp()
        mock_file = InMemoryUploadedFile(name='filename.txt',
                                         charset=None,
                                         content_type=None,
                                         field_name=None,
                                         file=None,
                                         size=None)
        expected_location = f'TestTitle-{timestamp}.txt'
        with patch('flickrapp.utils.file_utils.MinioUploader'), \
                patch('flickrapp.utils.file_utils.MinioUploader.upload'), \
                patch('flickrapp.utils.file_utils.datetime') as mock_datetime:
            mock_datetime.now.return_value = dt_now
            actual_location = upload_file(file=mock_file, title=title)
            self.assertEqual(actual_location, expected_location)

    @staticmethod
    def test_bucket_not_exists_bucket_created():
        mock_file = TemporaryUploadedFile('./test_data/file.txt', None, None, None, None)
        with patch('flickrapp.utils.file_utils.Minio') as mock_minio, \
                patch('flickrapp.utils.file_utils.Minio.bucket_exists', return_value=False), \
                patch('flickrapp.utils.file_utils.Minio.make_bucket') as mock_make_bucket, \
                patch('flickrapp.utils.file_utils.Minio.fput_object'):
            uploader = MinioUploader()
            uploader.client = mock_minio
            uploader.upload(source=mock_file, object_name="")
            mock_make_bucket.assert_called_once()

    @staticmethod
    def test_bucket_exists_bucket_not_created():
        mock_file = TemporaryUploadedFile('./test_data/file.txt', None, None, None, None)
        with patch('flickrapp.utils.file_utils.Minio') as mock_minio, \
                patch('flickrapp.utils.file_utils.Minio.bucket_exists', return_value=True), \
                patch('flickrapp.utils.file_utils.Minio.make_bucket') as mock_make_bucket, \
                patch('flickrapp.utils.file_utils.Minio.fput_object'):
            uploader = MinioUploader()
            uploader.client = mock_minio
            uploader.upload(source=mock_file, object_name="")
            mock_make_bucket.assert_not_called()

    @staticmethod
    def test_in_memory_file_gets_written():
        dt_now = datetime.now()
        mock_file = InMemoryUploadedFile(name='filename.txt',
                                         charset=None,
                                         content_type='text/plain',
                                         field_name=None,
                                         file=None,
                                         size=None)
        with patch('flickrapp.utils.file_utils.Minio') as mock_minio, \
                patch('flickrapp.utils.file_utils.Minio.bucket_exists', return_value=True), \
                patch('flickrapp.utils.file_utils.datetime') as mock_datetime, \
                patch('flickrapp.utils.file_utils.MinioUploader._write_tmp_file', return_value='/path') as mock_write_tmp_file, \
                patch('flickrapp.utils.file_utils.Minio.fput_object') as mock_fput:
            uploader = MinioUploader()
            uploader.client = mock_minio
            mock_datetime.now.return_value = dt_now
            uploader.upload(source=mock_file, object_name='testobject')
            mock_write_tmp_file.assert_called_once()
            mock_fput.assert_called_with(bucket_name='uploads',
                                         object_name="testobject",
                                         file_path='/path',
                                         content_type='text/plain')

    @staticmethod
    def test_temporary_file_returns_tmp_file_path():
        mock_file = TemporaryUploadedFile('./test_data/file.txt', 'text/plain', None, None, None)
        expected_path = mock_file.temporary_file_path()
        with patch('flickrapp.utils.file_utils.Minio') as mock_minio, \
                patch('flickrapp.utils.file_utils.Minio.bucket_exists', return_value=True), \
                patch('flickrapp.utils.file_utils.Minio.fput_object') as mock_fput:
            uploader = MinioUploader()
            uploader.client = mock_minio
            uploader.upload(source=mock_file, object_name='testobject')
            mock_fput.assert_called_with(bucket_name='uploads',
                                         object_name="testobject",
                                         file_path=expected_path,
                                         content_type='text/plain')

    def test_incorrect_file_argument_returns_value_error(self):
        mock_file = "an incorrect type"
        with patch('flickrapp.utils.file_utils.Minio') as mock_minio, \
                patch('flickrapp.utils.file_utils.Minio.bucket_exists', return_value=True), \
                patch('flickrapp.utils.file_utils.Minio.fput_object') as mock_fput, \
                self.assertRaises(ValueError) as context:
            uploader = MinioUploader()
            uploader.client = mock_minio
            uploader.upload(source=mock_file, object_name='testobject')
            self.assertTrue(f'Expected type {type(InMemoryUploadedFile)} or {type(TemporaryUploadedFile)}' in context)
            mock_fput.assert_not_called()
