import json
from pathlib import Path

import click

from ARXApiDataAcquire import ARXApiDataAcquire
from ARXPortfolioManager import ARXPortfolioManager
from ARXPortfolioSimulation import ARXPortfolioSimulation
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXYieldDataAnalysisCLI:

    def __init__(self, configuration_directory):
        self.configuration_directory = configuration_directory
        self.portfolio_path = self.configuration_directory / 'portfolio.json'
        self.yield_data_access = ARXYieldDataAccess(data_directory=Path("sources"), config_directory=Path("config"),
                                                    sql_directory=Path("SQL"))
        self.portfolio_manager = ARXPortfolioManager(self.configuration_directory / 'portfolio.json',
                                                     self.yield_data_access)
        start_date = "2021-01-01"  # Replace with your desired start date
        end_date = "2022-12-31"  # Replace with your desired end date
        df = self.yield_data_access.execute_get_yield_data_by_date_range(start_date, end_date)
        self.portfolio_simulation = ARXPortfolioSimulation(data=df)

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
            print("I. Import treasury data from API")
            print("S. Save API data to database")
            print("P. Portfolio and weighting")
            print("V. Calculate VaR")
            print("D. Calculate DV01")
            print("M. Portfolio Simulation")
            print("E. Exit")
            choice = input("Enter your choice: ").upper()

            if choice == 'I':
                self.import_treasury_data()
            elif choice == 'S':
                self.save_api_data_to_db()
            elif choice == 'P':
                self.manage_portfolio()
            elif choice == 'V':
                self.calculate_var()
            elif choice == 'D':
                self.calculate_dv01()
            elif choice == 'M':
                self.simulate_portfolio()
            elif choice == 'E':
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
        print("Delta yield:", self.portfolio_simulation.delta_yield[50:100])
        print(self.portfolio_simulation.get_portfolio_delta_yield()[50:100])
        print("Simulation complete!")

    def calculate_var(self):
        print("Calculating VaR...")
        # Add your VaR calculation function here
        print("VaR calculated!")

    def calculate_dv01(self):
        print("Calculating DV01...")
        # Add your DV01 calculation function here
        print("DV01 calculated!")

    def manage_portfolio(self):
        self.portfolio_manager.manage_portfolio()


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
