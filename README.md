# ARX Risk Analysis App

This project focuses on evaluating the risk of a portfolio comprised of different fixed income instruments, mainly U.S.
Treasury bonds of various maturities. The analysis uses daily yield data from the past two years and examines metrics
like Value at Risk (VaR) and DV01 to better understand the risk profile of the chosen instruments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Data Acquisition](#data-acquisition)
3. [Portfolio Simulation](#portfolio-simulation)
4. [Risk Metrics Calculation](#risk-metrics-calculation)
5. [Stretch Features](#stretch-features)
6. [Getting Started](#getting-started)
7. [Conclusions and Insights](#conclusions-and-insights)
8. [License](#license)

## Prerequisites

* Python 3.x
* SQL Server Database
* Libraries:
    - `quandl`
    - `pandas`
    - Other libraries specified in requirements.txt

To install the required libraries, run:
\```bash
pip install -r requirements.txt
\```

## Data Acquisition

U.S. Treasury bond yield data for various maturities is fetched from the `Quandl` API and stored in an SQL Server
database.

* Instruments: 3-month, 1-year, 5-year, 10-year, 30-year.

## Portfolio Simulation

The portfolio is constructed using arbitrary weightages for the instruments. Daily yield changes (delta yield) are
computed for the portfolio, providing insights into daily fluctuations.

## Risk Metrics Calculation

1. **VaR (Value at Risk)**: This metric provides a measure of the risk of the portfolio, showcasing potential losses on
   a given confidence level. VaR is calculated at both 95% and 99% confidence intervals using the Historical Simulation
   method.
2. **DV01**: Represents the sensitivity of the portfolio's price to a 1 basis point change in yield.

## Stretch Features

* **User-adjusted Weightages**: An interactive module that allows users to adjust the weightage of instruments and
  recalculate VaR.

## Getting Started

1. Clone this repository to your local machine.
2. Install necessary dependencies
3. If you are running SQL Server from a Docker file, you'll need to run the container first. These instructions are
   specific to a Mac:
   1. HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
   2. docker pull mcr.microsoft.com/mssql/server:2017-latest
   3. docker run -d --name ms-sql-server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YOURPASSWORD’ -p 1433:1433
       mcr.microsoft.com/mssql/server:2017-latest
   4. If you're running on a Mac, you will need to setup XCode command line tools. 
      5. sudo xcode-select --install

4. You will need a database/API configuration file in config / config.json like so. There is a template located at _config.json.
   \```
   {
   "server": "localhost,1433",
   "database": "ARXFinance",
   "username": "",
   "password": "",
   "quandl_key": "your api key here"
   }
   \```


5. As specified above, you'll also need a Quandl key in order to fetch fixed income instrument yield data. You can skip this step by placing CSV files in the sources directory and then running the import tool. 
6. Setup the SQL database server and ensure connection parameters in the code are correctly configured. 
7. Create a database named ARXFinance.
8. Create a new Python virtual environment like so: `python -m venv venv`
9. Activate the environment: `.\venv\Scripts\activate` or `source venv/bin/activate`.
10. Apply the python requirements file to obtain the necessary libraries: `pip install -r requirements.txt`.
11. Run the CLI Main Menu by running `python ARXMainMenu.py`

## Conclusions and Insights

A detailed report on the findings, insights about the risk profiles, and any challenges faced during the analysis can be
found [here](./REPORT.md).

## License

This project would be licensed under the MIT License.
