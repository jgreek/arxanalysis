import pandas as pd


class ARXPortfolioSimulation:

    def __init__(self, data: pd.DataFrame):
        self.data = self.transform_data(data)
        self.weights = None
        self.delta_yield = None
        self.portfolio_delta_yield = None

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data from long format to wide format.
        """
        # Drop duplicates based on 'Date' and 'InstrumentName'
        data = data.drop_duplicates(subset=['Date', 'InstrumentName'])

        return data.pivot(index='Date', columns='InstrumentName', values='Yield')

    def set_weights(self, weights: dict):
        """
        Set the weights for the portfolio.
        """
        # print(self.data.head())
        if not set(weights.keys()).issubset(set(self.data.columns)):
            raise ValueError("Some keys in the provided weights are not included in the data columns.")

        if abs(sum(weights.values()) - 1) > 1e-9:
            raise ValueError("Weights must sum to 1.")

        # Reorder data columns based on the order of the weights
        self.data = self.data[list(weights.keys())]

        # Convert weights dictionary values to a list for easier matrix operations
        self.weights = list(weights.values())

    def calculate_yield_changes(self):
        """
        Calculate day-to-day percentage change in yield for each instrument.
        """
        self.delta_yield = self.data.pct_change().fillna(0)

    def simulate(self):
        """
        Run the portfolio simulation to compute the portfolio's delta yield.
        It simply means the portfolio weighted average daily yield
          Portfolio Delta Yield Formula:
          ΔYield_portfolio = Σ (w_i * ΔYield_i)
              Where:
                - Δ Yield_portfolio is the portfolio's daily yield change.
                - w_i is the weight of the ith instrument in the portfolio.
                - Δ Yield_i is the daily yield change for the ith instrument.
                - The summation is over all instruments in the portfolio.

        """
        if self.delta_yield is None:
            self.calculate_yield_changes()

        # The reason for sum(axis=1) below is to compute the daily portfolio yield change for each date by summing
        # the weighted yield changes of all instruments.
        self.portfolio_delta_yield = (self.delta_yield * self.weights).sum(axis=1)

    def get_portfolio_delta_yield(self) -> pd.Series:
        """
        Get the portfolio's daily yield change.
        """
        return self.portfolio_delta_yield
