
"""
Modified from:

Animation of Elastic collisions with Gravity

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!

Modified by: Bryce Haley, Laura Gutierrez Funderburk
2020
"""
import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import scipy.integrate as integrate
import matplotlib.animation as animation
from IPython.display import HTML
import pandas as pd

import scripts


perimeter_raw = get_perimeter(1, 0.08, 0, 0.24, 0.0068)


class ParticleBox:
    """Orbits class
    
    init_state is an [N x 4] array, where N is the number of free_fish:
       [[x1, y1, vx1, vy1],
        [x2, y2, vx2, vy2],
        ...               ]

    bounds is the size of the box: [xmin, xmax, ymin, ymax]
    """
    def __init__(self,
                 init_state = [[1, 0, 0, -1],
                               [-0.5, 0.5, 0.5, 0.5],
                               [-0.5, -0.5, -0.5, 0.5]],
                 init_tide_state = [[-2,2],[-1, -1]],
                 init_perimeter = [perimeter_raw[0], (perimeter_raw[1] * -1)],
                 bounds = [-2, 2, -2, 2],
                 size = 0.04,
                 M = 0.05,
                 tide_movement_up = True,
                 end = False,
                 frozen_iter = 0):
        self.init_state = np.asarray(init_state, dtype=float)
        self.init_tide_state = np.asarray(init_tide_state, dtype=float)
        self.init_perimeter = np.asarray(init_perimeter, dtype=float)
        self.M = M * np.ones(self.init_state.shape[0])
        self.size = size
        self.state = self.init_state.copy()
        self.tide_state = self.init_tide_state.copy()
        self.perimeter = self.init_perimeter.copy()
        self.time_elapsed = 0
        self.bounds = bounds
        self.tide_movement_up = tide_movement_up
        self.end = end
        self.frozen_iter = frozen_iter
        

    def step(self, dt):
        """step once by dt seconds"""
        if self.time_elapsed==0:
            self.bounds[3] = -1
        
        self.time_elapsed += dt
        if not self.end:
            # update positions
            self.state[:, :2] += dt * self.state[:, 2:]
        
            #check for fish hitting the trap
            dist_arr = cdist(self.state[:,:2], np.array(list(zip(self.perimeter[0], self.perimeter[1]))))
            hit_trap = (dist_arr.min(axis=1) < self.size)
            for i in range(0, len(dist_arr)):
                if(self.perimeter[1,i]<self.bounds[3] - 1):
                    hit_trap[i] = False
            self.state[hit_trap, 2:] *= -1
        
        
            # check for crossing boundary
            crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
            crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
            crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
            crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

            self.state[crossed_x1, 0] = self.bounds[1] - self.size
            self.state[crossed_x2, 0] = self.bounds[0] + self.size

            self.state[crossed_y1, 1] = self.bounds[2] + self.size
            self.state[crossed_y2, 1] = self.bounds[3] - self.size

            #self.state[crossed_x1 | crossed_x2, 2] *= -1
            self.state[crossed_y1 | crossed_y2, 3] *= -1
            self.state[crossed_y1, 0] *= -1
        
            #moving boundary to show tidal movement
            if self.tide_movement_up:
                self.bounds[3] = self.bounds[3] + (1/300)
                self.tide_state[1,:] = self.bounds[3]
                if self.bounds[3] >= 2:
                    self.tide_movement_up = False
            else:
                if(self.bounds[3] > 0):
                    self.bounds[3] = self.bounds[3] - (1/300)
                    self.tide_state[1,:] = self.bounds[3]
                else:
                    self.end = True
        else:
            self.frozen_iter += 1
        
def init():
    """initialize animation"""
    global box, rect
    free_fish.set_data([], [])
    tide.set_data([], [])
    #perimeter.set_data([],[])
    rect.set_edgecolor('none')
    trapped_fish.set_data([], [])
    return free_fish, tide, rect, trapped_fish

