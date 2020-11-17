def split_list(lst):
    even_list = lst[::2]
    odd_list = lst[1::2]
            
    return {'odds': odd_list, 'evens': even_list}

class Fishtrap:
    """Fishtrap object will hold the model, variables and produce plots showing the population dynamics of our salmon."""
    def __init__(self, r=1.36,  b=0.00136, c=0.8, N1=700, N2=300):
        self.r = r
        self.b = b
        self.c = c
        self.N = [N1, N2]
        self.t = 2
        self.harvest_available = 0


    def run_step(self, N=None):
        """Run the model to produce the next years population abundance."""
        if N is None:
            N = self.N
        t = len(N)
        r = self.r
        c = self.c
        b = self.b
        
        return N[t-2] * math.exp(r - (b * N[t-2]) - (c * b * N[t-1]))
        
    def display(self):
        """Show the next year's abundance"""
        before_harvesting = self.run_step()
        self.harvest_available = math.floor(before_harvesting)
        
        print('year: ', self.t+1, 'num fish: ', math.floor(before_harvesting))
        
    def harvesting(self, harvest):
        """Run the model for one year and harvest fish set by Harvest"""
        if(isinstance(harvest, int)):
            if(harvest >= 0 and harvest <= self.harvest_available):
                self.N.append(math.floor(self.harvest_available - harvest))
                self.t += 1
                self.harvest_available = 0 
            elif(harvest >= 0):
                #if harvesting more than the available - kill the population
                self.N.append(0)
                self.t +=1
                self.harvest_available=0
            else:
                raise ValueError("harvest must be a positive number.")
        else:
            raise ValueError("harvest must be a valid integer. Try Again.")
            
    def make_figure(self, N):
        """Produce a simple line plot"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=N['odds'], x=np.linspace(1, 11, 6)))
        fig.add_trace(go.Scatter(y=N['evens'], x=np.linspace(2, 12, 6)))
        return fig
    
    def project_pop(self):
        """Project population without mutating the model's state (no harvesting)."""
        M = self.N[0:2]
        for x in range(10):
            M.append(self.run_step(M))
        split_N = split_list(M)

        return self.make_figure(split_N)
    
    def model_with_quota(self, quota):
        """Run the model for 10 years with a set quota"""
        for x in range(10):
            self.harvest_available = self.run_step()
            self.harvesting(quota)
        split_N = split_list(self.N)
        return self.make_figure(split_N)
    
    def reset(self):
        """return instance to default state"""
        self.N = self.N[0:2]
        self.t = 2
        self.harvest_available = 0
