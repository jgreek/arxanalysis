class ARXDV01Yields:
    def __init__(self, face_value, yield_rate, time_to_maturity, coupon_rate=0, frequency=2):
        self.face_value = face_value
        self.yield_rate = yield_rate
        self.time_to_maturity = time_to_maturity
        self.coupon_rate = coupon_rate
        self.frequency = frequency  # Semi-annual by default

    @property
    def bond_price(self):
        if self.coupon_rate == 0:  # It's a T-bill
            return self.face_value / (1 + self.yield_rate) ** self.time_to_maturity
        else:  # It's a T-note or T-bond
            coupon_payment = self.face_value * self.coupon_rate / self.frequency
            present_value_of_coupons = sum([coupon_payment / (1 + self.yield_rate / self.frequency) ** i
                                            for i in range(1, self.time_to_maturity * self.frequency + 1)])
            present_value_of_par = self.face_value / (1 + self.yield_rate / self.frequency) ** (
                    self.time_to_maturity * self.frequency)
            return present_value_of_coupons + present_value_of_par

    @property
    def modified_duration(self):
        if self.coupon_rate == 0:  # It's a T-bill
            return self.time_to_maturity
        else:  # It's a T-note or T-bond
            coupon_payment = self.face_value * self.coupon_rate / self.frequency
            weighted_times = sum([(i * coupon_payment) / (1 + self.yield_rate / self.frequency) ** i
                                  for i in range(1, self.time_to_maturity * self.frequency + 1)])
            weighted_times += self.time_to_maturity * self.face_value / (1 + self.yield_rate / self.frequency) ** (
                    self.time_to_maturity * self.frequency)
            return weighted_times / self.bond_price

    @property
    def dv01(self):
        change_in_yield = 0.0001
        return -self.modified_duration * change_in_yield * self.bond_price


if __name__ == "__main__":
    # Example for T-bill (e.g., 3-month)
    tbill = ARXDV01Yields(face_value=1000, yield_rate=0.02, time_to_maturity=0.25)
    print(f"3-month T-bill DV01: ${tbill.dv01:.2f}")

    # Example for T-bond (e.g., 10-year)
    tbond = ARXDV01Yields(face_value=1000, yield_rate=0.03, time_to_maturity=10, coupon_rate=0.025)
    print(f"10-year T-bond DV01: ${tbond.dv01:.2f}")

    data = """
    US_TREASURY_1_YR,2021-01-04,0.1
    """

    # Parsing the data
    lines = data.strip().split("\n")
    parsed_data = [line.split(",") for line in lines]

    # Define the maturity mapping
    maturity_mapping = {
        "US_TREASURY_1_YR": 1,
        # add other mappings if needed
    }

    results = []

    # Compute DV01 for each day
    for item in parsed_data:
        security, date, yield_rate = item
        maturity = maturity_mapping[security.split(",")[0]]
        treasury = ARXDV01Yields(face_value=1000, yield_rate=float(yield_rate) / 100,
                                 time_to_maturity=maturity)  # Convert percentage to decimal
        dv01_value = treasury.dv01
        results.append((date, dv01_value))

    # Displaying results
    for date, dv01_value in results:
        print(f"Date: {date}, DV01: ${dv01_value:.2f}")
