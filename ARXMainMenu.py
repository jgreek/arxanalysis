import json
from pathlib import Path

import pandas as pd

from ARXApiDataAcquire import ARXApiDataAcquire
from ARXUsTreasuryDV01Calc import ARXUsTreasuryDV01Calc
from ARXDatabaseSetup import ARXDatabaseSetup
from ARXPortfolioManager import ARXPortfolioManager
from ARXPortfolioSimulation import ARXPortfolioSimulation
from ARXVar import ARXParametricSimulation, ARXHistoricalSimulation, ARXVaRCalculator
from ARXVarReport import ARXVaRReport
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXYieldDataAnalysisCLI:
    """
    The ARXYieldDataAnalysisCLI class provides command-line interface functionality
    for the ARX Yield Data Analysis application. It offers a menu-driven interaction
    for tasks such as importing data, calculating VaR, simulating portfolios, etc.
    """
    def __init__(self, configuration_directory):
        self.start_date = "2021-01-01"
        self.end_date = "2023-01-01"

        self.configuration_directory = configuration_directory
        self.portfolio_path = self.configuration_directory / 'portfolio.json'
        self.yield_data_access = ARXYieldDataAccess(data_directory=Path("sources"), config_directory=Path("config"),
                                                    sql_directory=Path("SQL"))
        success, result = self.yield_data_access.verify_db_config()
        if not success:
            print("ALERT: ", result)
            self.error = result
            return
        self.error = None
        self.portfolio_manager = ARXPortfolioManager(self.configuration_directory / 'portfolio.json',
                                                     self.yield_data_access, start_date=self.start_date,
                                                     end_date=self.end_date)

        self.yield_data = self.yield_data_access.execute_get_yield_data_by_date_range(self.start_date, self.end_date)
        self.portfolio_simulation = ARXPortfolioSimulation(data=self.yield_data)

    def load_portfolio(self):
        try:
            with open(self.portfolio_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # If portfolio.json doesn't exist, create it with a default entry.
            default_portfolio = {
                "Treasury Bond 1 YR": 1.0
            }
            with open(self.portfolio_path, 'w') as file:
                json.dump(default_portfolio, file)
            return default_portfolio

    def save_portfolio(self):
        with open(self.portfolio_path, 'w') as file:
            json.dump(self.portfolio, file)

    def display_file_contents(self, file_path: str):
        """
        Display the contents of the specified file.
        """
        try:
            with open(file_path, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"\nERROR: The file {file_path} was not found!")
        except Exception as e:
            print(f"\nERROR reading {file_path}: {e}")

    def setup_database(self):
        """
        Set up the database by creating tables and stored procedures using the ARXDatabaseSetup class.
        """
        print("Setting up the database...")

        # Define the directories for config, SQL, and data
        config_directory = Path("config")
        sql_directory = Path("SQL") / "setup"
        data_directory = Path("data")

        # Initialize the data access and database setup classes
        loader = ARXYieldDataAccess(data_directory=data_directory, config_directory=config_directory,
                                    sql_directory=sql_directory)
        executor = ARXDatabaseSetup(sql_directory, loader.conn_str)

        # Execute the scripts to set up the database
        executor.execute_scripts()

        print("Database set up successfully.")
        self.error = None

    def main_menu(self):
        print("\nARX Yield Data Analysis CLI")
        print("-----------------------------------")
        print("Version: 1.0.0")
        print("Programmer: John Greek")
        print("Application Date: October 17, 2023")
        print("\nWelcome to the ARX Yield Data Analysis tool.")

        if self.error:
            print("\n*** Pre-inspection Alert message: ***")
            print(self.error)
            print(
                "\nPlease setup the database following the instruction in the README.md before using the application.")
            input("\nClick enter to continue: ").upper()
            print("-----------------------------------")

        while True:
            print("\nPlease select an option from the menu below:")
            print("-----------------------------------")

            print("\nOptions:")
            if self.error:
                print("X. Setup Database")
            print("I. Import yield data from API")
            print("S. Save API data to database")
            print("P. Portfolio and weighting")
            print("V. Calculate VaR")
            print("D. Calculate DV01")
            print("M. Portfolio Simulation")
            print("R. View readme.md")
            print("T. View report.md")
            print("E. Exit")

            choice = input("\nEnter your choice: ").upper()

            if choice == 'I':
                self.import_treasury_data()
            elif choice == 'X':
                self.setup_database()
            elif choice == 'S':
                self.save_api_data_to_db()
            elif choice == 'P':
                self.manage_portfolio()
            elif choice == 'V':
                self.calculate_var()
                input("\nClick enter to continue: ")
            elif choice == 'D':
                self.calculate_dv01()
                input("\nClick enter to continue: ")
            elif choice == 'M':
                self.simulate_portfolio()
                input("\nClick enter to continue: ")
            elif choice == 'R':
                self.display_file_contents("readme.md")
            elif choice == 'T':
                self.display_file_contents("report.md")
            elif choice == 'E':
                print("\nThank you for using ARX Yield Data Analysis CLI. Goodbye!")
                break

    def import_treasury_data(self):
        print("Fetching treasury yield data from API...")
        ticker = "US TREASURY"

        maturities = ["3 MO", "1 YR", "5 YR", "10 YR", "30 YR"]
        data_acquirer = ARXApiDataAcquire(ticker, self.start_date, self.end_date, maturities,
                                          config_directory=Path("config"),
                                          destination_directory=Path('sources'))
        data_acquirer.save_to_csv()
        print("Data fetched successfully")

    def save_api_data_to_db(self):
        print("Saving API data to db...")
        data_directory = Path("sources")
        config_directory = Path("config")
        sql_directory = Path("SQL")

        loader = ARXYieldDataAccess(data_directory=data_directory, config_directory=config_directory,
                                    sql_directory=sql_directory)
        loader.execute_insert()
        print("Saved API data to db successfully.")

    def simulate_portfolio(self):
        print("Simulating portfolio...")
        # Placeholder for your portfolio simulation function
        self.yield_data_access = ARXYieldDataAccess(data_directory=Path("sources"), config_directory=Path("config"),
                                                    sql_directory=Path("SQL"))
        pf = self.portfolio_manager.load_portfolio()
        self.portfolio_simulation.set_weights(pf)
        self.portfolio_simulation.simulate()
        print("Delta yield:", self.portfolio_simulation.delta_yield[20:100])
        print(self.portfolio_simulation.get_portfolio_delta_yield()[20:100])
        print("Simulation complete!")

    def calculate_var(self):
        print("Calculating VaR using the Historical Simulation methodology...")
        portfolio_details = self.portfolio_manager.load_portfolio()
        self.portfolio_simulation.set_weights(portfolio_details)
        self.portfolio_simulation.simulate()
        portfolio_delta_values = self.portfolio_simulation.get_portfolio_delta_yield()
        calculator = ARXVaRCalculator(strategy=ARXHistoricalSimulation())
        var_95 = calculator.compute(portfolio_delta_values, 0.95)
        var_99 = calculator.compute(portfolio_delta_values, 0.99)
        report = ARXVaRReport()
        report.generate(var_95, var_99)
        print("Calculating VaR using the Parametric Simulation methodology...")

        calculator = ARXVaRCalculator(strategy=ARXParametricSimulation())
        var_95 = calculator.compute(portfolio_delta_values, 0.95)
        var_99 = calculator.compute(portfolio_delta_values, 0.99)
        report = ARXVaRReport()
        report.generate(var_95, var_99)

    def calculate_dv01(self):
        yield_data_access = ARXYieldDataAccess(data_directory=Path("sources"), config_directory=Path("config"),
                                               sql_directory=Path("SQL"))
        df = yield_data_access.execute_get_yield_data_by_date_range(self.start_date, self.end_date)
        df = df[df["InstrumentName"].str.startswith("US_TREASURY_")]
        df['DV01'] = df.apply(ARXUsTreasuryDV01Calc.compute_dv01, axis=1)

        # Convert the 'Date' column to a datetime object
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[df['Date'].dt.day == 1]
        df['DV01'] = df.apply(ARXUsTreasuryDV01Calc.compute_dv01, axis=1)

        # Group by 'InstrumentName' and 'Date', then get the first value for each group
        grouped_df = df.groupby(['InstrumentName', 'Date']).first().reset_index()

        # Pivot the DataFrame
        pivot_df = grouped_df.pivot(index='Date', columns='InstrumentName', values='DV01')
        print(pivot_df)

        print("The above report shows DV01 per instrument as a pivot table for each first day of the month.")

    def manage_portfolio(self):
        self.portfolio_manager.manage_portfolio()


if __name__ == "__main__":
    cli = ARXYieldDataAnalysisCLI(configuration_directory=Path("config"))
    cli.main_menu()
