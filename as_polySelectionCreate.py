# encoding: utf-8
import maya.cmds as cmds
import re as re

class as_polySelectionCreate :
 def __init__(self):
  winName = 'win_apsb'
  if(cmds.window(winName,exists=1)):
   cmds.deleteUI(winName)
  cmds.window(winName,title='Polygon Selection Create')
  
  cmds.formLayout('form_apsbMain')
  cmds.button('btn_apsbA',label='Add',width=70,height=25,command=self.defineSource)
  cmds.button('btn_apsbR',label='Remove',width=70,height=25,command=self.itemRemove)
  cmds.button('btn_apsbRA',label='Clear',width=70,height=25,command=self.itemRemoveAll)

  cmds.treeView('tree_apsbPL',numberOfButtons=1,abr = False )
  cmds.treeView('tree_apsbPL', edit=True, removeAll = True )
  cmds.button('btn_apsbS',label='Select',width=70,height=25,command=self.select)
  cmds.button('btn_apsbL',label='locator',width=70,height=25,command=self.createLocator)
  cmds.button('btn_apsbC',label='Polygon',width=70,height=25,command=self.createPolygon)
  
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbA','top',5),('btn_apsbA','left',5)])
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbR','top',5)],ac=[('btn_apsbR','left',5,'btn_apsbA')])
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbRA','top',5)],ac=[('btn_apsbRA','left',5,'btn_apsbR')])
  cmds.formLayout('form_apsbMain',e=1,af=[('tree_apsbPL','left', 2),('tree_apsbPL','right', 2)],ac=[('tree_apsbPL','top',5,'btn_apsbA'),('tree_apsbPL','bottom', 5,'btn_apsbS')])
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbS','bottom',5),('btn_apsbS','left',5)])
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbL','bottom',5)],ac=[('btn_apsbL','left',5,'btn_apsbS')])
  cmds.formLayout('form_apsbMain',e=1,af=[('btn_apsbC','bottom',5)],ac=[('btn_apsbC','left',5,'btn_apsbL')])
  
  for x in '0123' :
   cmds.treeView('tree_apsbPL',e=1,addItem = ('vtx['+x+']',''))

  cmds.window(winName,e=1,widthHeight=[275,275],resizeToFitChildren=1)
  cmds.showWindow(winName)
  
 def defineSource(self,*a):
  sl = cmds.ls(selection=1,fl=1)
  s = ''
  for x in sl :
   s = s + x.split('.')[-1]
   if x != sl[-1] : s = s + ','
  cmds.treeView('tree_apsbPL',e=1,addItem = (s,''))
  
 def itemName(self,*a):
  pass
  
 def itemRemove(self,*a):
  sl = cmds.treeView('tree_apsbPL', q=1, selectItem = True )
  for x in sl :
   cmds.treeView('tree_apsbPL',e=1,removeItem=x)
  
 def itemRemoveAll(self,*a):
  cmds.treeView('tree_apsbPL', edit=True, removeAll = True )

 def executeCondition(self,*a):
  tis = cmds.treeView('tree_apsbPL',q=1,children=1) # tree items
  if tis is None : cmds.warning('Position List Empty') ; return 0
  sl = cmds.ls(selection=1)
  if(len(sl)==0): cmds.warning('Select some polygons.') ; return 0
  
 def select(self,tis,*a):
  self.executeCondition()
  tis = cmds.treeView('tree_apsbPL',q=1,children=1) # tree items
  sl = cmds.ls(selection=1)
  
  rsl = [] # re-select list
  for mn in sl : # mesh name
   if(cmds.nodeType(mn)=='transform'):
    c = cmds.listRelatives(mn,shapes=1,noIntermediate=1)
    if(len(c)==0): cmds.warning('Selection most be polygon.')
    else: mn = c[0]
   elif(cmds.nodeType(mn)=='mesh'):
    mns = mn.split('.')
    if len(mns) > 1 : mn = mns[0]
   else: cmds.warning('Selection most be polygon.')
   for ti in tis : # tree item
    xList = ti.split(',')
    for sti in xList : # splited tree item
     rsl.append(mn+'.'+sti)
  cmds.select(rsl,replace=1)

 def createLocator(self,tis,*a):
  self.executeCondition()
  tis = cmds.treeView('tree_apsbPL',q=1,children=1) # tree items
  sl = cmds.ls(selection=1)
  
  cll = [] # created locator name list
  for mn in sl : # mesh name
   if(cmds.nodeType(mn)=='transform'):
    c = cmds.listRelatives(mn,shapes=1,noIntermediate=1)
    if(len(c)==0): cmds.warning('Selection most be polygon.')
    else: mn = c[0]
   elif(cmds.nodeType(mn)=='mesh'):
    mns = mn.split('.')
    if len(mns) > 1 : mn = mns[0]
   else: cmds.warning('Selection most be polygon.')
   
   for ti in tis : # tree item
    xList = ti.split(',')
    xx = 0.0 ; xy = 0.0 ; xz = 0.0 ;
    for sti in xList : # splited tree item
     vn = mn+'.'+sti # vertex name
     if cmds.objExists(vn):
      yPos = cmds.xform(vn,q=1,translation=1,worldSpace=1)
      xx = xx + yPos[0]
      xy = xy + yPos[1]
      xz = xz + yPos[2]
    xx = xx / len(xList)
    xy = xy / len(xList)
    xz = xz / len(xList)
    loc = cmds.spaceLocator(position=[xx,xy,xz])
    cll.append(loc[0])
   
  cmds.select(cll,replace=1)

 def createPolygon(self,tis,*a):
  self.executeCondition()
  tis = cmds.treeView('tree_apsbPL',q=1,children=1) # tree items
  if len(tis) < 3 : cmds.warning('Position List most more than 3.') ; return 0
  sl = cmds.ls(selection=1)
  
  cpl = [] # created polygon name list
  for mn in sl : # mesh name
   if(cmds.nodeType(mn)=='transform'):
    c = cmds.listRelatives(mn,shapes=1,noIntermediate=1)
    if(len(c)==0): cmds.warning('Selection most be polygon.')
    else: mn = c[0]
   elif(cmds.nodeType(mn)=='mesh'):
    mns = mn.split('.')
    if len(mns) > 1 : mn = mns[0]
   else: cmds.warning('Selection most be polygon.')
   
   pl = [] # position list
   for ti in tis : # tree item
    xList = ti.split(',')
    xx = 0.0 ; xy = 0.0 ; xz = 0.0 ;
    for sti in xList : # splited tree item
     vn = mn+'.'+sti # vertex name
     if cmds.objExists(vn):
      yPos = cmds.xform(vn,q=1,translation=1,worldSpace=1)
      xx = xx + yPos[0]
      xy = xy + yPos[1]
      xz = xz + yPos[2]
    xx = xx / len(xList)
    xy = xy / len(xList)
    xz = xz / len(xList)
    pl.append([xx,xy,xz])
   
   cpl.append( cmds.polyCreateFacet(point=[pl[0],pl[1],pl[2]])[0] )
   for i in range(3,len(tis)):
    cmds.polyAppendVertex( a=[i-2,i-1,pl[i]] )
  
  cmds.select(cpl,replace=1)
   
as_polySelectionCreate()
