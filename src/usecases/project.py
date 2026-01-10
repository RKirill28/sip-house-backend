from src.api.deps import ProjectRepoDap

from src.core.schemas.project import (
    CreateProjectForm,
    CreateProjectModel,
    ReadProjectModel,
    UpdateProjectModel,
)
from src.services.file_validator import PdfFileValidatorService
from src.services.saver import FileSaverService


class CreateProject:
    def __init__(self, project_repo: ProjectRepoDap) -> None:
        self.project_repo = project_repo
        self.validator = PdfFileValidatorService()
        self.saver = FileSaverService()

    async def execute(self, project_create: CreateProjectForm) -> ReadProjectModel:
        pdf_file = project_create.pdf_file
        await pdf_file.seek(0)

        self.validator.validate_file(
            pdf_file.content_type,
            filename=pdf_file.filename,
            _file=pdf_file.file,
        )
        create_model = CreateProjectModel(
            name=project_create.name,
            description=project_create.description,
            price=project_create.price,
            price_description=project_create.price_description,
        )
        new = await self.project_repo.create(create_model)

        file_path = await self.saver.save(new.id, pdf_file)

        await self.project_repo.update(UpdateProjectModel(id=new.id, pdf_url=file_path))
        await self.project_repo.session.commit()

        return ReadProjectModel(
            **create_model.model_dump(), id=new.id, pdf_url=file_path
        )
