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
WHERE t.year >= 1870 AND t.year < 1875;
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
    title='MAPS',
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
    geo_key = 'geo'+str(i+1) if i != 0 else 'geo'
    G = nx.DiGraph()

    year_data = df[df['year'] == years[i]]

    for _, row in year_data.iterrows():
        origin = row['country_left']
        destination = row['country_joined']
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
                geo=geo_key,
                lon=[country_coords.loc[origin, 'lon'],
                     country_coords.loc[destination, 'lon']],
                lat=[country_coords.loc[origin, 'lat'],
                     country_coords.loc[destination, 'lat']],
                mode='lines',
                line=dict(width=weight, color='green'),
                opacity=0.6,
            )
        )

    data.append(go.Scattergeo(
        locationmode='ISO-3',
        showlegend=False,
        geo=geo_key,
        lon=[country_coords.loc[country, 'lon'] for country in G.nodes],
        lat=[country_coords.loc[country, 'lat'] for country in G.nodes],
        mode='markers',
        marker=dict(size=5, color='red', opacity=0.5),
        text=[country for country in G.nodes]
    )
    )

    # Year markers
    data.append(
        dict(
            type='scattergeo',
            showlegend=False,
            lon=[177],
            lat=[127],
            geo=geo_key,
            text=[years[i]],
            mode='text',
        )
    )

    layout[geo_key] = dict(
        showframe=False,
        showcoastlines = False,
        showland=True,
        showcountries=True,
        domain=dict(x=[], y=[]),
        subunitcolor="rgb(255, 255, 255)",
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)'
    )


z = 0
COLS = 2
ROWS = 2
for y in reversed(range(ROWS)):
    for x in range(COLS):
        geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
        layout[geo_key]['domain']['x'] = [
            float(x)/float(COLS), float(x+1)/float(COLS)]
        layout[geo_key]['domain']['y'] = [
            float(y)/float(ROWS), float(y+1)/float(ROWS)]
        z = z+1
        if z > 19:
            break

fig = go.Figure(data=data, layout=layout)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1})
fig.show()
