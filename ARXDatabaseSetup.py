import pyodbc
from pathlib import Path

from ARXYieldDataAccess import ARXYieldDataAccess


class ARXDatabaseSetup:
    def __init__(self, sql_directory: Path, connection_string: str):
        self.sql_directory = sql_directory
        self.connection_string = connection_string

    def _get_sql_files(self) -> list:
        """Get a list of .sql files from the specified directory."""
        return [file for file in self.sql_directory.iterdir() if file.suffix == '.sql']

    def execute_scripts(self):
        """Execute each .sql script found in the sql_directory."""
        sql_files = self._get_sql_files()
        if not sql_files:
            print("No SQL files found in the specified directory.")
            return

        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            for sql_file in sql_files:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                    try:
                        cursor.execute(sql_script)
                        conn.commit()
                        print(f"Executed {sql_file.name} successfully.")
                    except Exception as e:
                        print(f"Error executing {sql_file.name}: {e}")


if __name__ == "__main__":
    config_directory = Path("config")
    sql_directory = Path("SQL") / "setup"
    data_directory = Path("data")

    loader = ARXYieldDataAccess(data_directory=data_directory, config_directory=config_directory,
                                sql_directory=sql_directory)
    executor = ARXDatabaseSetup(sql_directory, loader.conn_str)
    executor.execute_scripts()
