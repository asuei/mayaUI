# encoding: utf-8
import maya.cmds as cmds
import re


class as_warAttr :
 def __init__(self):
  if(cmds.window('win_warAttr',exists=1)):
   cmds.deleteUI('win_warAttr')
  cmds.window('win_warAttr',title='WarAnim addAttr')

  cmds.formLayout('form_waaMain')
  #cmds.button('btn_waaATB',label='Add Body Tab',height=30,command=self.addTag)
  cmds.button('btn_waaATB',label='Add Body Tab',height=30,command=lambda *_: self.addTab('body'))
  cmds.button('btn_waaATF',label='Add Face Tab',height=30,command=lambda *_: self.addTab('face'))
  cmds.button('btn_waaATC',label='Add Tab (Input Below)',height=30,command=lambda *_: self.addTab('inputBelow'))
  cmds.textField('txt_waaATC',text='',height=23)
  cmds.separator('sprt1',style='in')
  cmds.button('btn_waaPXY',label='Add Pos XY',height=30,command=self.addPosXY)
  cmds.separator('sprt2',style='in')
  cmds.button('btn_waaAAL',label='Add Attach List (Select objects)',height=30,command=self.addAttachObjs)
  cmds.button('btn_waaAAS',label='Add Attach Side',height=30,command=self.addAttachSide)
  cmds.separator('sprt3',style='in')
  cmds.button('btn_waaASS',label='Add Shape Selection',height=30,command=self.addShape)
  cmds.button('btn_waaAWH',label='Add Width Height',height=30,command=self.addWidthHeight)
  cmds.separator('sprt4',style='in')

  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaATB','top',5),('btn_waaATB','left',5),('btn_waaATB','right',5)])
  cmds.formLayout('form_waaMain',e=1,ac=('btn_waaATF','top',5,'btn_waaATB'),af=[('btn_waaATF','left',5),('btn_waaATF','right',5)])
  cmds.formLayout('form_waaMain',e=1,ac=('btn_waaATC','top',5,'btn_waaATF'),af=[('btn_waaATC','left',5),('btn_waaATC','right',5)])
  cmds.formLayout('form_waaMain',e=1,ac=('txt_waaATC','top',5,'btn_waaATC'),af=[('txt_waaATC','left',5),('txt_waaATC','right',5)])
  cmds.formLayout('form_waaMain',e=1,af=[('sprt1','left',5),('sprt1','right',5)],ac=('sprt1','top',5,'txt_waaATC'))
  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaPXY','left',5),('btn_waaPXY','right',5)],ac=('btn_waaPXY','top',3,'sprt1'))
  cmds.formLayout('form_waaMain',e=1,af=[('sprt2','left',5),('sprt2','right',5)],ac=('sprt2','top',5,'btn_waaPXY'))
  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaAAL','left',5),('btn_waaAAL','right',5)],ac=('btn_waaAAL','top',5,'sprt2'))
  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaAAS','left',5),('btn_waaAAS','right',5)],ac=('btn_waaAAS','top',3,'btn_waaAAL'))
  cmds.formLayout('form_waaMain',e=1,af=[('sprt3','left',5),('sprt3','right',5)],ac=('sprt3','top',5,'btn_waaAAS'))
  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaASS','left',5),('btn_waaASS','right',5)],ac=('btn_waaASS','top',3,'sprt3'))
  cmds.formLayout('form_waaMain',e=1,af=[('btn_waaAWH','left',5),('btn_waaAWH','right',5)],ac=('btn_waaAWH','top',3,'btn_waaASS'))
  cmds.formLayout('form_waaMain',e=1,af=[('sprt4','left',5),('sprt4','right',5)],ac=('sprt4','top',5,'btn_waaAWH'))
  
  cmds.window('win_warAttr',e=1,widthHeight=[200,30],resizeToFitChildren=1)
  cmds.showWindow('win_warAttr')

 def addTab(self,txt,*a):
  if(txt=='inputBelow'): txt = cmds.textField('txt_waaATC',q=1,text=1)
  en = 'global:body:face'
  enList = en.split(':')
  if txt not in enList :
   en = en + ':' + txt
   enList.append(txt)
  for x in cmds.ls(selection=1):
   if cmds.objExists(x+'.warTab') == 0 :
    cmds.addAttr(x,longName='warTab',attributeType='enum',enumName=en)
    cmds.setAttr(x+'.warTab',enList.index(txt))
   else :
    cmds.warning(x+' warTab alreay exist.')

 def addPosXY(self,*a):
  for x in cmds.ls(selection=1) :
   if cmds.objExists(x+'.warPosX') == 0 :
    cmds.addAttr(x,longName='warPosX',attributeType='long')
   if cmds.objExists(x+'.warPosY') == 0 :
    cmds.addAttr(x,longName='warPosY',attributeType='long')
   
 def addAttachObjs(self,*a):
  sl = cmds.ls(selection=1)
  eList = ''
  for i,x in enumerate(sl[:-1]):
   eList = eList + x + ':'
  print(eList)
  if eList != '' :
   if cmds.objExists(sl[-1]+'.warAttach') == 0 :
    cmds.addAttr(sl[-1],longName='warAttach',attributeType='enum',enumName=eList)
   else : cmds.warning(x+'.warAttach is already exist.')
  else : cmds.warning('Select multi objects.')
    
 def addAttachSide(self,*a):
  for x in cmds.ls(selection=1) :
   if cmds.objExists(x+'.warAttachSide') == 0 :
    cmds.addAttr(x,longName='warAttachSide',attributeType='enum',enumName='none:top:bottom:left:right:topLeft:topRight:bottomLeft:bottomRight:topToLeft:topToRight:bottomToLeft:bottomToRight:leftToTop:rightToTop:leftToBottom:rightToBottom')

 def addShape(self,*a):
  for x in cmds.ls(selection=1) :
   if cmds.objExists(x+'.warShape') == 0 :
    cmds.addAttr(x,longName='warShape',attributeType='enum',enumName='rect:circle:trigU:trigD:trigL:trigR:diamond:trapezoidU:trapezoidD:hexagon')
    
 def addWidthHeight(self,*a):
  for x in cmds.ls(selection=1) :
   if cmds.objExists(x+'.warWidth') == 0 :
    cmds.addAttr(x,longName='warWidth',attributeType='long')
    cmds.setAttr(x+'.warWidth',10)
   if cmds.objExists(x+'.warHeight') == 0 :
    cmds.addAttr(x,longName='warHeight',attributeType='long')
    cmds.setAttr(x+'.warHeight',10)

as_warAttr()