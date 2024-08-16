import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.patches as mpatches

connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT year, COUNT(*) as count FROM transfers t 
WHERE year < 2024 AND year > 1990
GROUP BY(year)
ORDER BY (year) DESC;
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.line(df, x="year", y="average", title='teste')
# fig.show()

sns.set_theme(style="darkgrid")
sns.lineplot(data=df, x='year', y='count')

# Change the labels
plt.xlabel("Year")
plt.ylabel("Number of transfers")
plt.title("Number of transfers per year")
plt.savefig("num_transfers.png")
