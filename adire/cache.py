import json
import sqlite3


class Cache:
    def __init__(self, path="adire.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS solutions (
                key          TEXT PRIMARY KEY,
                task         TEXT,
                answer       TEXT,
                steps_json   TEXT,
                hits         INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def get(self, key):
        """Look up a solved problem. Returns a dict, or None on a miss."""
        row = self.conn.execute(
            "SELECT task, answer, steps_json, hits FROM solutions WHERE key=?",
            (key,)
        ).fetchone()
        if row is None:
            return None
        self.conn.execute(
            "UPDATE solutions SET hits = hits + 1 WHERE key=?", (key,)
        )
        self.conn.commit()
        return {"task": row[0], "answer": row[1],
                "steps": json.loads(row[2]), "hits": row[3]}

    def put(self, key, task, answer, steps):
        """Store a solved problem."""
        self.conn.execute(
            "INSERT OR REPLACE INTO solutions (key, task, answer, steps_json) "
            "VALUES (?, ?, ?, ?)",
            (key, task, answer, json.dumps(steps))
        )
        self.conn.commit()