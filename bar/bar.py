import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT COUNT(*) AS transfers, year FROM transfers
WHERE year > 1900
GROUP BY(year)
ORDER BY(year);
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='year', y='transfers')
# fig.show()


sns.barplot(data=df, x='year', y='transfers')
plt.savefig("output_plot.png")