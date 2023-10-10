import csv
import pathlib


class CSVTransformer:
    def __init__(self, source_file, destination_directory, ticker=None, date_index=0, yield_index=1):
        self.source_file = pathlib.Path(source_file)
        self.destination_directory = pathlib.Path(destination_directory)

        # If ticker is not provided, extract from filename
        self.ticker = ticker or self.source_file.stem.split('_')[0]
        self.DateIndex = date_index
        self.YieldIndex = yield_index

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def transform(self):
        output_rows = []

        # Read the source CSV file
        with self.source_file.open('r') as f:
            reader = csv.reader(f)
            for row in reader:
                # Extract date and yield values based on indices
                date = row[self.DateIndex]
                yield_value = row[self.YieldIndex]

                # Check if yield is a float
                if self.is_float(yield_value):
                    output_rows.append([self.ticker, date, yield_value])

        # Save the transformed CSV to the destination directory
        output_path = self.destination_directory / f"{self.ticker}_yield_data.csv"
        with output_path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["InstrumentName", "Date", "Yield"])  # Header row
            writer.writerows(output_rows)


if __name__ == "__main__":
    transformer = CSVTransformer(
        source_file=pathlib.Path('raw') / 'Commercial_Paper_Interest_Rates_010121-010123.csv',
        ticker="CommericalPaperIR",
        destination_directory='sources')
    transformer.transform()
    transformer = CSVTransformer(
        source_file=pathlib.Path('raw') / 'daily-treasury-rates.csv',
        ticker="TreasuryRates2021",
        destination_directory='sources')
    transformer.transform()

    transformer = CSVTransformer(
        source_file=pathlib.Path('raw') / 'ICE_BofA_US_High_Yield_Index_Effective_Yield_010121_010123.csv',
        ticker="ICE_Bofa_US_HighYield",
        destination_directory='sources')
    transformer.transform()
    transformer = CSVTransformer(
        source_file=pathlib.Path('raw') / 'US_Treasury_10Yr_Constant_Maturity_Yield_2021-01-01_to_2023-01-01.csv',
        ticker="US_Treasury_10Yr_Constant_Maturity",
        destination_directory='sources')
    transformer.transform()
