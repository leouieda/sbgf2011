import cPickle as pickle
from enthought.mayavi import mlab
from fatiando import mesh, vis, utils

with open("data.pickle") as f:
    data = pickle.load(f)

fig = mlab.figure(size=(600,730))
fig.scene.background = (1, 1, 1)

pos = 0
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


mlab.show()
