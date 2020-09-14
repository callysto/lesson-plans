import requests as r
import pandas as pd

# Define a function to drop the history.prefix
# Create function drop_prefix
def drop_prefix(self, prefix):
    self.columns = self.columns.str.lstrip(prefix)
    return self



# Define function which removes history. prefix, and orders the column dates in ascending order
def order_dates(flat_df):

    # Drop prefix
    flat_df.drop_prefix('history.')
    flat_df.drop_prefix("coordinates.")
    # Isolate dates columns
    flat_df.iloc[:,6:].columns = pd.to_datetime(flat_df.iloc[:,6:].columns)
    # Transform to datetim format
    sub = flat_df.iloc[:,6:]
    sub.columns = pd.to_datetime(sub.columns)
    # Sort
    sub2 = sub.reindex(sorted(sub.columns), axis=1)
    sub3 = flat_df.reindex(sorted(flat_df.columns),axis=1).iloc[:,-5:]
    # Concatenate
    final = pd.concat([sub2,sub3], axis=1, sort=False)
    return final


def fit_data(Delta, beta, mu, epsilon,gamma,alpha,delta):

    
    S0, E0,I0, R0,D0 = 3700000,0,1,0,0
    # Total population, N.
    N = S0 + E0 + I0 + R0
    # Initial conditions vector
    y0 = [S0,E0, I0, R0,D0]
    ret = odeint(deriv, y0, t, args=(Delta, beta, mu, epsilon,gamma,alpha,delta))
    S, E,I, R ,D= ret.T
    
    seir_simulation = pd.DataFrame({"Susceptible":S,"Exposed":E,"Infectious":I,"Recovered":R,"Time (days)":t})
    seir_simulation['date'] = pd.date_range(start='01/24/2020', periods=len(seir_simulation), freq='D')
    
    trace3 = go.Scatter(x = non_cumulative_cases.index,y=non_cumulative_cases["TotalDailyCase"])
    trace2 = go.Scatter(x = seir_simulation["date"],y=seir_simulation["Infectious"],yaxis='y2')
    layout = go.Layout(
        title= ('First guess to fit model: infectious against number of reported cases in ' + str(country)),
        yaxis=dict(title='Daily Number of  Reported Infections',\
                   titlefont=dict(color='blue'), tickfont=dict(color='blue')),
            yaxis2=dict(title='Number of infectious members (our model)', titlefont=dict(color='red'), \
                        tickfont=dict(color='red'), overlaying='y', side='right'),
            showlegend=False)
    fig = go.Figure(data=[trace3,trace2],layout=layout)
    
    fig.show()

def plot_model_and_data(b):
    
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
    display(tab1)
    print("Each infection will generate approximately", numerator/denominator , "new infections.")
    
    fit_data(Delta, beta, mu, eps,gamma,alpha,delta)
    
if __name__ == "__main__":
    
    # PD formatting
    # Call function
    pd.core.frame.DataFrame.drop_prefix = drop_prefix

    ## Getting data
    try:
        print("Downloading COVID-19 data - Canada")
        API_response_confirmed = r.get("https://covid19api.herokuapp.com/confirmed")
        data = API_response_confirmed.json() # Check the JSON Response Content documentation below
        confirmed_df = pd.json_normalize(data,record_path=["locations"])

        # Flattening the data 
        flat_confirmed = pd.json_normalize(data=data['locations'])
        flat_confirmed.set_index('country', inplace=True)
        print("Download is successful!")
    except:
        
        print("COULD NOT ESTABLISH CONNECTION TO SERVER!!! TRY LATER")
        
    try:   
        
        # Apply function
        final_confirmed = order_dates(flat_confirmed)
        country = "Canada"
        by_prov = final_confirmed[final_confirmed.index==country].set_index("province").T.iloc[:-4,]
        by_prov["TotalDailyCase"] = by_prov.sum(axis=1)
        
        # This variable contains data on COVID 19 daily cases
        non_cumulative_cases = by_prov.diff(axis=0)
        
        t = np.linspace(0, len(non_cumulative_cases["TotalDailyCase"]), len(non_cumulative_cases["TotalDailyCase"]))

    except:
        
        print("COULD NOT ACCESS DF - ENSURE FORMAT IS CORRECT")
        
        
    style = {'description_width': 'initial'}
    
    
    
    # Create interactive menu with parameters
    all_the_widgets1 = [widgets.FloatSlider(
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
    CD_button1 = widgets.Button(
        button_style='success',
        description="Run Simulations", 
        layout=Layout(width='15%', height='30px'),
        style=style
    )    

    # Connect widget to function - run subsequent cells
    CD_button1.on_click( plot_model_and_data )

    # user menu using categories found above
    tab4 = VBox(children=[HBox(children=all_the_widgets[0:3]),HBox(children=all_the_widgets[3:6]),
                          HBox(children=all_the_widgets[6:]),
                          CD_button1])
    tab1 = widgets.Tab(children=[tab4])
    tab1.set_title(0, 'Choose Parameters')
    
    # Let's add a date
    # A grid of time points (in days)
    # Initial number of infected and recovered individuals, I0 and R0.
    


