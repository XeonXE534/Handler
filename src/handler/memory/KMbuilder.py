import sqlite3
from pathlib import Path

from src.handler.utils.logger import get_logger

# THIS DOES NOT HAVE ANY SAFEGUARDS, BE CAREFUL WITH IT. IT WILL WIPE YOUR DB IF YOU RUN IT.
class KMapBuilder:
    def __init__(self):
        self.logger = get_logger("KMapBuilder")
        self.db_path = Path(__file__).parent / "data.db"
        self.sch_path = Path(__file__).parent / "schema.sql"
        self.conn = sqlite3.connect(self.db_path)

        self._init_db()

    def _init_db(self):
        self.logger.info("Running schema...")
        with open(self.sch_path, "r") as f:
            sql = f.read()

        self.conn.executescript(sql)
        self.conn.commit()

if __name__ == "__main__":
    KMapBuilder()