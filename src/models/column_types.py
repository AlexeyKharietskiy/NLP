import datetime
from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import text

intpk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
        )]