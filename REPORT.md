# Report on ARX Yield Data Analysis

## 1. Introduction
**Purpose**: This project assesses the risk associated with a portfolio containing various fixed income assets, primarily U.S. Treasury instruments spanning various maturities. Leveraging two years of daily yield data, we delve into key metrics such as Value at Risk (VaR) and DV01 to provide a comprehensive insight into the risk characteristics of the selected instruments. 

**Importance**: Evaluating risk in fixed income portfolios, especially with instruments like U.S. Treasury bonds, is essential for making informed investment decisions. Utilizing metrics such as VaR and DV01 not only provides investors insights into potential losses and price sensitivities but also offers quantitative and software engineers a framework to develop robust financial models and applications.

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

The ARXApiDataAcquire class handles acquiring the yield data from the API and saving it to a CSV file for each instrument. 

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
### Instrument Weightages
- Weightages assigned to each instrument and the reasoning.

### Delta Yield Calculation
- Methodology for computing daily yield changes.

## 4. VaR Calculation
### Historical Simulation Method
- Explanation and benefits/limitations of this method.

### VaR Outcomes
- Display of 1-day VaR at the 95% and 99% confidence levels.

## 5. DV01 Calculation
### Methodology
- Process to compute DV01 for each instrument.

### Results
- Outcomes and insights from DV01 calculations.

## 6. Stretch (Optional)
### Portfolio Adjustment Feature
- Feature that allows users to adjust weightage.

### Alternate VaR Methodology
- Description and comparison between original and alternate methods.

## 7. Challenges & Learnings
During the course of this project, a number of challenges were encountered and navigated:

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
4. **DV01 Strategy**:Selecting the right DV01 strategy posed a significant hurdle. DV01, a measure of a bond's sensitivity to yield changes, has various calculation methods, each with unique assumptions and applicability. The challenge was navigating these techniques to find one that combined simplicity, accuracy, and relevance for the portfolio, especially given the diverse maturities and coupon structures. This process required research, domain understanding, and iterative testing.

## 8. Conclusion
- Summary of findings and real-world importance of the analysis.

## 9. Appendices (if needed)
- Supplementary data, charts, or tables.

## 10. Documentation
### README Overview
- Contents of the README.

### Assumptions
- Assumptions made during the analysis.

