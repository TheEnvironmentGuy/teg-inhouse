import bpy
import ImperialPrimitives

bpy.ops.mesh.primitive_cube_add()
ImperialPrimitives.SetupObject(size=(11,2,3))