import click
from datetime import datetime, timedelta
from YieldDataWorkflow import YieldDataWorkflow


# Other required imports...
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'mysecretpassword',
    'host': 'localhost'
}
@click.command()
@click.option('--tickers', prompt='Please enter tickers separated by comma',
              help='Tickers like IBM, F or weighted IBM:.33, F:.66')
@click.option('--start_date', default=None, type=str,
              help='Start date in format YYYY-MM-DD. Defaults to 2 years ago from today.')
@click.option('--end_date', default=None, type=str, help='End date in format YYYY-MM-DD. Defaults to today.')
@click.option('--create_db', is_flag=True, help='Flag to create the database.')
@click.option('--drop_db', is_flag=True, help='Flag to drop the database.')
def run_workflow(tickers, start_date, end_date, create_db, drop_db):
    tickers_list = tickers.split(',')
    tickers_weights = {}

    for ticker in tickers_list:
        if ':' in ticker:
            t, w = ticker.split(':')
            tickers_weights[t] = float(w)
        else:
            tickers_weights[ticker] = None

    # If weights are not provided, distribute them evenly
    if None in tickers_weights.values():
        uniform_weight = 1.0 / len(tickers_weights)
        for ticker in tickers_weights:
            tickers_weights[ticker] = uniform_weight
    print("Your ticker weights are: ", tickers_weights)
    # Convert date strings to date objects, if they are provided
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Initialize workflow with your DB params
    workflow = YieldDataWorkflow(db_params)

    # Run the workflow
    workflow.run(list(tickers_weights.keys()), start_date, end_date, create_db, drop_db)

    # PLACEHOLDER: Call other classes/functions here
    print("PLACEHOLDER: Daily Yield")
    print("PLACEHOLDER: VaR")
    print("PLACEHOLDER: DV01")


if __name__ == '__main__':
    run_workflow()

