# Create a mock array of tuples
# generate an OpenSCAD file from that data.
# 
# Robert Carlsen | @robertcarlsen

from random import *

# this is from the SolidPython lib
from solid import *

# working on some processing
import numpy
import scipy
from scipy import spatial

# make some fake:
mock_stars = []
for i in range(0, 20, 1):
    this_star = []
    for c in range(3):
        this_star.append(random())
    mock_stars.append(this_star)

#print mock_stars


# have data...now model the scad.
model_data = []

# the mock data is normalized...let's make this bigger
# this is just the coordinate scale at the moment
# lets presume this is mm.
scale = 100

star_base_radius = 3.0
column_radius = [2.0, 1.0]

# this is the naive 'ball and stick' representation:
"""
for i, coord in enumerate(mock_stars):
    #print coord
    scaled_coord = [x*scale for x in coord]

    # testing
    star_rand_scale = uniform(0.5, 1.25)

    s = translate(scaled_coord)(
              sphere(star_rand_scale * star_base_radius),
              translate([0,0,-scaled_coord[2]])(
                  cylinder(r1=column_radius[0], r2=column_radius[1], h=scaled_coord[2])
                  )
            )
    model_data.append(s)

# combine all model_data and add a base plate, 
u = translate([-scale/2, -scale/2, 0])(model_data,cube([scale, scale, 2]))
"""

# trying a more sophisticated model
neighbors_list = []
# play with the leafsize here
star_tree = scipy.spatial.cKDTree(mock_stars,leafsize=100)
for star in mock_stars:
    # need to twiddle these dials
    neighbors = star_tree.query(star,k=2,distance_upper_bound=20)
    # print neighbors
    
    scaled_coord = [x*scale for x in mock_stars[neighbors[1][0]]]
    # make a column between the current
    neighbors_list.append(
            # getting our location, and the distance as the sphere
            translate(scaled_coord)(sphere(scale*neighbors[0][1]))
            )
model_data = neighbors_list

# no need for a base plate here (but may need support)
u = translate([-scale/2, -scale/2, 0])(model_data)

scad = scad_render(u)
#print scad

# want to modify the resulting scad file:
scad = "$fn=20;\n"+scad

f = open('output.scad', 'w')
f.write(scad)
f.close()

# writing directly to a file:
#scad_render_to_file(u, 'output.scad')

"""
# and now for something completely different:
# try the .xyz format
# item count
# comment
# name x y z
xyz = str(len(mock_stars)) + "\n"
xyz += "this is a test xyz format file with mock data\n"

for star in range(0, len(mock_stars)-1):
    xyz += "H " + " ".join("%10.5f" % x for x in (x*scale for x in mock_stars[star])) + "\n"

ff = open('output.xyz', 'w')
ff.write(xyz)
ff.close()
"""

