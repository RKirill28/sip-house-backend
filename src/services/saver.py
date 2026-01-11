from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from src.core.conifg import settings

import aiofiles


class FileSaverService:
    UPLOADS_BASE_DIR = settings.UPLOADS_BASE_DIR

    async def save(self, file: UploadFile) -> str:
        file_path = self.UPLOADS_BASE_DIR
        file_path.mkdir(parents=True, exist_ok=True)
        filename = str(uuid4()) + Path(file.filename).suffix
        file_path = file_path / filename

        await file.seek(0)

        async with aiofiles.open(file_path, "wb") as f:
            while chunks := await file.read(1024 * 1024):
                await f.write(chunks)

        return str(file_path.relative_to(file_path.parent.parent))
