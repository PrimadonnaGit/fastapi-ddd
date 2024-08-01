import os

from fastapi import UploadFile

from board.domain.file.file import File
from board.domain.file.file_repository import FileRepository
from .file_dto import FileResponseDTO


class FileApplicationService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def save_file(self, file: UploadFile, post_id: int) -> FileResponseDTO:
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        file_entity = File(
            filename=file.filename, filepath=file_location, post_id=post_id
        )
        saved_file = self.file_repository.save(file_entity)
        return FileResponseDTO.model_validate(saved_file)

    def get_files_by_post(self, post_id: int) -> list[FileResponseDTO]:
        files = self.file_repository.find_by_post_id(post_id)
        return [FileResponseDTO.model_validate(file) for file in files]

    def delete_file(self, id: int) -> None:
        file = self.file_repository.find_by_id(id)
        if not file:
            raise ValueError("File not found")
        os.remove(file.filepath)
        self.file_repository.delete(id)
