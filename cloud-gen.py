# Create a mock array of tuples
# generate an OpenSCAD file from that data.
# 
# Robert Carlsen | @robertcarlsen

from random import *

# this is from the SolidPython lib
from solid import *



# make some fake:
mock_stars = []
for i in range(0, 100, 1):
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

for i, coord in enumerate(mock_stars):
    #print coord
    scaled_coord = [x*scale for x in coord]
    s = translate(scaled_coord)(
              sphere(star_base_radius),
              translate([0,0,-scaled_coord[2]])(
                  cylinder(r1=column_radius[0], r2=column_radius[1], h=scaled_coord[2])
                  )
            ) # TODO: add cylinder stick
    model_data.append(s)

u = translate([-scale/2, -scale/2, 0])(union()(model_data)+cube([scale, scale, 2]))

#scad = scad_render(u)
#print scad

# try writing to a file:
scad_render_to_file(u, 'output.scad')

