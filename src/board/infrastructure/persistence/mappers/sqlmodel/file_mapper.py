from board.domain.file.file import File
from board.infrastructure.persistence.mappers.base import BaseMapper
from board.infrastructure.persistence.sqlmodel.models import FileModel


class SQLModelFileMapper(BaseMapper[File, FileModel]):
    @staticmethod
    def to_domain(db_file: FileModel) -> File:
        return File(
            id=db_file.id,
            filename=db_file.filename,
            filepath=db_file.filepath,
            post_id=db_file.post_id,
        )

    @staticmethod
    def to_orm(file: File) -> FileModel:
        return FileModel(
            id=file.id,
            filename=file.filename,
            filepath=file.filepath,
            post_id=file.post_id,
        )
