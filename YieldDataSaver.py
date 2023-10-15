import uuid

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from YieldDataLoader import YieldDataLoader


class YieldDataSaver:
    def __init__(self, db_params, data_directory):
        self.db_params = db_params
        self.data_directory = data_directory
        self.conn = psycopg2.connect(**db_params)
        self.loader = None  # This will be initialized in the fetch_and_save method

    def fetch_and_save(self, ticker, start_date=None, end_date=None):
        # Create an instance of YieldDataLoader and fetch data
        self.loader = YieldDataLoader(self.data_directory, ticker, start_date, end_date)
        file_path = self.loader.fetch_data()

        # Load the data from the file to a DataFrame
        data = pd.read_csv(file_path)

        # Add necessary columns to the DataFrame
        data['ticker'] = ticker
        data['id'] = [str(uuid.uuid4()) for _ in range(len(data))]

        # Renaming the columns to match the database schema
        # Rename columns
        column_mapping = {
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
            "ticker": "ticker",
            "id": "id"
        }
        data = data.rename(columns=column_mapping)

        # Save the data to PostgreSQL using pandas
        engine_str = f"postgresql+psycopg2://{self.db_params['user']}:{self.db_params['password']}@{self.db_params['host']}/{self.db_params['dbname']}"
        engine = create_engine(engine_str)
        data.to_sql('yield_data', engine, if_exists='append', index=False)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Database connection parameters
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'mysecretpassword',
        'host': 'localhost'
    }

    data_directory = "data"

    saver = YieldDataSaver(db_params, data_directory)
    saver.fetch_and_save("AAPL")  # for example, using the AAPL ticker
    saver.close()
