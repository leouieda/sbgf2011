import cPickle as pickle
import numpy
from enthought.mayavi import mlab
from fatiando import vis, utils
from fatiando.mesh import vfilter

with open("body.pickle") as f:
    body = pickle.load(f)
with open("seeds.pickle") as f:
    seeds = numpy.array([seed['cell'] for seed in pickle.load(f)])

def setview(scene):
    pass
    
x1, x2 = -1530000, -1410000
y1, y2 = -5390000, -5340000
z1, z2 = -1000, 10000.
extent = [y1, y2, x1, x2, -z2, -z1]
ranges = [0,50,0,120,10,-1]

scene = mlab.figure(size=(1000,700))
scene.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(body, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,390]

p = vis.plot_prism_mesh(seeds, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,390]

a = mlab.axes(p, nb_labels=5, extent=extent, ranges=ranges, color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.font_factor = 1
a.axes.label_format = "%.1f"
a.axes.x_label, a.axes.y_label, a.axes.z_label = "E (km)", "N (km)", "Z (km)"

mlab.outline(color=(0,0,0), extent=extent)

setview(scene)

mlab.show()
