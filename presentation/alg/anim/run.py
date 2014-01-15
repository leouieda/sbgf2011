import cPickle as pickle
import pylab
import numpy
from enthought.mayavi import mlab

import fatiando.inv.gplant as gplant
import fatiando.grav.synthetic as synthetic
import fatiando.mesh
import fatiando.utils as utils
import fatiando.vis as vis

log = utils.get_logger()
utils.set_logfile('run.log')
log.info(utils.header())

# GENERATE SYNTHETIC DATA
################################################################################
# Make the prism model
model = []
model.append({'x1':600, 'x2':1600, 'y1':1000, 'y2':2000, 'z1':800, 'z2':1800,
               'value':500})
model.append({'x1':3400, 'x2':4400, 'y1':1000, 'y2':2000, 'z1':1600, 'z2':2600,
               'value':1000})
model = numpy.array(model)
with open("model.pickle", 'w') as f:
    pickle.dump(model, f)

x1, x2 = 0, 5000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [x1, x2, y1, y2, -z2, -z1]

# Now calculate all the components of the gradient tensor and contaminate the
# data with gaussian noise
error = 0.05
fields = ['gz']
data = {}
for i, field in enumerate(fields):
    data[field] = synthetic.from_prisms(model, x1=0, x2=5000, y1=0, y2=3000,
                                        nx=25, ny=15, height=1, field=field)
    data[field]['value'] = utils.contaminate(data[field]['value'],
                                                    stddev=error,
                                                    percent=False)
    data[field]['error'] = error*numpy.ones(len(data[field]['value']))

#field = 'gz'
#pylab.figure()
#pylab.axis('scaled')
#vis.contourf(data[field], levels=10)
#pylab.show()

with open("data.pickle", 'w') as f:
    pickle.dump(data, f)

# PERFORM THE INVERSION
################################################################################
#~ # Generate a prism mesh
mesh = fatiando.mesh.prism_mesh(x1=x1, x2=x2, y1=y1, y2=y2, z1=z1, z2=z2,
                                nx=25, ny=15, nz=15)
 
# Set the seeds and save them for later use
log.info("Setting seeds in mesh:")
seeds = []
seeds.append(gplant.get_seed((1100, 1500, 1300), 500, mesh))
seeds.append(gplant.get_seed((3900, 1500, 2100), 1000, mesh))

# Make a mesh for the seeds to plot them
seed_mesh = numpy.array([seed['cell'] for seed in seeds])

#fig = mlab.figure()
#fig.scene.background = (1, 1, 1)
#p = vis.plot_prism_mesh(seed_mesh, style='surface')
#p = vis.plot_prism_mesh(model, style='wireframe')
#mlab.show()
 
# Run the inversion
results = gplant.grow(data, mesh, seeds, compactness=10**(4), power=3,
                      threshold=10**(-3), norm=2, neighbor_type='reduced',
                      jacobian_file=None, distance_type='radial')

# Unpack the results and calculate the adjusted data
estimate, residuals, misfits, goals, changes = results
fatiando.mesh.fill(estimate, mesh)
adjusted = gplant.adjustment(data, residuals)
with open("changes.pickle", 'w') as f:
    pickle.dump(changes, f)
with open("adj.pickle", 'w') as f:
    pickle.dump(adjusted, f)
with open('mesh.pickle', 'w') as f:
    pickle.dump(mesh, f)
with open("seeds.pickle", 'w') as f:
    pickle.dump(seed_mesh, f)

# PLOT THE INVERSION RESULTS
################################################################################
log.info("Plotting")

field = 'gz'
pylab.figure()
pylab.axis('scaled')
levels = vis.contour(data[field], levels=8, color='b')
vis.contour(adjusted[field], levels=levels, color='r')
pylab.show()

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure()
fig.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(seed_mesh, style='surface')
p = vis.plot_prism_mesh(model, style='wireframe')
p = vis.plot_prism_mesh(fatiando.mesh.vfilter(mesh,1,2000), style='surface', opacity=0.4)

a = mlab.axes(p, nb_labels=0, extent=extent, color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.label_format = ""
a.axes.x_label, a.axes.y_label, a.axes.z_label = "", "", ""
a.property.line_width = 1
    
mlab.show()
