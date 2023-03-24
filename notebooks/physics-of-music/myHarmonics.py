## Import some code modules
import plotly.graph_objects as go
from IPython.display import Audio, display, clear_output
from numpy import pi, sin, power, linspace, array, real
from ipywidgets import interactive, FloatSlider, Dropdown, Output, HBox, VBox

## Setup a default waveform
rate, t_max = 44100, 5
t = linspace(0,t_max,rate*t_max)
signal = sin(2*pi*220*t)

# some useful coefficients for harmonics
n_harms = 9
sine = array([1]+[0]*(n_harms-1))  # this vector defines how many harmonics
ns = array(range(n_harms))
sawtooth = 1/(1+ns)
square = sawtooth*((1+ns)%2)
triangle = square*square*real(1j**ns)

fejer = power(1-ns/n_harms,.75)
sawtooth = sawtooth*fejer
square = square*fejer

# create slides to set the harmonics
def slider_handler(change):
    signal = 0
    for i,s in enumerate(sliders,start=1):
        signal += s.value*sin(i*2*pi*220*t)
    out.clear_output()
    with out:
        display(Audio(data=signal, rate=rate,autoplay=False))
    fig_widget.data[0]['y'] = signal[:nsamples]

sliders = []
for i in range(len(sine)):
    slider = FloatSlider(
        description=f"Harmonic {i+1}", min=-1, max = 1, step = .01)
    slider.observe(slider_handler, names='value')
    sliders.append(slider)
    
# create a drop menu to preselect nice waveforms
d_vals = (sine,triangle,square,sawtooth)
d_list = ("Sine wave", "Triangle wave","Square wave","Sawtooth wave" )

def dropdown_handler(change):
    for i,s in enumerate(sliders):
        s.value = d_vals[d_list.index(change.new)][i]
        
dropdown = Dropdown(description="Presets:", options=d_list)
dropdown.observe(dropdown_handler, names='value')

# create a audio playback tool
out = Output()
with out:
    display(Audio(data=signal, rate=rate))

# create a figure to display the waveform
nsamples = 1024
fig = go.Figure(data=go.Scatter(x= t[:nsamples], y=signal[:nsamples], mode='lines'))
fig.update_xaxes(title_text='Time (mS)').update_yaxes(title_text='Amplitude')
fig_widget = go.FigureWidget(fig)

# Set up the user interface
dropdown.value = d_list[1]
HBox([VBox(children=sliders+[dropdown]+[out]),fig_widget])