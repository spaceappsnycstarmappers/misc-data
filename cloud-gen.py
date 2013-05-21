# Create a mock array of tuples
# generate an OpenSCAD file from that data.
# 
# Robert Carlsen | @robertcarlsen

from random import *

# this is from the SolidPython lib
from solid import *
from solid.utils import *

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
    if rownum == 0:
        header = row
    else:
        this_row_coords = [0,0,0]
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

# NOTE: the mock data is normalized.
# this should be the desired maximum length of the resulting model bounding box
# lets presume this is mm.
model_scale = 80

"""
mock_stars = []
star_base_radius = 3.0
column_radius = [2.0, 1.0]

for i, coord in enumerate(mock_stars):
    #print coord
    scaled_coord = [x*model_scale for x in coord]

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
u = translate([-model_scale/2, -model_scale/2,0])(model_data,translate([-5,-5,0])(cube([model_scale+10, model_scale+10, 2])))

scad = scad_render(u)
#print scad

# want to modify the resulting scad file:
scad = "$fn=20;\n"+scad

f = open('output.scad', 'w')
f.write(scad)
f.close()
"""

# make the shape hollow for shapeways.
makeHollow = True
wallThickness = 2.0 # mm

# trying a more sophisticated model
# k-nearest neighbors
# inverting space...filling the "space" with shape
# returns a pySolid object.
def hood(star_data):
    mock_stars = star_data

    max_extents = [0,0,0]
    min_extents = [0,0,0]

    minimum_height = 10000 # used to calculate a base plane
    g = 1.1 # (was 1.01) fudge factor to ensure intersections with each sphere

    neighbors_list = []
    hollow_list = []
    
    # calculated by the first pass of the star model
    scale_factor = 1.0
    
    # to simplify things, and to prevent having to run cKDTree twice, 
    # get this as a 4-tuple of [xyz,r] in the first pass.
    star_list = []

    # play with the leafsize here
    star_tree = scipy.spatial.cKDTree(mock_stars,leafsize=100)
    for star in mock_stars:
        # need to twiddle these dials
        neighbors = star_tree.query(star,k=2,distance_upper_bound=20)

        r = mock_stars[neighbors[1][0]]
        normalized_len = len(r)
        normalized_coord = [x/normalized_len for x in r]

        scaled_coord = normalized_coord
        scaled_radius = g*neighbors[0][1]/normalized_len # the g-factor helps ensure intersection
        
        max_extents = max(max_extents, [p+scaled_radius for p in scaled_coord])
        min_extents = min(min_extents, [p-scaled_radius for p in scaled_coord])

        star_list.append([scaled_coord,scaled_radius])

    print max_extents
    print min_extents

    hood_size = [x1 - x2 for (x1, x2) in zip(max_extents, min_extents)]
    hood_scale = min([model_scale/x for x in hood_size])
    print hood_scale

    scale_factor = hood_scale

## --- ##
    for star in star_list:
        coord = [n*scale_factor for n in star[0]]
        radius = star[1]*scale_factor

        # TODO: make a column between the current node and neighbor
        # getting our location, and the distance as the sphere
        if coord[0] + coord[1] + coord[2] == 0:
            item = color(Yellow)(translate(coord)(sphere(radius)))
        else:
            item = translate(coord)(sphere(radius))

        # this makes each sphere hollow, but not the entire structure
        if makeHollow and radius > wallThickness:
            hollow_list.append(translate(coord)(sphere(radius - wallThickness)))

        neighbors_list.append(item)

    model_data = neighbors_list

    # shift the data to the center, and up a bit to make way for the base
    #u = translate([-model_scale/2, -model_scale/2,
    #    (-1 * min_extents[2] if min_extents[2] < 0 else 0) +5])(model_data)
    
    # something does not *look* quite right here, but the math should work out.
    model_translate = [
            -(scale_factor*(max_extents[0]+min_extents[0]))/2.0,
            -(scale_factor*(max_extents[1]+min_extents[1]))/2.0,
            (-1 * scale_factor*min_extents[2] if scale_factor*min_extents[2] < 0 else 0) +5 ]

    #model_translate = [0,0,0]
    bounds = [scale_factor*n for n in hood_size]
    print bounds

    print model_translate

    # move the model data into position:
    u = translate(model_translate)(model_data)

    # make a base pedestal:
    u += cylinder(h=30, r=8) + cylinder(h=2, r=20)

    # do the same as above, but then subtract the interior from the shell
    if makeHollow:
        interior = translate(model_translate)(union()(hollow_list))
        interior += cylinder(h=30, r=8-4)

        u -= interior

    return u


# generate one 'hood
# try with real data!!
u = hood(sun_data)
scad = scad_render(u)
f = open('sol.scad', 'w')
# all this muck is for something not supported by SolidPython 
# (or, something I can't find)

nameLabelScad = 'writecylinder("SUN",[0,0,0],20,2,h=5,t=2,space=1.1,face="top",ccw=true);\n'
eventLabelScad = 'writecylinder("Space Apps 2013",[0,0,0],20,2,h=5,t=2,space=1.1,face="top",ccw=false);\n'

f.write("use <write.scad>\n$fn=30;\n"+scad+'\n\n' + nameLabelScad + eventLabelScad)
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
    xyz += "H " + " ".join("%10.5f" % x for x in (x*model_scale for x in mock_stars[star])) + "\n"

ff = open('output.xyz', 'w')
ff.write(xyz)
ff.close()
"""

