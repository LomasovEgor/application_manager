from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    path: Mapped[str]
    status: Mapped[bool]


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    program_name: Mapped[str]
    action: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
