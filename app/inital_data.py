import logging
import sys
sys.path.append(r"D:\workspace\FastAPI_template")
from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating inital data")
    init()
    logger.info("Inital data created")

if __name__ == "__main__":
    main()
