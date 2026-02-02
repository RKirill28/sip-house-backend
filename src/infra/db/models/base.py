from uuid import uuid4, UUID

from sqlalchemy.types import TypeDecorator, BINARY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import uuid


class MyUUID(TypeDecorator):
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value.bytes
        return uuid.UUID(value).bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(bytes=value)


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(MyUUID, primary_key=True, default=uuid4)
