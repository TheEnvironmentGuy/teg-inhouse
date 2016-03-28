import bpy

#Define vertices, faces, edges
verts = [(0,0,0),(0,0,1)]
faces = [(0,1)]

#Define mesh and object
mymesh = bpy.data.meshes.new("Cube")
myobject = bpy.data.objects.new("Cube", mymesh)

#Set location and scene of object
myobject.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(myobject)

#Create mesh
mymesh.from_pydata(verts,[],faces)
mymesh.update(calc_edges=True)
myobject.select = True
