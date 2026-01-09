from pathlib import Path
from typing import BinaryIO, override
from PIL import Image

from fastapi import UploadFile
import magic


class FileValidationError(Exception):
    pass


class ValidationFileImageError(FileValidationError):
    """Ошибка валидации картинки"""


class FileValidatorService:
    ALLOW_FILE_SUFFIXES: list[str]
    ALLOW_FILE_CONTENT_TYPE: list[str]

    VALIDATOR_EXCEPTION: type[FileValidationError]

    def _validate_file_type(self, _file: BinaryIO) -> None:
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(_file.read(2048))
        if file_type not in self.ALLOW_FILE_CONTENT_TYPE:
            raise self.VALIDATOR_EXCEPTION

    def _vaildate_content_type(self, content_type: str) -> None:
        if content_type not in self.ALLOW_FILE_CONTENT_TYPE:
            raise self.VALIDATOR_EXCEPTION

    def _validate_for_nullbyte(self, filename: str) -> None:
        if "\0" in filename or "\x00" in filename:
            raise self.VALIDATOR_EXCEPTION

    def _validate_file_suffix(self, filename: str) -> None:
        suffix = Path(filename).suffix.lower()
        if len(Path(filename).suffixes) > 1:
            raise self.VALIDATOR_EXCEPTION

        if suffix not in self.ALLOW_FILE_SUFFIXES:
            raise self.VALIDATOR_EXCEPTION

    def _validate_filename(self, filename: str) -> None:
        self._validate_for_nullbyte(filename)
        self._validate_file_suffix(filename)

    def validate_file(
        self, file_content_type: str | None, filename: str | None, _file: BinaryIO
    ) -> None:
        """
        Validates a file by its Content-Type header, filename extension, and magic number.

        Args:
            file_content_type (str): The MIME type provided by the client (e.g., "image/png").
            filename (str): The original name of the file to validate suffixes.
            _file (bytes): The raw file content (or header bytes) to verify the actual MIME type.

        Raises:
            FileValidationError: If any of the validation checks fail.
        """
        if file_content_type:
            self._vaildate_content_type(file_content_type)
        if filename:
            self._validate_filename(filename)

        self._validate_file_type(_file)


class ImageFileValidatorService(FileValidatorService):
    """Позволяет провалидировать файл как картинку."""

    ALLOW_FILE_SUFFIXES = [".png", ".jpg", ".jpeg"]
    ALLOW_FILE_CONTENT_TYPE = ["image/png", "image/jpeg"]
    VALIDATOR_EXCEPTION = ValidationFileImageError

    def _validate_for_image(self, file_stream: BinaryIO) -> None:
        try:
            file_stream.seek(0)
            with Image.open(file_stream) as img:
                img.verify()
            file_stream.seek(0)
        except Exception:
            raise self.VALIDATOR_EXCEPTION

    @override
    def validate_file(
        self, file_content_type: str | None, filename: str | None, _file: BinaryIO
    ) -> None:
        super().validate_file(file_content_type, filename, _file)
        self._validate_for_image(file_stream=_file)
