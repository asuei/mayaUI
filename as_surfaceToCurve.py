# encoding: utf-8
import sys
import maya.cmds as cmds

class as_surfaceToCurve:
 def __init__(self):
  if(cmds.window('ancUi',exists=1)):
   cmds.deleteUI('ancUi')
  cmds.window('ancUi',title='NURBS create Curve')

  cmds.formLayout('form_ancMain')
  cmds.text('txt_anc1',label='Axis:')
  cmds.radioCollection('rc_ancUv')
  cmds.radioButton('rb_ancU',label='U')
  cmds.radioButton('rb_ancV',label='V',select=1)
  cmds.text('txt_anc3',label='Curve Control Type:')
  cmds.radioCollection('rc_ancCct')
  cmds.radioButton('rb_ancCNone',label='None',select=1)
  cmds.text('txt_anc4',label='NURBS Control Type:')
  cmds.radioCollection('rc_ancNct')
  cmds.radioButton('rb_ancNNone',label='None',select=1)
  cmds.radioButton('rb_ancWire',label='Wire')
  cmds.button('btn_ancEx',label='Execute',command=self.createCrv)

  cmds.window('ancUi',e=1,resizeToFitChildren=1,widthHeight=[245,200])
  cmds.showWindow('ancUi')

  cmds.formLayout('form_ancMain',e=1,af=[('txt_anc1','top',5),('txt_anc1','left',10)])
  cmds.formLayout('form_ancMain',e=1,af=('rb_ancU','left',10),ac=('rb_ancU','top',1,'txt_anc1'))
  cmds.formLayout('form_ancMain',e=1,ac=[('rb_ancV','top',1,'txt_anc1'),('rb_ancV','left',1,'rb_ancU')])
  cmds.formLayout('form_ancMain',e=1,af=('txt_anc3','left',10),ac=('txt_anc3','top',10,'rb_ancU'))
  cmds.formLayout('form_ancMain',e=1,af=('rb_ancCNone','left',10),ac=('rb_ancCNone','top',1,'txt_anc3'))
  cmds.formLayout('form_ancMain',e=1,af=('txt_anc4','left',10),ac=('txt_anc4','top',10,'rb_ancCNone'))
  cmds.formLayout('form_ancMain',e=1,af=('rb_ancNNone','left',10),ac=('rb_ancNNone','top',1,'txt_anc4'))
  cmds.formLayout('form_ancMain',e=1,ac=[('rb_ancWire','top',1,'txt_anc4'),('rb_ancWire','left',1,'rb_ancNNone')])
  cmds.formLayout('form_ancMain',e=1,af=[('btn_ancEx','left',10),('btn_ancEx','bottom',10),('btn_ancEx','right',10)],ac=('btn_ancEx','top',5,'rb_ancNNone'))

 def createCrv(self,*a):
  cmds.radioCollection('rc_ancUv',q=1,select=1)
  cmds.radioCollection('rc_ancCct',q=1,select=1)
  cmds.radioCollection('rc_ancNct',q=1,select=1)
  sl = cmds.ls(selection=1,long=1)
  sls = cmds.ls(selection=1)
  selList = []
  for i,x in enumerate(sl):
   sn = sls[i]
   if cmds.nodeType(x) == 'transform':
    ns = cmds.listRelatives(x,type='nurbsSurface')
    if ns : x= ns[0]
   if cmds.nodeType(x) == 'nurbsSurface':
    svAttr = '.spansV' ; vAttr = '.v' ; maxAttr = '.minMaxRangeV'
    if cmds.radioCollection('rc_ancUv',q=1,select=1) == 'rb_ancU' : svAttr = '.spansU' ; vAttr = '.u' ; maxAttr = '.minMaxRangeU'
    v = cmds.getAttr(x+svAttr)
    crvList = []
    for j in range(v):
     vv = float(j)
     if cmds.getAttr(x+maxAttr)[0][1] == 1.0 : vv = 1.0 / v * j
     dc = cmds.duplicateCurve(x+vAttr+'['+str(vv)+']',constructionHistory=0,object=1)[0]
     crvList.append(dc)
    cCrv = cmds.duplicateCurve(x+vAttr+'[0]',constructionHistory=0,object=1,name='crv_'+sls[i])[0]
    bs = cmds.blendShape(crvList,cCrv)[0]
    cmds.delete(crvList)
    for j in range(v): cmds.setAttr(bs+'.'+crvList[j],1.0/v)
    cmds.delete(cCrv,constructionHistory=1)
    selList.append(cCrv)
    if cmds.radioCollection('rc_ancNct',q=1,select=1) == 'rb_ancWire' :
     cmds.wire(x,w=cCrv,dropoffDistance=[0,100])
  if len(selList) > 0 : cmds.select(selList,replace=1)
  else : sys.stderr.write('No NURBS surface select.')

as_surfaceToCurve()

