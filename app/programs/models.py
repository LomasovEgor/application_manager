from datetime import datetime

from sqlalchemy.orm import mapped_column

from app.database import Base


class Program(Base):
    __tablename__ = 'programs'

    id: int = mapped_column(primary_key=True, index=True)
    name: str = mapped_column(unique=True)
    status: bool = mapped_column(default=False)


class History(Base):
    __tablename__ = 'history'
    id: int = mapped_column(primary_key=True, index=True)
    program_id: id = mapped_column()
    action: str = mapped_column()
    timestamp: datetime = mapped_column(default=datetime.utcnow)
