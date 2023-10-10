import json
from pathlib import Path

import click

from ARXApiDataAcquire import ARXApiDataAcquire
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXYieldDataAnalysisCLI:

    def __init__(self, configuration_directory):
        self.configuration_directory = configuration_directory
        self.portfolio_path = self.configuration_directory / 'portfolio.json'
        self.portfolio = self.load_portfolio()

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

    def main_menu(self):
        while True:
            print("\nARX Yield Data Analysis CLI")
            print("-----------------------------------")
            print("1. Import treasury data from API")
            print("2. Save API data to database")
            print("3. Set up, review, and update portfolio & weights")
            print("4. Calculate VaR")
            print("5. Calculate DV01")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                # Placeholder function for data import
                self.import_treasury_data()
            elif choice == '2':
                # Placeholder function for installing prerequisites
                self.save_api_data_to_db()
            elif choice == '3':
                # Function to manage portfolio
                self.manage_portfolio()
            elif choice == '4':
                # Placeholder function for VaR
                self.calculate_var()
            elif choice == '5':
                # Placeholder function for DV01
                self.calculate_dv01()
            elif choice == '6':
                break

    def import_treasury_data(self):
        print("Fetching treasury data from API...")
        ticker = "US TREASURY"
        start_date = "2021-01-01"
        end_date = "2023-01-01"
        maturities = ["3 MO", "1 YR", "5 YR", "10 YR", "30 YR"]
        data_acquirer = ARXApiDataAcquire(ticker, start_date, end_date, maturities, config_directory=Path("config"),
                                          destination_directory=Path('sources'))
        data_acquirer.save_to_csv()
        print("Data fetched successfully!")

    def save_api_data_to_db(self):
        print("Saving API data to db...")
        data_directory = Path("sources")
        config_directory = Path("config")
        sql_directory = Path("SQL")

        loader = ARXYieldDataAccess(data_directory=data_directory, config_directory=config_directory,
                                    sql_directory=sql_directory)
        loader.execute_insert(data_directory)
        print("Saved API data to db successfully.")

    def manage_portfolio(self):
        while True:
            print("\nPortfolio Management")
            print("---------------------")
            print("1. View Portfolio")
            print("2. Update Portfolio")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_portfolio()
            elif choice == '2':
                self.update_portfolio()
            elif choice == '3':
                break

    def view_portfolio(self):
        portfolio_str = ",".join([f"{instrument}:{weight}" for instrument, weight in self.portfolio.items()])
        print("\nCurrent Portfolio:")
        print(portfolio_str)

    def update_portfolio(self):
        self.view_portfolio()
        updated_portfolio_str = input("\nEnter the updated portfolio in the format 'Ticker1:0.3,Ticker2:0.3,...': ")
        updated_portfolio = {}

        for item in updated_portfolio_str.split(","):
            if ":" in item:
                instrument, weight = item.split(":")
                updated_portfolio[instrument] = float(weight)
            else:
                # If no weight is provided, set it to 0 for now
                updated_portfolio[item] = 0.0

        # If user didn't specify weights, calculate even distribution
        if sum(updated_portfolio.values()) == 0:
            num_instruments = len(updated_portfolio)
            even_weight = 1.0 / num_instruments
            for instrument in updated_portfolio:
                updated_portfolio[instrument] = even_weight

        self.portfolio = updated_portfolio
        self.save_portfolio()

    def calculate_var(self):
        print("Calculating VaR...")
        # Add your VaR calculation function here
        print("VaR calculated!")

    def calculate_dv01(self):
        print("Calculating DV01...")
        # Add your DV01 calculation function here
        print("DV01 calculated!")


@click.group()
def cli():
    pass


@cli.command()
def import_data():
    ARXYieldDataAnalysisCLI().import_treasury_data()


@cli.command()
def install_prereqs():
    ARXYieldDataAnalysisCLI().save_api_data_to_db()


@cli.command()
def portfolio():
    ARXYieldDataAnalysisCLI().manage_portfolio()


@cli.command()
def calculatevar():
    ARXYieldDataAnalysisCLI().calculate_var()


@cli.command()
def calculatedv01():
    ARXYieldDataAnalysisCLI().calculate_dv01()


@cli.command()
def mainmenu():
    ARXYieldDataAnalysisCLI().main_menu()


if __name__ == "__main__":
    cli = ARXYieldDataAnalysisCLI(configuration_directory=Path("config"))
    cli.main_menu()
