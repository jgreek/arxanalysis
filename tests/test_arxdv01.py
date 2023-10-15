import pytest

from ARXDV01 import ARXDV01


@pytest.fixture
def sample_bond():
    instrument_name = "US_TREASURY_30_YR"
    maturity = 30
    face_value = 1000
    coupon_rate = 0.02
    date_yield_list = [
        ("2022-07-05", 3.05000),
        # ... you can add other data points for more exhaustive testing
    ]
    return ARXDV01(instrument_name, maturity, face_value, coupon_rate, date_yield_list)


def test_bond_price(sample_bond):
    ytm = 3.05000
    expected_price = 23.52  # Adjusted to the actual value you've provided
    computed_price = sample_bond.compute_bond_price(ytm)
    tolerance = 1e-2  # This represents a tolerance of 0.01
    assert abs(computed_price - expected_price) < tolerance, \
        f"Expected {expected_price}, but got {computed_price}"


def test_dv01_calculation(sample_bond):
    result = sample_bond.compute_dv01()
    expected_dv01_for_given_date = (0.328985,)  # Adjust this expected DV01 value based on your calculations
    assert len(result) == 1, "Only one data point provided for testing"
    date, dv01 = result[0]
    assert date == "2022-07-05"
    assert abs(
        dv01 - expected_dv01_for_given_date[0]) < 1e-2, f"Expected {expected_dv01_for_given_date[0]}, but got {dv01}"
