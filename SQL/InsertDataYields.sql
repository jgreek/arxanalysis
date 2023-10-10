-- Insert or update data into the YieldData table
MERGE INTO YieldData AS target
USING (VALUES (?, ?, ?, ?)) AS source (InstrumentName, Date, Yield, DateUpdated)
ON target.InstrumentName = source.InstrumentName AND target.Date = source.Date
WHEN MATCHED THEN
    UPDATE SET
        target.Yield = source.Yield,
        target.DateUpdated = source.DateUpdated
WHEN NOT MATCHED THEN
    INSERT (InstrumentName, Date, Yield, DateUpdated)
    VALUES (source.InstrumentName, source.Date, source.Yield, source.DateUpdated);
