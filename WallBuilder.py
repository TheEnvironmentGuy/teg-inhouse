'''
@author: Jeremy Bayley
@email : TheEnvironmentGuy@gmail.com
@websight : TheEnvironmentGuy.com

Friday March 25 2016
Blender 2.77

-*- coding: utf-8 -*-
'''

import bpy
import ImperialPrimitives as ip

inch = 0.0254
foot = 0.3048
stud_length = foot*8

ceiling_height = foot*8
wall_length = foot*6
drywall_size = [foot*4, inch/2, foot*8]
woodstock_size = [inch*2.5, foot*8, inch*1.5]
stud_distance = inch*16


def Main():
    bpy.ops.mesh.primitive_cube_add()
    ip.SetupObject(size=[11,2,3])



if __name__ == '__main__':
    Main()
