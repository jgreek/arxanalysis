-- Create a user-defined table type for YieldData
CREATE TYPE dbo.YieldDataList AS TABLE
(
    InstrumentName VARCHAR(255),
    Date           DATE,
    Yield          DECIMAL(10, 2)
);
