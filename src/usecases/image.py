from src.api.deps import ImageRepoDap

from src.core.schemas.image import CreateImageForm, CreateImageInDBModel
from src.services.saver import FileSaverService


class CreateImage:
    def __init__(self, image_repo: ImageRepoDap) -> None:
        self.image_repo = image_repo
        self.validator = ImageFileValidatorService()
        self.saver = FileSaverService()

    async def execute(self, create_image_form: CreateImageForm) -> CreateImageInDBModel:
        image_file = create_image_form.image_file
        await image_file.seek(0)

        self.validator.validate_file(
            image_file.content_type,
            filename=image_file.filename,
            _file=image_file.file,
        )

        file_path = await self.saver.save(create_image_form.project_id, image_file)
        create_image = CreateImageInDBModel(
            project_id=create_image_form.project_id,
            name=create_image_form.name,
            description=create_image_form.description,
            main_image=create_image_form.main_image,
            sort=create_image_form.sort,
            done_project_id=create_image_form.done_project_id,
            url=file_path,
        )

        await self.image_repo.create(create_image)

        return create_image
