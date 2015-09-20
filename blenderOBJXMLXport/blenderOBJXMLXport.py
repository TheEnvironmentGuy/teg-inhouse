#Blender export scene or collection of individuals
#Note that this file is temporary and will be reformated into another directory

#Overview
#Gather objects to export in Blender
#Solve export paths using object names and project target
#Generate file directory trees if necissary
#commit too git for version control
#Export unique meshes at center
#export xml file containing locRotSca and instances for whole scene
#include target specific data in xml if applicable
#Identify objects that have been modifyed since last export
#Call on external application to import scene or individual assets
#perform mesh checks to ensure compatibility with target engine

#For more help on xml
#http://lxml.de/tutorial.html

# -*- coding: utf-8 -*-

#Find and import the systems lxml module
#Not all systems have same one so this acts as a failsafe

'''
-*- coding: utf-8 -*-

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


projectRootDir = ""
logData = None
logDir = "b2g.log"
xmlDir = "b2g.xml"
xmlRoot = None
scriptVer = "Devel 0.0.0"
objectCount = 0
blendPath = bpy.path.abspath('//')
exportMesh = ".obj"
objectUniqueList = {}


def main():
    #start the log
    log()
    print_stamp()
    
    #Get list of objects
    objectList = object_list(listType="selection")
    if objectList == False: 
        #Quit if unable to list objects
        print_stamp(start=False)
        log(write=False)
    else:
        #Organise objectList by node type
        objectDic = object_sort(objectList)
        #print objectDic in a readable formatt
        for key, value in objectDic.items():
            print(key)
            for item in value:
                print("\t%s" %(item)) 
        
        #Create organized folders for all exports. 
        project_make_folders()
        
        #Generate xml file
        xmlTree= xml_make(objectDic)
        
        #add list objects to xml
        
        #Export xml
        xml_write_file(xmlTree)
            
        #Export objects
        object_export(objectDic)
        
        #Sucess, close any open files and end program
        print_stamp(start=False)
        log(write=False)
    


def log(write=True):
    if write == True:
        #Start logging
        logData = open(logDir, 'w', encoding='utf-8')
        sys.stdout = logData
    if write == False:
        #Stop logging
        sys.stdout = sys.__stdout__
        

def print_stamp(short=True, start=True):
    if start:
        if short:
            #short version
            print("")
            print("Start of log")
            print("Timestamp: %s %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
            print("ScriptVer: %s" %(scriptVer))
            print("Links: %s" %("None"))
            print("Platform: %s" %(sys.platform))
            print("PythonVer: %s" %(sys.hexversion))
            print("BlenderVer: %s" %(bpy.app.version_string))
            print("")
        else:
            #Long version. Note that this does not work correctly as of yet
            print("Timestamp: %s %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
            print("%s" %(bpy.ops.wm.sysinfo()))
    else:
        print("")
        print("Timestamp: %s %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
        print("End of log")
        print("")


def object_list(listType="selection", multiScene=False, organizeType="outliner"):
    #Creates an organized list of nodes
    if listType is "selection":
        print("Gathering objects by selection")
        objectList = bpy.context.selected_objects
        #Check that selection isnt Zero
        if len(objectList) <= 0:
            print("No objects selected")
        else:
            print("Found %s objects" %(len(objectList)))
            return(objectList)
    
    elif listType is "scene":
        bpy.ops.object.select_all(action='DESELECT')
        print("Gathering objects by scene")
        objectList = bpy.context.scene
        object_sort(objectList)
        if multiScene:
            print("Including objects in other scenes")
            #Get nodes from all scenes
            nodes = [1,2,3,4]
        else:
            #Get scene nodes
            nodes = [1,2,3,4]
            print("Found %s objects")
    
    elif listType is "children":
        bpy.ops.object.select_all(action='DESELECT')
        print("Gathering objects by children")
        #Get children nodes
        objectList = bpy.context.selected_objects()
        #Check that selection isnt Zero
        if len(objectList) <= 0:
            print("error: no objects selected")
        else:
            #Get child nodes
            children = []
            for node in objectList:
                children.append(1)
                pass
            print("Found %s child objects" %(len(children)))
            return(children)
    
    else:
        #Did not use valid listType
        print("error: in '%s' wrong 'listType'" %(sys._getframe().f_code.co_name))
        return(False)
    
    
def project_make_folders(projectStructure="outliner"):
    if projectStructure is "outliner":
        print("Sorting objects by outliner")
    elif projectStructure is "name":
        print("Sorting objects by name")
    elif projectStructure is "projectMatch":
        print("Sorting objects by project matching")
    else:
        print("error: in '%s' wrong 'sortType'" %(sys._getframe().f_code.co_name))
        return(False)


def object_sort(objectList):
    #Group objectList items into dic according to type and return the dic  
    #Make sure we have somthing in list
    if len(objectList) >= 1:
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
        return(objectDic)


def object_check_diff():
    #This is example code not viable
    #check mesh if changed
    for node in list:
        vertexCount = len(node.vertices)
        for vertex in node.vertices:
            #do stuff
            pass


def object_clean(mesh):
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select = true
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.mesh.tris_convert_to_quads
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

def project_make_dir(exportList):
    #Make nessisary directorys too export files.
    pass


def object_get_dir():
    pass


def object_export(objectDic):
    #http://www.blender.org/api/blender_python_api_2_69_release/bpy.ops.export_scene.html#bpy.ops.export_scene.obj
    print("Exporting meshes as '%s'" %(exportMesh))
    for key, values in objectDic.items():
        if key == "MESH":
            for item in values:
               attributes = object_attributes(objectType="MESH", object=item)
               bpy.ops.object.select_all(action='DESELECT')
               item.select = True
               bpy.ops.export_scene.obj(filepath=blendPath, check_existing=False, use_selection=True, use_animation=False, use_mesh_modifiers=True, use_smooth_groups=True, use_normals=True, use_uvs=True, use_materials=False, use_triangles=False, use_nurbs=False, use_vertex_groups=False, group_by_object=False, keep_vertex_order=False, global_scale=1.0)
               
    #bpy.ops.export_scene.obj(filepath=str(path + ob.name + exportMesh), use_selection=True)
    #node.select = False


def xml_make(objectDic):
    #Create xml data
    xmlRoot = etree.Element("xmlRoot")
    xmlTree = etree.ElementTree(xmlRoot)

    for key, values in objectDic.items():
        #Create first level subElements (object categorys)
        subElementOne = str(key)
        subElementOne = etree.Element(subElementOne) 
        xmlRoot.append(subElementOne)
        if key == "MESH":
            #Create second level subElements (individual objects)
            for value in values:
                subElementTwo = str(value)
                subElementTwo = etree.Element(subElementTwo)
                subElementOne.append(subElementTwo)
                for attribute in object_attributes(objectType="MESH", object=value):
                    #Add attributes to second level subElement
                    subElementTwo.set(attribute, 'None')
    return(xmlTree)


def object_attributes(objectType, object):
    bpy.ops.object.select_all(action='DESELECT')
    object.select = True
    attributeDic = {}
    if objectType == "MESH":
        #Create attributes for mesh
        attributeList = {"name":bpy.context.selected_objects}
        for attribute in attributeList:
            newAttribute = {attribute:""}
            attributeDic[attribute] = attributeList[attribute]
            dic_add_locrotsca(dic=attributeDic, object=object)
            print(attributeDic)
            return(attributeList)
    elif objectType == "CAMERA":
        #Create attributes for camera
        attributeList = {"name":bpy.context.selected_objects}
        dic_add_locrotsca(dic=attributeDic, object=object)
        print(attributeDic)
        return(attributeList)

        
      
      
def dic_add_locrotsca(object, dic):
    #Get Loc Rot Sca of object and return dic
    #Converts blenders vector format to a regular Python list
    locationVector = object.location
    scaleVector = object.scale
    dic["Scale"] = [0, 0, 0]
    dic["Location"] = [0, 0, 0]
    count=0
    for value in locationVector:
        dic["Location"][count] = round(value, 2) 
        count+=1
    count=0
    for value in scaleVector:
        dic["Scale"][count] = round(value, 2) 
        count+=1
    #Convert radians to degrees
    radians = bpy.context.object.rotation_euler
    dic["Rotation"] = [0, 0, 0]
    count=0
    for radian in radians:
        #Converts radians into degrees
        dic["Rotation"][count] = round(radian*(180/math.pi), 2)
        count+=1
    return(dic)


def xml_add_element():
    #Sorts data and adds them to xml elements.
    pass


def xml_write_file(xmlTree):
    #Saves xml data about the exported objects
    print("Exporting xml too '%s'" %(xmlDir))
    xmlTree.write(xmlDir, encoding='utf-8')
    #with open(xmlDir, 'w', encoding='utf-8') as xmlFile:
    #    xmlFile = xmlData

    '''
    #Elements are lists
    child = root[0]
    print(child.tag)
    print(len(root))
    children = list(root)

    #iterate through children and print tag
    for child in root:
            print(child.tag)

    #insert a child at index 0
    root.insert(0, etree.Element("child0"))

    #Print the first and last child of root
    start = root[:1]
    end = root[-1:]
    print(start[0].tag, end[0].tag)

    #Test if there is element
    print(etree.iselement(root))
    #test if element has children
    if len(root):
            print("Element has children")
            
    #move an element
    root[0] = root[-1]
    '''

def xml_read_file():
    pass


if __name__ == '__main__':
    main()
