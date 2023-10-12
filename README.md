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
* SQL Express Database
* Libraries:
    - `quandl`
    - `sqlalchemy`
    - `pandas`

To install the required libraries, run:
\```bash
pip install quandl sqlalchemy pandas
\```

## Data Acquisition

U.S. Treasury bond yield data for various maturities is fetched from the `Quandl` API and stored in an SQL Express
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
* **Greeks Calculation**: The Delta, Gamma, and Vega for the portfolio are computed and analyzed.

## Getting Started

1. Clone this repository to your local machine.
2. Install necessary dependencies.
3. If you are running SQL Server from a Docker file, you'll need to run the container first. These instructions are
   specific to a Mac:
    4. HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
    5. docker pull mcr.microsoft.com/mssql/server:2017-latest
    6. docker run -d --name ms-sql-server -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YOURPASSWORD’ -p 1433:1433
       mcr.microsoft.com/mssql/server:2017-latest

3. You will need a configuration file in config / config.json like so:
   \```
   {
   "server": "localhost,1433",
   "database": "ARXFinance",
   "username": "",
   "password": "",
   "quandl_key": "your api key here"
   }
   \```


3. You'll also need a Quandl key in order to fetch fixed income instrument yield data. You can skip this step by placing CSV files in the sources directory and then running the import tool. 
4. Setup SQL database and ensure connection parameters in the code are correctly configured.
4. Run the data acquisition script to fetch and store data.
5. Run the main analysis script to get risk metrics.
6. (Optional) Use the stretch features for additional insights.

## Challenges

During the course of this project, a number of challenges were encountered and successfully navigated:

1. **Data Source Dilemma**:
   Initially, my approach to acquiring data was through downloading CSV files from multiple sources. This presented a
   challenge in ensuring consistency and reliability of the data. The process was simplified by ultimately leveraging
   the `Quandl` API, which provided a more standardized and consistent data source.

2. **Platform and Tool Constraints**:
   I had a strong preference for using SQL Server, particularly due to its capabilities with stored procedures. However,
   running on a Mac posed a challenge, as SQL Server isn't natively supported on macOS. The workaround was using Docker
   containers. By downloading the correct Docker container for SQL Server, I was able to bridge the platform gap and
   efficiently use SQL Server on macOS.

3. **Data Formatting and Consistency**:
   With multiple CSV files initially in the picture, a key challenge was to ensure consistent formatting. It was vital
   that the data was not just consistent across different files but also reliable for analysis. Through a combination of
   Python scripts and manual checks, I managed to format and validate the data for consistency and reliability.

These challenges not only added complexity to the project but also provided valuable learning experiences. Overcoming
them required a mix of technical knowledge, problem-solving skills, and adaptability.

## Conclusions and Insights

A detailed report on the findings, insights about the risk profiles, and any challenges faced during the analysis can be
found [here](./REPORT.md).

## License

This project is licensed under the MIT License.
