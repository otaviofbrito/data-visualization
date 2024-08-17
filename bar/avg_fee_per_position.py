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
SELECT p.main_position AS position, AVG(t.transfer_fee) as avg FROM transfers t
JOIN players p ON t.player_id = p.id
WHERE t.transfer_type = 'Not loan' AND t.transfer_fee > 0 AND p.main_position IS NOT NULL
GROUP BY p.main_position
ORDER BY avg DESC;
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='type', y='transfers')
# fig.show()

figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='r')

sns.set_theme(style="dark")

palette = sns.color_palette("Spectral", len(df['position'].unique()))

fig = sns.barplot(data=df, x='position', y='avg', hue='avg', palette=palette)
legend_labels = [f'{t} ({df[df["position"] == t]["avg"].sum()/1e3:.2f}k)' for t in df['position'].unique()]
handles = [mpatches.Patch(color=palette[i], label=legend_labels[::-1][i]) for i in range(len(legend_labels))]
plt.legend(handles=handles)

plt.xticks(rotation=30)

plt.xlabel("Positions")  # X-axis label
plt.ylabel("Average Transfer Fee in Euros")  # Y-axis label
plt.title("Average Transfer fee per Player Position")


plt.savefig("avg_fee_position.png")