# encoding: utf-8
import sys
import maya.cmds as cmds
import maya.mel as mel


class as_wireWeight:
 def __init__(self):
  if(cmds.window('awwUi',exists=1)):
   cmds.deleteUI('awwUi')
  cmds.window('awwUi',title='Wire Weight')


  cmds.formLayout('form_awwMain')
  cmds.text('txt_aww1',label='Falloff Curve:')
  cmds.radioCollection('rc_awwFc')
  cmds.radioButton('rb_awwLc',label='Linear',select=1)
  cmds.radioButton('rb_awwSc',label='Smooth')
  cmds.text('txt_aww3',label='Evaluation Type:')
  cmds.radioCollection('rc_awwEt')
  cmds.radioButton('rb_awwP',label='Point',select=1)
  cmds.radioButton('rb_awwL',label='Length')
  
  cmds.text('txt_aww4',label='Start Weight:')
  cmds.floatField('ff_aww1',minValue=0, maxValue=1.0, value=0.01,precision=2,width=40 )
  cmds.text('txt_aww5',label='End Weight:')
  cmds.floatField('ff_aww2',minValue=0, maxValue=1.0, value=1.0,precision=2,width=40)
  
  cmds.floatSliderGrp('fs_awwA',min=0,max=1,value=0,step=0.01,field=True)
  cmds.floatSliderGrp('fs_awwB',min=0,max=1,value=1,step=0.01,field=True)
  
  cmds.button('btn_awwEx',label='Execute',command=self.setWeight)


  cmds.window('awwUi',e=1,resizeToFitChildren=1,widthHeight=[245,200])
  cmds.showWindow('awwUi')


  cmds.formLayout('form_awwMain',e=1,af=[('txt_aww1','top',5),('txt_aww1','left',10)])
  cmds.formLayout('form_awwMain',e=1,af=('rb_awwLc','left',10),ac=('rb_awwLc','top',1,'txt_aww1'))
  cmds.formLayout('form_awwMain',e=1,ac=[('rb_awwSc','top',1,'txt_aww1'),('rb_awwSc','left',1,'rb_awwLc')])
  cmds.formLayout('form_awwMain',e=1,af=('txt_aww3','left',10),ac=('txt_aww3','top',10,'rb_awwLc'))
  cmds.formLayout('form_awwMain',e=1,af=('rb_awwP','left',10),ac=('rb_awwP','top',1,'txt_aww3'))
  cmds.formLayout('form_awwMain',e=1,ac=[('rb_awwL','top',1,'txt_aww3'),('rb_awwL','left',1,'rb_awwP')])
  cmds.formLayout('form_awwMain',e=1,af=('txt_aww4','left',10),ac=('txt_aww4','top',8,'rb_awwL'))
  cmds.formLayout('form_awwMain',e=1,ac=[('ff_aww1','top',5,'rb_awwL'),('ff_aww1','left',1,'txt_aww4')])
  cmds.formLayout('form_awwMain',e=1,ac=[('txt_aww5','top',8,'rb_awwL'),('txt_aww5','left',20,'ff_aww1')])
  cmds.formLayout('form_awwMain',e=1,ac=[('ff_aww2','top',5,'rb_awwL'),('ff_aww2','left',1,'txt_aww5')])
  cmds.formLayout('form_awwMain',e=1,af=[('fs_awwA','left',10),('fs_awwA','right',10)],ac=('fs_awwA','top',10,'txt_aww4'))
  cmds.formLayout('form_awwMain',e=1,af=[('fs_awwB','left',10),('fs_awwB','right',10)],ac=('fs_awwB','top',1,'fs_awwA'))
  cmds.formLayout('form_awwMain',e=1,af=[('btn_awwEx','left',10),('btn_awwEx','bottom',10),('btn_awwEx','right',10)],ac=('btn_awwEx','top',5,'fs_awwB'))


 def setWeight(self,*a):
  fc =  cmds.radioCollection('rc_awwFc',q=1,select=1)
  et = cmds.radioCollection('rc_awwEt',q=1,select=1)
  sr = cmds.floatSliderGrp('fs_awwA',q=1,value=1)
  er = cmds.floatSliderGrp('fs_awwB',q=1,value=1)
  sv = cmds.floatField('ff_aww1',q=1,value=1)
  ev = cmds.floatField('ff_aww2',q=1,value=1)
  
  sl = cmds.ls(selection=1,long=1)
  sls = cmds.ls(selection=1)
  selList = []
  for i,x in enumerate(sl):
   sn = sls[i]
   sp = cmds.listRelatives(x,shapes=1)[0]
   w = cmds.listConnections(sp,type='wire')[0]
   if w is not None :
    sd = cmds.getAttr(x+'.spans') + cmds.getAttr(x+'.degree')
    for j in range(sd) :
     r = float(j) / float(sd-1)
     ra = mel.eval('linstep('+str('0')+','+str(1/(ev-sv))+','+str(r)+')')+sv
     wt = mel.eval('linstep('+str(sr)+','+str(er)+','+str(ra)+')')
     if fc == 'rb_awwSc' :
      wt = mel.eval('smoothstep('+str(sr)+','+str(er)+','+str(ra)+')')
     #print wt
     cmds.percent(w,x+'.cv['+str(j)+']',v=wt)


as_wireWeight()
