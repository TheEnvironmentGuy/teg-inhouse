#-*- coding: utf-8 -*-

'''
#Created Sep, 2015
@author: Jeremy Bayley
'''

#Find and import the systems lxml module
#Not all systems have same one so this acts as a failsafe

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    #print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          raise Exception("Failed to import ElementTree from any known place")
          sys.exit(1)

try: 
    import os
    import sys
    import time
    import bpy
    import math
except ImportError:
    raise Exception("error importing modules")
    
    
__version__ = '0.1.0'


projectRootDir = ""
logData = None
logDir = "b2g.log"
xmlData = {}
scriptVer = __version__
blendPath = bpy.path.abspath('//')


def main():
    log()
    objectDic = object_dic()
    export(objectDic)
    xml_add_data(data=objectDic)
    log(False)
    

def log(write=True):
    if write == True:
        #Start logging
        logData = open(logDir, 'w', encoding='utf-8')
        sys.stdout = logData
        print("")
        print("Start of log")
        print("Timestamp: %s %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
        print("ScriptVer: %s" %(scriptVer))
        print("Links: %s" %("None"))
        print("Platform: %s" %(sys.platform))
        print("PythonVer: %s" %(sys.hexversion))
        print("BlenderVer: %s" %(bpy.app.version_string))
        print("")
    if write == False:
        #Stop logging
        print("")
        print("Timestamp: %s %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
        print("End of log")
        print("")
        sys.stdout = sys.__stdout__
      
        
def object_dic(selectionType="selection"):
    #Returns a dic with all objects that we want organized by node type and with per node attributres
    #Gather objects by selection type
    if selectionType is "selection":
        print("Gathering objects by selection")
        objectList = bpy.context.selected_objects
        if len(objectList) <= 0:
            print("No objects selected")
        else:
            print("Found %s objects" %(len(objectList)))
    
    #Got all objects, no need to have selection anymore        
    bpy.ops.object.select_all(action='DESELECT')
    
    #Group selections by node type
    objectDic = {}
    for object in objectList:
            object.select = True
            #Add object type to dic if not present
            objectType = object.type
            if objectType not in objectDic:
                objectDic[objectType] = []
            #Add object to dic
            objectDic[objectType].append(object)
            object.select = False
    
    #Add attributes to each individual object
    attributeDic = {}
    for nodeType, nodeList in objectDic.items():
        attributeDic[nodeType] = {}
        for node in nodeList:
            node.select = True
            locVec, scaVec, rotVec = node.location, node.scale, bpy.context.object.rotation_euler
            locVec = [locVec[0], locVec[1], locVec[2]]
            rotVec = [rotVec[0], rotVec[1], rotVec[2]]
            scaVec= [scaVec[0], scaVec[1], scaVec[2]]
            #Convert radians to degrees
            '''
            degrees = rotVec
            degrees[0] *= (180/math.pi)
            degrees[1] *= (180/math.pi)
            degrees[2] *= (180/math.pi)
            '''
            attributeDic[nodeType].update({node:{"rotation":rotVec, "location":locVec, "scale":scaVec}})
            
    #attributeDic = {nodeType : {node:{attributes}}}
    print(attributeDic)
    return(attributeDic)


def export(objectDic):
    #Exports all mesh objects as obj's
    #http://www.blender.org/api/blender_python_api_2_69_release/bpy.ops.export_scene.html#bpy.ops.export_scene.obj
    bpy.ops.object.select_all(action='DESELECT')
    if objectDic["MESH"]:
        print("\nExporting meshes as .obj")
        for key, attributes in objectDic["MESH"].items():
            key.select = True
            #We zero out vectors before export beacuse we will use xml file to get vecotors when importing.
            bpy.ops.object.location_clear()
            bpy.ops.object.rotation_clear()
            bpy.ops.object.scale_clear()
            #Save out the object
            objectName = str(key)[21:-3]
            savePath = str(blendPath) + str(objectName) + ".obj"
            bpy.ops.export_scene.obj(filepath=str(savePath), check_existing=False, use_selection=True, use_animation=False, use_normals=True, use_uvs=True, use_materials=False, group_by_object=False, path_mode="RELATIVE")
            #Return objects to original position
            key.location = objectDic["MESH"][key]["location"]
            key.rotation_euler = objectDic["MESH"][key]["rotation"]
            key.scale = objectDic["MESH"][key]["scale"]
        
def xml_add_data(data):
    if not etree.Element("xmlRoot"):
        xmlRoot = etree.Element("xmlRoot")
        xmlTree = etree.ElementTree(xmlRoot)
        print("\nStarted new XML\n")
        
    for key in data.items():
        print("key", key)
        #xmlData[key] = etree.Element("%s" %(str(key)))
    
    print(etree.tostring(xmlRoot))


if __name__ == '__main__':
    main()