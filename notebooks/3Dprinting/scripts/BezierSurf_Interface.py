import scripts.models.canoeModel as canoe 
import scripts.BezierSurface as bs
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from ipywidgets import interact, fixed, interact_manual #, interactive
import ipywidgets as widgets
from IPython.display import display


def Canoe():
    stepSize = 0.05
    widgetLength = widgets.FloatSlider(min = 4, 
                                 max = 10, 
                                 step = stepSize, 
                                 value = 7.687, 
                                 description = "length (m)", 
                                 continuous_update = False)
    
    widgetWidth = widgets.FloatSlider(min = 0.1, 
                                max = 3, 
                                step = stepSize, 
                                value = 1.250, 
                                description = "width (m)", 
                                continuous_update = False)
    
    widgetHeight = widgets.FloatSlider(min = 0.1, 
                                 max = 3, 
                                 step = stepSize, 
                                 value = 1.135, 
                                 description = "height (m)", 
                                 continuous_update = False)
    
    widgetNames   = widgets.Dropdown(options = [("Nootkan-Style Canoe", 1), ("Haida-Dugout Canoe", 2)],
                              value = 1,
                              description = "Canoe type: ")
    
    #ui = widgets.HBox([length, width, height, name])
    #out = widgets.interactive_output(CanoeGraph, {"length": length, "width": width, "height": height, "name": name})
    
    #display(ui, out)
    
    widgets.interact_manual(CanoeGraph, length = widgetLength, width = widgetWidth, height = widgetHeight, name   = widgetNames)

## Introduce some globals that we can use elsewhere
XX,YY,ZZ,YY_mirror =[],[],[],{}

def CanoeGraph(length, width, height, name):
    global XX, YY, ZZ, YY_mirror
    XX, YY, ZZ = canoe.GetCanoe(length, width, height, name, 4)
    YY_mirror = np.multiply(YY, -1)
    
    myColor = np.ones(shape = XX.shape)
    #remove axis labels
    trace1 = go.Surface(x=XX, 
                        y=YY, 
                        z=ZZ, 
                        surfacecolor=myColor, 
                        showscale = False, 
                        contours ={"z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}})
    trace2 = go.Surface(x=XX, 
                        y=YY_mirror, 
                        z=ZZ, 
                        surfacecolor=myColor, 
                        showscale = False, 
                        contours ={"z": {"show": True, "start": 0.02, "end": 0.7, "size": 0.15, "color":"white"}})
    
    axisDictionary = dict(title = '', showbackground = False, showgrid = False, showline = False, showticklabels = False)
    fig = go.Figure(data = [trace1, trace2])
    fig.update_layout(scene = dict( aspectmode= "data",
                                    xaxis = axisDictionary,
                                    yaxis = axisDictionary,
                                    zaxis = axisDictionary))
    fig.show()
