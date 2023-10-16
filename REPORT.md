# Report on ARX Yield Data Analysis

## 1. Introduction
**Purpose**: This project assesses the risk associated with a portfolio containing various fixed income assets, primarily U.S. Treasury instruments spanning various maturities. Leveraging two years of daily yield data, this project looks into metrics such as Value at Risk (VaR) and DV01 to provide a comprehensive insight into the risk characteristics of the selected instruments. 

**Importance**: Evaluating risk in fixed income portfolios, especially with instruments like U.S. Treasury bonds, is useful for making informed investment decisions. Utilizing metrics such as VaR and DV01 not only provides investors insights into potential losses and price sensitivities. It can also provide engineers a framework to develop robust financial models and applications.

**Assets**: The project consists of a suite of Python scripts comprising a CLI-based system. Instructions for running the tool are included in the README.md.  


**Note about the name**: ARX stands for "Asset Risk eXplorer," a fun and zippy namespace prefix.

## 2. Data Acquisition and Storage
### Instruments and Rationale
These instruments were chosen for their simplicity, wide availability and consistency of data. The following provides further rationale for each:
- US_TREASURY_10_YR: A benchmark for long-term U.S. interest rates, the 10-year Treasury note can serve as a reference point for mortgage rates, auto loans, and other consumer lending products. 
- US_TREASURY_30_YR: Representing the longest maturity among U.S. Treasury securities, the 30-year bond provides insight into long-term investor outlook.
- US_TREASURY_1_YR: The 1-year T-Bill provides a snapshot of short-term interest rate movements and investor sentiment over the near horizon. 
- US_TREASURY_5_YR: The 5-year note sits in the middle of the yield curve and reflects medium-term economic forecasts.
- US_TREASURY_3_MO: This shorter-term instrument is one barometer of liquidity conditions in the financial system. 


### Data Source
The Quandl public API was used to locate the essential instrument data including instrument name, maturity, date, and yield. 

The ARXApiDataAcquire class handles acquiring the yield data from the API and saving it to a CSV file for each instrument. A separate class ARXYieldDataAccess focuses on saving the individual CSV files to the SQL Server database. This separation of concerns keeps the data acquisition piece focused on 3rd party data integration while the data access layer focused on data persistence and retrieval.  

This methodology is helpful because the data can be viewed easily in CSV and additional files can be imported if not available from the API.


### SQL Server Database
- The developer obtained a Docker container containing SQL Server in order to store instrument yields.
- A simple YieldData schema was created in order to capture the instrument yield data:

`CREATE TABLE YieldData (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    InstrumentName NVARCHAR(255) NOT NULL,
    Date DATE NOT NULL,
    Yield FLOAT NOT NULL,
    DateUpdated DATETIME DEFAULT GETDATE() NOT NULL
)`

- A stored procedure `GetYieldDataByDateRange` was created in order to fetch yields for a given date range.

## 3. Portfolio Simulation
The ARXPortfolioSimulation class provides a way to simulate the performance of a financial portfolio based on historical yield data. It transforms the data into a structured format suitable for analysis. The class then allows users to set specific portfolio weights for each financial instrument. During this process, it anticipates and checks for edge cases such as weights that don't sum up to one or weights assigned to instruments not present in the dataset, raising errors for such discrepancies. It then calculates the day-to-day percentage change in yields for each instrument. The core functionality of the class is its ability to compute the portfolio's delta yield, which represents the weighted average daily yield change across all instruments. Finally, users can retrieve this portfolio's delta yield data. The results will be consumed within the VaR segment of the system.

## 4. VaR Calculation
### Historical Simulation Method
The Historical Simulation method for calculating VaR utilizes past data to forecast potential future losses. It works by sorting all previous returns from the most negative to the most positive and then determining the VaR by selecting the return at a certain percentile.

### Remark on the Implementation
In this implementation, the Strategy Pattern is employed to allow flexibility in choosing the VaR calculation method. The ARXVaRStrategy serves as an abstract base class that mandates the implementation of a calculate method. Specific strategies, such as the ARXHistoricalSimulation and ARXParametricSimulation, provide concrete implementations for this method.

The use of the Strategy Pattern ensures that the system is extensible, allowing for the easy addition of new VaR calculation methods in the future. It also ensures that the VaR calculation is decoupled from the main VaR calculator, adhering to the Single Responsibility Principle and making the system more maintainable.
## 5. DV01 Calculation
### Methodology:
The code is designed to calculate the DV01, or Dollar Value of an 01, which represents the price sensitivity of a bond to a 1 basis point change in yield. The methodology differentiates between zero-coupon and coupon-paying bonds. For zero-coupon bonds, the price is computed by discounting the face value at the bond's yield, while for coupon-paying bonds, the price incorporates the present value of future coupon payments and the face value. The DV01 is then derived by comparing the bond's price at its current yield with its price after a 1 basis point increase. Instrument names are parsed to determine the maturity, distinguishing between those specified in months and years. T-Bills and 1-Year T-Notes are treated as zero-coupon bonds, while other instruments are treated as coupon bonds, with their coupon rate assumed to be equal to their yield. The program retrieves yield data, filters for relevant instruments, and applies the DV01 calculation to each instrument, outputting the results.

### Assumptions:

**Coupon Rate for Coupon-Paying Bonds**: The coupon rate of a bond is assumed to be equal to its yield for the non-zero coupon bonds. In real-world scenarios, the coupon rate often differs from the yield.

