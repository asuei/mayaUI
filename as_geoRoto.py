# encoding: utf-8
import maya.cmds as cmds
import re as re


class as_geoRoto :
 def __init__(self):
  if(cmds.window('win_agr',exists=1)):
   cmds.deleteUI('win_agr')
  cmds.window('win_agr',title='Geo Roto')


  cmds.formLayout('form_agrMain')
  cmds.text('txt_agrDJ',label='Source Geometry :')
  cmds.button('btn_agrDJ',label='>',width=21,height=21,command=self.defineSource)
  cmds.textField('tf_agrDJ')
  cmds.text('txt_agrJT',label='Target Geometry :')
  cmds.button('btn_agrJT',label='>',width=21,height=21,command=self.defineTarget)
  cmds.textField('tf_agrJT')
  cmds.text('txt_agrN',label='blendShape Name :')
  cmds.textField('tf_agrN')
  cmds.text('txt_agrIV',label='Keyframe Interval :')
  cmds.intField('if_agrIV',minValue=1,value=3)
  cmds.separator('sprt_agr',style='in')
  cmds.button('btn_agrE',label='Enforce',height=30,command=self.transferEnforce)


  cmds.formLayout('form_agrMain',e=1,af=[('txt_agrDJ','top',5),('txt_agrDJ','left',5)])
  cmds.formLayout('form_agrMain',e=1,ac=('btn_agrDJ','top',5,'txt_agrDJ'),af=('btn_agrDJ','left',5))
  cmds.formLayout('form_agrMain',e=1,ac=[('tf_agrDJ','top',5,'txt_agrDJ'),('tf_agrDJ','left',5,'btn_agrDJ')],af=('tf_agrDJ','right',5))
  cmds.formLayout('form_agrMain',e=1,ac=('txt_agrJT','top',5,'btn_agrDJ'),af=('txt_agrJT','left',5))
  cmds.formLayout('form_agrMain',e=1,ac=('btn_agrJT','top',5,'txt_agrJT'),af=('btn_agrJT','left',5))
  cmds.formLayout('form_agrMain',e=1,ac=[('tf_agrJT','top',5,'txt_agrJT'),('tf_agrJT','left',5,'btn_agrJT')],af=('tf_agrJT','right',5))
  cmds.formLayout('form_agrMain',e=1,ac=('txt_agrN','top',5,'btn_agrJT'),af=('txt_agrN','left',5))
  cmds.formLayout('form_agrMain',e=1,ac=('tf_agrN','top',5,'txt_agrN'),af=[('tf_agrN','left',5),('tf_agrN','right',5)])
  cmds.formLayout('form_agrMain',e=1,ac=('txt_agrIV','top',5,'tf_agrN'),af=('txt_agrIV','left',5))
  cmds.formLayout('form_agrMain',e=1,ac=[('if_agrIV','top',2,'tf_agrN'),('if_agrIV','left',5,'txt_agrIV')])
  cmds.formLayout('form_agrMain',e=1,ac=('sprt_agr','top',7,'txt_agrIV'),af=[('sprt_agr','left',5),('sprt_agr','right',5)])
  cmds.formLayout('form_agrMain',e=1,ac=('btn_agrE','top',5,'sprt_agr'),af=[('btn_agrE','left',5),('btn_agrE','right',5),('btn_agrE','bottom',5)])


  cmds.window('win_agr',e=1,widthHeight=[180,10],resizeToFitChildren=1)
  cmds.showWindow('win_agr')


 def defineSource(self,*a):
  lss = cmds.ls(selection=1)[0]
  lsl = cmds.ls(selection=1,long=1)[0]
  sp = cmds.listRelatives(lsl,shapes=1,fullPath=1)[0]
  if cmds.nodeType(sp) == 'mesh' :
   cmds.textField('tf_agrDJ',e=1,text=lss)


 def defineTarget(self,*a):
  lss = cmds.ls(selection=1)[0]
  lsl = cmds.ls(selection=1,long=1)[0]
  sp = cmds.listRelatives(lsl,shapes=1,fullPath=1)[0]
  if cmds.nodeType(sp) == 'mesh' :
   cmds.textField('tf_agrJT',e=1,text=lss)
   lc = cmds.listConnections(sp) ; bse = 0
   for x in lc :
    if cmds.nodeType(x) == 'blendShape' :
     cmds.textField('tf_agrN',e=1,text=x)
     bse = 1
   if bse==0 : cmds.textField('tf_agrN',e=1,text='')


 def transferEnforce(self,*a):
  source = cmds.textField('tf_agrDJ',q=1,text=1)
  target = cmds.textField('tf_agrJT',q=1,text=1)
  bs = cmds.textField('tf_agrN',q=1,text=1)
  ignNum = cmds.intField('if_agrIV',q=1,value=1)
  su = ['','a','b','c','d','e','f','g','h','i','j','k'] # suffix
  
  ct = int(round(cmds.currentTime(query=1)))
  pdac = cmds.polyDuplicateAndConnect(source,renameChildren=1)[0]
  tn = source.split(':')[-1]+'_'+str(ct)
  for s in su :
   if cmds.objExists(tn+s) == 0 :
    tn = tn+s
    break
  cmds.rename(pdac,tn)
  
  if bs == '' :
   bs = cmds.blendShape(tn,target)[0]
   cmds.textField('tf_agrN',e=1,text=bs)
  else :
   #wc = cmds.blendShape(bs,q=1,weightCount=1)
   bsAttr = cmds.aliasAttr(bs,q=1) ; il = []
   il = [ int(re.findall('\d+',bsAttr[i])[0]) for i in range(1,len(bsAttr),2) ]
   cmds.blendShape(bs,e=1,target=(target,max(il)+1,tn,1.0))
   
  cmds.setKeyframe(bs+'.'+tn,v=1,t=ct)
  cmds.setKeyframe(bs+'.'+tn,v=0,t=ct-ignNum)
  cmds.setKeyframe(bs+'.'+tn,v=0,t=ct+ignNum)
  cmds.select(tn,replace=1)


as_geoRoto()