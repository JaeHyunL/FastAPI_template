import os
import logging
import sys
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

sys.path.append(r"D:\workspace\FastAPI_template")
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1

os.environ['SQLALCHEMY_WARN_20'] = 'no'

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        print('그래도 워닝이지 익셉션까지는..', e)
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initalizing")


if __name__ == "__main__":
    main()
