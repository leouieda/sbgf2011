import cPickle as pickle
from enthought.mayavi import mlab
from fatiando import mesh, vis, utils

with open("mesh.pickle") as f:
    res = pickle.load(f)
with open("data.pickle") as f:
    data = pickle.load(f)

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

pos = 1000
field = 'gz'
scale = 200
Y, X, Z = utils.extract_matrices(data[field])
p = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
p.contour.filled_contours = True
p.actor.actor.position = (0,0,pos)
p.actor.actor.scale = (1,1,scale)

a = mlab.axes(p, nb_labels=0, extent=[0,3000,0,3000,pos,pos + scale*Z.max()], color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.label_format = ""
a.axes.x_label, a.axes.y_label, a.axes.z_label = "", "", ""
a.property.line_width = 1

scene = fig
scene.scene.camera.position = [5845.7904104772751, 10826.008452051316, 3697.0607477775502]
scene.scene.camera.focal_point = [1317.7924322687745, 1352.1830042500999, -1036.6534494994289]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.18123807301145317, -0.36888651509323656, 0.91163342406554104]
scene.scene.camera.clipping_range = [5326.0395401897185, 18409.2672096317]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()

mlab.show()
