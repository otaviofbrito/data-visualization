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
SELECT AVG(transfer_fee) AS average, year FROM transfers
WHERE year > 1900 AND year <= 2024 AND transfer_fee != 0
GROUP BY(year)
ORDER BY(year);
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.line(df, x="year", y="average", title='teste')
# fig.show()

sns.lineplot(data=df, x='year', y='average')

# Change the labels
plt.xlabel("Year")
plt.ylabel("Fee in millions of euros")
plt.title("Average Transfer Fee in Euros")

plt.savefig("avg_fee.png")
