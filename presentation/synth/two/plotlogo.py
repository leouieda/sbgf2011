import cPickle as pickle
import numpy
from enthought.mayavi import mlab
from fatiando import vis, utils
from fatiando.mesh import vfilter

with open("data.pickle") as f:
    data = pickle.load(f)['gz']
with open("model.pickle") as f:
    model = pickle.load(f)

x1, x2 = 0, 5000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [y1, y2, x1, x2, -z2, -z1]
ranges = [0,3,0,5,3,0]

scene = mlab.figure(size=(1000,700))
scene.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(model, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]


a = mlab.axes(p, nb_labels=3, extent=extent, ranges=ranges, color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.font_factor = 1.2
a.axes.label_format = "%.1f"
a.axes.x_label, a.axes.y_label, a.axes.z_label = "E (km)", "N (km)", "Z (km)"

mlab.outline(color=(0,0,0), extent=extent)

pos = 0
scale = 1
Y, X, Z = utils.extract_matrices(data)
p = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
p.contour.filled_contours = True
p.actor.actor.position = (0,0,pos)
p.actor.actor.scale = (1,1,scale)

mlab.show()
