import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import psycopg2



class YieldDataLoader:
    def __init__(self, data_directory, ticker, start_date=None, end_date=None):
        self.ticker = ticker

        # If start and end dates are not provided, default to the past 2 years
        self.end_date = end_date or datetime.today().date()
        self.start_date = start_date or self.end_date - timedelta(days=730)

        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)


    def fetch_data(self):
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        file_path = Path(self.data_directory / f"{self.ticker}_yield_data.csv")
        data.to_csv(file_path)
        return file_path




def test_connection():
    try:
        # Define our connection string
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='mysecretpassword'"

        # Print the connection string to check
        print("Connecting to database\n ->%s" % (conn_string))

        # Get a connection
        conn = psycopg2.connect(conn_string)

        # Get a cursor object from the connection
        cursor = conn.cursor()

        # Execute a simple query: select version of PostgreSQL
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()

        print("\nConnected!\nPostgreSQL version: ", db_version)

    except Exception as e:
        print("Error: Unable to connect to the database")
        print(e)
    finally:
        if conn:
            conn.close()
            print("\nConnection closed.")


if __name__ == "__main__":


    test_connection()
