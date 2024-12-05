from abc import ABC, abstractmethod

from models import Base

from sqlalchemy import select


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self, filter_by: dict) -> list:
        pass

    @abstractmethod
    async def add_one(self, data: dict) -> None:
        pass

    @abstractmethod
    async def get_one(self, data: dict) -> None:
        pass


class SqlAlchemyRepository(AbstractRepository):
    model = None

    async def get_all(self, filter_by: dict) -> list:
        query = select(self.model).filter_by(**filter_by)
