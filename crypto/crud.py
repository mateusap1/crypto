from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
from crypto import Database

import psycopg2

class CRUD:
    def __init__(self, db: Database):
        self.db = db

    def execute_query(self, query: str, params: tuple = ()) -> Any:
        with self.db.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            try:
                return cursor.fetchall()
            except psycopg2.ProgrammingError:
                return None

    def execute_update(self, query: str, params: tuple = ()): 
        with self.db.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.db.conn.commit()

    def create(self, table: str, data: Dict[str, Any]) -> None:
        keys = ", ".join(data.keys())
        values_placeholder = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({keys}) VALUES ({values_placeholder})"
        self.execute_update(query, tuple(data.values()))

    def read(self, table: str, conditions: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        query = f"SELECT * FROM {table} "
        if where_clause:
            query += f"WHERE {where_clause}"
        return self.execute_query(query, tuple(conditions.values()))

    def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> None:
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        self.execute_update(query, tuple(data.values()) + tuple(conditions.values()))

    def delete(self, table: str, conditions: Dict[str, Any]) -> None:
        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute_update(query, tuple(conditions.values()))
