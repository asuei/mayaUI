# encoding: utf-8
import sys
import maya.cmds as cmds

class as_crvAverageCv:
 def __init__(self):
  if(cmds.window('win_acac',exists=1)):
   cmds.deleteUI('win_acac')
  cmds.window('win_acac',title='Average Curve CV number')

  cmds.formLayout('form_acacMain')
  
  cmds.radioCollection('rdc_acac1')
  cmds.radioButton('rd_acacFL',label='Fit longest',select=1)
  cmds.radioButton('rd_acacFS',label='Fit shortest')
  cmds.radioButton('rd_acacSL',label='Specific Length')
  cmds.intField('if_acacFL',minValue=0,value=10)
  cmds.intField('if_acacFS',minValue=0,value=3)
  cmds.floatField('ff_acacSL',minValue=0,value=5)
  cmds.button('btn_acacEx',label='Execute',width=20,height=20,command=self.execute)

  cmds.window('win_acac',e=1,resizeToFitChildren=1,widthHeight=[215,130])
  cmds.showWindow('win_acac')
  
  cmds.formLayout('form_acacMain',e=1,af=[('rd_acacFL','top',5),('rd_acacFL','left',5)])
  cmds.formLayout('form_acacMain',e=1,af=('rd_acacFS','left',5),ac=('rd_acacFS','top',5,'rd_acacFL'))
  cmds.formLayout('form_acacMain',e=1,af=('rd_acacSL','left',5),ac=('rd_acacSL','top',5,'rd_acacFS'))
  cmds.formLayout('form_acacMain',e=1,ac=[('if_acacFL','top',-18,'rd_acacFL'),('if_acacFL','left',5,'rd_acacFL')])
  cmds.formLayout('form_acacMain',e=1,ac=[('if_acacFS','top',-18,'rd_acacFS'),('if_acacFS','left',5,'rd_acacFS')])
  cmds.formLayout('form_acacMain',e=1,ac=[('ff_acacSL','top',-18,'rd_acacSL'),('ff_acacSL','left',5,'rd_acacSL')])
  cmds.formLayout('form_acacMain',e=1,ac=('btn_acacEx','top',10,'rd_acacSL'),af=[('btn_acacEx','left',5),('btn_acacEx','right',5),('btn_acacEx','bottom',5)])
  
 def execute(self,*a):
  jb = cmds.radioCollection('rdc_acac1',q=1,select=1)
  fl = cmds.intField('if_acacFL',q=1,value=1)
  fs = cmds.intField('if_acacFS',q=1,value=1)
  jl = cmds.floatField('ff_acacSL',q=1,value=1)

  sel = cmds.ls(selection=1)
  lenList = []
  for x in sel :
   if cmds.nodeType(x) != 'nurbsCurve' :
    for y in cmds.listRelatives(x) :
     if cmds.nodeType(y) == 'nurbsCurve' :
      x = y
   lenList.append(cmds.arclen(x))
  ll = max(lenList) / fl
  sl = min(lenList) / fs
  for x in sel :
   cvn = cmds.getAttr(x+'.spans') + cmds.getAttr(x+'.degree')
   fcvn = int(round(cmds.arclen(x)/jl))
   if jb == 'if_acacFL' : fcvn = int(round(cmds.arclen(x)/ll))
   if jb == 'if_acacFS' : fcvn = int(round(cmds.arclen(x)/sl))
   if fcvn < 4 : fcvn = 4
   if cvn != fcvn :
    cmds.rebuildCurve(x,constructionHistory=0,replaceOriginal=1,rebuildType=0,keepRange=0,spans=fcvn-3,degree=3)
  
as_crvAverageCv()

