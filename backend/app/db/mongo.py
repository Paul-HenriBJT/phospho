from loguru import logger

from app.core.config import (
    MONGODB_MAXPOOLSIZE,
    MONGODB_MINPOOLSIZE,
    MONGODB_NAME,
    MONGODB_URL,
)
from motor.motor_asyncio import AsyncIOMotorClient

mongo_db = None


async def get_mongo_db():
    if mongo_db is None:
        raise Exception("Mongo is not initialized.")
    return mongo_db[MONGODB_NAME]


async def connect_and_init_db():
    global mongo_db
    try:
        if MONGODB_URL is None:
            logger.warning("MONGODB_URL is None. Skipping mongo connection.")
            return
        try:
            mongo_db = AsyncIOMotorClient(
                MONGODB_URL,
                maxPoolSize=MONGODB_MAXPOOLSIZE,
                minPoolSize=MONGODB_MINPOOLSIZE,
                uuidRepresentation="standard",
            )
            logger.info(f"Connected to mongodb (MONGODB_NAME={MONGODB_NAME})")

        except Exception as e:
            logger.warning(f"Error while connecting to Mongo: {e}")
            raise e
    except Exception as e:
        logger.exception(f"Could not connect to mongo: {e}")
        raise e


async def close_mongo_db():
    global mongo_db
    if mongo_db is None:
        logger.warning("Connection is None, nothing to close.")
        return
    mongo_db.close()
    mongo_db = None
    logger.info("Mongo connection closed.")
