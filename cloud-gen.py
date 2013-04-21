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
def mock_data():
    mock_stars = []
    for i in range(0, 20, 1):
        this_star = []
        for c in range(3):
            this_star.append(random())
        mock_stars.append(this_star)
    return mock_stars

#print mock_stars

# read CSV file
# real data!
import csv 

ifile  = open('sun_nearest_k_neighbors.csv', "rb")
reader = csv.reader(ifile)

sun_data = []

rownum = 0
for row in reader:
    # Save header row:
    this_row_coords = [0,0,0]
    if rownum == 0:
        header = row
    else:
        colnum = 0
        for col in row:
            #print '%-8s: %s' % (header[colnum], col)

            if header[colnum] == "X":
                this_row_coords[0] = float(col) 

            if header[colnum] == "Y":
                this_row_coords[1] = float(col) 
            
            if header[colnum] == "Z":
                this_row_coords[2] = float(col) 

            colnum += 1
             
    sun_data.append(this_row_coords)
    rownum += 1
 
ifile.close()


# have data...now model the scad.
model_data = []

# the mock data is normalized...let's make this bigger
# this is just the coordinate scale at the moment
# lets presume this is mm.
scale = 50

"""
mock_stars = []
star_base_radius = 3.0
column_radius = [2.0, 1.0]

for i, coord in enumerate(mock_stars):
    #print coord
    scaled_coord = [x*scale for x in coord]

    # testing
    star_rand_scale = uniform(0.5, 1.25)

    s = translate(scaled_coord)(
              translate([0,0,star_rand_scale*star_base_radius/2])(sphere(star_rand_scale * star_base_radius)),
              translate([0,0,-scaled_coord[2]])(
                  cylinder(r1=column_radius[0], r2=column_radius[1], h=scaled_coord[2])
                  )
            )
    model_data.append(s)

# combine all model_data and add a base plate, 
u = translate([-scale/2, -scale/2, 0])(model_data,translate([-5,-5,0])(cube([scale+10, scale+10, 2])))

scad = scad_render(u)
#print scad

# want to modify the resulting scad file:
scad = "$fn=20;\n"+scad

f = open('output.scad', 'w')
f.write(scad)
f.close()
"""

# trying a more sophisticated model
# k-nearest neighbors
# inverting space...filling the "space" with shape
# returns a pySolid object.
def hood(star_data):
    mock_stars = star_data
    minimum_height = 10000 # used to calculate a base plane
    g = 1.01 # fudge factor to ensure intersections with each sphere

    neighbors_list = []
    
    # play with the leafsize here
    star_tree = scipy.spatial.cKDTree(mock_stars,leafsize=100)
    for star in mock_stars:
        # need to twiddle these dials
        neighbors = star_tree.query(star,k=2,distance_upper_bound=20)
        # print neighbors
        
        scaled_coord = [x*scale for x in mock_stars[neighbors[1][0]]]
        scaled_radius = g*scale*neighbors[0][1]
        # TODO: make a column between the current node and neighbor
        neighbors_list.append(
                # getting our location, and the distance as the sphere
                translate(scaled_coord)(sphere(scaled_radius))
                )
        # update the minimum_height if necessary
        bottom = scaled_coord[2] - scaled_radius
        if bottom < minimum_height:
            minimum_height = bottom

    model_data = neighbors_list

    # shift the data to the center, and up a bit to make way for the base
    u = translate([-scale/2, -scale/2,
        (-1 * minimum_height if minimum_height < 0 else 0) +5])(model_data)

    # make a base pedestal
    #u += cylinder(h=40, r=7) + cylinder(h=2, r=20)
    return u


# generate one 'hood
# try with real data!!
u = hood(sun_data)
scad = scad_render(u)
f = open('output.scad', 'w')
f.write("$fn=30;\n"+scad)
f.close()



"""
# make several iterations
for n in range(0, 10):
    u = hood(mock_data())
    scad = scad_render(u)

    f = open('hood-'+str(n)+'.scad', 'w')
    f.write(scad)
    f.close()
"""

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

for star in range(0, len(mock_stars)):
    xyz += "H " + " ".join("%10.5f" % x for x in (x*scale for x in mock_stars[star])) + "\n"

ff = open('output.xyz', 'w')
ff.write(xyz)
ff.close()
"""

