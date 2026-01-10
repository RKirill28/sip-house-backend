from fastapi import APIRouter, File, UploadFile, HTTPException

from src.core.conifg import settings
from src.services.file_validator import GeneralValidationError

from src.api.deps import FileSaverServiceDap, ValidatorServiceDap


files_router = APIRouter(prefix=settings.api.v1.files_prefix)


@files_router.post("/upload")
async def upload_file(
    file_saver: FileSaverServiceDap,
    file_validator: ValidatorServiceDap,
    files: list[UploadFile],
) -> dict:
    try:
        for file in files:
            file_validator.validate_file(file.content_type, file.filename, file.file)
    except GeneralValidationError:
        raise HTTPException(422, "The file validation error: This file is not allowed.")

    urls = []
    for file in files:
        url = await file_saver.save(file)
        urls.append(url)

    return {"urls": urls}
