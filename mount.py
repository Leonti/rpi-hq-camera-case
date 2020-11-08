#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

from solid import *
from solid.utils import *

cap = cylinder(d = 38.5, h = 30)

cap_hole = cylinder(d = 35.5, h = 28)

mounting_holes = translate([53, -10, 27])(cylinder(d = 3.5, h = 10)
    + translate([0, 20, 0])(cylinder(d = 3.5, h = 10))
)

bridge = (
    translate([0, -38.5/2, 28])(
        cube([60, 38.5, 2])
        + translate([0, 0, -10])(cube([60, 2, 10]))
        + translate([0, 38.5 - 2, -10])(cube([60, 2, 10]))
        )
    - mounting_holes)

cap_with_bridge = cap + bridge - cap_hole

camera_holder = translate([45, -38.5/2, 30])(
    cube([15, 38.5, 1.5])
    + translate([15/2, 38.5/2 + 1, 9])(rotate([90, 0, 0])(
        cylinder(d = 15, h = 2)
        ))
    + translate([0, 38.5/2 - 1, 0])(cube([15, 2, 9]))
    - translate([15/2, 38.5/2 + 1, 9])(rotate([90, 0, 0])(
        cylinder(d = 3.5, h = 10)
        ))   
) - mounting_holes

full = camera_holder