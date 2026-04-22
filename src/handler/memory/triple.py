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

    def store_fact(self, s: str, p: str, o: str, confidence: float = 1.0, source: str = 'user'):
        s_id = self.get_node_id(s)
        p_id = self.get_node_id(p)
        o_id = self.get_node_id(o)

        self.cursor.execute(
            """INSERT OR IGNORE INTO relationships 
             (subject_id, predicate_id, object_id, confidence, source) 
             VALUES (?, ?, ?, ?, ?)""",
            (s_id, p_id, o_id, confidence, source)
        )
        self.conn.commit()

    def query_fact(self, subject: str, predicate: str = None) -> list[str]:
        if predicate:
            sql = """
                SELECT onode.name, r.confidence, r.source
                FROM relationships r
                JOIN nodes snode ON r.subject_id = snode.id
                JOIN nodes pnode ON r.predicate_id = pnode.id
                JOIN nodes onode ON r.object_id = onode.id
                WHERE snode.name = ?
                AND pnode.name = ?
                ORDER BY r.confidence DESC
            """
            self.cursor.execute(sql, (subject, predicate))
        else:
            sql = """
                SELECT onode.name, r.confidence, r.source
                FROM relationships r
                JOIN nodes snode ON r.subject_id = snode.id
                JOIN nodes onode ON r.object_id = onode.id
                WHERE snode.name = ?
                ORDER BY r.confidence DESC
            """
            self.cursor.execute(sql, (subject,))

        rows = self.cursor.fetchall()
        return rows if rows else []

    def query_multihop(self, subject: str, predicate: str = 'is_a', max_depth: int = 5) -> list[dict]:
        sql = """
        WITH RECURSIVE chain(object_id, depth) AS (
            SELECT r.object_id, 1
            FROM relationships r
            JOIN nodes snode ON r.subject_id = snode.id
            JOIN nodes pnode ON r.predicate_id = pnode.id
            WHERE snode.name = ?
            AND pnode.name = ?

            UNION ALL

            SELECT r.object_id, chain.depth + 1
            FROM relationships r
            JOIN chain ON r.subject_id = chain.object_id
            JOIN nodes pnode ON r.predicate_id = pnode.id
            WHERE pnode.name = ?
            AND chain.depth < ?
        )
        SELECT DISTINCT n.name, chain.depth
        FROM chain
        JOIN nodes n ON chain.object_id = n.id
        ORDER BY chain.depth ASC
        """
        self.cursor.execute(sql, (subject, predicate, predicate, max_depth))
        rows = self.cursor.fetchall()
        return [{"object": row[0], "depth": row[1]} for row in rows]

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()