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
scale = 100

for i, coord in enumerate(mock_stars):
    #print coord
    s = translate([x*scale for x in coord])(
            sphere(1.0)
            ) # TODO: add cylinder stick
    model_data.append(s)

u = translate([-scale/2, -scale/2, -scale/2])(union()(model_data))
#scad = scad_render(u)
#print scad

# try writing to a file:
scad_render_to_file(u, 'output.scad')

