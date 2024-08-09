import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as mpatches


connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT SUM(t.transfer_fee) as sum, c.club_name AS clubs FROM transfers t
JOIN clubs c ON t.joined_club_id = c.id
GROUP BY (t.joined_club_id)
ORDER BY (sum) DESC LIMIT 10;
"""

query2 = """
SELECT SUM(t.transfer_fee) as sum, c.club_name AS clubs FROM transfers t
JOIN clubs c ON t.left_club_id = c.id
GROUP BY (t.left_club_id)
ORDER BY (sum) DESC LIMIT 10;
"""

df = pd.read_sql(query2, connection)


connection.close()

# fig = px.bar(df, x='year', y='transfers')
# fig.show()
palette = sns.color_palette("mako", len(df['clubs'].unique()))

figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='r')
sns.set_theme(style="darkgrid")
sns.barplot(data=df, x='sum', y='clubs', hue='sum',palette=palette)


legend_labels = [f'{t} ({df[df["clubs"] == t]["sum"].sum()/1e6:.2f}m)' for t in df['clubs'].unique()]
handles = [mpatches.Patch(color=palette[i], label=legend_labels[i]) for i in range(len(legend_labels))]
plt.legend(handles=handles)


# Change the labels
plt.xlabel("Total Spent in Euros")
plt.ylabel("Clubs")
plt.title("Top Selling Clubs")

plt.savefig("topSelling.png")
