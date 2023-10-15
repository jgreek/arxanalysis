import pyodbc

# Define connection parameters
server = 'localhost,1433'  # Use 'localhost' because it's a Docker container, and port 1433 maps to the SQL Server port
database = 'master'  # Use the 'master' database for testing connection
username = 'SA'  # SA is the system administrator account in SQL Server
password = 'Greekdev245'  # SA password as specified in the Docker run command

# Create a connection string
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

try:
    # Establish a connection to SQL Server
    conn = pyodbc.connect(conn_str)
    print("Connected to SQL Server")

    # Close the connection
    conn.close()
    print("Connection closed")
except pyodbc.Error as e:
    print(f"Error: {e}")

import pyodbc

# Define your connection parameters
server = 'localhost,1433'  # Use 'localhost' because it's a Docker container, and port 1433 maps to the SQL Server port
database = 'ARXFinance'  # Replace with the name of the database (ARXFinance in this case)
username = 'SA'  # SA is the system administrator account in SQL Server
password = 'Greekdev245'  # SA password as specified in the Docker command

# Create a connection string
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

try:
    # Establish a connection to SQL Server
    conn = pyodbc.connect(conn_str)
    print("Connected to SQL Server")

    # Define the start and end dates for the date range
    start_date = '2020-01-05'
    end_date = '2020-01-10'

    # Create a cursor
    cursor = conn.cursor()

    # Execute the stored procedure with the date range parameters
    cursor.execute("EXEC GetYieldDataByDateRange ?, ?", start_date, end_date)

    # Fetch and display the results
    results = cursor.fetchall()

    for row in results:
        print(row)  # You can access individual columns by index (e.g., row[0], row[1], row[2])

    # Close the cursor and connection
    cursor.close()
    conn.close()
    print("Connection closed")
except pyodbc.Error as e:
    print(f"Error: {e}")
