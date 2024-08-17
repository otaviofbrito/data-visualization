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
SELECT COUNT(*) AS transfers, transfer_type AS type FROM tm_db.transfers
WHERE year > 1900
GROUP BY(transfer_type);
"""

df = pd.read_sql(query, connection)


connection.close()

# fig = px.bar(df, x='type', y='transfers')
# fig.show()

palette = sns.color_palette("mako", len(df['type'].unique()))

sns.barplot(data=df, x='type', y='transfers', hue='transfers', palette=palette)
legend_labels = [f'{t} ({df[df["type"] == t]["transfers"].sum()/1e6:.2f}m)' for t in df['type'].unique()]
handles = [mpatches.Patch(color=palette[i], label=legend_labels[::-1][i]) for i in range(len(legend_labels))]
plt.legend(handles=handles)

plt.xlabel("Type of Transfer")  # X-axis label
plt.ylabel("Number of Transfers")  # Y-axis label
plt.title("Distribution of Transfer Types")


plt.savefig("transfer_type.png")