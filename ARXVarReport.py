class ARXVaRReport:
    """
    A class to format and display VaR (Value at Risk) results.
    """

    def __init__(self):
        """
        Initializes the ARXVaRReport class by setting up the border and empty lines for display.
        """
        # Border line for the top and bottom of the box.
        self.border_line = '+' + '-' * 28 + '+'

        # Empty line for spacing within the box.
        self.empty_line = '|' + ' ' * 28 + '|'

    def generate(self, var_95, var_99):
        """
        Generates and prints a formatted VaR report.

        Parameters:
        - var_95 (float): The computed VaR at 95% confidence level.
        - var_99 (float): The computed VaR at 99% confidence level.
        """
        # Convert the numeric VaR values to formatted strings.
        var_95_str = f"VaR 95%: {var_95 * 100:.2f}%"
        var_99_str = f"VaR 99%: {var_99 * 100:.2f}%"

        # Center-align the VaR strings within the box.
        var_95_line = '|' + var_95_str.center(28) + '|'
        var_99_line = '|' + var_99_str.center(28) + '|'

        # Print the formatted VaR report.
        print(self.border_line)
        print(self.empty_line)
        print(var_95_line)
        print(var_99_line)
        print(self.empty_line)
        print(self.border_line)
        print("VaR calculated.")

