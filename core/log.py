import logging
from db.crud.log import create_log
from core.settings import DEGUG
import asyncio


# Create a custom handler for tortoise ORM
class TortoiseHandler(logging.Handler):
    def emit(self, record):
        asyncio.create_task(create_log(self.format(record), record.levelname))


# Create a logger and set the level
logger = logging.getLogger("tortoise_logger")
if DEGUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Add the Tortoise handler to the logger
tortoise_handler =  TortoiseHandler()
tortoise_handler.setFormatter(formatter)
logger.addHandler( tortoise_handler)
