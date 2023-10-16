from pathlib import Path
from ARXYieldDataAccess import ARXYieldDataAccess


class ARXUsTreasuryDV01Calc:
    def __init__(self, face_value, yield_rate, time_to_maturity, coupon_rate=None):
        self.face_value = face_value
        self.yield_rate = yield_rate
        self.time_to_maturity = time_to_maturity
        self.coupon_rate = coupon_rate

    @property
    def dv01(self):
        """
        Compute the DV01 (Dollar Value of an 01) of the bond.

        The DV01 is the price sensitivity of the bond to a 1 basis point (0.01%) change in yield.
        It's calculated by taking the difference between the bond's price at its current yield
        and its price after a 1 basis point increase in yield.

        Returns:
        - float: The DV01 of the bond.
        """

        # Define the magnitude of the yield change for DV01 calculation:
        # 1 basis point (0.01% or 0.0001 in decimal form).
        delta = 0.0001

        # Check if the bond is a zero-coupon bond (no coupon payments, only face value at maturity).
        if self.coupon_rate is None:
            # Calculate the initial bond price using the current yield.
            price_initial = self.zero_coupon_price(self.yield_rate)

            # Calculate the bond price after a 1 basis point increase in yield.
            price_increase = self.zero_coupon_price(self.yield_rate + delta)
        else:
            # For coupon-paying bonds, follow the same logic but using the coupon bond price formula.
            price_initial = self.coupon_bond_price(self.yield_rate)
            price_increase = self.coupon_bond_price(self.yield_rate + delta)

        # The DV01 is the difference between the initial bond price and the bond price after the yield change.
        return price_initial - price_increase

    def zero_coupon_price(self, yield_rate):
        """
        Compute the present value price of a zero-coupon bond.

        Zero-coupon bonds do not pay any interest until maturity. Their price is the discounted value
        of their face value, using the provided yield rate.

        Parameters:
        - yield_rate (float): The market yield rate (as a decimal, e.g., 0.025 for 2.5%).

        Returns:
        - float: The present value price of the zero-coupon bond.
        """

        # Calculate the present value of the bond's face value.
        # The price is the face value discounted by the yield rate over the bond's time to maturity.
        return self.face_value / (1 + yield_rate) ** self.time_to_maturity

    def coupon_bond_price(self, yield_rate):
        """
        Compute the present value price of a coupon-paying bond.

        Parameters:
        - yield_rate (float): The market yield rate (as a decimal, e.g., 0.025 for 2.5%)

        Returns:
        - float: The present value price of the bond.
        """

        # Calculate the value of the coupon payment.
        # It is the product of the coupon rate (as a fraction) and the face value of the bond.
        coupon = self.coupon_rate * self.face_value

        # Determine the number of coupon periods based on the time to maturity.
        # We're assuming semi-annual coupons (twice a year), so multiply the maturity in years by 2.
        periods = int(self.time_to_maturity * 2)

        # Calculate the present value of all future coupon payments.
        # The list comprehension iterates through each coupon payment and discounts it back to the present.
        # The discounting assumes semi-annual compounding, hence the 'yield_rate / 2'.
        coupons_pv = sum([coupon / (1 + yield_rate / 2) ** i for i in range(1, periods + 1)])

        # Calculate the present value of the face value of the bond, which is returned at the end of the bond's life.
        # The face value is discounted back from the end of its term.
        face_value_pv = self.face_value / (1 + yield_rate / 2) ** periods

        # Sum up the present value of the coupons and the face value to get the total price of the bond.
        return coupons_pv + face_value_pv

    @staticmethod
    def compute_dv01(row):
        """
        Compute the DV01 (Dollar Value of an 01) for a given row of instrument data.

        Parameters:
        - row: A Pandas Series representing a row from a DataFrame containing yield data.
               Expected columns are 'InstrumentName' and 'Yield'.

        Returns:
        - float: The calculated DV01 for the instrument.
        """

        # Extract the name of the instrument (e.g., 'US_TREASURY_10_YR')
        instrument = row['InstrumentName']

        # Convert the yield from percentage to a decimal (e.g., 2.5% -> 0.025)
        yield_rate = row['Yield'] / 100

        # Parse the time to maturity from the instrument name
        # Extract the last two parts of the instrument name (e.g., '10_YR' from 'US_TREASURY_10_YR')
        maturity_str = '_'.join(instrument.split('_')[-2:])

        # Check if the instrument is a T-Bill with maturity in months
        if 'MO' in maturity_str:
            # Convert the maturity string to a numerical value and then to years
            # For instance, '3_MO' becomes 3/12 = 0.25 years
            time_to_maturity = int(maturity_str.replace('MO', '').replace('_', '')) / 12
        # Check if the instrument has a maturity in years
        elif 'YR' in maturity_str:
            # Convert the maturity string to a numerical value
            # For instance, '10_YR' becomes 10 years
            time_to_maturity = int(maturity_str.replace('YR', '').replace('_', ''))
        else:
            # Raise an error for unknown maturity formats
            raise ValueError(f"Unknown maturity format in instrument: {instrument}")

        # Determine the type of treasury instrument based on its maturity
        # T-Bills and 1-Year T-Notes are considered zero-coupon
        if 'MO' in maturity_str or '1_YR' in maturity_str:
            treasury = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=yield_rate, time_to_maturity=time_to_maturity)
        else:
            # For other maturities, assume they are coupon bonds and set the coupon rate to be equal to the yield
            # Note: In a real-world scenario, the coupon rate should be retrieved from accurate sources.
            # Due to the coupon rate not being available via the API, use yield rate for now but provide for it to be used in future.
            treasury = ARXUsTreasuryDV01Calc(face_value=1000, yield_rate=yield_rate, time_to_maturity=time_to_maturity,
                                             coupon_rate=yield_rate)

        # Return the computed DV01 for the instrument
        return treasury.dv01


if __name__ == "__main__":
    start_date = "2021-01-01"
    end_date = "2023-01-01"

    yield_data_access = ARXYieldDataAccess(data_directory=Path("sources"), config_directory=Path("config"),
                                           sql_directory=Path("SQL"))
    df = yield_data_access.execute_get_yield_data_by_date_range(start_date, end_date)
    df = df[df["InstrumentName"].str.startswith("US_TREASURY_")]
    df['DV01'] = df.apply(ARXUsTreasuryDV01Calc.compute_dv01, axis=1)
    print(df[["InstrumentName", "DV01"]])
