from pathlib import Path
from uuid import UUID
from random import choice

from fastapi import UploadFile

from src.core.conifg import settings

import string
import aiofiles


class FileSaverService:
    UPLOADS_BASE_DIR = settings.UPLOADS_BASE_DIR

    def _generate_random_filename(self, filetype: str) -> str:
        letters = list(string.ascii_letters)
        return ("".join([choice(letters) for _ in range(12)])) + filetype

    async def save(self, project_id: UUID, file: UploadFile) -> str:
        file_path = self.UPLOADS_BASE_DIR / str(project_id)
        file_path.mkdir(parents=True, exist_ok=True)
        filename = self._generate_random_filename(Path(file.filename).suffix)
        file_path = file_path / filename

        async with aiofiles.open(file_path, "wb") as f:
            while chunks := await file.read(1024 * 1024):
                await f.write(chunks)

        return str(file_path)
