from preswald import connect, get_df, query, table, text, plotly
import plotly.express as px

connect()
df = get_df("all_month")

sql_cast = """
CREATE OR REPLACE TABLE quakes AS
SELECT *, CAST(mag AS DOUBLE) AS mag_num
FROM all_month
"""
query(sql_cast, "all_month")

sql_big = """
SELECT time, place, mag_num AS mag, depth, latitude, longitude
FROM quakes
WHERE mag_num >= 4
ORDER BY mag_num DESC
"""
big = query(sql_big, "all_month")

text("# Global Earthquakes — last 30 days")

fig_map = px.scatter_geo(
    big,
    lat="latitude",
    lon="longitude",
    color="mag",
    size="mag",
    hover_name="place",
    projection="natural earth"
)
fig_map.update_layout(
    title_text="<b>Where the big shakes happened</b>",
    coloraxis_colorbar=dict(len=0.5)
)
plotly(fig_map)

table(big, title="Magnitude ≥ 4 events")

fig_time = px.scatter(
    df,
    x="time",
    y=df["mag"].cast(float),
    title="Magnitude trend (all quakes)",
    height=300,
    opacity=0.6
)
plotly(fig_time)
