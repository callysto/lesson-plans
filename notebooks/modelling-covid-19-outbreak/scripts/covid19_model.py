import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from ipywidgets import interact, interact_manual, widgets, Layout, VBox, HBox, Button
from IPython.display import display, Javascript, Markdown, HTML, clear_output
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go



# The SEIR model differential equations.
def deriv(y, t, Delta, beta, mu, epsilon,gamma,alpha,delta):
    
    """
    
    """
    
    S, E, I, R, D = y
    N = S + E + I + R
    dS = Delta*N  - beta*S*I/N - mu*S + delta*R
    dE = beta*S*I/N - (mu + epsilon)*E
    dI = epsilon*E - (gamma + mu + alpha)*I
    dR = gamma*I - mu*R - delta*R
    dD = alpha*I 
    
    return [dS,dE, dI, dR, dD]


def plot_infections(Delta, beta, mu, epsilon,gamma,alpha,delta):
    """
    
    """
    
    # Initial number of infected and recovered individuals, I0 and R0.
    S0, E0,I0, R0 ,D0 = 3700,0,100,0,0
    # Total population, N.
    N = S0 + E0 + I0 + R0
    # Initial conditions vector
    y0 = S0,E0, I0, R0, D0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(Delta, beta, mu, epsilon,gamma,alpha,delta))
    S, E,I, R, D = ret.T

    seir_simulation = pd.DataFrame({"Susceptible":S,"Exposed":E,"Infected":I,"Recovered":R,"Deaths":D, "Time (days)":t})

    layout = dict( xaxis=dict(title='Time (days)', linecolor='#d9d9d9', mirror=True),
              yaxis=dict(title='Number of people', linecolor='#d9d9d9', mirror=True))
    
    fig = go.Figure(layout=layout)
    
#    fig.add_trace(go.Scatter(x=seir_simulation["Time (days)"], y=seir_simulation["Susceptible"],
#                        mode='lines',
#                        name='Susceptible'))
    
    fig.add_trace(go.Scatter(x=seir_simulation["Time (days)"], y=seir_simulation["Exposed"],
                        mode='lines',
                        name='Exposed'))
    
    fig.add_trace(go.Scatter(x=seir_simulation["Time (days)"], y=seir_simulation["Infected"],
                    mode='lines',
                    name='Infected'))
    
    fig.add_trace(go.Scatter(x=seir_simulation["Time (days)"], y=seir_simulation["Recovered"],
                        mode='lines', name='Recovered'))

    fig.add_trace(go.Scatter(x=seir_simulation["Time (days)"], y=seir_simulation["Deaths"],
                        mode='lines', name='Deaths'))

    fig.update_layout(title_text="Projected Susceptible, Exposed, Infectious, Recovered, Deaths")

    fig.show();
    

def tinker_beta(beta):
    epsilon = 0.1
    alpha = 0.005
    gamma = 0.1
    mu = 0
    Delta = 0
    delta = 0.00
    numerator = beta*epsilon
    denominator = (alpha + gamma + mu)*(epsilon + mu)
    print("Each infection will generate approximately", numerator/denominator , "new infections.")
    plot_infections(Delta, beta, mu, epsilon, gamma, alpha,delta)
    
    
def tinker_beta_alpha(beta,alpha):
    epsilon = 0.1
    gamma = 0.1
    mu = 0
    Delta = 0
    delta = 0.00
    numerator = beta*epsilon
    denominator = (alpha + gamma + mu)*(epsilon + mu)
    print("Each infection will generate approximately", numerator/denominator , "new infections.")
    plot_infections(Delta, beta, mu, epsilon, gamma, alpha,delta)
    
    
def plot_model(b):
    
    """
    
    """
    beta = all_the_widgets[0].value
    eps = all_the_widgets[1].value
    gamma = all_the_widgets[2].value
    alpha = all_the_widgets[3].value
    Delta =  all_the_widgets[4].value
    mu =  all_the_widgets[5].value
    delta =  all_the_widgets[6].value
    numerator = beta*eps
   
    denominator = (alpha + gamma + mu)*(eps + mu)
    clear_output()
    display(tab)
    print("Each infection will generate approximately", numerator/denominator , "new infections.")
    plot_infections(Delta, beta, mu, eps,gamma,alpha,delta)
    
    
    
if __name__ == "__main__":
    
    style = {'description_width': 'initial'}
    # A grid of time points (in days)
    t = np.linspace(0, 750, 750)

    # Create interactive menu with parameters
    all_the_widgets = [widgets.FloatSlider(
                            min=0, max=1, step=0.01, value=0.5,style =style,description='Beta: contact rate'),
                       widgets.FloatSlider(
                           min=0.1, max=1.0, step=.1, value=.1,style =style,description='Epsilon: infectiousness rate'),
                       widgets.FloatSlider(
                           min=0.1, max=1.0, step=.1, value=.1,style =style,description='Gamma: rate of recovery'),
                       widgets.FloatSlider(
                           min=0, max=1.0, step=.005, value=.005,style =style,description='Alpha: COVID-19 death rate'),
                      widgets.FloatSlider(
                           min=0, max=1.0, step=.005, value=0,style =style,description='Delta: Birth rate'),
                      widgets.FloatSlider(
                           min=0, max=1.0, step=.005, value=0,style =style,description='mu: Natural death rate'),
                      widgets.FloatSlider(
                           min=0, max=1.0, step=.005, value=0.005,style =style,description='delta: re-incorporation rate')]


    # Button widget
    CD_button = widgets.Button(
        button_style='success',
        description="Run Simulations", 
        layout=Layout(width='15%', height='30px'),
        style=style
    )    

    # Connect widget to function - run subsequent cells
    CD_button.on_click( plot_model )

    # user menu using categories found above
    tab3 = VBox(children=[HBox(children=all_the_widgets[0:3]),HBox(children=all_the_widgets[3:6]),
                          HBox(children=all_the_widgets[6:]),
                          CD_button])
    tab = widgets.Tab(children=[tab3])
    tab.set_title(0, 'Choose Parameters')
    
    clear_output()
    
    
    

