# Selects time steps of a slice in a 3D GASCANS CFD simulation and stores them in a .npz file ready for Baler. 
# Short explanation on GASCANS format: 
# Ux, Uy, Uz are the three components of the flow velocity.
# Each component is stored in a 3D matrix, with one value for each cell of the mesh. 
# The order of the coordinates in the 3D matrix is z, y, x. For example: Ux[z,y,x]

import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.animation import FuncAnimation

def getIndex( cf, ci, d ):
   "Converts the dimensionless coordinates to cell indices"
   index = int((cf - ci)/d + 0.5)
   return index;
   
def animate(t):
    cs = plt.contourf(tiled_data[t,:,:], cmap=cm, levels=50)
    #plt.colorbar(cs, orientation = 'horizontal')
    #plt.gca().set_aspect('equal') 

# Change font size
plt.rcParams.update({'font.size': 8})
   
colours = 'b', 'g', 'orange'
lines = 'solid', 'dotted', 'dashed', 'dashdot'
cm = 'magma_r'


#### GASCANS CFD results ####
data_path = './/'
fname = 'hdf_R0N0_fine.h5'
fname_saved = 'CFDAnimation_fine.npz'

# Time step at which to start extracting the data       
start_time = 500

# Number of time steps in between extracted slices
time_step = 500

# Number of extracted slices
num_steps = 60 

# Z value of the selected slice. 
z_s = 1


   
fsim  = h5py.File(data_path+fname, 'r')

YPos = fsim['Time_0/YPos']
XPos = fsim['Time_0/XPos']

cells_x = len(XPos[0,0,:])
cells_y = len(YPos[0,:,0])

if cells_x != cells_y:
    raise Exception("Simulation domain needs to be a square. Cells_x = " + str(cells_x) + " Cells_y = " + str(cells_y)) 

tiled_data = np.zeros([num_steps, cells_x, cells_x])

for t in range(0, num_steps):

    time = 'Time_' + str(start_time + t*time_step)
    print(time)
    Ux = fsim[time + '/Ux']
    Uy = fsim[time + '/Uy']
        
    # To extract Ux
    tiled_data[t,:,:] = Ux[z_s,:,:]
    # To extract Uy
    # tiled_data[t,:,:] = Uy[z_s,:,:]

# Save to Numpy
np.savez(data_path+fname_saved, data=tiled_data, names=[])
 
# Show animation 
fig, ax = plt.subplots()
ani = FuncAnimation(fig, animate, frames=num_steps, interval=50, repeat=False)
ani.save('CFDAnimation_fine.gif', writer='imagemagick', fps=20)
plt.show()



