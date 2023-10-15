import json
from pathlib import Path

import click

from ARXApiDataAcquire import ARXApiDataAcquire
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXPortfolioManager:
    def __init__(self, configuration_directory, yield_data_access: ARXYieldDataAccess):
        self.configuration_directory = configuration_directory
        self.portfolio_path = self.configuration_directory
        self.portfolio = self.load_portfolio()
        self.yield_data_access = yield_data_access

    def load_portfolio(self):
        try:
            with open(self.portfolio_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            default_portfolio = {
                "Treasury Bond 1 YR": 1.0
            }
            with open(self.portfolio_path, 'w') as file:
                json.dump(default_portfolio, file)
            return default_portfolio

    def save_portfolio(self):
        with open(self.portfolio_path, 'w') as file:
            json.dump(self.portfolio, file)

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
        portfolio_str = ", ".join([f"{instrument}: {weight}" for instrument, weight in self.portfolio.items()])
        print("\nCurrent Portfolio:")
        print(portfolio_str)

    def update_portfolio(self):
        self.view_portfolio()
        updated_portfolio = {}

        start_date = "2021-01-01"
        end_date = "2023-01-01"
        df = self.yield_data_access.execute_get_yield_data_by_date_range(start_date, end_date)
        print(df[df["InstrumentName"] == "USTreasuryYield"])

        unique_instruments = self.yield_data_access.get_unique_instruments(df)
        if unique_instruments:
            print("\nAvailable Tickers:")
            for idx, ticker in enumerate(unique_instruments, 1):
                print(f"{idx}. {ticker}")

        while True:
            instrument_choice = input("\nEnter the number for the ticker (or type 'done' to finish): ")

            if instrument_choice.lower() == 'done':
                break

            try:
                instrument_index = int(instrument_choice) - 1  # Convert to zero-based index
                if 0 <= instrument_index < len(unique_instruments):
                    instrument = unique_instruments[instrument_index]
                else:
                    print("Invalid choice. Please choose a valid number.")
                    continue
            except ValueError:
                print("Please enter a valid number or 'done'.")
                continue

            weight = float(input(f"Enter the weight for {instrument}: "))
            updated_portfolio[instrument] = weight

        self.portfolio = updated_portfolio
        self.save_portfolio()
