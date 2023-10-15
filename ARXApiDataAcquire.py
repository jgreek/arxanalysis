import json
import quandl
from pathlib import Path


class ARXApiDataAcquire:
    def __init__(self, ticker, start_date, end_date, maturities, config_directory=Path.cwd(),
                 destination_directory=Path.cwd(), nasdaq_datalink_code="USTREASURY/YIELD"):
        self.ticker = ticker.replace(" ", "_")
        self.start_date = start_date
        self.nasdaq_datalink_code = nasdaq_datalink_code
        self.end_date = end_date
        self.maturities = maturities
        self.config_directory = Path(config_directory)
        self.destination_directory = Path(destination_directory)
        self.destination_directory.mkdir(parents=True, exist_ok=True)
        self.api_key = self.load_config()

    def load_config(self):
        try:
            # Load database configuration from config.json
            with open(self.config_directory / 'config.json', 'r') as config_file:
                config = json.load(config_file)
                return config["quandl_key"]
        except FileNotFoundError:
            print("Configuration file not found.")
            return None

    def get_yield_data(self):
        if not self.api_key:
            print("API key not loaded. Can't fetch data.")
            return None

        quandl.ApiConfig.api_key = self.api_key
        data = quandl.get(self.nasdaq_datalink_code, start_date=self.start_date, end_date=self.end_date)
        return data[self.maturities]

    def save_to_csv(self):
        data = self.get_yield_data()
        if data is not None:
            for maturity in self.maturities:
                safe_maturity = maturity.replace(" ", "_")
                filename = self.destination_directory / f"{self.ticker}_{safe_maturity}_yield_data.csv"
                # By default, the dates are set as the index of the DataFrame when data is fetched from Quandl.
                # By resetting the index, the dates are transformed from being the index to being a regular column in
                # the DataFrame. This is helpful for saving the data to CSV where we want dates as a column.
                subset = data[[maturity]].reset_index()
                subset.columns = ['Date', 'Yield']
                subset.insert(0, 'InstrumentName', f"{self.ticker}_{safe_maturity}")
                subset.to_csv(filename, index=False)
                print(f"Saved data for {maturity} to {filename}")


# Usage
if __name__ == "__main__":
    ticker = "US TREASURY"
    start_date = "2021-01-01"
    end_date = "2023-01-01"
    maturities = ["3 MO", "1 YR", "5 YR", "10 YR", "30 YR"]
    data_acquirer = ARXApiDataAcquire(ticker, start_date, end_date, maturities, config_directory=Path("config"),
                                      destination_directory=Path('sources'))
    data_acquirer.save_to_csv()
