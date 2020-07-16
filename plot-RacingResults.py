!pip install numpy pandas scipy plotly chart-studio sagemaker boto3 Markdown 
import pandas as pd
import numpy as np
import scipy as sp
import plotly
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import chart_studio as py
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

trackdf = pd.read_csv('track.csv')
df = pd.read_csv('raceResults.csv')
#df = pd.concat([df, pd.read_csv('raceResults2.csv')], ignore_index=True)

plotsdf = df.query('reward > 1.5')

plotsdf['xHeading'] = np.cos(plotsdf['heading'])
plotsdf['yHeading'] = np.sin(plotsdf['heading'])
#plotsdf.insert(7,"xHeading",np.cos(plotsdf['heading']),True)
#plotsdf.insert(7,"yHeading",np.sin(plotsdf['heading']),True)

#plotsdf.head()
#list(plotsdf.columns.values)
#np.cos(plotsdf['heading'])

fig = make_subplots(rows=2, cols=3, subplot_titles=("Rewards","Speed Reward","Position Reward","Speed","Track Differential","% Distance from Center"))

trackPlot = go.Scatter(x=trackdf['x'], y=trackdf['y'], mode='markers', name='track', 
                       marker=dict(color='Black', size=2), showlegend=False)

fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['reward'], #set color equal to a variable
                                                    colorscale='Peach', # one of plotly colorscales
                                                    showscale=False
                                                ), showlegend=False
                        ), row=1, col=1
             )

fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['speedReward'],
                                                    colorscale='Peach', 
                                                    showscale=False
                                                ), showlegend=False
                        ), row=1, col=2
             )


fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['centerReward'],
                                                    colorscale='Peach',
                                                    showscale=False
                                                ), showlegend=False
                        ), row=1, col=3
             )

fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['Speed'],
                                                    colorscale='Cividis',
                                                    showscale=True
                                                ), showlegend=False
                        ), row=2, col=1
             )

fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['TrackDifferential'],
                                                    colorscale='Viridis',
                                                    showscale=False
                                                ), showlegend=False
                        ), row=2, col=2
             )

fig.add_trace(go.Scatter(x=plotsdf['x'], y=plotsdf['y'], mode='markers', marker=
                                                dict(
                                                    size=3,
                                                    color=plotsdf['percDistanceFromCenter'],
                                                    colorscale='Viridis',
                                                    showscale=False
                                                ), showlegend=False
                        ), row=2, col=3
             )

fig.add_trace(trackPlot, row=1, col=1)
fig.add_trace(trackPlot, row=1, col=2)
fig.add_trace(trackPlot, row=1, col=3)
#fig.add_trace(trackPlot, row=2, col=1)
fig.show()

fig = ff.create_quiver(plotsdf['x'], plotsdf['y'], 1.5*plotsdf['xHeading'], 1.5*plotsdf['yHeading'])
fig.show()
