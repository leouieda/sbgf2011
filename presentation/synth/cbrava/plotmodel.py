import cPickle as pickle
try:
    from enthought.mayavi import mlab
except:
    from mayavi import mlab

from fatiando import vis, mesh

with open("model.pickle") as f:
    model = pickle.load(f)

extent = [0,50000,0,100000,-10000,0]
ranges = [0, 50, 0, 100, 10, 0]

scene = mlab.figure()
scene.scene.background = (1, 1, 1)

p = vis.plot_prism_mesh(model, style='surface', xy2ne=True)
mlab.get_engine().scenes[0].children[-1].children[0].children[0].children[0].scalar_lut_manager.data_range = [0,400]

axes = mlab.axes(p, nb_labels=5, extent=extent, ranges=ranges, color=(0,0,0))
axes.label_text_property.color = (0,0,0)
axes.title_text_property.color = (0,0,0)
axes.axes.label_format = "%-#.1f"
mlab.outline(color=(0,0,0), extent=extent)
mlab.show()
