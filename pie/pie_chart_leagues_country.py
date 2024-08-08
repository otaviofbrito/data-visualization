import mysql.connector
import pandas as pd
import plotly.express as px

connection = mysql.connector.connect(
        host='localhost',
        user='user',
        password='user',
        database='tm_db',
        port=3307
    )

query = "SELECT COUNT(id) AS qt, country FROM leagues GROUP BY country;"

df = pd.read_sql(query, connection)

connection.close()
###

df.loc[df['qt'] < 3, 'country'] = 'Other countries'

fig = px.pie(df, values='qt', names='country', title='Leagues')
fig.show()