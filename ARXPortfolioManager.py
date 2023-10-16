import json
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXPortfolioManager:
    """
    The ARXPortfolioManager class provides tools for managing and updating a portfolio of financial instruments.

    This class allows users to:
    - Load and save portfolio configurations from/to a json file.
    - View the current state of the portfolio.
    - Update the portfolio with new instrument weightings based on available tickers fetched via `yield_data_access`.

    Attributes:
        configuration_directory (str): The directory containing portfolio configuration files.
        portfolio_path (str): The path to the portfolio file.
        portfolio (dict): Dictionary representation of the current portfolio with instrument names as keys and their weights as values.
        yield_data_access (ARXYieldDataAccess): An instance of ARXYieldDataAccess (used for fetching the list of available tickers)
        start_date (str): Start date.
        end_date (str): End date.

    """
    def __init__(self, configuration_directory, yield_data_access, start_date, end_date):
        self.configuration_directory = configuration_directory
        self.portfolio_path = self.configuration_directory
        self.portfolio = self.load_portfolio()
        self.yield_data_access = yield_data_access
        self.start_date = start_date
        self.end_date = end_date

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

        try:
            df = self.yield_data_access.execute_get_yield_data_by_date_range(self.start_date, self.end_date)
            unique_instruments = self.yield_data_access.get_unique_instruments(df)
            if unique_instruments:
                print("\nAvailable Tickers:")
                for idx, ticker in enumerate(unique_instruments, 1):
                    print(f"{idx}. {ticker}")
            else:
                print("No tickers found. You can add them manually.")
        except Exception as e:
            print(f"Error fetching available tickers: {e}")
            print("You can still add tickers manually.")
            unique_instruments = []

        while True:
            instrument_choice = input(
                "\nEnter the number for the ticker or type in a ticker name (or type 'done' to finish): ")

            if instrument_choice.lower() == 'done':
                break

            if instrument_choice.isdigit():
                try:
                    instrument_index = int(instrument_choice) - 1  # Convert to zero-based index
                    if 0 <= instrument_index < len(unique_instruments):
                        instrument = unique_instruments[instrument_index]
                    else:
                        print("Invalid choice. Please choose a valid number or type in a ticker name.")
                        continue
                except ValueError:
                    print("Please enter a valid number or 'done'.")
                    continue
            else:
                # User entered a ticker name manually
                instrument = instrument_choice

            weight = float(input(f"Enter the weight for {instrument}: "))
            updated_portfolio[instrument] = weight

        self.portfolio = updated_portfolio
        self.save_portfolio()
