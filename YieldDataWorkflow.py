from datetime import datetime, timedelta

from YieldDataSaver import YieldDataSaver
from YieldDatabaseManager import YieldDatabaseManager


class YieldDataWorkflow:

    def __init__(self, db_params, data_directory="data"):
        self.db_params = db_params
        self.data_directory = data_directory

    def run(self, tickers, start_date=None, end_date=None, create_table_flag=False, drop_table_flag=False):
        print("Starting the Yield Data Workflow...")

        # Initialize DatabaseManager
        print("Initializing Database Manager...")
        db_manager = YieldDatabaseManager(self.db_params)

        # Optionally Create the table
        if create_table_flag:
            print("Creating the yield_data table...")
            db_manager.create_yield_data_table()

        # Optionally Drop the table
        if drop_table_flag:
            response = input(
                "You are about to drop the yield_data table. This will permanently delete all data in the table. Are you sure? (y/n): ")
            if response.lower() == 'y':
                print("Dropping the yield_data table...")
                db_manager.drop_yield_data_table()
            else:
                print("Canceled drop table.")

        # Close connection
        print("Closing the database connection...")
        db_manager.close()

        # Default to the past 2 years if no dates provided
        end_date = end_date or datetime.today().date()
        start_date = start_date or end_date - timedelta(days=730)

        # Process each ticker
        for ticker in tickers:
            print(f"\nProcessing ticker: {ticker}...")
            saver = YieldDataSaver(self.db_params, data_directory=self.data_directory)
            saver.fetch_and_save(ticker=ticker, start_date=start_date, end_date=end_date)

        print("Yield Data Workflow Completed!")

if __name__ == "__main__":
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'mysecretpassword',
        'host': 'localhost'
    }

    tickers = ["TLT", "IBM", "IEI", "SHY", "JNK"]

    workflow = YieldDataWorkflow(db_params)
    workflow.run(tickers, create_table_flag=True, drop_table_flag=True)
