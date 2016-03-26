'''
@author: Jeremy Bayley
@email : TheEnvironmentGuy@gmail.com
@websight : TheEnvironmentGuy.com

Friday March 25 2016
Blender 2.77

-*- coding: utf-8 -*-
'''

import bpy
import os


bpy.ops.object.select_all(action='DESELECT')
object_list = bpy.context.scene.objects
object_mesh = []

#For Linux % Mac
os.system('clear')
#For Windows
os.system('cls')

if len(object_list) <= 0:
    print("No objects")
else:
    print("Found %s objects" %(len(object_list)))
    for item in object_list:
        if item.type == 'MESH':
            object_mesh.append(item)
    if len(object_mesh) == 0:
        print("No MESH objects")
    else:
        print("Found %s MESH objects" %(len(object_mesh)))
        for mesh in object_mesh:
            #bpy.data[mesh].select = True
            mesh.select = True
            mesh.modifiers.new("Spam", type='WIREFRAME')
            mesh.select = False
