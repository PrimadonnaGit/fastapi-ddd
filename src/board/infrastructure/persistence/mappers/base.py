from abc import ABC, abstractmethod
from typing import TypeVar, Generic

DomainType = TypeVar("DomainType")
ORMType = TypeVar("ORMType")


class BaseMapper(ABC, Generic[DomainType, ORMType]):
    @staticmethod
    @abstractmethod
    def to_domain(orm_object: ORMType) -> DomainType:
        pass

    @staticmethod
    @abstractmethod
    def to_orm(domain_object: DomainType) -> ORMType:
        pass
