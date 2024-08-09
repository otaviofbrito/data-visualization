import mysql.connector
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

connection = mysql.connector.connect(
    host='localhost',
    user='user',
    password='user',
    database='tm_db',
    port=3307
)

query = """
SELECT p.name, t.year, t.transfer_fee, t.transfer_type,
 c1.country AS country_left,
 c2.country AS country_joined
FROM transfers t
JOIN (SELECT clubs.id, cts.country FROM clubs
		JOIN (SELECT l.id, c.country FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c1
ON left_club_id = c1.id
JOIN (SELECT clubs.id, cts.country FROM clubs
		JOIN (SELECT l.id, c.country FROM leagues l
				JOIN countries c
                ON l.country_id = c.country) cts
		ON clubs.id_current_league = cts.id) c2
ON joined_club_id = c2.id
JOIN players p
ON player_id = p.id
WHERE t.year >= 1910;
"""

df = pd.read_sql(query, connection)

country_coords = pd.read_sql(
    "SELECT country, latitude AS lat, longitude AS lon, name FROM tm_db.countries;", connection)

connection.close()

country_coords.set_index('country', inplace=True)

years = df['year'].unique()
years = sorted(years)

data = []
layout = dict(
    # showlegend = False,
    autosize=True,
    hovermode=False,
    legend=dict(
        x=0.7,
        y=-0.1,
        bgcolor="rgba(255, 255, 255, 0)",
        font=dict(size=11),
    )
)

# Create graph

for i in range(len(years)):
    G = nx.DiGraph()

    year_data = df[df['year'] == years[i]]

    for _, row in year_data.iterrows():
        origin = row['country_left']
        destination = row['country_joined']
        if G.has_edge(origin, destination):
            G[origin][destination]['weight'] += 1
        else:
            G.add_edge(origin, destination, weight=1)

    for edge in G.edges(data=True):
        origin = edge[0]
        destination = edge[1]
        weight = edge[2]['weight']
        data.append(
            go.Scattergeo(
                locationmode='ISO-3',
                showlegend=False,
                name=int(years[i]),
                lon=[country_coords.loc[origin, 'lon'],
                     country_coords.loc[destination, 'lon']],
                lat=[country_coords.loc[origin, 'lat'],
                     country_coords.loc[destination, 'lat']],
                mode='lines',
                line=dict(width=1, color='green'),
                opacity=0.6,
            )
        )
    data.append(go.Scattergeo(
        locationmode='ISO-3',
        showlegend=False,
        lon=[country_coords.loc[country, 'lon'] for country in G.nodes],
        lat=[country_coords.loc[country, 'lat'] for country in G.nodes],
        mode='markers',
        marker=dict(size=5, color='red', opacity=0.5),
        text=[country for country in G.nodes]
    )
    )

    layout['title'] = str(years[i])
    fig = go.Figure(data=data, layout=layout)
    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        showland=True,
        showcountries=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)'
    )
    fig.update_layout(height=350, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.write_image(file="./graph/plotsUnique/plot" +
                    str(years[i]) + ".png", format='png')
