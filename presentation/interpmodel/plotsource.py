import cPickle as pickle
from enthought.mayavi import mlab
from fatiando import mesh, vis, utils

with open("mesh.pickle") as f:
    res = pickle.load(f)

x1, x2 = 0, 3000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [x1, x2, y1, y2, -z2, -z1]

# Plot the adjusted model plus the skeleton of the synthetic model
fig = mlab.figure(size=(600,730))
fig.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(mesh.vfilter(res,900,2001), style='surface', opacity=1)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,2000]

#a = mlab.axes(p, nb_labels=0, extent=extent, color=(0,0,0))
#a.label_text_property.color = (0,0,0)
#a.title_text_property.color = (0,0,0)
#a.axes.label_format = ""
#a.axes.x_label, a.axes.y_label, a.axes.z_label = "", "", ""
#a.property.line_width = 1

mlab.outline(p, extent=extent, color=(0,0,0))

scene = fig
scene.scene.camera.position = [5617.6246210610589, 9378.6744914189112, 1832.0425527256102]
scene.scene.camera.focal_point = [1435.8921050117997, 1598.1461572098237, -1715.9026272606379]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.18883236854009863, -0.3216128720649955, 0.92785101019163696]
scene.scene.camera.clipping_range = [4531.9434654515926, 15755.396726380868]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()

mlab.show()
