-- Create a stored procedure to insert multiple rows of yield data
CREATE OR ALTER PROCEDURE InsertYieldData @YieldDataList AS dbo.YieldDataList READONLY
AS
BEGIN
    INSERT INTO YieldData (InstrumentName, Date, Yield, DateUpdated)
    SELECT InstrumentName, Date, Yield, GETDATE()
    FROM @YieldDataList;
END;
