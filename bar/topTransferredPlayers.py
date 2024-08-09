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
SELECT COUNT(*) as qt, p.citizenship_1 AS ctz, p.name AS name FROM transfers t
JOIN players p ON t.player_id = p.id
GROUP BY(player_id)
HAVING(qt >= 38)
ORDER BY(qt) DESC;
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='year', y='transfers')
# fig.show()

# Create a table
fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the size as needed

# Hide the axes
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

df.columns = ['Number of Transfers', 'Citizenship', 'Player Name']
# Create the table
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='center',
    rowColours=['#f5f5f5'] * len(df),
    colColours=['#d3d3d3'] * len(df.columns)
)

# Adjust the table appearance
table.auto_set_font_size(True)
table.scale(1.2, 1.2)  # Adjust scale if necessary


plt.savefig("output_plot.png")
