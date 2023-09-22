import pandas as pd
import sqlite3
from threading import Thread, Lock
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression

# Scrape csv data file and store data in SQLite database
data = pd.read_csv("AGGI_Table.csv", delimiter=',', skiprows=2)
conn = sqlite3.connect("grftable.db")
data.to_sql('grftable', conn, if_exists='replace')

db_lock = Lock()


def get_yearly_data(gas, year):
    with db_lock:
        conn = sqlite3.connect("grftable.db")
        cursor = conn.cursor()
        gas_col = gas if gas not in ('CFC*', 'HFCs*') else f'"{gas}"'
        query = f"SELECT {gas_col} FROM grftable WHERE Year = {year}"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    return data


def plot_linear_regression(gas):
    years = list(range(1990, 2020))
    data = [get_yearly_data(gas, year) for year in years]

    X = np.array(years).reshape(-1, 1)
    y = np.array(data).reshape(-1, 1)
    reg = LinearRegression().fit(X, y)
    reg_line = reg.predict(X)

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=years, y=data, mode='markers', name='Data'), row=1, col=1)
    fig.add_trace(go.Scatter(x=years, y=reg_line.flatten(), mode='lines', name='Linear Regression'), row=1, col=1)

    fig.update_layout(title=f"Linear Regression for {gas}",
                      xaxis_title="Year",
                      yaxis_title="Radiative Forcing",
                      yaxis_type='log')
    fig.show()


gases = ['CO2', 'CH4', 'N2O', 'CFC*', 'HCFCs', 'HFCs*']
threads = []
for gas in gases:
    thread = Thread(target=plot_linear_regression, args=(gas,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
