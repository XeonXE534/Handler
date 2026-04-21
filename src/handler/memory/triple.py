import sqlite3
from pathlib import Path

class TripleStorageThingy:
    def __init__(self, db_name: str = "data.db"):
        self.db_path = Path(__file__).parent / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def get_node_id(self, name):
        self.cursor.execute('INSERT OR IGNORE INTO nodes (name) VALUES (?)', (name,))
        self.cursor.execute('SELECT id FROM nodes WHERE name = ?', (name,))
        return int(self.cursor.fetchone()[0])

    def store_fact(self, s, p, o):
        s_id = self.get_node_id(s)
        p_id = self.get_node_id(p)
        o_id = self.get_node_id(o)

        self.cursor.execute(
            'INSERT OR IGNORE INTO relationships (subject_id, predicate_id, object_id) VALUES (?, ?, ?)',
            (s_id, p_id, o_id)
        )
        self.conn.commit()

    def query_fact(self, subject):
        sql = """
            SELECT onode.name, onode.name
            FROM relationships r
            JOIN nodes snode ON r.subject_id = snode.id
            JOIN nodes pnode ON r.predicate_id = pnode.id
            JOIN nodes onode ON r.object_id = onode.id
            WHERE snode.name = ?
        """
        self.cursor.execute(sql, (subject, ))
        result = self.cursor.fetchone()

        return result[0] if result else "I don't know that yet :("
