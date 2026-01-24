import io
from pathlib import Path
from typing import BinaryIO
from PIL import Image
from PIL.Image import Image as ImageType
from PIL.ImageFile import ImageFile
from uuid import uuid4


from src.core.conifg import settings

import magic


class ImageCompressor:
    ALLOWED_MIME_TYPES = ["image/png", "image/jpeg"]

    def __init__(self, max_width: int = 600) -> None:
        self.max_width = max_width

    def _compress(self, _file: BinaryIO) -> ImageType | ImageFile:
        img = Image.open(_file)
        img.seek(0)

        width, height = img.size
        if width > self.max_width:
            new_height = int(height * (self.max_width / width))
            done_img = img.resize(
                (self.max_width, new_height), Image.Resampling.LANCZOS
            )
            img.close()
            return done_img
        else:
            return img

    def compress_image(self, _file: BinaryIO, file_type: str) -> io.BytesIO:
        _file.seek(0)
        buffer = io.BytesIO()
        compressed_file = self._compress(_file)
        compressed_file.save(
            buffer, format="jpeg" if file_type == "image/jpeg" else "png"
        )
        compressed_file.close()
        return buffer


class FileWorkerService:
    UPLOADS_BASE_DIR = settings.UPLOADS_BASE_DIR

    def __init__(self, image_compressor: ImageCompressor) -> None:
        self._image_compressor = image_compressor

    def _get_file_path(self, filename: str) -> Path:
        file_path = self.UPLOADS_BASE_DIR
        file_path.mkdir(parents=True, exist_ok=True)
        filename = str(uuid4()) + Path(filename).suffix
        return file_path / filename

    def _get_mime_type(self, _file: BinaryIO) -> str:
        _file.seek(0)
        mime = magic.Magic(mime=True)
        return mime.from_buffer(_file.read(2048))

    def remove(self, file_url: str) -> None:
        file_path = Path(file_url)
        if file_path:
            path = settings.BASE_DIR / file_path
            if path.is_file():
                path.unlink(missing_ok=True)

    async def save(self, filename: str, file: BinaryIO) -> str:
        file.seek(0)

        file_path = self._get_file_path(filename)
        file_type = self._get_mime_type(file)
        if file_type in ["image/png", "image/jpeg"]:
            file = self._image_compressor.compress_image(file, file_type)
            file.seek(0)

        file.seek(0)
        with open(file_path, "wb") as f:
            f.write(file.read())

        return str(file_path.relative_to(file_path.parent.parent))
