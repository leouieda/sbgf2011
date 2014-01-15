"""
Example script for doing inverting synthetic data GPlant
"""

import pickle
import logging

import pylab
import numpy
from enthought.mayavi import mlab

import fatiando.inv.gplant as gplant
import fatiando.grav.io as io
import fatiando.grav.synthetic as synthetic
import fatiando.mesh
import fatiando.utils as utils
import fatiando.vis as vis

# Get a logger
#log = utils.get_logger(logging.WARNING)
log = utils.get_logger()
# Set logging to a file
utils.set_logfile('synthetic.log')
# Log a header with the current version info
log.info(utils.header())

# GENERATE SYNTHETIC DATA
################################################################################
# Make the prism model
model = []
model.append({'x1':15000, 'x2':85000, 'y1':15000, 'y2':35000, 'z1':0, 'z2':8000,
              'value':300})
model.append({'x1':25000, 'x2':55000, 'y1':35000, 'y2':42000, 'z1':0, 'z2':6000,
              'value':400})
model = numpy.array(model)

extent = [0,50000,0,100000,-10000,0]
ranges = [0, 50, 0, 100, 10, 0]

# Show the model before calculating to make sure it's right
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
plot = vis.plot_prism_mesh(model, style='surface', xy2ne=True)
axes = mlab.axes(plot, nb_labels=5, extent=extent, ranges=ranges, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.0f"
mlab.outline(color=(0,0,0), extent=extent)
mlab.show()

# Now calculate all the components of the gradient tensor
error = 0.5
data = {}
data['gz'] = synthetic.from_prisms(model, x1=0, x2=extent[3], y1=0, y2=extent[1],
                                   nx=50, ny=25, height=0, field='gz')
data['gz']['value'], error = utils.contaminate(data['gz']['value'],
                                               stddev=error,
                                               percent=False,
                                               return_stddev=True)
data['gz']['error'] = error*numpy.ones(len(data['gz']['value']))
io.dump('gz.txt', data['gz'])

# Plot the data
pylab.figure()
pylab.axis('scaled')
vis.contour(data['gz'], 8, xkey='y', ykey='x', nx=31, ny=61)
#cb = pylab.colorbar()
#cb.set_label('mGal')
pylab.xlabel("Easting (m)")
pylab.ylabel("Northing (m)")
pylab.savefig("data_raw.pdf")
pylab.show()

# RUN THE INVERSION
################################################################################
# Generate a model space mesh
x1, x2 = extent[2], extent[3]
y1, y2 = extent[0], extent[1]
z1, z2 = extent[5]+0.1, -1*extent[4]
mesh = fatiando.mesh.prism_mesh(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2, 
                                nx=100, ny=50, nz=10)

# Set the seeds and save them for later use
log.info("Getting seeds from mesh:")
spoints1 = []
sdens1 = []
dx, dy = 5000, 3000
for x in numpy.arange(15000 + dx, 85000, dx):
    for y in numpy.arange(15000 + dy, 35000, dy):
        spoints1.append((x, y, 500))
        sdens1.append(300)
        
pylab.savetxt("seeds1.txt", numpy.array(spoints1))

spoints2 = []
sdens2 = []
dx = 3000
for x in numpy.arange(25000 + dx, 55000, dx):
    spoints2.append((x, 39500, 500))
    sdens2.append(400)

pylab.savetxt("seeds2.txt", numpy.array(spoints2))

spoints = []
spoints.extend(spoints1)
spoints.extend(spoints2)
sdens = []
sdens.extend(sdens1)
sdens.extend(sdens2)
seeds = [gplant.get_seed(p, dens, mesh) for p, dens in zip(spoints, sdens)]

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

# Show the seeds first to confirm that they are right
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(model, style='wireframe', xy2ne=True)
plot = vis.plot_prism_mesh(seed_mesh, style='surface', xy2ne=True)
axes = mlab.axes(plot, nb_labels=5, extent=extent, ranges=ranges, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.0f"
mlab.outline(color=(0,0,0), extent=extent)
mlab.show()

# Run the inversion
results = gplant.grow(data, mesh, seeds, compactness=10.**(5), power=3,
                      threshold=10*10**(-7), norm=2, neighbor_type='reduced',
                      jacobian_file=None, distance_type='cell')

# Unpack the results and calculate the adjustment
estimate, residuals, misfits, goals = results
adjusted = gplant.adjustment(data, residuals)
fatiando.mesh.fill(estimate, mesh)
corpo = fatiando.mesh.vfilter(mesh, 1, 1000)

# Pickle results for later
log.info("Pickling results")
io.dump('adjusted.txt', adjusted['gz'])
#output = open('mesh.pickle', 'w')
#pickle.dump(mesh, output)
#output.close()
output = open('model.pickle', 'w')
pickle.dump(model, output)
output.close()
output = open('body.pickle', 'w')
pickle.dump(corpo, output)
output.close()
seed_file = open("seeds.pickle", 'w')
pickle.dump(seeds, seed_file)
seed_file.close()
res_file = open("results.pickle", 'w')
pickle.dump(results, res_file)
res_file.close()

# PLOT THE RESULTS
################################################################################
log.info("Plotting")

# Plot the residuals and goal function per iteration
pylab.figure(figsize=(8,6))
pylab.suptitle("Inversion results:", fontsize=16)
pylab.subplots_adjust(hspace=0.4)
pylab.subplot(2,1,1)
pylab.title("Residuals")
vis.residuals_histogram(residuals)
pylab.xlabel('Eotvos')
ax = pylab.subplot(2,1,2)
pylab.title("Goal function and RMS")
pylab.plot(goals, '.-b', label="Goal Function")
pylab.plot(misfits, '.-r', label="Misfit")
pylab.xlabel("Iteration")
pylab.legend(loc='upper left', prop={'size':9}, shadow=True)
ax.set_yscale('log')
ax.grid()
pylab.savefig('residuals.pdf')

# Plot the ajustment
pylab.figure()
pylab.axis('scaled')
levels = vis.contour(data['gz'], levels=5, color='b', label='Data',
                        xkey='y', ykey='x', nx=31, ny=31)
vis.contour(adjusted['gz'], levels=levels, color='r', label='Predicted',
                        xkey='y', ykey='x', nx=31, ny=31)
pylab.legend(loc='lower right', prop={'size':9}, shadow=True)
pylab.xlabel("Easting (m)")
pylab.ylabel("Northing (m)")
pylab.savefig("adjustment_raw.pdf")

pylab.show()

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)
vis.plot_prism_mesh(model, style='wireframe', xy2ne=True)
vis.plot_prism_mesh(seed_mesh, style='surface', xy2ne=True)
plot = vis.plot_prism_mesh(corpo, style='surface', xy2ne=True)
axes = mlab.axes(plot, nb_labels=5, extent=extent, ranges=ranges, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.0f"
mlab.outline(color=(0,0,0), extent=extent)

mlab.show()