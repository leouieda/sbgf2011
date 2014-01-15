import cPickle as pickle
import numpy
from enthought.mayavi import mlab
from fatiando import vis, utils
from fatiando.mesh import vfilter

with open("mesh.pickle") as f:
    mesh = pickle.load(f)
with open("model.pickle") as f:
    model = pickle.load(f)
with open("seeds.pickle") as f:
    seeds = pickle.load(f)

def setview(scene):    
    scene.scene.camera.position = [-6731.6617523492614, -741.06724943117445, 2538.740101856331]
    scene.scene.camera.focal_point = [1418.1486135568678, 3057.6315582939146, -2067.7535690252648]
    scene.scene.camera.view_angle = 30.0
    scene.scene.camera.view_up = [0.42170409069839254, 0.17430913833059022, 0.88982132149251703]
    scene.scene.camera.clipping_range = [3963.8607698693286, 16944.971724745214]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()
    
x1, x2 = 0, 5000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [y1, y2, x1, x2, -z2, -z1]
ranges = [0,3,0,5,3,0]

scene = mlab.figure(size=(1000,700))
scene.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(model, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]

p = vis.plot_prism_mesh(mesh, style='surface', xy2ne=True)

p = vis.plot_prism_mesh(seeds, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]

a = mlab.axes(p, nb_labels=3, extent=extent, ranges=ranges, color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.font_factor = 1.2
a.axes.label_format = "%.1f"
a.axes.x_label, a.axes.y_label, a.axes.z_label = "E (km)", "N (km)", "Depth (km)"

mlab.outline(color=(0,0,0), extent=extent)

setview(scene)

mlab.show()
