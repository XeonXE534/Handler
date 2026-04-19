import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

from src.handler.utils.metadataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA import metadata

APP_NAME = str(metadata()["version"])
PROJ_NAME = str(metadata()["project_name"])

def get_log_dir() -> Path:
    # if sys.platform.startswith("win"):
    #     base = Path(os.getenv("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
    #     return base / APP_NAME / "Logs"
    # This thing is never getting a Winshit version so I am not even gonna bother with it

    base = Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / APP_NAME.lower() / "log"

def get_logger(name: str = PROJ_NAME) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_level = os.getenv(f"{PROJ_NAME.upper()}_LOG_LEVEL", "DEBUG").upper()
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{PROJ_NAME.lower()}.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    fh = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.propagate = False

    return logger