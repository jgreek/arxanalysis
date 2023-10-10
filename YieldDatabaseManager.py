import psycopg2


class YieldDatabaseManager:
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def create_yield_data_table(self):
        # SQL command to create the table
        create_table_command = """
        CREATE TABLE IF NOT EXISTS public.yield_data
        (
            date DATE NOT NULL,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            adj_close DOUBLE PRECISION,
            volume BIGINT,
            ticker TEXT NOT NULL,
            id UUID PRIMARY KEY,
            CONSTRAINT unique_ticker_date UNIQUE (ticker, date)
        );
        """

        # Execute the SQL command for table creation
        self.cursor.execute(create_table_command)

        # Commit changes
        self.conn.commit()

        # Create unique index
        create_index_command = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_yield_data_date_ticker ON public.yield_data(date, ticker);
        """

        # Execute the SQL command for index creation
        self.cursor.execute(create_index_command)

        # Commit changes
        self.conn.commit()

    def drop_yield_data_table(self):
        drop_table_command = """
         DROP TABLE IF EXISTS public.yield_data;
         """
        self.cursor.execute(drop_table_command)
        self.conn.commit()

    def close(self):
        # Close the database connection
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    # Database connection parameters
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'mysecretpassword',
        'host': 'localhost'
    }

    # Initialize DatabaseManager
    db_manager = YieldDatabaseManager(db_params)

    # Create the table (this can be controlled by a flag as well)
    create_table_flag = True  # Set to False if you don't want to create the table
    if create_table_flag:
        db_manager.create_yield_data_table()

    # Close connection
    db_manager.close()
