from sqlmodel import Session, select

from board.domain.file.file import File
from board.domain.file.file_repository import FileRepository
from board.infrastructure.persistence.mappers.sqlmodel.file_mapper import (
    SQLModelFileMapper,
)
from .models import FileModel


class SQLModelFileRepository(FileRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = SQLModelFileMapper()

    def save(self, file: File) -> File:
        db_file = self.mapper.to_orm(file)
        self.session.add(db_file)
        self.session.commit()
        self.session.refresh(db_file)
        return self.mapper.to_domain(db_file)

    def find_by_id(self, id: int) -> File | None:
        statement = select(FileModel).where(FileModel.id == id)
        db_file = self.session.exec(statement).first()
        return self.mapper.to_domain(db_file) if db_file else None

    def find_by_post_id(self, post_id: int) -> list[File]:
        statement = select(FileModel).where(FileModel.post_id == post_id)
        db_files = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_file) for db_file in db_files]

    def delete(self, id: int) -> None:
        db_file = self.session.get(FileModel, id)
        if db_file:
            self.session.delete(db_file)
            self.session.commit()
