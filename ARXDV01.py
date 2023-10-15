class ARXDV01:
    def __init__(self, instrument_name, maturity, face_value, coupon_rate, date_yield_list):
        self.instrument_name = instrument_name
        self.maturity = maturity
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.date_yield_list = date_yield_list

    def calculate_bond_price(self, yield_to_maturity):
        # Assuming simple annual coupon payments and ignoring day count for simplicity
        # Implement more comprehensive bond pricing if needed
        total_coupons = sum([self.face_value * self.coupon_rate / (1 + yield_to_maturity) ** n
                             for n in range(1, int(self.maturity) + 1)])
        principal = self.face_value / (1 + yield_to_maturity) ** self.maturity
        return total_coupons + principal

    def calculate_dv01(self):
        # Find bond price for a 1 bp decrease and 1 bp increase in yield
        initial_yield = self.date_yield_list[-1][1]  # Assuming last entry is the current yield
        price_down_1bp = self.calculate_bond_price(initial_yield - 0.0001)
        price_up_1bp = self.calculate_bond_price(initial_yield + 0.0001)

        # Calculate absolute price changes
        absolute_change_down = price_down_1bp - self.calculate_bond_price(initial_yield)
        absolute_change_up = self.calculate_bond_price(initial_yield) - price_up_1bp

        # Average the absolute price changes
        dv01 = (absolute_change_down + absolute_change_up) / 2
        return dv01


def main():
    # Sample parameters
    instrument_name = "Treasury 5 1/8 of May 2016"
    maturity = 10  # making an assumption here, as maturity wasn't provided
    face_value = 100  # again, assuming par value of 100
    coupon_rate = 0.05125  # 5 1/8% annual coupon converted to a decimal
    date_yield_list = [('01/01/2023', 0.0378), ('02/01/2023', 0.0380)]  # example dates and yields

    # Initialize ARXDV01
    bond = ARXDV01(instrument_name, maturity, face_value, coupon_rate, date_yield_list)

    # Calculate DV01
    dv01 = bond.calculate_dv01()
    print(f"DV01 for {instrument_name}: ${dv01:.2f}")


if __name__ == "__main__":
    main()
