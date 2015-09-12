#Blender export
#Note that this file is temporary and will be reformated into another directory

#Find and import the systems lxml module
#Not all systems have same one so this acts as a failsafe
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
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
          print("Failed to import ElementTree from any known place")


#Define the top node of the file
root = etree.Element("root")
print(root.tag)

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


        
