# db_workflow/datatool.py
from sqlalchemy import create_engine, text
from llm import generate_sql

import re



class DataTool:

    def __init__(self, db_url: str, schema: str):
        self.engine = create_engine(db_url)
        self.schema = schema
    
    def _clean_sql(self, sql: str) -> str:
        sql = sql.strip()
        sql = re.sub(r"```[a-zA-Z]*", "", sql)  # remove ```sql, ```postgres etc
        sql = sql.replace("```", "")            # remove closing ```
        return sql.strip()

    def nl_query(self, nl_text: str):
        sql = generate_sql(nl_text, self.schema)
        print("\nGenerated SQL:\n", sql)

        sql = self._clean_sql(sql)      # <<-- CLEAN SQL
        print("\nCleaned SQL:\n", sql)

        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.mappings().all()
            rows = [dict(r) for r in rows]     # ← safe now, optional


        return {
            "sql": sql,
            "rows": rows,
            "stats": self._compute_stats(rows)
        }


    def _compute_stats(self, rows):
        """Detect numeric columns and compute avg/min/max"""
        if not rows:
            return {}

        numeric_cols = []
        first = rows[0]

        for col, val in first.items():
            if isinstance(val, (int, float)):
                numeric_cols.append(col)

        stats = {}

        for col in numeric_cols:
            values = [r[col] for r in rows if r[col] is not None]
            if not values:
                continue

            stats[col] = {
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "count": len(values)
            }

        return stats
