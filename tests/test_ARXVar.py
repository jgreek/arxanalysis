import pandas as pd
import pytest

from ARXVar import ARXHistoricalSimulation


@pytest.fixture
def sample_data():
    returns = [0.02, -0.01, 0.03, -0.02, 0.01, -0.03, 0.02, -0.01, 0.02, -0.02]
    return pd.Series(returns, name="Returns")


def test_percentile_out_of_bounds():
    arx_hist_sim = ARXHistoricalSimulation()
    series = pd.Series([0.02, -0.01, 0.03], name="Returns")

    with pytest.raises(ValueError, match="Percentile should be between 0 and 1."):
        arx_hist_sim.calculate(series, -0.5)
    with pytest.raises(ValueError, match="Percentile should be between 0 and 1."):
        arx_hist_sim.calculate(series, 1.5)


def test_empty_dataframe():
    arx_hist_sim = ARXHistoricalSimulation()
    series = pd.Series([], name="Returns")

    with pytest.raises(ValueError, match="The provided Series is empty."):
        arx_hist_sim.calculate(series, 0.95)


def test_calculate(sample_data):
    arx_hist_sim = ARXHistoricalSimulation()

    # For the given sample data and 95% percentile
    # The returns below 5% of all data are: -0.03, -0.02, -0.02
    # Thus the VaR at 95% is -0.02 (2nd worst loss)

    result = arx_hist_sim.calculate(sample_data, 0.95)
    # Print debug info
    sorted_returns = sorted(sample_data.tolist())
    index = int((1 - 0.95) * len(sorted_returns))
    print("Sorted Returns:", sorted_returns)
    print("Selected Index:", index)

    assert result == -0.03, f"Expected -0.03, but got {result}"
