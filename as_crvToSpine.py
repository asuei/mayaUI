# encoding: utf-8
import sys
import maya.cmds as cmds

class as_crvToSpine:
 def __init__(self):
  if(cmds.window('win_ac2s',exists=1)):
   cmds.deleteUI('win_ac2s')
  cmds.window('win_ac2s',title='Curve SpineIK')

  cmds.formLayout('form_ac2sMain')
  
  cmds.text('txt_ac2sT1',label=' Joint Length : ')
  cmds.floatField('ff_ac2sJL',width=60,minValue=0.1,value=1)

  cmds.text('txt_ac2sT2',label=' Joint Axis : ')
  cmds.radioCollection('rdc_ac2sJA')
  cmds.radioButton('rd_ac2sX',label='+X',select=1)
  cmds.radioButton('rd_ac2sY',label='+Y')
  cmds.radioButton('rd_ac2sZ',label='+Z')
  cmds.radioButton('rd_ac2sx',label='-X')
  cmds.radioButton('rd_ac2sy',label='-Y')
  cmds.radioButton('rd_ac2sz',label='-Z')
  #cmds.checkBox('cb_ac2sWUO',label='set Curve to World Up Object')
  cmds.radioCollection('rdc_ac2sWU')
  cmds.radioButton('rd_ac2sWU',label='None',select=1)
  cmds.radioButton('rd_ac2sWUC',label='set Curve to World Up Object')
  cmds.radioButton('rd_ac2sWUT',label='set to')
  cmds.button('btn_ac2sST',label='>',width=20,height=20,command=self.setTo)
  cmds.textField('tf_ac2sST',width=100,height=20)
  cmds.button('btn_ac2sEx',label='Generate',width=145,height=30,command=self.generate)

  cmds.window('win_ac2s',e=1,resizeToFitChildren=1,widthHeight=[215,175])
  cmds.showWindow('win_ac2s')
  
  cmds.formLayout('form_ac2sMain',e=1,af=[('txt_ac2sT1','top',10),('txt_ac2sT1','left',5)])
  cmds.formLayout('form_ac2sMain',e=1,af=('ff_ac2sJL','top',5),ac=('ff_ac2sJL','left',5,'txt_ac2sT1'))
  cmds.formLayout('form_ac2sMain',e=1,af=[('btn_ac2sEx','bottom',5),('btn_ac2sEx','left',5)])
  cmds.formLayout('form_ac2sMain',e=1,af=('txt_ac2sT2','left',5),ac=('txt_ac2sT2','top',10,'txt_ac2sT1'))
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sX','top',10,'txt_ac2sT1'),('rd_ac2sX','left',5,'txt_ac2sT2')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sY','top',10,'txt_ac2sT1'),('rd_ac2sY','left',5,'rd_ac2sX')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sZ','top',10,'txt_ac2sT1'),('rd_ac2sZ','left',5,'rd_ac2sY')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sx','top',0,'rd_ac2sX'),('rd_ac2sx','left',5,'txt_ac2sT2')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sy','top',0,'rd_ac2sX'),('rd_ac2sy','left',5,'rd_ac2sX')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('rd_ac2sz','top',0,'rd_ac2sX'),('rd_ac2sz','left',5,'rd_ac2sY')])
  cmds.formLayout('form_ac2sMain',e=1,af=('rd_ac2sWU','left',5),ac=('rd_ac2sWU','top',0,'rd_ac2sx'))
  cmds.formLayout('form_ac2sMain',e=1,af=('rd_ac2sWUC','left',5),ac=('rd_ac2sWUC','top',1,'rd_ac2sWU'))
  cmds.formLayout('form_ac2sMain',e=1,af=('rd_ac2sWUT','left',5),ac=('rd_ac2sWUT','top',3,'rd_ac2sWUC'))
  cmds.formLayout('form_ac2sMain',e=1,ac=[('btn_ac2sST','top',3,'rd_ac2sWUC'),('btn_ac2sST','left',5,'rd_ac2sWUT')])
  cmds.formLayout('form_ac2sMain',e=1,ac=[('tf_ac2sST','top',3,'rd_ac2sWUC'),('tf_ac2sST','left',0,'btn_ac2sST')])

 def setTo(self,*a):
  cmds.textField('tf_ac2sST',e=1,text=cmds.ls(selection=1)[0])
  
 def generate(self,*a):
  jl = cmds.floatField('ff_ac2sJL',q=1,value=1)
  jax = cmds.radioCollection('rdc_ac2sJA',q=1,select=1)
  wu = cmds.radioCollection('rdc_ac2sWU',q=1,select=1)
  st = cmds.textField('tf_ac2sST',q=1,text=1)
  gik = cmds.createNode('transform',name='grp_spineIk',skipSelect=1)
  axAttr = '.translateX' ; dir = 1 ; fax = 0 ; uax = 0
  if jax in ['rd_ac2sY','rd_ac2sy'] : axAttr = '.translateY'
  if jax in ['rd_ac2sZ','rd_ac2sz'] : axAttr = '.translateZ'
  if jax in ['rd_ac2sx','rd_ac2sy','rd_ac2sz'] : dir = -1
  if jax == 'rd_ac2sY' : fax = 2 ; uax = 6
  if jax == 'rd_ac2sZ' : fax = 4 ; uax = 0
  if jax == 'rd_ac2sx' : fax = 1 ; uax = 1
  if jax == 'rd_ac2sy' : fax = 3 ; uax = 7
  if jax == 'rd_ac2sz' : fax = 5 ; uax = 1
  for x in cmds.ls(selection=1):
   len = cmds.arclen(x,constructionHistory=0)
   jn = ( len / jl ) + 1
   joList = []
   for i in range(int(jn)):
    jo = cmds.createNode('joint')
    if i > 0 : cmds.parent(jo,joList[-1])
    cmds.setAttr(jo+axAttr,jl*dir)
    joList.append(jo)
   ik = cmds.ikHandle(startJoint=joList[0],endEffector=joList[-1],sol='ikSplineSolver',createCurve=0,curve=x,parentCurve=0)
   if wu != 'rd_ac2sWU' :
    cmds.setAttr(ik[0]+'.dTwistControlEnable',1)
    cmds.setAttr(ik[0]+'.dWorldUpType',3)
    cmds.setAttr(ik[0]+'.dForwardAxis',fax)
    cmds.setAttr(ik[0]+'.dWorldUpAxis',uax)
    if wu == 'rd_ac2sWUT' :
     cmds.connectAttr(st+'.xformMatrix',ik[0]+'.dWorldUpMatrix')
   cmds.parent(ik[0],gik)
  
as_crvToSpine()

