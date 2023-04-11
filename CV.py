from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

folderPath = 'W:/'
df=pd.read_excel(f'{folderPath}/Experience_CV.xlsx')
df_group = df.groupby(by=["Country", "Year Start", "Project Type"]).size().reset_index(name="counts")
df_map = df.groupby(by=["Country"]).size().reset_index(name="counts")

app = Dash(__name__)
server=app.server


app.layout = html.Div([
    html.H4('GEOSCIENCE EXPERIENCE'),
    html.P("Select a plot:"),
    dcc.RadioItems(
        id='selection',
        options=["Experience - Map", "Experience - Bar", "Experience - Sunburst"],
        value='Experience - Sunburst',
    ),
    dcc.Loading(dcc.Graph(id="graph"), type="cube")
])


@app.callback(
    Output("graph", "figure"), 
    Input("selection", "value"))
def display_animated_graph(selection):
    animations = {
        'Experience - Map': px.scatter_geo(
            df_map, locations="Country", color="Country", locationmode="country names", size="counts", projection="natural earth", title="Experience Distribution Map - Hover over the data points"),
        'Experience - Sunburst': px.sunburst(
            df, path=['Region', 'Country', 'Project Type'], color='Country', title="Region, Country and Project Type Sunburst Plot - Click on the sectors to expand/collapse the plot"),
        'Experience - Bar': px.bar(
            df_group, x="Year Start", y="counts", color="Project Type", title="Project Type by Year Bar Chart - Hover over the bars", hover_name="Country"),
    }
    return animations[selection]


app.run_server(debug=True)
