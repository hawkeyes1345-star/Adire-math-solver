import json
import sqlite3
import numpy as np
from adire.embed import embed, similarity


def _describe(task, latex):
    """A semantic description for matching — captures the TYPE, not just symbols.
    This makes all 'solve linear equation' problems match each other strongly."""
    return f"{task} problem: {latex}"


class Cache:
    def __init__(self, path="adire.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS solutions (
                key TEXT PRIMARY KEY, task TEXT, answer TEXT,
                steps_json TEXT, hits INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS problem_vectors (
                key TEXT PRIMARY KEY, latex TEXT, task TEXT, vector TEXT
            )
        """)
        self.conn.commit()

    # ---------------- TIER 1: exact match ----------------
    def get(self, key):
        row = self.conn.execute(
            "SELECT task, answer, steps_json, hits FROM solutions WHERE key=?",
            (key,)
        ).fetchone()
        if row is None:
            return None
        self.conn.execute("UPDATE solutions SET hits = hits + 1 WHERE key=?", (key,))
        self.conn.commit()
        return {"task": row[0], "answer": row[1],
                "steps": json.loads(row[2]), "hits": row[3]}

    def put(self, key, task, answer, steps, latex=None):
        self.conn.execute(
            "INSERT OR REPLACE INTO solutions (key, task, answer, steps_json) "
            "VALUES (?, ?, ?, ?)",
            (key, task, answer, json.dumps(steps))
        )
        if latex is not None:
            vec = embed(_describe(task, latex)).tolist()
            self.conn.execute(
                "INSERT OR REPLACE INTO problem_vectors (key, latex, task, vector) "
                "VALUES (?, ?, ?, ?)",
                (key, latex, task, json.dumps(vec))
            )
        self.conn.commit()

    # ---------------- TIER 2: semantic similarity ----------------
    def find_similar(self, latex, task, threshold=0.6):
        rows = self.conn.execute(
            "SELECT key, latex, vector FROM problem_vectors"
        ).fetchall()
        if not rows:
            return None

        query_vec = embed(_describe(task, latex))
        best_score, best_key, best_latex = 0.0, None, None
        for key, stored_latex, vec_json in rows:
            if stored_latex == latex:
                continue
            vec = np.array(json.loads(vec_json))
            score = similarity(query_vec, vec)
            if score > best_score:
                best_score, best_key, best_latex = score, key, stored_latex

        if best_key is None or best_score < threshold:
            return None

        sol = self.conn.execute(
            "SELECT steps_json FROM solutions WHERE key=?", (best_key,)
        ).fetchone()
        if sol is None:
            return None
        return {"latex": best_latex, "steps": json.loads(sol[0]),
                "similarity": round(best_score, 3)}