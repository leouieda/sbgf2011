"""
Example script for doing inverting synthetic data GPlant
"""

import pickle

import pylab
import numpy
from enthought.mayavi import mlab
import matplotlib

import fatiando.grav.io as io
import fatiando.utils as utils
import fatiando.vis as vis

# Get a logger
log = utils.get_logger()

f = open('body.pickle')
corpo = pickle.load(f)
f.close()
f = open('model.pickle')
model = pickle.load(f)
f.close()
f = open("seeds.pickle")
seeds = pickle.load(f)
f.close()
f = open("results.pickle")
results = pickle.load(f)
f.close()

data = io.load('gz.txt')
adjusted = io.load('adjusted.txt')

seed1x, seed1y, seed1z = numpy.loadtxt("seeds1.txt", unpack=True)
seed2x, seed2y, seed2z = numpy.loadtxt("seeds2.txt", unpack=True)

extent = [0,50000,0,100000,-10000,0]
ranges = [0, 50, 0, 100, 10, 0]

contour1x = [model[0]['x1'], model[0]['x2'], model[0]['x2'], model[0]['x1'], model[0]['x1']]
contour1y = [model[0]['y1'], model[0]['y1'], model[0]['y2'], model[0]['y2'], model[0]['y1']]
contour2x = [model[1]['x1'], model[1]['x2'], model[1]['x2'], model[1]['x1'], model[1]['x1']]
contour2y = [model[1]['y1'], model[1]['y1'], model[1]['y2'], model[1]['y2'], model[1]['y1']]

contour1x = 0.001*numpy.array(contour1x)
contour1y = 0.001*numpy.array(contour1y)
contour2x = 0.001*numpy.array(contour2x)
contour2y = 0.001*numpy.array(contour2y)
seed1x = 0.001*seed1x
seed1y = 0.001*seed1y
seed2x = 0.001*seed2x
seed2y = 0.001*seed2y
data['x'] = 0.001*data['x']
data['y'] = 0.001*data['y']
adjusted['x'] = 0.001*adjusted['x']
adjusted['y'] = 0.001*adjusted['y']

matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

# Plot the data
pylab.figure()
pylab.axis('scaled')
vis.contourf(data, levels=15, xkey='y', ykey='x', nx=25, ny=50)
cb = pylab.colorbar()
cb.set_label("mGal")
pylab.plot(contour1y, contour1x, '-k', linewidth=2)
pylab.plot(contour2y, contour2x, '-k', linewidth=2)
size = 4
alpha = 1
pylab.plot(seed1y, seed1x, 'ob', markersize=size, alpha=alpha)
pylab.plot(seed2y, seed2x, 'or', markersize=size, alpha=alpha)
#cb = pylab.colorbar()
#cb.set_label('mGal')
pylab.xlabel("Easting (km)")
pylab.ylabel("Northing (km)")
#pylab.savefig("data_raw.pdf")

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

# Plot the residuals and goal function per iteration
#pylab.figure(figsize=(8,6))
#pylab.suptitle("Inversion results:", fontsize=16)
#pylab.subplots_adjust(hspace=0.4)
#pylab.subplot(2,1,1)
#pylab.title("Residuals")
#vis.residuals_histogram(residuals)
#pylab.xlabel('Eotvos')
#ax = pylab.subplot(2,1,2)
#pylab.title("Goal function and RMS")
#pylab.plot(goals, '.-b', label="Goal Function")
#pylab.plot(misfits, '.-r', label="Misfit")
#pylab.xlabel("Iteration")
#pylab.legend(loc='upper left', prop={'size':9}, shadow=True)
#ax.set_yscale('log')
#ax.grid()
#pylab.savefig('residuals.pdf')

# Plot the ajustment
pylab.figure()
pylab.axis('scaled')
levels = vis.contour(data, levels=5, color='b', label='Data',
                        xkey='y', ykey='x', nx=31, ny=61)
vis.contour(adjusted, levels=levels, color='r', label='Predicted',
                        xkey='y', ykey='x', nx=31, ny=61)
pylab.legend(loc='lower right', prop={'size':9}, shadow=True)
pylab.xlabel("Easting (km)")
pylab.ylabel("Northing (km)")
#pylab.savefig("adjustment_raw.pdf")

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