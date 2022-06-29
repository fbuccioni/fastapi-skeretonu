import os
import re

from fastapi_contrib.db.utils import setup_mongodb as setup, create_indexes
from fastapi_contrib.conf import settings as contrib_settings

from .util.monkeypatch import fastapi_contrib_mongodb
from .conf import settings

contrib_settings.fastapi_app = "app.app"
database_url = settings.database_default_url

contrib_settings.mongodb_dsn = (
    os.path.dirname(database_url) + '/'
    + re.sub(r'^.+?\?', '?', os.path.basename(database_url))
)
contrib_settings.mongodb_dbname = re.sub(f'\?.*$', '', os.path.basename(database_url))


async def init():
    await create_indexes()


__all__ = ('init', 'setup')