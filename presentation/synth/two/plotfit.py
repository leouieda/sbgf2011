import cPickle as pickle
import numpy
import pylab
from fatiando import vis, utils
from fatiando.mesh import vfilter

with open("data.pickle") as f:
    data = pickle.load(f)['gz']
with open("adj.pickle") as f:
    adj = pickle.load(f)['gz']

def xy2ne(g):
    g['x'], g['y'] = g['y'], g['x']
    return g

xy2ne(data)
xy2ne(adj)
    
pylab.figure()
pylab.axis('scaled')
levels = vis.contour(data, levels=8, color='b', label="Observed")
vis.contour(adj, levels=levels, color='r', label="Predicted")
pylab.xlabel("E (km)")
pylab.ylabel("N (km)")

pylab.figure()
pylab.axis('scaled')
levels = vis.contourf(data, levels=8)
vis.contour(data, levels=levels, color='k')
pylab.xlabel("E (km)")
pylab.ylabel("N (km)")

pylab.figure()
pylab.axis('scaled')
levels = vis.contourf(adj, levels=8)
vis.contour(adj, levels=levels, color='k')
pylab.xlabel("E (km)")
pylab.ylabel("N (km)")

pylab.show()
