from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from database.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"