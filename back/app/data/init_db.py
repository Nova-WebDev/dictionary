from app.data.db import engine
from app.data.base import Base

def _load_models():
    pass


async def init_db():
    _load_models()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
