# encoding: utf-8
import maya.cmds as cmds
import re as re

class as_maxMinConnect :
 def __init__(self):
  if(cmds.window('win_mmc',exists=1)):
   cmds.deleteUI('win_mmc')
  cmds.window('win_mmc',title='Max Min Connect')

  cmds.formLayout('form_mmcMain')
  cmds.text('txt_mmcNN',label='Ganarate Nodes Name :')
  cmds.button('btn_mmcNN',label='>',width=21,height=21,command=self.defineSource)
  cmds.textField('tf_mmcNN')
  cmds.separator('sprt_agr',style='in')
  cmds.button('btn_mmcT',label='Translate',height=30,command=self.transferEnforce)
  cmds.button('btn_mmcR',label='Rotate',height=30,command=self.transferEnforce)

  cmds.formLayout('form_mmcMain',e=1,af=[('txt_mmcNN','top',5),('txt_mmcNN','left',5)])
  cmds.formLayout('form_mmcMain',e=1,ac=('btn_mmcNN','top',5,'txt_mmcNN'),af=('btn_mmcNN','left',5))
  cmds.formLayout('form_mmcMain',e=1,ac=[('tf_mmcNN','top',5,'txt_mmcNN'),('tf_mmcNN','left',5,'btn_mmcNN')],af=('tf_mmcNN','right',5))
  cmds.formLayout('form_mmcMain',e=1,ac=('sprt_agr','top',7,'tf_mmcNN'),af=[('sprt_agr','left',5),('sprt_agr','right',5)])
  cmds.formLayout('form_mmcMain',e=1,ac=('btn_mmcT','top',5,'sprt_agr'),af=[('btn_mmcT','left',5),('btn_mmcT','right',5)])
  cmds.formLayout('form_mmcMain',e=1,ac=('btn_mmcR','top',5,'btn_mmcT'),af=[('btn_mmcR','left',5),('btn_mmcR','right',5),('btn_mmcR','bottom',5)])

  cmds.window('win_mmc',e=1,widthHeight=[180,10],resizeToFitChildren=1)
  cmds.showWindow('win_mmc')


 def defineSource(self,*a):
  lss = cmds.ls(selection=1)[0]
  lsl = cmds.ls(selection=1,long=1)[0]
  cmds.textField('tf_mmcNN',e=1,text=lss)

 def transferEnforce(self,*a):
  print attr
  n = cmds.textField('tf_mmcNN',q=1,text=1)
  sl = cmds.ls(selection=1)
  sL = cmds.ls(selection=1,long=1)
  
  clampList = []
  for i in range(len(sl)-2):
   
   plus = cmds.createNode('plusMinusAverage',name='plus_'+n+'_T',skipSelect=1)
   if i == 0 : cmds.connectAttr(sL[i]+'.translate',plus+'.input3D[0]')
   else : cmds.connectAttr(clampList[-1]+'.output',plus+'.input3D[0]')
   cmds.connectAttr(sL[i+1]+'.translate',plus+'.input3D[1]')
   clamp = cmds.createNode('clamp',name='clp_'+n+'_T',skipSelect=1)
   clampList.append(clamp)
   cmds.connectAttr(plus+'.output3D',clamp+'.input')

   listA = ['X','Y','Z'] ; listB = ['R','G','B']
   for a,b in zip(listA,listB):
    cds = cmds.createNode('condition',name='cds_'+n+a+'_T',skipSelect=1)
    cmds.setAttr(cds+'.operation',2)
    if i == 0 :
     cmds.connectAttr(sL[i]+'.translate'+a,cds+'.firstTerm')
     cmds.connectAttr(sL[i]+'.translate'+a,cds+'.colorIfTrue.colorIfTrueR')
     cmds.connectAttr(sL[i]+'.translate'+a,cds+'.colorIfFalse.colorIfFalseG')
    else :
     cmds.connectAttr(clampList[i-1]+'.output'+b,cds+'.firstTerm')
     cmds.connectAttr(clampList[i-1]+'.output'+b,cds+'.colorIfTrue.colorIfTrueR')
     cmds.connectAttr(clampList[i-1]+'.output'+b,cds+'.colorIfFalse.colorIfFalseG')
    cmds.connectAttr(sL[i+1]+'.translate'+a,cds+'.secondTerm')
    cmds.connectAttr(sL[i+1]+'.translate'+a,cds+'.colorIfFalse.colorIfFalseR')
    cmds.connectAttr(sL[i+1]+'.translate'+a,cds+'.colorIfTrue.colorIfTrueG')
    cmds.connectAttr(cds+'.outColor.outColorR',clamp+'.max.max'+b)
    cmds.connectAttr(cds+'.outColor.outColorG',clamp+'.min.min'+b)

   if(i==len(sl)-3) : cmds.connectAttr(clampList[-1]+'.output',sL[-1]+'.translate')
  return 0

as_maxMinConnect()