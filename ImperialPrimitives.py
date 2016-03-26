'''
@author: Jeremy Bayley
@email : TheEnvironmentGuy@gmail.com
@websight : TheEnvironmentGuy.com

Friday March 25 2016
Blender 2.77

-*- coding: utf-8 -*-
'''

import bpy

inch = 0.0254
foot = 0.3048

def Main():
    bpy.ops.mesh.primitive_cube_add()
    SetupObject(size=[6,26,1])

def SetupObject(size):
    '''
    Moves selected object to center grid, shifts geometry by +1' in XYZ, 
    scales to size and applys translations. Only works on unmodified primitives.
    Size is Vec3 in inches
    '''
    
    #Center object
    bpy.ops.object.location_clear()
    
    #Move pivot to corner and place object in (x+,y+,z+).
    bpy.ops.object.editmode_toggle()
    bpy.ops.transform.translate(value=(foot, foot, foot))
    bpy.ops.object.editmode_toggle()
    
    #calculate scale values. Note that 1:1 scale is .5 so we divide by 2.
    size[0] *= inch/foot/2
    size[1] *= inch/foot/2
    size[2] *= inch/foot/2
    
    #scale object
    bpy.ops.transform.resize(value=(size[0], size[1], size[2]))
    bpy.ops.object.transform_apply(scale=True)
    
    #Show info
    bpy.context.object.data.show_extra_edge_length = True


if __name__ == '__main__':
    Main()