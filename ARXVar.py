import math
from abc import ABC, abstractmethod
import pandas as pd

from scipy.stats import norm


# Define the ARX VaR Strategy Interface
class ARXVaRStrategy(ABC):
    @abstractmethod
    def calculate(self, df: pd.DataFrame, percentile: float):
        pass


# Implement Historical Simulation as an ARX VaR Strategy
class ARXHistoricalSimulation(ARXVaRStrategy):
    """
    This class implements the Historical Simulation method for calculating Value at Risk (VaR).
    In this approach, the VaR is determined based on actual historic market values. It
    assumes that historical market data can be used as a proxy for estimating potential
    future returns. The idea is to sort all returns from the most negative to the most
    positive and then pick the return at a certain percentile as the VaR.

    For instance, if we want to calculate the VaR at a 95% confidence level, we look at
    the 5th worst return in our sorted list. This means there's a 5% chance that losses
    could exceed this amount.
    """

    def calculate(self, series: pd.Series, percentile: float):
        if not (0 <= percentile <= 1):
            raise ValueError("Percentile should be between 0 and 1.")

        # Check if Series is empty
        if series.empty:
            raise ValueError("The provided Series is empty.")

        sorted_returns = sorted(series.tolist())

        # Calculate the desired position in the sorted list to find the VaR.
        index = math.ceil((1 - percentile) * len(sorted_returns)) - 1

        return sorted_returns[index]


class ARXParametricSimulation(ARXVaRStrategy):
    def calculate(self, series: pd.Series, percentile: float):
        # Calculate the mean return.
        mean_return = series.mean()

        # Calculate the standard deviation of returns.
        std_dev = series.std()

        # Get the z-score for the given percentile
        z_score = norm.ppf(1 - percentile)

        # Calculate VaR
        var = -(mean_return - z_score * std_dev)

        return var


# ARX VaR Calculator with Strategy Pattern
class ARXVaRCalculator:
    def __init__(self, strategy: ARXVaRStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ARXVaRStrategy):
        self.strategy = strategy

    def compute(self, series: pd.Series, percentile: float):
        return self.strategy.calculate(series, percentile)
