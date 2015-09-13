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
except ImportError:
    raise Exception("error importing modules")


projectRootDir = ""
logData = None
logDir = "b2g.log"
xmlDir = "b2g.xml"
xmlData = ""
xmlRoot = None
scriptVer = "Devel 0.0.0"
objectCount = 0




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
        #Sort object list
        object_sort(objectList)
        
        #Create a xml data set
        xml_new()
        
        #add list objects to xml
        
        #Export xml
        xml_write_file()
            
        #Export objects
        object_export()
        
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
        selection = bpy.context.selected_objects
        #Check that selection isnt Zero
        if len(selection) <= 0:
            print("No objects selected")
        else:
            print("Found %s objects" %(len(selection)))
            return(selection)
    
    elif listType is "scene":
        print("Gathering objects by scene")
        if multiScene:
            print("Including objects in other scenes")
            #Get nodes from all scenes
            nodes = [1,2,3,4]
        else:
            #Get scene nodes
            nodes = [1,2,3,4]
            print("Found %s objects")
    
    elif listType is "children":
        print("Gathering objects by children")
        #Get children nodes
        selection = bpy.context.selected_objects()
        #Check that selection isnt Zero
        if len(selection) <= 0:
            print("error: no objects selected")
        else:
            #Get child nodes
            children = []
            for node in selection:
                children.append(1)
                pass
            print("Found %s child objects" %(len(children)))
            return(children)
    
    else:
        #Did not use valid listType
        print("error: in '%s' wrong 'listType'" %(sys._getframe().f_code.co_name))
        return(False)
    
    
def object_sort(sortType="outliner"):
    if sortType is "outliner":
        print("Sorting objects by outliner")
    elif sortType is "name":
        print("Sorting objects by name")
    elif sortType is "projectMatch":
        print("Sorting objects by project matching")
    else:
        print("error: in '%s' wrong 'sortType'" %(sys._getframe().f_code.co_name))
        return(False)

def project_make_dir():
    #Make nessisary directorys too export files.
    pass


def object_export():
    print("Exporting meshes as '%s'" %("OBJ"))


def xml_new():
    xmlRoot = etree.Element("xmlRoot")
    print("Created new xml root")


def xml_add_element():
    #Sorts data and adds them to xml elements.
    pass


def xml_write_file():
    #Saves xml data about the exported objects
    print("Exporting xml too '%s'" %(xmlDir))
    with open(xmlDir, 'w', encoding='utf-8') as xmlFile:
        xmlFile = xmlData

    '''
    #add child groups
    root.append(etree.Element("child1"))
    #A more efficient method
    child2 = etree.SubElement(root, "child2")

    #serialize the data
    print(etree.tostring)



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
