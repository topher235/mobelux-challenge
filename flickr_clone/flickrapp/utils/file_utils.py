from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from minio import Minio

from flickr_clone import settings


class FileUploader(ABC):
    @abstractmethod
    def upload(self, source, destination):
        pass


class MinioUploader(FileUploader):
    def __init__(self):
        self.client = Minio(endpoint=f'{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}',
                            access_key=settings.MINIO_USERNAME,
                            secret_key=settings.MINIO_PASSWORD,
                            secure=False)  # b/c we're in a local dev environment
        self.bucket_name = 'uploads'

    def upload(self, source: Union[InMemoryUploadedFile, TemporaryUploadedFile], object_name: str):
        """
        Uploads the given file to Minio using the Minio client api. Django stores uploaded
        files either in memory or in a temporary location, depending on file size. If the
        file is already in a temporary location, we can supply that location to Minio.
        Otherwise, we need to write the file to a temporary location before giving that
        to Minio.

        :param source: Django UploadedFile subclass for an uploaded file
        :param object_name: String name of the object when stored in Minio
        :return:
        """
        # Need to make sure the upload bucket exists
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

        # Get the path of the file
        if isinstance(source, InMemoryUploadedFile):
            path = f'/tmp/{datetime.now().timestamp()}'
            with open(path, 'wb+') as out:
                out.write(source.read())
        elif isinstance(source, TemporaryUploadedFile):
            path = source.temporary_file_path()
        else:
            raise ValueError(f'Expected type {type(InMemoryUploadedFile)} or {type(TemporaryUploadedFile)} '
                             f'but got {type(source)}')

        # Upload the file to the bucket
        self.client.fput_object(bucket_name=self.bucket_name,
                                object_name=f'{object_name}.{source.name.split(".")[-1]}',
                                file_path=path,
                                content_type=source.content_type)


def upload_file(file: Union[InMemoryUploadedFile, TemporaryUploadedFile], title: str) -> str:
    """
    Uploads a given file to the Minio storage.

    :param file: File to be uploaded
    :param title: String title of the file
    :return: String final location of the file
    """
    upload_location = f'{title}-{datetime.now().timestamp()}'
    uploader = MinioUploader()
    uploader.upload(source=file, object_name=upload_location)
    return upload_location