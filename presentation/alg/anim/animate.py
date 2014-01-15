import cPickle as pickle
import numpy
from enthought.mayavi import mlab
from fatiando import vis, utils
from fatiando.mesh import vfilter

with open("mesh.pickle") as f:
    mesh = pickle.load(f)
with open("data.pickle") as f:
    data = pickle.load(f)['gz']
with open("adj.pickle") as f:
    adj = pickle.load(f)['gz']
with open("model.pickle") as f:
    model = pickle.load(f)
with open("changes.pickle") as f:
    changes = pickle.load(f)
    
estimate = mesh.ravel()
x1, x2 = 0, 5000
y1, y2 = 0, 3000
z1, z2 = 0, 3000
extent = [y1, y2, x1, x2, -z2, -z1]
ranges = [0,3,0,5,3,0]
dshape = (data['ny'], data['nx'])
Y, X, Z = utils.extract_matrices(data)
neighborcolor = (0.1, 0.1, 0.1)

def setden(e,d):
    e['value'] = d
    return e

def setview(scene):    
    scene.scene.camera.position = [-11978.536823271232, -925.93553026480663, 2177.903325392459]
    scene.scene.camera.focal_point = [818.377739158537, 2580.2852687956774, -345.59067831382299]
    scene.scene.camera.view_angle = 30.0
    scene.scene.camera.view_up = [0.18327538439221325, 0.038083300249243945, 0.9823236715655449]
    scene.scene.camera.clipping_range = [8864.9794387069087, 20780.748659615412]
    scene.scene.camera.compute_view_plane_normal()
    scene.scene.render()

def init(changes, ns):
    for chset in changes[0:ns]:
        seed = numpy.array([estimate[chset['new']]])
        pnew = vis.plot_prism_mesh(seed, style='surface', xy2ne=True)
        mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]
         
        neighbors = numpy.array([setden(e, chset['dens']) for e in [estimate[n] for n in chset['nn']]])
        pnn = vis.plot_prism_mesh(neighbors, style='wireframe', xy2ne=True)
        pnn.actor.property.color = neighborcolor
        pnn.actor.property.line_width = 1
    pos = 0
    scale = 800
    Z = numpy.reshape(data['value'] - changes[ns-1]['res'], dshape)
    ct = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
    ct.contour.filled_contours = True
    ct.actor.actor.position = (0,0,pos)
    ct.actor.actor.scale = (1,1,scale)

def update(chset):
    mlab.get_engine().scenes[0].children[-1].remove()
    new = numpy.array([estimate[chset['new']]])
    pnew = vis.plot_prism_mesh(new, style='surface', xy2ne=True)    
    neighbors = numpy.array([setden(e, chset['dens']) for e in [estimate[n] for n in chset['nn']]])
    pnn = vis.plot_prism_mesh(neighbors, style='wireframe', xy2ne=True)
    pnn.actor.property.color = neighborcolor
    pnn.actor.property.line_width = 1
    pos = 0
    scale = 800
    Z = numpy.reshape(data['value'] - chset['res'], dshape)
    ct = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
    ct.contour.filled_contours = True
    ct.actor.actor.position = (0,0,pos)
    ct.actor.actor.scale = (1,1,scale)

def chcolor():    
    mlab.get_engine().scenes[0].children[-3].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]

scene = mlab.figure(size=(700,700))
scene.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(model, style='wireframe', xy2ne=True)
#p.actor.property.color = (0.8,0.8,0.8)
p.actor.actor.visibility = False

#p = vis.plot_prism_mesh(mesh, style='surface', xy2ne=True)
#mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.lut_mode = "Greys"
#mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]

#p = vis.plot_prism_mesh(vfilter(mesh,1,2000), style='surface', xy2ne=True)
#mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,1000]

a = mlab.axes(p, nb_labels=0, extent=extent, ranges=ranges, color=(0,0,0))
a.label_text_property.color = (0,0,0)
a.title_text_property.color = (0,0,0)
a.axes.font_factor = 1.2
a.axes.label_format = ""
a.axes.x_label, a.axes.y_label, a.axes.z_label = "X", "Y", "Z"

mlab.outline(color=(0,0,0), extent=extent)

#pos = 0
#scale = 800
#Z = utils.extract_matrices(adj)[-1]
#p = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
#p.contour.filled_contours = True
#p.actor.actor.position = (0,0,pos)
#p.actor.actor.scale = (1,1,scale)

pos = 1300
field = 'gz'
scale = 800
Z = utils.extract_matrices(data)[-1]
p = mlab.contour_surf(X, Y, Z, contours=10, colormap='jet')
p.contour.filled_contours = True
p.actor.actor.position = (0,0,pos)
p.actor.actor.scale = (1,1,scale)
setview(scene)
mlab.savefig("chset%04d.png" % (0))

ns = 2
init(changes, ns)
setview(scene)
mlab.savefig("chset%04d.png" % (1)) 

for i, chset in enumerate(changes[ns:]):
    update(chset)
    setview(scene)
    mlab.savefig("chset%04d.png" % (i+2))
    chcolor()

mlab.show()
