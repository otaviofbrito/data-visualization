import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.patches as mpatches
from matplotlib.pyplot import figure


connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT p.main_position AS position, COUNT(*) as qt FROM transfers t
JOIN players p ON t.player_id = p.id
WHERE p.main_position IS NOT NULL
GROUP BY p.main_position
ORDER BY qt DESC;
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='type', y='transfers')
# fig.show()

figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='r')

sns.set_theme(style="dark")

palette = sns.color_palette("Spectral", len(df['position'].unique()))

fig = sns.barplot(data=df, x='position', y='qt', hue='qt', palette=palette)
legend_labels = [f'{t} ({df[df["position"] == t]["qt"].sum()/1e3:.2f}k)' for t in df['position'].unique()]
handles = [mpatches.Patch(color=palette[i], label=legend_labels[::-1][i]) for i in range(len(legend_labels))]
plt.legend(handles=handles)

plt.xticks(rotation=30)

plt.xlabel("Positions")  # X-axis label
plt.ylabel("Number of Transfers")  # Y-axis label
plt.title("Number of Transfers per Player Position")


plt.savefig("transfersPerPosition.png")