import plotly.graph_objs as go
from dash import dcc

def create_graph(x, y1, y2):
    # Pump graph
    trace1 = go.Scatter(x=x, y=y1,
                        mode='lines+markers',
                        line=dict(color='#FFD700', width=2),
                        connectgaps=True,
                        name='Current basals')

    # Recommendations graph
    trace2 = go.Scatter(x=x, y=y2,
                        mode='lines+markers',
                        line=dict(color='#FF8C00', width=2),
                        connectgaps=True,
                        name='Recommended basals',)

    # Create figure with multiple traces
    data = [trace1, trace2]
    d = 50 # distance
    layout = go.Layout(
        margin=go.layout.Margin(
            # l=d,  # left margin
            r=d,  # right margin
            # b=d,  # bottom margin
            t=d  # top margin
        ),
        legend={'x': 0.7}, # 0-1 legend is on top of graph, >1 legend on right side of graph
    )
    fig = dict(data=data, layout=layout)
    graph = dcc.Graph(figure=fig)
    return graph