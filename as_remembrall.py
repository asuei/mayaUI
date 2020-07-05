# encoding: utf-8
import maya.cmds as cmds
import re

class as_remembrall :
 def __init__(self):
  if(cmds.window('win_remen',exists=1)):
   cmds.deleteUI('win_remen')
  cmds.window('win_remen',title='Remembrall')

  cmds.formLayout('form_remenMain')
  
  cmds.button('btn_remenL1',label='Load',width=60,height=25,command=self.loadContentCmd('tsl_remen1'))
  cmds.textScrollList('tsl_remen1',width=60)
  cmds.button('btn_remenS1',label='Select',width=60,height=30,command=self.selectContentCmd('tsl_remen1'))
  
  cmds.button('btn_remenL2',label='Load',width=60,height=25,command=self.loadContentCmd('tsl_remen2'))
  cmds.textScrollList('tsl_remen2',width=60)
  cmds.button('btn_remenS2',label='Select',width=60,height=30,command=self.selectContentCmd('tsl_remen2'))
  
  cmds.button('btn_remenL3',label='Load',width=60,height=25,command=self.loadContentCmd('tsl_remen3'))
  cmds.textScrollList('tsl_remen3',width=60)
  cmds.button('btn_remenS3',label='Select',width=60,height=30,command=self.selectContentCmd('tsl_remen3'))

  cmds.formLayout('form_remenMain',e=1,af=[('btn_remenL1','top',5),('btn_remenL1','left',5)])
  cmds.formLayout('form_remenMain',e=1,af=[('btn_remenS1','bottom',5),('btn_remenS1','left',5)])
  cmds.formLayout('form_remenMain',e=1,ac=[('tsl_remen1','top',5,'btn_remenL1'),('tsl_remen1','bottom',5,'btn_remenS1')],af=('tsl_remen1','left',5))
  cmds.formLayout('form_remenMain',e=1,af=('btn_remenL2','top',5),ac=('btn_remenL2','left',5,'btn_remenL1'))
  cmds.formLayout('form_remenMain',e=1,af=('btn_remenS2','bottom',5),ac=('btn_remenS2','left',5,'btn_remenL1'))
  cmds.formLayout('form_remenMain',e=1,ac=[('tsl_remen2','top',5,'btn_remenL2'),('tsl_remen2','bottom',5,'btn_remenS2'),('tsl_remen2','left',5,'btn_remenS1')])
  cmds.formLayout('form_remenMain',e=1,af=('btn_remenL3','top',5),ac=('btn_remenL3','left',5,'btn_remenL2'))
  cmds.formLayout('form_remenMain',e=1,ac=[('tsl_remen3','top',5,'btn_remenL3'),('tsl_remen3','bottom',5,'btn_remenS3'),('tsl_remen3','left',5,'btn_remenS2')])
  cmds.formLayout('form_remenMain',e=1,af=('btn_remenS3','bottom',5),ac=('btn_remenS3','left',5,'btn_remenL2'))

  cmds.window('win_remen',e=1,widthHeight=[180,10],resizeToFitChildren=1)
  cmds.showWindow('win_remen')

 def loadContentCmd(self,c):
  return lambda args:self.loadContent(c)

 def loadContent(self,c,*a):
  cmds.textScrollList(c,e=1,removeAll=1)
  ls = cmds.ls(selection=1,flatten=1)
  for x in ls :
   spx = x.split('.')
   if len(spx) > 1 :
    cmds.textScrollList(c,e=1,append=('.'+spx[-1]))

 def selectContentCmd(self,c):
  return lambda args:self.selectContent(c)

 def selectContent(self,c,*a):
  ls = cmds.ls(selection=1,long=1)[0]
  sel = []
  c = cmds.textScrollList(c,q=1,allItems=1)
  for x in c :
   sel.append(ls+x)
  cmds.select(sel,replace=1)

as_remembrall()