**Bond Convention**: The code assumes that all bonds make semi-annual coupon payments (i.e., twice a year). This is typical for US treasuries, but there are bonds with other payment frequencies.

**Bond Maturities**: The code assumes that T-Bills and 1-Year T-Notes are zero-coupon bonds, while other maturities are coupon-paying bonds.

**Data Source**: The code assumes that the data source (via ARXYieldDataAccess) provides accurate and reliable yield data.

**Instrument Naming**: The code assumes a specific naming convention for instruments (like "US_TREASURY_10_YR") to extract maturity information.

### Edge Cases:

**Unknown Maturity Formats**: If an instrument name doesn't end with "_MO" (for months) or "_YR" (for years), the code will raise a ValueError. It currently doesn't handle other maturity formats.

**Data Filtering**: The code filters only those instruments that start with "US_TREASURY_". Any other naming might lead to data not being considered.

**Zero-Coupon Bonds**: The code considers T-Bills and 1-Year T-Notes as zero-coupon bonds. If there's a bond that doesn't pay a coupon and also doesn't match these names, it'll be incorrectly treated as a coupon bond.

### Results
The DV01 measures an instrument's price sensitivity to a 1 basis point movement in its yield. Analyzing the data, the US_TREASURY_30_YR consistently has the highest DV01, signifying its high sensitivity to interest rate changes, while the US_TREASURY_3_MO displays the least. There's a discernible decline in DV01 for most instruments from February 2021 to December 2022, suggesting reduced interest rate sensitivity. Instruments like US_TREASURY_5_YR and US_TREASURY_10_YR occupy intermediate positions. Overall, longer-duration treasuries, such as the 30-year, are more prone to price changes from yield shifts, marking them as potentially riskier investments.

## 6. Stretch (Optional)

**Portfolio Adjustment Feature:**
This feature provides users the flexibility to manage their investment portfolio. Users can view their current allocation of assets and adjust the weightage based on their investment strategy or market insights.

How it's implemented:
1. Loading the Portfolio: On selecting the portfolio tool, the existing portfolio from a configuration file. If no file is found, it sets up a default portfolio.
2. Viewing the Portfolio: Users can opt to view their current portfolio, which shows the allocation of assets by their weightage.
3. Updating the Portfolio: This allows users to make adjustments to their portfolio. The CLI provides a list of available tickers from the dataset, and users can assign new weights to each ticker. Once completed, the updated portfolio replaces the current one and saves back to the configuration file.


### Alternate VaR Methodology
I've provided a preliminary version of a parametric solution for VaR calculation. This method gauges the potential losses an investment portfolio might face based on historical price fluctuations. Imagine looking back at how the price of a stock has moved up and down in the past. By measuring the average price change (mean) and how erratic those changes were (standard deviation), this predicts to a certain confidence level, the worst expected loss in the future. Essentially, the parametric solution takes past price behavior as a benchmark to estimate future risk. 





## 7. Challenges & Learnings
During the course of this project, a number of challenges were encountered and navigated:

1. **Data Sources**:
   Initially, the approach to acquiring data was through downloading CSV files from multiple sources. This presented a
   challenge in ensuring consistency and reliability of the data. The process was simplified by ultimately leveraging
   the `Quandl` API, which provided a more standardized and consistent data source.

2. **Platform and Tool Constraints**:
   SQL Server was used, particularly due to its capabilities with stored procedures. However,
   running on a Mac posed a challenge, as SQL Server isn't natively supported on macOS. The workaround was using Docker
   containers. By downloading the correct Docker container for SQL Server, one is able to bridge the platform gap and
   efficiently use SQL Server on macOS.

3. **Data Formatting and Consistency**:
   With multiple CSV files initially in the picture, a key challenge was to ensure consistent formatting. It was vital
   that the data was not just consistent across different files but also reliable for analysis.

4. **DV01 Strategy**: DV01, a measure of a bond's sensitivity to yield changes, has various calculation methods, each with unique assumptions and applicability. The challenge was navigating these techniques to find one that combined simplicity, accuracy, and relevance for the portfolio, especially given the diverse maturities and coupon structures.


## 8. Conclusion
The "Asset Risk eXplorer" (ARX) project delivered an in-depth risk assessment for a fixed income portfolio, spotlighting U.S. Treasury instruments. Through Value at Risk (VaR) and DV01 metrics, the study revealed the instruments' vulnerabilities to yield shifts and potential losses. Notably, the US_TREASURY_30_YR bond showed significant sensitivity to interest rate fluctuations, coupled with a declining DV01 trend in most instruments between February 2021 and December 2022.

The simulation and adjustment capabilities equip users with data-driven strategies, optimizing portfolio adjustments and fostering strategic investment decisions. Despite challenges in data sourcing and methodology, the outcomes underline the project's rigor and reliability. ARX underlines the importance of thorough risk assessment in modern financial management.

Suggestions for Future Improvements and Scalability:

**Expand Dataset**: Incorporating more diverse assets or global bonds can enhance the tool's versatility and broaden its scope.

**Automate Data Updates**: Establishing automated data pipelines will ensure the system remains up-to-date with market changes.

**Cloud Integration:** Hosting ARX on a cloud platform can improve accessibility and scalability.

**Incorporate Machine Learning**: Predictive analytics could offer insights into potential risks and market behaviors. 
Potential feature candidates include: Automated Portfolio Rebalancing, 
Sentiment Analysis for Market Prediction, Adaptive Stress Testing tools.
