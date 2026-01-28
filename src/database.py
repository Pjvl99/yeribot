from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional, Dict
import pandas as pd
from .config import Config

class DatabaseClient:
    def __init__(self):
        self.client = None
        self._connect()

    def _connect(self):
        """Initializes the BigQuery client."""
        try:
            # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in env
            self.client = bigquery.Client(project=Config.GCP_PROJECT)
        except Exception as e:
            print(f"Failed to connect to BigQuery: {e}")

    def query_df(self, sql: str) -> pd.DataFrame:
        """Executes a query and returns a Pandas DataFrame."""
        if not self.client:
            return pd.DataFrame()
        try:
            return self.client.query_and_wait(sql).to_dataframe()
        except Exception as e:
            print(f"Query Error: {e}")
            return pd.DataFrame()

    def execute_non_query(self, sql: str):
        """Executes INSERT/UPDATE queries."""
        if not self.client:
            return
        try:
            self.client.query_and_wait(sql)
        except Exception as e:
            print(f"Execution Error: {e}")

    # Domain specific queries
    def get_user_activity(self, number: str, activity_table: str) -> pd.DataFrame:
        sql = f"SELECT numero, puntos, intentos FROM actividades.{activity_table} WHERE numero = '{number}' LIMIT 1"
        return self.query_df(sql)

    def register_user(self, table: str, number: str, points: int):
        sql = f"INSERT INTO actividades.{table} VALUES('{number}', {points}, 1)"
        self.execute_non_query(sql)