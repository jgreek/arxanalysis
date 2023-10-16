import pytest
import pandas as pd

from ARXUsTreasuryDV01Calc import ARXUsTreasuryDV01Calc


def test_zero_coupon_price():
    # Create an instance of the ARXUsTreasuryDV01Calc class for a zero-coupon bond
    bond = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=0.025, time_to_maturity=10)

    # Calculate the zero-coupon price
    price = bond.zero_coupon_price(0.025)

    # The expected value based on the formula: F / (1 + r)^n
    expected_price = 1000 / (1 + 0.025) ** 10

    # Assert that the calculated price is close to the expected price (within a small tolerance)
    assert abs(price - expected_price) < 1e-6  # 1e-6 is a small tolerance for floating-point comparisons


def test_coupon_bond_price():
    # Create an instance of the ARXUsTreasuryDV01Calc class for a coupon-paying bond
    bond = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=0.025, time_to_maturity=10, coupon_rate=0.025)

    # Calculate the coupon bond price
    price = bond.coupon_bond_price(0.025)

    # Calculate the expected value based on the given formula
    coupon = 0.025 * 1000
    periods = 10 * 2
    coupons_pv = sum([coupon / (1 + 0.025 / 2) ** i for i in range(1, periods + 1)])
    face_value_pv = 1000 / (1 + 0.025 / 2) ** periods
    expected_price = coupons_pv + face_value_pv

    # Assert that the calculated price is close to the expected price (within a small tolerance)
    assert abs(price - expected_price) < 1e-6


def test_dv01_zero_coupon():
    # Create an instance of the ARXUsTreasuryDV01Calc class for a zero-coupon bond
    bond = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=0.025, time_to_maturity=10)

    # Calculate the DV01
    dv01 = bond.dv01

    # Calculate the expected DV01 manually
    delta = 0.0001
    price_initial = bond.zero_coupon_price(0.025)
    price_increase = bond.zero_coupon_price(0.025 + delta)
    expected_dv01 = price_initial - price_increase

    # Assert that the calculated DV01 is close to the expected DV01 (within a small tolerance)
    assert abs(dv01 - expected_dv01) < 1e-6


def test_dv01_coupon_bond():
    # Create an instance of the ARXUsTreasuryDV01Calc class for a coupon-paying bond
    bond = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=0.025, time_to_maturity=10, coupon_rate=0.025)

    # Calculate the DV01
    dv01 = bond.dv01

    # Calculate the expected DV01 manually
    delta = 0.0001
    price_initial = bond.coupon_bond_price(0.025)
    price_increase = bond.coupon_bond_price(0.025 + delta)
    expected_dv01 = price_initial - price_increase

    # Assert that the calculated DV01 is close to the expected DV01 (within a small tolerance)
    assert abs(dv01 - expected_dv01) < 1e-6


def test_compute_dv01():
    # Create a sample data row mimicking a DataFrame row for a 10-year US Treasury instrument
    data = {
        'InstrumentName': 'US_TREASURY_10_YR',
        'Yield': 2.5  # 2.5% in percentage form
    }
    row = pd.Series(data)

    # Calculate the DV01 using the staticmethod
    dv01 = ARXUsTreasuryDV01Calc.compute_dv01(row)

    # Manually calculate the expected DV01
    # Initialize a bond instance (use coupon rates equal to yield until the data is made available via API)
    bond = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=0.025, time_to_maturity=10, coupon_rate=0.025)
    expected_dv01 = bond.dv01

    # Assert that the calculated DV01 is close to the expected DV01 (within a small tolerance)
    assert abs(dv01 - expected_dv01) < 1e-6


# If you want to run the tests from the command line
if __name__ == '__main__':
    pytest.main()
