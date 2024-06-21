import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from app import get_db_connection
import pandas as pd
import plotly.express as px
import sqlite3
import logging

app = dash.Dash(__name__)

logging.basicConfig(level=logging.INFO)

# 12
def load_transaction_data():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    df['time'] = pd.to_datetime(df['time'])
    conn.close()
    return df

# 13
def prepare_transactions():
    transactions = load_transaction_data()
    transactions['denied'] = transactions['status'].apply(lambda x: 1 if x == 'denied' else 0)
    transactions['failed'] = transactions['status'].apply(lambda x: 1 if x == 'failed' else 0)
    transactions['reversed'] = transactions['status'].apply(lambda x: 1 if x == 'reversed' else 0)
    transactions['count'] = 1
    return transactions

# 14
def generate_fig(transactions):
    if transactions.empty:
        logging.warning("No transactions to display")
        return px.line(title='No transactions to display')

    transactions.set_index('time', inplace=True)
    transactions_resampled = transactions.resample('min').sum()

    transactions_resampled['z_score_failed'] = (transactions_resampled['failed'] - transactions_resampled['failed'].mean()) / transactions_resampled['failed'].std()
    transactions_resampled['z_score_reversed'] = (transactions_resampled['reversed'] - transactions_resampled['reversed'].mean()) / transactions_resampled['reversed'].std()
    transactions_resampled['z_score_denied'] = (transactions_resampled['denied'] - transactions_resampled['denied'].mean()) / transactions_resampled['denied'].std()

    anomalies = transactions_resampled[
        (transactions_resampled['z_score_failed'].abs() > 2) |
        (transactions_resampled['z_score_reversed'].abs() > 2) |
        (transactions_resampled['z_score_denied'].abs() > 2)
    ]

    fig = px.line(transactions_resampled, x=transactions_resampled.index, y='count', title='Transactions Over Time')

    if not anomalies.empty:
        fig.add_scatter(x=anomalies.index, y=anomalies['count'], mode='markers', name='Anomalies', marker=dict(color='red', size=10))

    # Customize x-axis to show only the time
    fig.update_layout(xaxis=dict(tickformat='%H:%M'))

    return fig

# 15
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Atualiza a cada 5 segundos
        n_intervals=0
    )
])

# 16
@app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    transactions = prepare_transactions()
    fig = generate_fig(transactions)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
