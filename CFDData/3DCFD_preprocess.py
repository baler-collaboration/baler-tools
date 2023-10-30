# Selects a 3D region of a 3D GASCANS CFD simulation and stores it in a .npz file ready for Baler. 

import numpy as np
import matplotlib.pyplot as plt
import h5py


# Change font size
plt.rcParams.update({'font.size': 8})
   
colours = 'b', 'g', 'orange'
lines = 'solid', 'dotted', 'dashed', 'dashdot'
cm = 'viridis'


#### GASCANS CFD results ####
data_path = 'D:\\run\\Baler_3D_flow\\LB_dx20\\output20210208161121\\'
fname = 'hdf_R0N0.h5'
fname_saved = '3DCFD.npz'
case_name = '3DCFD'
       
time = 37500

   
fsim  = h5py.File(data_path+fname, 'r')

YPos = fsim['Time_0/YPos']
XPos = fsim['Time_0/XPos']
ZPos = fsim['Time_0/ZPos']

cells_x = len(XPos[0,0,:])
cells_y = len(YPos[:,0,0])
cells_z = len(ZPos[:,0,0])

# Limits of the region to extract
x0 = 40
y0 = 1
z0 = 50
xf = 180
yf = 40
zf = 110

tiled_data = np.zeros([zf-z0, yf-y0, xf-x0])

# Note: change Ux, for Uy or Uz to extract the y and z components of the velocity vector.
time_h5 = 'Time_' + str(time)
Ux = fsim[time_h5 + '/Ux'] 
tiled_data[:,:,:] = Ux[z0:zf, y0:yf, x0:xf]


# Save to Numpy
np.savez(data_path+fname_saved, data=tiled_data, names=[])

# Show a slice of the date
fig = plt.figure(1, figsize=(10,5))
cs = plt.contourf(tiled_data[:,int((yf-y0)/2),:], cmap=cm, levels=50)
plt.colorbar(cs, orientation = 'horizontal')
plt.gca().set_aspect('equal')
plt.xlabel('x [cells]')
plt.ylabel('z [cells]')
plt.savefig(case_name+'horizontal.png', bbox_inches='tight')


fig = plt.figure(2, figsize=(10,5))
cs = plt.contourf(tiled_data[int((zf-z0)/2),:,:], cmap=cm, levels=50)
plt.colorbar(cs, orientation = 'horizontal')
plt.gca().set_aspect('equal')
plt.xlabel('x [cells]')
plt.ylabel('y [cells]')
plt.savefig(case_name+'vertical.png', bbox_inches='tight')
 
plt.show()



