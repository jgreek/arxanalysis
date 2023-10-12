import pyodbc
import pandas as pd
from pathlib import Path
import json


class ARXYieldDataAccess:
    def __init__(self, data_directory, config_directory, sql_directory):
        self.data_directory = Path(data_directory)
        self.config_directory = Path(config_directory)
        self.sql_directory = Path(sql_directory)
        self.conn_str = self.load_database_config()

    def load_database_config(self):
        try:
            # Load database configuration from config.json
            with open(self.config_directory / 'config.json', 'r') as config_file:
                config = json.load(config_file)

            # Construct the connection string
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config['server']};DATABASE={config['database']};UID={config['username']};PWD={config['password']}"
            return conn_str
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            raise Exception("Error loading database configuration from config.json") from e

    def load_insert_query(self):
        try:
            # Load SQL query from the InsertDataYields.sql file
            with open(self.sql_directory / 'InsertDataYields.sql', 'r') as sql_file:
                insert_query = sql_file.read()
            return insert_query
        except FileNotFoundError as e:
            raise Exception("Error loading SQL query from InsertDataYields.sql") from e

    def execute_insert(self):
        insert_query = self.load_insert_query()
        # Establish a connection to SQL Server
        conn = pyodbc.connect(self.conn_str)

        # Create a cursor
        cursor = conn.cursor()

        # Iterate through CSV files in the data directory
        for csv_file in self.data_directory.glob('*.csv'):
            print("Integrating csv data: ", csv_file)
            df = pd.read_csv(csv_file)

            # Iterate through the rows and insert data row by row
            for index, row in df.iterrows():
                instrument_name = row['InstrumentName']
                date = row['Date']
                yield_value = row['Yield']
                if not isinstance(yield_value, float):
                    continue
                date_updated = pd.Timestamp.now()

                # Execute the SQL query with placeholders
                cursor.execute(
                    insert_query,
                    instrument_name, date, yield_value, date_updated
                )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    def execute_get_yield_data_by_date_range(self, start_date, end_date):
        try:
            # Establish a connection to SQL Server
            conn = pyodbc.connect(self.conn_str)

            # Create a cursor
            cursor = conn.cursor()

            # Execute the GetYieldDataByDateRange stored procedure with placeholders
            cursor.execute("EXEC GetYieldDataByDateRange ?, ?", start_date, end_date)

            # Fetch all rows and store them in a DataFrame
            rows = []
            row = cursor.fetchone()
            pd.set_option('display.max_columns', None)  # Display all columns

            while row:
                rows.append(list(row))
                row = cursor.fetchone()

            df = pd.DataFrame(rows, columns=["Id", "InstrumentName", "Date", "Yield", "DateUpdated"])
            return df

        except pyodbc.Error as e:
            print(f"Error: {e}")

    def get_unique_instruments(self, df):
        """Retrieve unique instrument names from the data fetched between the given date range."""
        return df["InstrumentName"].unique().tolist()


# Example usage:
if __name__ == "__main__":
    data_directory = Path("sources")  # Replace with your data directory path
    config_directory = Path("config")
    sql_directory = Path("SQL")

    loader = ARXYieldDataAccess(data_directory=data_directory, config_directory=config_directory,
                                sql_directory=sql_directory)
    loader.execute_insert()

    # Example usage of execute_get_yield_data_by_date_range
    start_date = "2022-01-01"  # Replace with your desired start date
    end_date = "2022-01-31"  # Replace with your desired end date

    df = loader.execute_get_yield_data_by_date_range(start_date, end_date)
    print(df[df["InstrumentName"] == "USTreasuryYield"])

    unique_instruments = loader.get_unique_instruments(df)
    print(f"Unique Instruments:  {unique_instruments}")
