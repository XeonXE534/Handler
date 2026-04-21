import sqlite3
from pathlib import Path
from src.handler.utils.logger import get_logger

# Note: Move the nuke code to entry point
import argparse

parser = argparse.ArgumentParser(description="Initialize the KMap database.")
parser.add_argument("--nuke", action="store_true", help="Force reinitialization of the database (will wipe existing data).")

args = parser.parse_args()
# THIS DOES NOT HAVE ANY SAFEGUARDS, BE CAREFUL WITH IT
class KMapBuilder:
    def __init__(self):
        self.logger = get_logger("KMapBuilder")
        self.db_path = Path(__file__).parent / "data.db"
        self.sch_path = Path(__file__).parent / "schema.sql"
        self.nuke_path = Path(__file__).parent / "nuke_db_and_rebuild.sql"
        self.conn = sqlite3.connect(self.db_path)

        self._init_db()

    def _init_db(self):
        if args.nuke:
            print("Nuke flag detected! This will wipe the existing database and rebuild it.")
            proceed = input("Are you sure?: (y/N) ")
            if proceed.lower() != "y":
                print("Aborting nuke operation.")
                return
            else:
                with open(self.nuke_path, "r") as f:
                    sql = f.read()
                self.conn.executescript(sql)
                self.conn.commit()
                print("Database nuked and rebuilt successfully")

        else:
            self.logger.info("Running schema...")
            with open(self.sch_path, "r") as f:
                sql = f.read()

            self.conn.executescript(sql)
            self.conn.commit()

if __name__ == "__main__":
    KMapBuilder()