def animate(i):
    """perform animation step"""
    global box, rect, dt, ax, fig
    box.step(dt)

    ms = int(fig.dpi * 2 * box.size * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    
    # update high tide line
    tide.set_data(box.tide_state)
    
    # update the trap showing above water
    # perimiter referes to the perimeter of the trap
    perimeter_arr = box.perimeter.copy()
    mask  = perimeter_arr[1] >= box.bounds[3] - 1

    perimeter_arr = np.array([perimeter_arr[0][mask], perimeter_arr[1][mask]])

    perimeter_arr = np.array([np.array_split(perimeter_arr[0], 2), np.array_split(perimeter_arr[1], 2)])
    
    left_perimeter = perimeter_arr[:,0]
    right_perimeter = perimeter_arr[:,1]

    perimeter_right.set_data(right_perimeter)
    perimeter_left.set_data(left_perimeter)
    
    #update the fishs
    x = box.state[:, 0]
    y = box.state[:, 1]
    
    df = pd.DataFrame({'x':x, 'y':y})
    in_df = df[df[['x', 'y']].apply(lambda row : row['x']**2 + row['y']** 2 <= 1 and row['y'] <= 0, axis=1)]
    out_df = df[df[['x','y']].apply(lambda row : row['x']**2 + row['y']**2 > 1 or row['y'] > 0, axis=1)]

    free_fish.set_data(np.array(out_df.x), np.array(out_df.y))
    free_fish.set_markersize(ms)
    
    #let animation freeze after trap is closed
    if box.frozen_iter < 99:
        trapped_fish.set_data(np.array(in_df.x), np.array(in_df.y))
    # remove caught fish from the trap
    else:
        trapped_fish.set_data([],[])
    trapped_fish.set_markersize(ms)
    
    #update patches (beach and water)
    beach.set_bounds(-2, box.bounds[3], 4, 2-box.bounds[3])
    water.set_bounds(-2, -2, 4, 2+box.bounds[3])

    return free_fish, tide, rect, trapped_fish, perimeter_left, perimeter_right, beach, water

if __name__ == "__main__":

    #------------------------------------------------------------
    # set up initial state
    np.random.seed(0)
    init_state = -0.5 + np.random.random((50, 4))
    init_state[:, 0] *= 3.9
    init_state[:, 1] *= 0.3
    init_state[:, 1] -= 1.6

    box = ParticleBox(init_state, size=0.04)
    dt = 1. / 30 # 30fps

    #------------------------------------------------------------
    # set up figure and animation
    fig = plt.figure()
    fig.suptitle('Aerial View - Animation of Trap', fontsize=16)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))
    ax.axis('off')

    # free_fish holds the locations of the fish 'particle' not trapped
    free_fish, = ax.plot([], [], 'o', color='salmon', ms=6, label='free fish')

    trapped_fish, = ax.plot([], [], 'o', color='black', ms=6, label='captured fish')

    # tide holds the tide level for each timestep
    tide, = ax.plot([], [], '-', color='white', ms=2)

    # perimeter holds the trap
    perimeter_right, = ax.plot([],[], '-', color='dimgrey', ms=2, label='trap above water')
    perimeter_left, = ax.plot([],[], '-', color='dimgrey', ms=2)
   
    handles, labels = ax.get_legend_handles_labels()

    beach_patch = Patch(facecolor='yellow', label='sand')
    water_patch = Patch(facecolor='blue', label='water')

    handles.append(beach_patch)
    handles.append(water_patch)
    
    plt.legend(handles=handles, loc='lower right', framealpha=1)
    
    # rect is the box edge
    rect = plt.Rectangle(box.bounds[::2],
                         box.bounds[1] - box.bounds[0],
                         box.bounds[3] - box.bounds[2],
                         ec='none', lw=2, fc='none')
    
    beach = plt.Rectangle( (-2, -1), 4, 3, color='yellow', alpha=0.2)
    water = plt.Rectangle( (-2, -2), 4, 1, color='blue', alpha=0.2)
    ax.add_patch(rect)
    ax.add_patch(beach)
    ax.add_patch(water)





    # plt.rcParams["animation.html"] = "jshtml"

    ani = animation.FuncAnimation(fig, animate, frames=1700,
                                  interval=10, blit=True, init_func=init)

    plt.close()


    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    HTML(ani.to_html5_video())
