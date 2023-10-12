-- Create a stored procedure to retrieve YieldData by date range
CREATE OR ALTER PROCEDURE GetYieldDataByDateRange
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN
    SELECT Id, InstrumentName, Date, Yield, DateUpdated
    FROM YieldData
    WHERE Date >= @StartDate AND Date <= @EndDate;

END;



