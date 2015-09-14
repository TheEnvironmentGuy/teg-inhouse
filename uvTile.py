'''
TheEnvironmentGuy 19-01-15
Places UV's of selected objects into random quadrants in 0-1 space
The operation will temporatly dissable construction history.
If you only select one object the object will be seperated then recombined
TODO
Handel multiple selection that need seperation
Scale uvs to fill entire quadrant
Work directly on UV islands (not seperating mesh)
Port to Blender
Replace is statments in for loop with case
OPtions for tileing by n#
'''

import maya.cmds as cmds
import random

#Dissable construction history
CH = cmds.constructionHistory(q=True, tgl=True)
if CH is True:
  cmds.constructionHistory(toggle=False)
else:
  selection = cmds.ls(selection=True)
  name = selection[0]
  count = -1
  
#Handel for invalid selection
SelList = len(selection)
if SelList == 0:
  print("Error, no selection")
  pass
else:
  #seporate object if combined
  if SelList == 1:
    cmds.polySeperate(selection)
    recombine = True
    selection = cmds.ls(selection=True)
    #handel for non tileable
    if len(selection) == 1:
      print("Error, nothing to tile")
      pass
    else:
      #tileUV
      for shapes in selection:
        count = count + 1
        rand = random.randint(1,4)
        cmds.select(selection[count])
        cmds.select(cmds.polyListComponentConversion(tuv=True), r=True)
        if rand == 1:
          #topLeft
          cmd.polyEditUV(scaleU=0.5, scaleV=0.5, vValue=0.5)
          pass
        if rand == 2:
          #topLeft
          cmd.polyEditUV(scaleU=0.5, scaleV=0.5, vValue=0)
          pass
        if rand == 3:
          #topLeft
          cmd.polyEditUV(scaleU=0.5, scaleV=0.5, vValue=0.5, uValue=0.5)
          pass
        if rand == 4:
          #topLeft
          cmd.polyEditUV(scaleU=0.5, scaleV=0.5, vValue=0, uValue=0.5)
          pass
          
      #cleanup
      if recombine is True:
        cmds.polyUnite(selection)
      cmds.DeleteHistory()
      cmds.rename(name)
      if CH is True:
        cmds.constructionHistory(toggle is True)
      pass
