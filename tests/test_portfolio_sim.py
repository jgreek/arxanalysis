import pandas as pd
import pytest

from ARXPortfolioSimulation import ARXPortfolioSimulation

# Sample data for the tests
data = {
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
    'InstrumentName': ['A', 'B', 'A', 'B'],
    'Yield': [1.5, 2.5, 1.55, 2.55]
}
df = pd.DataFrame(data)


# Test for the transform_data method
def test_transform_data():
    simulation = ARXPortfolioSimulation(df)
    transformed = simulation.transform_data(df)
    assert 'A' in transformed.columns and 'B' in transformed.columns
    assert transformed.iloc[0]['A'] == 1.5


# Test for the set_weights method
def test_set_weights():
    simulation = ARXPortfolioSimulation(df)
    weights = {'A': 0.6, 'B': 0.4}
    simulation.set_weights(weights)
    assert simulation.weights == [0.6, 0.4]

    with pytest.raises(ValueError):  # Testing the ValueError for incorrect keys
        simulation.set_weights({'A': 0.6, 'C': 0.4})

    with pytest.raises(ValueError):  # Testing the ValueError for sum of weights != 1
        simulation.set_weights({'A': 0.6, 'B': 0.5})


# Test for the simulate method
def test_simulate():
    simulation = ARXPortfolioSimulation(df)
    weights = {'A': 0.6, 'B': 0.4}
    simulation.set_weights(weights)
    simulation.simulate()
    portfolio_delta_yield = simulation.get_portfolio_delta_yield()

    assert portfolio_delta_yield is not None
    assert isinstance(portfolio_delta_yield, pd.Series)

    # Check for the correct values in the portfolio delta yield.
    assert portfolio_delta_yield.iloc[0] == 0.0  # First value should be zero due to pct_change()
    # Expected value for the second date: 0.6*(1.55-1.5)/1.5 + 0.4*(2.55-2.5)/2.5
    assert round(portfolio_delta_yield.iloc[1], 8) == round(0.028, 8)
