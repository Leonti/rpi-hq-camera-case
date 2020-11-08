#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys

from solid import *
from solid.utils import *

import mount

SEGMENTS = 48

HEIGHT = 100
DIAMETER = 100

rpi_stl = color("green")(import_stl('rpi.stl'))
camera_stl = color("green")(import_stl('camera.stl'))

rpi = translate([32, 1.1, 0])(rotate([-90, 0, 90])(rpi_stl))
camera = translate([6, 48.6, 5])(rotate([0, 0, -90])(camera_stl))

def camera_mounts(mount):
    return (mount +
    translate([30, 0, 0])(mount) +
    translate([30, 30, 0])(mount) +
    translate([0, 30, 0])(mount)
    )

def rpi_mounts(mount):
    return (mount +
    translate([23, 0, 0])(mount) +
    translate([23, 58, 0])(mount) +
    translate([0, 58, 0])(mount)
    )        

screw_hole_diameter = 2.85
screw_through_hole_diameter = 3.2

camera_stands_front = translate([10, 14.6, 1.9])(camera_mounts((
    cylinder(d = 6, h = 3.1)
    + cylinder(d = 2.4, h = 4.5)
    ))) - translate([35, 0, 0])(cube([60, 60, 60]))

camera_stands_back = translate([10, 14.6, -10])(camera_mounts((
    cylinder(d = 6, h = 15)
    + cylinder(d = 8, h = 13)
    - translate([0, 0, 5])(cylinder(d = screw_hole_diameter, h = 11))
    ))
    - translate([-10, -10, 0])(cube([20, 50, 40]))
    )

def rounded_box(x, y, z, corner_radius):
    return hull()(translate([0 + corner_radius,0+ corner_radius,0])(cylinder(d = corner_radius * 2, h = z)), 
    translate([x- corner_radius,0+ corner_radius,0])(cylinder(d = corner_radius * 2, h = z)),
    translate([x- corner_radius,y- corner_radius,0])(cylinder(d = corner_radius * 2, h = z)),
    translate([0+ corner_radius,y- corner_radius,0])(cylinder(d = corner_radius * 2, h = z))
    )

bottom_case = (translate([-0.5, 0,-10])(
    rounded_box(50, 68 + 2, 12, 4)
    - translate([2, 1, 1])(rounded_box(47, 68, 11.5, 3))
    - translate([1.2, 20.8, 4])(cube([0.8, 17.3, 9]))
    - translate([13, -1, 6.6])(cube([13, 3, 2.5]))
    - translate([-1, 7.7, 4.5])(cube([3, 12, 5]))
    - translate([-1, 38.1, 5.2])(cube([3, 9, 4]))
    - translate([0.9, 50.6, 5.2])(cube([3, 9, 4]))
    + translate([6, 4.6, 1])(rpi_mounts(
        cylinder(d = 6.3, h = 10 - 1.5 - 1)
        - translate([0, 0, 1])(cylinder(d = screw_hole_diameter, h = 7))
        ))
)
+ camera_stands_back
) - translate([-23, 34, -40])(mount.mounting_holes)

camera_holes = translate([10, 14.6, -1])(
    camera_mounts(cylinder(d = screw_through_hole_diameter, h = 15))
    - translate([-10, -10, 0])(cube([20, 50, 40]))
    )


recessed_screw_hole = (
    cylinder(d = 8, h = 6)
    - translate([0, 0, 3.5])(cylinder(d = 5.5, h = 3))
    - cylinder(d = screw_through_hole_diameter, h = 10)
)
recessed_screw_holes = translate([5.5, 4.6, 2])(
    rpi_mounts(recessed_screw_hole)
    )

recessed_screw_holes_cutouts = translate([5.5, 4.6, 2])(
    rpi_mounts(cylinder(d = 7, h = 6))
    )

top_case_walls = (translate([-0.5, 0, 2])(
    rounded_box(50, 68 + 2, 5, 4)
    - translate([1, 1, -0.5])(rounded_box(48, 68, 10, 3))
    ))

top_case = (translate([-0.5, 0, 6.5])(
    rounded_box(50, 68 + 2, 1.5, 4)
    ) 
    - camera_holes
    - recessed_screw_holes_cutouts
    + recessed_screw_holes
    - translate([25, 29.5, 4])(cylinder(d = 35.5, h = 5))
    - translate([42, 62, -1])(cylinder(d=5, h=25))
    ) + top_case_walls

top_case_left = top_case - translate([-1, 0, 0])(
    cube([100, 29.5, 10])
    )

top_case_right = top_case - translate([-1, 29.5])(
    cube([100, 100, 10])
)

top_case_bottom = top_case - translate([24.5, 11.75, 0])(
    cube([50, 35.5, 10])
)

top_case_top = (top_case
    - translate([-0.5, 0,  0])(cube([100, 11.75, 20]))
    - translate([-0.5, 47.25,  0])(cube([100, 100, 20]))
    - translate([-0.5, 10, 0])(cube([25, 50, 20]))
)

inner_plate = (translate([3, 2.1, 0])(
    cube([28, 63, 2])
    - translate([(28 - 23) / 2, (63 - 58)/2, -1])(rpi_mounts(cylinder(d = screw_through_hole_diameter, h = 6)))
    - translate([16, 5.5, -0.1])(cube([12, 52, 3]))
) + camera_stands_front
)

full = (
    camera 
    + rpi 
    + inner_plate
    + bottom_case
)

full = bottom_case + top_case_left + top_case_right
#full = inner_plate + recessed_screw_holes + top_case
full = (
    cube([50, 68 + 2, 12]) 
    + translate([0, 0, 10])(rounded_box(50, 68 + 2, 12, 4))
)

full = top_case_bottom

stls = [
    {
        'name': 'case_front_left', 
        'obj': top_case_left
    },
    {
        'name': 'case_front_right', 
        'obj': top_case_right
    },
    {
        'name': 'case_front_top', 
        'obj': top_case_top
    },
    {
        'name': 'case_front_bottom', 
        'obj': top_case_bottom
    },
    {
        'name': 'case_bottom', 
        'obj': bottom_case
    }
]

def render_stls():
    for stl in stls:
        name = stl['name']
        print(f'Rendering {name}')
        scad_render_to_file(stl['obj'], os.path.join(
            out_dir, 'to_render.scad'), file_header='$fn = %s;' % SEGMENTS)
        os.system(f'openscad -o stl/{name}.stl ./to_render.scad')

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'rpicamera.scad')

    render_stls()

    a = full #mount.full

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)