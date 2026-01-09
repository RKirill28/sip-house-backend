from pathlib import Path

import magic


class FileValidationError(Exception):
    pass


class ValidationFileImageError(FileValidationError):
    """Ошибка валидации картинки"""


class FileValidatorService:
    ALLOW_FILE_SUFFIXES: list[str]
    ALLOW_FILE_CONTENT_TYPE: list[str]

    VALIDATOR_EXCEPTION: type[FileValidationError]

    def _validate_file_type(self, _file: bytes) -> None:
        mime = magic.Magic()
        file_type = mime.from_buffer(_file)
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
        self._validate_file_suffix(filename)
        self._validate_for_nullbyte(filename)

    def validate_file(
        self, file_content_type: str, filename: str, _file: bytes
    ) -> None:
        self._vaildate_content_type(file_content_type)
        self._validate_file_suffix(filename)
        self._validate_filename(filename)
        self._validate_file_type(_file)


class ImageFileValidatorService(FileValidatorService):
    """Позволяет провалидировать файл как картинку."""

    ALLOW_FILE_SUFFIXES = [".png", ".jpg", ".jpeg"]
    ALLOW_FILE_CONTENT_TYPE = ["image/png", "image/jpeg"]
    VALIDATOR_EXCEPTION = ValidationFileImageError
