# Threading

Scraped the CSV data file and stored the data in SQLite database

Created 6 agents to handle annual data. These agents extract the yearly data from 1990-2019

After collecting the data, plotted a linear regression graph for each threaded agent using Plotly

Threading Rules:

1. Only one agent can access the database at a time.

2. The database inquiry only request one cell of data per request for data.

3. The agents must make repeated requests for annual data.
