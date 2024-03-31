# encoding: utf-8
import sys
import math
import maya.cmds as cmds
import maya.mel as mel
import re as re
import colorsys

if cmds.pluginInfo('matrixNodes',q=1,loaded=1)==0 : cmds.loadPlugin('matrixNodes')
if cmds.pluginInfo('quatNodes',q=1,loaded=1)==0 : cmds.loadPlugin('quatNodes')

class warRig:

 def __init__(self): # UI
  if(cmds.window('win_warRig',exists=1)):
   cmds.deleteUI('win_warRig')
  cmds.window('win_warRig',title='warRig')
  jobNum = cmds.scriptJob(conditionTrue=["SomethingSelected",self.limbranchSel],parent='win_warRig')
  jobNum = cmds.scriptJob(event=["SelectionChanged",self.limbranchSel],parent='win_warRig')
  jobNum = cmds.scriptJob(conditionFalse=["SomethingSelected",self.limbDisable],parent='win_warRig')

# UI Layout
  tab = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
  grid1 = cmds.gridLayout(numberOfColumns=1,cellWidth=320)
  cmds.optionMenu('aMenu',label='  Phase 1 : Adjuster                                        ',)
  cmds.menuItem( label='Biped')
  cmds.menuItem( label='Quadruped')
  cmds.menuItem( label='Bird')
  cmds.button(label='basic',command=self.basicAdjuster,backgroundColor=[0.15,0.15,0.15])
  cmds.gridLayout(numberOfRowsColumns=[1,3],cellWidth=106)
  cmds.optionMenu('limbMenu',label='',changeCommand=self.limbMenuCmd,enable=0)
  #cmds.optionMenu('limbMenu',label='',changeComma nd=self.limbMenuCmd)
  cmds.optionMenu('extraMenu1',label='',changeCommand=self.extraMenu1Cmd)
  cmds.menuItem( label='Tail')
  cmds.menuItem( label='Ear')
  cmds.menuItem( label='Tongue')
  cmds.menuItem( label='torsoAround')
  cmds.menuItem( label='extraArm')
  cmds.menuItem( label='extraLeg')
  cmds.menuItem( label='downBelow')
  cmds.optionMenu('extraMenu2',label='',changeCommand=self.extraMenu2Cmd)
  cmds.menuItem( label='backWing')
  cmds.menuItem( label='arm2Wing')
  cmds.menuItem( label='thirdEye')
  cmds.menuItem( label='extraBodyLeg')
  cmds.setParent( '..' )
  #cmds.formLayout('form_warBox')
  cmds.rowLayout(numberOfColumns=5)
  cmds.text(label=' Facial Level : ')
  cmds.radioCollection('rbtnC_facial')
  cmds.radioButton('rbtn_f1',label='simple',changeCommand=self.facialLevel,select=1)
  cmds.radioButton('rbtn_f2',label='basic')
  cmds.radioButton('rbtn_f3',label='expert',changeCommand=self.facialLevel)
  cmds.radioButton('rbtn_f4',label='master')
  cmds.setParent( '..' )
#  cmds.button(label='tail',command=self.tailAdjuster)
  if cmds.objExists('faceAdj.level'):
   fl = cmds.getAttr('faceAdj.level')
   if fl==1 : cmds.radioButton('rbtn_f1',e=1,select=1)
   elif fl==2 : cmds.radioButton('rbtn_f2',e=1,select=1)
   elif fl==3 : cmds.radioButton('rbtn_f3',e=1,select=1)
   elif fl==4 : cmds.radioButton('rbtn_f4',e=1,select=1)

  cmds.text(label='Phase 2 : Joint                                                                             ')
  cmds.button(label='Create Hierachy',command=self.createHierachy,backgroundColor=[0.15,0.15,0.15])
  cmds.button(label='Create Joint  or  Re-locating joints',command=self.createSkeleton,backgroundColor=[0.15,0.15,0.15])
  cmds.gridLayout(numberOfRowsColumns=[1,3],cellWidth=106)
  #cmds.text(label='               Fix Joint')
  cmds.optionMenu('j2Menu',label='',changeCommand=self.j2MenuCmd)
  cmds.menuItem( label='eyelidHalf')
  cmds.menuItem( label='tongueExtra')
  cmds.optionMenu('j1Menu',label='',changeCommand=self.j1MenuCmd)
  cmds.menuItem( label='armTwist')
  cmds.menuItem( label='legTwist')
  cmds.menuItem( label='elbowOut')
  cmds.menuItem( label='kneeOut')
  cmds.menuItem( label='shoulderIK')
  cmds.menuItem( label='armUpDn')
  cmds.menuItem( label='cutPelvis')
  cmds.menuItem( label='wristAdj')
  cmds.menuItem( label='fingerAssist')
  cmds.optionMenu('axisFixMenu',label='',changeCommand=self.axisFixCmd)
  cmds.menuItem( label='xPlus+z(ankle)')
  cmds.menuItem( label='xMinus+z(ankle)')
  cmds.menuItem( label='yPlus+z(arm)')
  cmds.menuItem( label='yMinus+z(arm)')
  cmds.menuItem( label='zPlus+y(wrist)')
  cmds.menuItem( label='zMinus+y(wrist)')
  cmds.setParent( '..' )
  cmds.text(label='Phase 3.0 : Controller Preset                                                      ')
  cmds.button(label='Finger Pose  or  set check animKey',command=self.fingerPosePreset)
  cmds.gridLayout(numberOfRowsColumns=[1,3],cellWidth=107)
  cmds.button(label='Ctrl Parameter',command=self.createCtrlParameter,backgroundColor=[0.34,0.34,0.34])
  cmds.button(label='Leg Rotate Pivot',command=self.legRotatePreset)
  cmds.button(label='Leg Pivot Circle',command=self.legPivotCirclePreset,backgroundColor=[0.34,0.34,0.34])
  cmds.setParent( '..' )
  cmds.gridLayout(numberOfRowsColumns=[1,3],cellWidth=107)
  cmds.button(label='Assign Hair Control',command=self.assignHairCtrl,backgroundColor=[0.34,0.34,0.34])
  cmds.setParent( '..' )
  #cmds.button(label='Ctrl Size',enable=0)

  cmds.optionMenu('oMenu',label='  Phase 3.1 : Controller                                        ',changeCommand=self.defineJoint)
  cmds.menuItem( label='default')
#  cmds.button(label='Save As..',command=self.fileSaveAs)
  btn_gc = cmds.button(label='Generate Controller',command=self.createCtrl,backgroundColor=[0.15,0.15,0.15])
  cmds.gridLayout(numberOfRowsColumns=[1,4],cellWidth=80)
  cmds.button(label='curve ctrl',enable=1,command=self.ctrlOnCurve)
  cmds.button(label='cfc(motion)',enable=1,command=self.crvFollowCrv)
  cmds.button(label='mocap',command=self.mocapJoint)
  cmds.button(label='delete ctrl',enable=1,command=self.deleteCtrl)
  cmds.setParent( '..' )
  cmds.setParent( '..' )
  form2 = cmds.formLayout()
  grid2 = cmds.gridLayout(numberOfColumns=2,cellWidth=160)
  cmds.checkBox(label='tail')
  cmds.checkBox(label='ear')
  cmds.checkBox(label='tongue')
  cmds.checkBox(label='extra arm')
  cmds.checkBox(label='extra leg')
  cmds.checkBox(label='downBelow')
  cmds.checkBox(label='back wing')
  cmds.checkBox(label='arm2 wing')
  cmds.checkBox(label='third eye')
  cmds.checkBox(label='extra body&leg')
  cmds.setParent( '..' )
  cmds.formLayout( form2, edit=True, attachForm=((grid2, 'top',10), (grid2, 'left',10), (grid2, 'bottom',10), (grid2, 'right',10)) )
  cmds.setParent( '..' )
  grid3 = cmds.gridLayout(numberOfColumns=2,cellWidth=160)
  cmds.text(label='Ctrl Curve')
  cmds.text(label='Test Animation')
  cmds.iconTextButton( style='iconAndTextHorizontal', image1='sphere.png', label='sphere' )
  cmds.iconTextButton( style='iconAndTextHorizontal', image1='sphere.png', label='sphere' )
  cmds.tabLayout(tab,e=1,tabLabel=((grid1,'Main'), (form2,'Extra Rigs'),(grid3,'Features')) )
  cmds.showWindow('win_warRig')
  self.defineJoint()

##############################################################################################################
############################################### UI Function Module ###########################################
##############################################################################################################

 def limbDisable(self,*a):
  cmds.optionMenu('limbMenu',e=1,enable=0)

 def limbranchSel(self,*a):
  mAdj = ['wristAdj','ankleAdj','wrist2Adj','ankle2Adj','rearAnkleAdj']
  aDict = {}
  aDict['wristAdj'] = ['finger','palm','wing','shoe','tarsus']
  aDict['ankleAdj'] = ['shoe','toe','paw','web','claw','hoof','tentacle']
  aDict['wrist2Adj'] = ['shoe','hoof','tarsus','batWing','finger']
  aDict['ankle2Adj'] = ['shoe','hoof','tarsus']
  aDict['rearAnkleAdj'] = ['hoof']
  sl = cmds.ls(selection=1)
  if len(sl) == 1 :
   if sl[0] in mAdj:
    cmds.optionMenu('limbMenu',e=1,enable=1)
    menuItems = cmds.optionMenu('limbMenu',q=1,itemListLong=1)
    if menuItems: cmds.deleteUI(menuItems)
    for x in aDict[sl[0]] :
     cmds.menuItem(label=x,parent='limbMenu')
   else : cmds.optionMenu('limbMenu',e=1,enable=0)
  else : cmds.optionMenu('limbMenu',e=1,enable=0)

 def limbMenuCmd(self,*a):
  sl = cmds.ls(selection=1)[0]
  lp = cmds.optionMenu('limbMenu',q=1,value=1)
  
  c = cmds.listRelatives(sl,shapes=0)
  c.remove(sl+'Shape')
  eAdj = []
  la = cmds.listAttr(sl,userDefined=1)
  for x in cmds.listRelatives(sl,shapes=0,allDescendents=1,fullPath=0) :
   if x.endswith('Adj') == 1 : eAdj.append(x)
  for x in eAdj :
   aa = cmds.listAttr(x,keyable=1)
   for y in aa :
    if la is None or x+y not in la :
     cmds.addAttr(sl,longName=x+y,attributeType='double')
    cmds.setAttr(sl+'.'+x+y,cmds.getAttr(x+'.'+y))
  
  cmds.delete(c)

  if sl == 'wristAdj' and lp == 'finger' :
   self.thumbAdjuster('thumb',sl,[1,0,0])
   self.digitAdjuster('finger',['index','middle','ring','little'],sl,[1,0,0])
  if lp == 'palm' :
   #self.thumbAdjuster('thumb',sl,[0,0,1])
   self.toeAdjuster('thumb',3,sl,[0,0,1])
   self.digitAdjuster('',['index','middle','ring','little'],'wristAdj',[0,0,1])
  if lp == 'wing' :
   self.createAdj('thumb0',sl,[0,0,0,0,0,0])
   self.createAdj('thumb1','thumb0Adj',[0,0,0,1,1,1])
   self.createAdj('index0','wristAdj',[0,0,0,0,0,0])
   self.createAdj('index1','index0Adj',[0,2,0,1,1,1])
   self.createAdj('index2','index1Adj',[0,2,0,1,1,1])
   self.createAdj('index3','index2Adj',[0,2,0,1,1,1])
  if sl == 'wristAdj' and lp == 'shoe' :
   self.createAdj('palm',sl,[0,0,0,1,1,1])
   self.createAdj('finger','palmAdj',[2,0,0,1,1,1])
  if sl == 'wristAdj' and lp == 'tarsus' :
   self.createAdj('palm',sl,[0,0,0,1,1,1])
   self.createAdj('finger','palmAdj',[2,0,0,1,1,1])
   self.createAdj('frontHoof','fingerAdj',[2,0,0,1,1,1])
   
  if sl == 'ankleAdj' and lp == 'shoe' :
   self.createAdj('ball',sl,[0,0,0,1,1,1])
   self.createAdj('toe','ballAdj',[2,0,0,1,1,1])
  if sl == 'ankleAdj' and lp == 'toe' :
   self.toeAdjuster('bigToe',3,0,sl,[0,0,1])
   self.digitAdjuster('foot',['indexToe','middleToe','fourthToe','littleToe'],'ankleAdj',[0,0,1])
  if sl == 'ankleAdj' and lp == 'paw' :
   self.digitAdjuster('',['indexToe','middleToe','fourthToe','littleToe'],'ankleAdj',[0,0,1])
  if sl == 'ankleAdj' and lp == 'web' :
   self.digitAdjuster('',['indexToe','middleToe','fourthToe'],'ankleAdj',[0,0,1])
  if sl == 'ankleAdj' and lp == 'claw' :
   self.digitAdjuster('',['bigToe','indexToe','middleToe','fourthToe'],'ankleAdj',[0,0,1])
  if sl == 'ankleAdj' and lp == 'hoof' :
   self.createAdj('ball',sl,[0,0,0,1,1,1])
   self.createAdj('toe','ballAdj',[2,0,0,1,1,1])
   self.createAdj('backHoof','toeAdj',[2,0,0,1,1,1])
  if sl == 'ankleAdj' and lp == 'tentacle' :
   self.createAdj('ball',sl,[0,0,0,1,1,1])
   self.createAdj('toe','ballAdj',[2,0,0,1,1,1])
   self.createAdj('backTentacle','toeAdj',[2,0,0,1,1,1])
  if sl == 'wrist2Adj' and lp == 'shoe' :
   self.createAdj('palm2',sl,[0,0,0,1,1,1])
   self.createAdj('finger2','palm2Adj',[2,0,0,1,1,1])
  if sl == 'wrist2Adj' and lp == 'hoof' :
   self.createAdj('palm2',sl,[0,0,0,1,1,1])
   self.createAdj('finger2','palm2Adj',[2,0,0,1,1,1])
   self.createAdj('frontHoof2','finger2Adj',[2,0,0,1,1,1])

  if sl == 'wrist2Adj' and lp == 'batWing' :
   self.toeAdjuster('wThumb',1,0,sl,[1,0,0])
   self.toeAdjuster('wIndex',3,0,sl,[1,0,0])
   self.toeAdjuster('wMiddle',3,0,sl,[1,0,0])
   self.toeAdjuster('wRing',3,0,sl,[1,0,0])
   self.toeAdjuster('wLittle',3,0,sl,[1,0,0])
  if sl == 'wrist2Adj' and lp == 'finger' :
   self.thumbAdjuster('thumb2','wrist2Adj',[1,0,0])
   self.digitAdjuster('finger2',['index2','middle2','ring2','little2'],'wrist2Adj',[1,0,0])
   
  if sl == 'ankle2Adj' and lp == 'shoe' :
   self.createAdj('ball2',sl,[0,0,0,1,1,1])
   self.createAdj('toe2','ball2Adj',[2,0,0,1,1,1])
  if sl == 'ankle2Adj' and lp == 'hoof' :
   self.createAdj('ball2',sl,[0,0,0,1,1,1])
   self.createAdj('toe2','ball2Adj',[2,0,0,1,1,1])
   self.createAdj('backHoof2','toe2Adj',[2,0,0,1,1,1])
   
  if sl == 'rearAnkleAdj' and lp == 'hoof' :
   self.createAdj('rearBall',sl,[0,0,0,1,1,1])
   self.createAdj('rearToe','rearBallAdj',[2,0,0,1,1,1])
   self.createAdj('rearHoof','rearToeAdj',[2,0,0,1,1,1])

  c = cmds.listRelatives(sl,shapes=0)
  c.remove(sl+'Shape')
  eAdj = []
  la = cmds.listAttr(sl,userDefined=1)
  for x in cmds.listRelatives(sl,shapes=0,allDescendents=1,fullPath=0) :
   if x.endswith('Adj') == 1 : eAdj.append(x)
  for x in eAdj :
   aa = cmds.listAttr(x,keyable=1)
   for y in aa :
    if la is not None and x+y in la :
     cmds.setAttr(x+'.'+y,cmds.getAttr(sl+'.'+x+y))
    else : self.adjusterPosition(x)
 
 def extraMenu1Cmd(self,*a):
  op = cmds.optionMenu('extraMenu1',q=1,value=1) ; dv = []
  if op == 'Tail' :
   if cmds.objExists('tailAdj') :
    sys.stderr.write('Tail adjuster already exist.')
   else :
    self.createAdj('tail','rootAdj',[2,0,0,1,1,1])
    self.torsoAdjuster(['tail','tailTip'],'tailAdj')
    cmds.setAttr('tailTipAdj.jointNumber',6)
    self.adjusterPosition('tailAdj','tailTipAdj')
  if op == 'Ear' :
   if cmds.objExists('earAdj') :
    sys.stderr.write('Ear adjuster already exist.')
   else :
    self.createAdj('earRoot','headAdj',[0,0,0,0,0,0])
    self.createAdj('ear','earRootAdj',[0,0,0,0,0,0])
    self.createAdj('earIn','earAdj',[0,0,0,0,0,0])
    self.createAdj('earInTip','earInAdj',[0,0,0,0,0,0])
    self.createAdj('earOut','earAdj',[0,0,0,0,0,0])
    self.createAdj('earOutTip','earOutAdj',[0,0,0,0,0,0])
    self.adjusterPosition('earRootAdj','earAdj','earInAdj','earInTipAdj','earOutAdj','earOutTipAdj')
  if op == 'torsoAround' :
   if self.exCheck(['chestFrontAdj','chestSideAdj']) :
    sys.stderr.write('Torso around adjuster already exist.')
   else :
    self.createAdj('abdomeFront','rootAdj',[2,0,0,1,1,1])
    self.createAdj('abdomeSide','rootAdj',[0,0,0,1,1,1])
    self.createAdj('spine1Front','spine1Adj',[2,0,0,1,1,1])
    self.createAdj('spine1Side','spine1Adj',[0,0,0,1,1,1])
    self.createAdj('spine2Front','spine2Adj',[2,0,0,1,1,1])
    self.createAdj('spine2Side','spine2Adj',[0,0,0,1,1,1])
    self.createAdj('chestFront','chestAdj',[2,0,0,1,1,1])
    self.createAdj('chestSide','chestAdj',[0,0,0,1,1,1])
    cmds.addAttr('chestFrontAdj',longName='jointNumber',attributeType='long')
    cmds.addAttr('chestSideAdj',longName='jointNumber',attributeType='long')
    cmds.connectAttr('chestAdj.jointNumber','chestFrontAdj.jointNumber')
    cmds.connectAttr('chestAdj.jointNumber','chestSideAdj.jointNumber')
    self.curveCtrled('gLine_chestFront',['abdomeFrontAdj','spine1FrontAdj','spine2FrontAdj','chestFrontAdj'],2)
    self.curveCtrled('gLine_chestSide',['abdomeSideAdj','spine1SideAdj','spine2SideAdj','chestSideAdj'],2)
    self.adjusterPosition('abdomeFrontAdj','abdomeSideAdj','spine1FrontAdj','spine1SideAdj','spine2FrontAdj','spine2SideAdj','chestFrontAdj','chestSideAdj')
  if op == 'Tongue' :
   if cmds.objExists('tongueAdj') :
    sys.stderr.write('Tongue adjuster already exist.')
   else :
    self.createAdj('tongue','jawAdj',[2,0,0,1,1,1])
    self.torsoAdjuster(['tongue','tongueTip'],'tongueAdj')
    cmds.setAttr('tongueTipAdj.jointNumber',5)
    self.adjusterPosition('tongueAdj','tongue1Adj','tongueTipAdj')

  if op == 'extraArm' :
   if cmds.objExists('shoulder2Adj') :
    sys.stderr.write('Extra Arm adjuster already exist.')
   else :
    self.legAdjuster(['arm2','elbow2','wrist2','shoulder2'],'chestAdj')
    self.adjusterPosition('shoulder2Adj','arm2Adj','elbow2Adj','wrist2Adj')
  if op == 'extraLeg' :
   if cmds.objExists('hip2Adj') :
    sys.stderr.write('Extra Leg adjuster already exist.')
   else :
    self.legAdjuster(['hip2','knee2','ankle2'],'rootAdj')
    self.adjusterPosition('hip2Adj','knee2Adj','ankle2Adj')
  if op == 'downBelow' :
   self.createAdj('downBelow','rootAdj',[2,0,0,1,1,1])
   self.createAdj('penis','downBelowAdj',[2,0,0,1,1,1])
   self.createAdj('scrotum','downBelowAdj',[0,0,0,1,1,1])
   self.createAdj('nut','scrotumAdj',[0,0,0,1,1,1])
   self.adjusterPosition('downBelowAdj','penisAdj','scrotumAdj')

  if dv :
   for x in dv : cmds.setAttr(x[0]+'.translate',x[1],x[2],x[3],type="double3")

 def extraMenu2Cmd(self,*a):
  op = cmds.optionMenu('extraMenu2',q=1,value=1) ; dv = []
  if op == 'backWing' :
   if cmds.objExists('backWingAdj') :
    sys.stderr.write('Back Wing adjuster already exist.')
   else :
    self.armAdjuster(['wingShoulder','wingArm','wingElbow','wingWrist'],'chestAdj' )
    #self.adjusterPosition('tailAdj','tailTipAdj')
  if op == 'arm2Wing' :
   if cmds.objExists('arm2Wing1Adj') :
    sys.stderr.write('arm2 Wing adjuster already exist.')
   else :
    self.toeAdjuster('arm2Wing1',3,0,'arm2Adj',[1,0,0])
    self.toeAdjuster('arm2Wing2',3,0,'arm2Adj',[1,0,0])
    self.toeAdjuster('arm2Wing3',3,0,'arm2Adj',[1,0,0])
    self.toeAdjuster('arm2Wing4',3,0,'arm2Adj',[1,0,0])
  if op == 'thirdEye' :
   if self.exCheck(['thirdEyeAdj']):
    sys.stderr.write('third eye adjuster already exist.')
   else:
    cmds.createNode('transform',name='thirdEyeAdj_cons',parent='faceAdj')
    cmds.parentConstraint('headAdj','thirdEyeAdj_cons')
    self.createAdj('thirdEye','thirdEyeAdj_cons',[0,0,0,0,0,0],'sphere')
    self.createAdj('thirdSight','thirdEyeAdj',[0,0,0,1,1,1],'none')
    cmds.createNode('transform',name='thirdLidAdj_cons',parent='thirdEyeAdj')
    cmds.parentConstraint('headAdj','thirdLidAdj_cons')
    self.createAdj('thirdUplidMain','thirdLidAdj_cons',[0,0,0,0,0,0],'faceSpot')
    self.createAdj('thirdLowlidMain','thirdLidAdj_cons',[0,0,0,0,0,0],'faceSpot')
    self.adjusterPosition('thirdEyeAdj','thirdSightAdj','thirdUplidMainAdj','thirdLowlidMainAdj')
  if op == 'extraBodyLeg' :
   if self.exCheck(['rearPelvisAdj']):
    sys.stderr.write('extraTorsoLeg adjuster already exist.')
   else:
    self.torsoAdjuster(['body','rearPelvis'],'rootAdj')
    cmds.setAttr('rearPelvisAdj.jointNumber',5)
    self.legAdjuster(['rearHip','rearKnee','rearAnkle'],'rearPelvisAdj')
    self.createAdj('rearTail','rearPelvisAdj',[2,0,0,1,1,1])
    self.torsoAdjuster(['rearTail','rearTailTip'],'rearTailAdj')
    cmds.setAttr('rearTailTipAdj.jointNumber',4)
    self.adjusterPosition('rearPelvisAdj','body1Adj','body2Adj','rearHipAdj','rearAnkleAdj','rearTailAdj','rearTailTipAdj')
   
 def a1MenuRemove(self,*a):
  op = cmds.optionMenu('a1Menu',q=1,value=1)
  if op == 'Tail' :
   if cmds.objExists('tailAdj') :
    cmds.delete('tailAdj')
   else :
    sys.stderr.write('Tail adjuster does not exist.')

 def j1MenuCmd(self,*a):
  op = cmds.optionMenu('j1Menu',q=1,value=1)
  if op == 'armTwist' : self.createArmTwist()
  if op == 'legTwist' : self.createLegTwist()
  if op == 'elbowOut' : self.createJointOut(self.elbowJo[0],self.elbowFixJo,self.armJo[0],'elbow','arm')
  if op == 'kneeOut' : self.createJointOut(self.kneeJo[0],self.kneeFixJo,self.hipJo[0],'knee','hip')
  if op == 'shoulderIK' : self.createShoulderIk()
  #if op == 'armUpDn' : self.createArmUpDn()
  if op == 'cutPelvis' : self.createCutPelvis()
  if op == 'wristAdj' : pass
  if op == 'fingerAssist' : self.createFingerAssist()
  if op == 'eyelidHalf' : self.createEyelidHalf()

 def j2MenuCmd(self,*a):
  op = cmds.optionMenu('j2Menu',q=1,value=1)
  if op == 'eyelidHalf' : self.createEyelidHalf()
  if op == 'tongueExtra' : self.createTongueExtra()

 def axisFixCmd(self,*a):
  op = cmds.optionMenu('axisFixMenu',q=1,value=1)
  if op == 'xPlus+z(ankle)' : self.createAxisFix('X',1,'Z')
  if op == 'xMinus+z(ankle)' : self.createAxisFix('X',-1,'Z')
  if op == 'yPlus+z(arm)' : self.createAxisFix('Y',1,'Z')
  if op == 'yMinus+z(arm)' : self.createAxisFix('Y',-1,'Z')
  if op == 'zPlus+y(wrist)' : self.createAxisFix('Z',1,'Y')
  if op == 'zMinus+y(wrist)' : self.createAxisFix('Z',-1,'Y')
  
##############################################################################################################
##############################################  Adjuster Phase ###############################################
##############################################################################################################
  
 def basicAdjuster(self,*a):
  if cmds.objExists('rootAdj') :
   sys.stderr.write('Already exist, set visibility on.')
   cmds.setAttr('rootAdj.v',keyable=1,lock=0)
   cmds.showHidden('rootAdj',above=1)
   if cmds.objExists(self.rootJo) : cmds.setAttr(self.rootJo+'.v',0)
   if cmds.objExists(self.rootJo) :
    cmds.setAttr(self.rootJo+'.overrideEnabled',1)
    cmds.setAttr(self.rootJo+'.overrideDisplayType',2)
  else :
   av = cmds.optionMenu('aMenu',q=1,value=1)

   self.createAdj('root','',[2,0,0,0,1,1])
   self.torsoAdjuster(['spine','chest'],'rootAdj')
   self.createAdj('neck','chestAdj',[2,0,0,1,1,1])
   self.torsoAdjuster(['neck','head'],'neckAdj')
   self.createAdj('top','headAdj',[2,0,0,1,1,1])
   self.facialLevel()
   if av == 'Biped' :
    cmds.setAttr('chestAdj.jointNumber',3)
    cmds.setAttr('headAdj.jointNumber',2)
    self.armAdjuster(['shoulder','arm','elbow','wrist'],'chestAdj')
    self.legAdjuster(['hip','knee','ankle'],'rootAdj')
    self.thumbAdjuster('thumb','wristAdj',[1,0,0])
    self.digitAdjuster('finger',['index','middle','ring','little'],'wristAdj',[1,0,0])
    self.createAdj('ball','ankleAdj',[0,0,0,1,1,1])
    self.createAdj('toe','ballAdj',[2,0,0,1,1,1])

   if av == 'Quadruped' :
    cmds.setAttr('chestAdj.jointNumber',5)
    self.legAdjuster(['arm','elbow','wrist','shoulder'],'chestAdj')
    self.legAdjuster(['hip','knee','ankle'],'rootAdj')
    self.toeAdjuster('thumb',3,0,'wristAdj',[0,0,1])
    self.digitAdjuster('',['index','middle','ring','little'],'wristAdj',[0,0,1])
    self.digitAdjuster('',['indexToe','middleToe','fourthToe','littleToe'],'ankleAdj',[0,0,1])
    self.createAdj('tail','rootAdj',[2,0,0,1,1,1])
    self.torsoAdjuster(['tail','tailTip'],'tailAdj')
    cmds.setAttr('tailTipAdj.jointNumber',8)

   if av == 'Bird' :
    self.armAdjuster(['shoulder','arm','elbow','wrist'],'chestAdj')
    self.createAdj('thumb0','wristAdj',[0,0,0,0,0,0])
    self.createAdj('thumb1','thumb0Adj',[0,0,0,1,1,1])
    self.createAdj('index0','wristAdj',[0,0,0,0,0,0])
    self.createAdj('index1','index0Adj',[0,2,0,1,1,1])
    self.createAdj('index2','index1Adj',[0,2,0,1,1,1])
    self.createAdj('index3','index2Adj',[0,2,0,1,1,1])
    self.legAdjuster(['hip','knee','ankle'],'rootAdj')
    self.digitAdjuster('',['indexToe','middleToe','fourthToe'],'ankleAdj',[0,0,1])
    self.createAdj('tail','rootAdj',[2,0,0,1,1,1])

   self.adjusterPosition() # set all adjuster default position
   if cmds.objExists('grp_temp') :
    p = cmds.listRelatives('rootAdj',parent=1)
    if p != 'grp_temp' : cmds.parent('rootAdj','grp_temp')
  
# torso, neck, tail adjuster module, exsample part = ['spine','chest']
 def torsoAdjuster(self,part,hrc,*a):
   cmds.createNode('transform',name=part[0]+'1Adj_ex',parent=hrc)
   self.createAdj(part[0]+'1',part[0]+'1Adj_ex',[2,0,0,1,1,1])
   cmds.createNode('transform',name=part[0]+'2Adj_ex',parent=hrc)
   cmds.createNode('transform',name=part[0]+'2Adj_cons',parent=part[0]+'1Adj')
   self.createAdj(part[0]+'2',part[0]+'2Adj_cons',[2,0,0,1,1,1])
   cmds.pointConstraint(part[0]+'2Adj_ex',part[0]+'2Adj_cons')
   cmds.createNode('transform',name=part[1]+'Adj_cons',parent=part[0]+'2Adj')
   self.createAdj(part[1],part[1]+'Adj_cons',[2,0,0,1,1,1])
   cmds.addAttr(part[1]+'Adj',longName='jointNumber',attributeType='long',min=1,max=10,defaultValue=3,keyable=1)
   cmds.pointConstraint(hrc,part[1]+'Adj_cons')

   cmds.createNode('multiplyDivide',name='multiply_'+part[0]+'1Adj')
   cmds.connectAttr(part[1]+'Adj.translate','multiply_'+part[0]+'1Adj.input1')
   cmds.setAttr('multiply_'+part[0]+'1Adj.input2',0.33333,0.33333,0.33333)
   cmds.connectAttr('multiply_'+part[0]+'1Adj.output',part[0]+'1Adj_ex.translate')
   cmds.createNode('multiplyDivide',name='multiply_'+part[0]+'2Adj')
   cmds.connectAttr(part[1]+'Adj.translate','multiply_'+part[0]+'2Adj.input1')
   cmds.setAttr('multiply_'+part[0]+'2Adj.input2',0.66666,0.66666,0.66666)
   cmds.connectAttr('multiply_'+part[0]+'2Adj.output',part[0]+'2Adj_ex.translate')

   cmds.curve(d=3,p=[(0,0,0),(0,0,0),(0,0,0),(0,0,0)],k=[0,0,0,1,1,1],name='gLine_'+part[0])
   cmds.parent('gLine_'+part[0],hrc,relative=1)
   cmds.rename(cmds.listRelatives('gLine_'+part[0],shapes=1)[0],'gLine_'+part[0]+'Shape')
   cmds.createNode('transform',name='v_'+part[0]+'1Adj',parent=hrc)
   cmds.pointConstraint(part[0]+'1Adj','v_'+part[0]+'1Adj')
   cmds.createNode('transform',name='v_'+part[0]+'2Adj',parent=hrc)
   cmds.pointConstraint(part[0]+'2Adj','v_'+part[0]+'2Adj')
   cmds.connectAttr('v_'+part[0]+'1Adj.translate','gLine_'+part[0]+'Shape.controlPoints[1]')
   cmds.connectAttr('v_'+part[0]+'2Adj.translate','gLine_'+part[0]+'Shape.controlPoints[2]')
   cmds.connectAttr(part[1]+'Adj.translate','gLine_'+part[0]+'Shape.controlPoints[3]')
   #cmds.displaySmoothness('gLine_'+part[0],divisionsU=3,pointsWire=16,pointsShaded=4,polygonObject=3)
   rCrv = cmds.rebuildCurve('gLine_'+part[0],name='gLine_'+part[0]+'Rebuild',rebuildType=1,constructionHistory=1,replaceOriginal=0,endKnots=1,keepRange=0,keepControlPoints=0 ,spans=20,degree=3)
   #cmds.parent(rCrv[0],hrc,relative=1)
   cmds.parent(rCrv[0],hrc)
   cmds.setAttr(rCrv[1]+'.rebuildType',0)
   cmds.setAttr('gLine_'+part[0]+'Rebuild.template',1)
   #cmds.setAttr('gLine_'+part[0]+'.template',1)
   cmds.setAttr('gLine_'+part[0]+'.v',0)

   cmds.createNode('condition',name='cdt_'+part[0]+'Adj2')
   cmds.setAttr('cdt_'+part[0]+'Adj2.operation',2)
   cmds.connectAttr(part[1]+'Adj.jointNumber','cdt_'+part[0]+'Adj2.firstTerm')
   cmds.setAttr('cdt_'+part[0]+'Adj2.secondTerm',2)
   cmds.setAttr('cdt_'+part[0]+'Adj2.colorIfTrueR',1)
   cmds.setAttr('cdt_'+part[0]+'Adj2.colorIfFalseR',0)
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR',part[0]+'1Adj.drawLabel')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR',part[0]+'1AdjShape.visibility')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR',part[0]+'2Adj.drawLabel')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR',part[0]+'2AdjShape.visibility')
   cmds.createNode('multDoubleLinear',name='mdl_'+part[0]+'Adj1')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR','mdl_'+part[0]+'Adj1.input1')
   cmds.setAttr('mdl_'+part[0]+'Adj1.input2',0.33333)
   cmds.connectAttr('mdl_'+part[0]+'Adj1.output','multiply_'+part[0]+'1Adj.input2X')
   cmds.connectAttr('mdl_'+part[0]+'Adj1.output','multiply_'+part[0]+'1Adj.input2Y')
   cmds.connectAttr('mdl_'+part[0]+'Adj1.output','multiply_'+part[0]+'1Adj.input2Z')
   cmds.createNode('multDoubleLinear',name='mdl_'+part[0]+'Adj2')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorR','mdl_'+part[0]+'Adj2.input1')
   cmds.setAttr('mdl_'+part[0]+'Adj2.input2',0.66666)
   cmds.connectAttr('mdl_'+part[0]+'Adj2.output','multiply_'+part[0]+'2Adj.input2X')
   cmds.connectAttr('mdl_'+part[0]+'Adj2.output','multiply_'+part[0]+'2Adj.input2Y')
   cmds.connectAttr('mdl_'+part[0]+'Adj2.output','multiply_'+part[0]+'2Adj.input2Z')
   cmds.createNode('multiplyDivide',name='multiply_'+part[0]+'Adj1Rvs')
   cmds.createNode('multiplyDivide',name='multiply_'+part[0]+'Adj2Rvs')
   cmds.connectAttr(part[0]+'1Adj.translate','multiply_'+part[0]+'Adj1Rvs.input1')
   cmds.connectAttr(part[0]+'2Adj.translate','multiply_'+part[0]+'Adj2Rvs.input1')
   cmds.createNode('multDoubleLinear',name='mdl_'+part[0]+'AdjRvs')
   cmds.connectAttr('cdt_'+part[0]+'Adj2.outColorG','mdl_'+part[0]+'AdjRvs.input1')
   cmds.setAttr('mdl_'+part[0]+'AdjRvs.input2',-1)
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj1Rvs.input2X')
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj1Rvs.input2Y')
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj1Rvs.input2Z')
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj2Rvs.input2X')
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj2Rvs.input2Y')
   cmds.connectAttr('mdl_'+part[0]+'AdjRvs.output','multiply_'+part[0]+'Adj2Rvs.input2Z')
   cmds.connectAttr('multiply_'+part[0]+'Adj1Rvs.output',part[0]+'1Adj_ex.rotatePivotTranslate')
   cmds.connectAttr('multiply_'+part[0]+'Adj2Rvs.output',part[0]+'2Adj_ex.rotatePivotTranslate')

   cmds.createNode('condition',name='cdt_'+part[0]+'Adj3')
   cmds.setAttr('cdt_'+part[0]+'Adj3.operation',2)
   cmds.connectAttr(part[1]+'Adj.jointNumber','cdt_'+part[0]+'Adj3.firstTerm')
   cmds.setAttr('cdt_'+part[0]+'Adj3.secondTerm',3)
   cmds.setAttr('cdt_'+part[0]+'Adj3.colorIfTrueR',1)
   cmds.setAttr('cdt_'+part[0]+'Adj3.colorIfFalseR',0)
   cmds.connectAttr('cdt_'+part[0]+'Adj3.outColorR','gLine_'+part[0]+'Rebuild.visibility')

 def facialLevel(self,*a):
  sel = cmds.radioCollection('rbtnC_facial',q=1,select=1)
  fclv = int(sel[-1])
  if cmds.objExists('faceAdj.level'): cmds.setAttr('faceAdj.level',fclv)
  if cmds.objExists('headAdj') == 0 : return 0
  
  if cmds.objExists('faceAdj') == 0 :
   cmds.createNode('transform',name='faceAdj_consA',parent='headAdj')
   cmds.createNode('transform',name='faceAdj_consB',parent='faceAdj_consA')
   self.createAdj('face','faceAdj_consB',[0,0,0,0,0,0],'none')
   cmds.setAttr('faceAdj.overrideDisplayType',1)
   cmds.addAttr('faceAdj',longName='level',attributeType='long',keyable=1)
   cmds.createNode('condition',name='cd_faceAdj')
   cmds.setAttr('cd_faceAdj.operation',5)
   cmds.connectAttr('cd_faceAdj.outColorR','faceAdj.tz')
   cmds.createNode('addDoubleLinear',name='adl_faceAdj')
   cmds.createNode('multDoubleLinear',name='mdl_faceAdj')
   cmds.connectAttr('adl_faceAdj.output','mdl_faceAdj.input1')
   cmds.setAttr('mdl_faceAdj.input2',0.5)
   cmds.connectAttr('mdl_faceAdj.output','faceAdj.ty')
  
  if fclv >= 1 and cmds.objExists('eyeAdj') == 0 :
   cmds.createNode('transform',name='eyeAdj_cons',parent='faceAdj')
   cmds.parentConstraint('headAdj','eyeAdj_cons')
   self.createAdj('eye','eyeAdj_cons',[0,0,0,0,0,0],'sphere')
   self.createAdj('sight','eyeAdj',[0,0,0,1,1,1],'none')
   cmds.connectAttr('eyeAdj.tz','cd_faceAdj.firstTerm')
   cmds.connectAttr('eyeAdj.tz','cd_faceAdj.colorIfTrueR')
   cmds.connectAttr('eyeAdj.ty','adl_faceAdj.input1')

  if fclv >= 1  and cmds.objExists('jawAdj') == 0 :
   cmds.createNode('transform',name='jawAdj_cons',parent='faceAdj')
   cmds.parentConstraint('headAdj','jawAdj_cons')
   self.createAdj('jaw','jawAdj_cons',[0,0,0,0,0,0],'jaw')
   self.createAdj('jawTip','jawAdj',[2,0,0,1,1,1],'faceSpot')
   cmds.connectAttr('jawAdj.tz','cd_faceAdj.secondTerm')
   cmds.connectAttr('jawAdj.tz','cd_faceAdj.colorIfFalseR')
   cmds.connectAttr('jawAdj.ty','adl_faceAdj.input2')
  
  # basic eyelid adj
  if cmds.objExists('uplidMainAdj') == 0 :
   if cmds.objExists('lidAdj_cons') == 0 :
    cmds.createNode('transform',name='lidAdj_cons',parent='eyeAdj')
    cmds.parentConstraint('headAdj','lidAdj_cons')
   self.createAdj('uplidMain','lidAdj_cons',[0,0,0,0,0,0],'faceSpot')
   
  if cmds.objExists('lowlidMainAdj') == 0 :
   if cmds.objExists('lidAdj_cons') == 0 :
    cmds.createNode('transform',name='lidAdj_cons',parent='eyeAdj')
    cmds.parentConstraint('headAdj','lidAdj_cons')
   self.createAdj('lowlidMain','lidAdj_cons',[0,0,0,0,0,0],'faceSpot')

  # eyebrow adj
  adjList = ['browAAdj','browBAdj'] # brow adj
  if self.exCheck(adjList) == 0 :
   if fclv >= 2 :
    self.createAdj('brow','headAdj',[0,0,0,0,0,0],'none')
    cmds.setAttr('browAdj.overrideDisplayType',1)
    cmds.createNode('transform',name='browAdj_cons',parent='browAdj')
    cmds.parentConstraint('headAdj','browAdj_cons')
    self.createAdj('browA','browAdj_cons',[0,0,0,0,0,0],'faceSpot')
    self.createAdj('browB','browAdj_cons',[0,0,0,0,0,0],'faceSpot')
    self.createAdj('browM','browAAdj',[0,0,0,0,0,0],'none')
    cmds.setAttr('browMAdj.overrideDisplayType',1)
    cmds.connectAttr('eyeAdj.translateX','browAdj.translateX')
    cmds.connectAttr('eyeAdj.translateZ','browAdj.translateZ')
    pmaBrow = cmds.createNode('plusMinusAverage')
    cmds.setAttr(pmaBrow+'.operation',3)
    cmds.connectAttr('browAAdj.translateY',pmaBrow+'.input1D[0]')
    cmds.connectAttr('browBAdj.translateY',pmaBrow+'.input1D[1]')
    cmds.connectAttr(pmaBrow+'.output1D','browAdj.translateY')
    cmds.createNode('multDoubleLinear',name='mdl_browMAdj')
    cmds.connectAttr('browAAdj.translateX','mdl_browMAdj.input1')
    cmds.setAttr('mdl_browMAdj.input2',-1)
    cmds.connectAttr('mdl_browMAdj.output','browMAdj.translateX')
    self.posingSet(adjList,'faceAdj')
  else :
   if fclv < 2 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete('browAdj')
  
  # basic lip(mouth) adj
  lipList = ['upLipM','upLipL1','corner','loLipL1','loLipM']
  grp = 'lipAdj_cons'
  adjList = [ x+'Adj' for x in lipList ]
  if self.exCheck(adjList) == 0 :
   if fclv >= 2 :
    cmds.createNode('transform',name=grp,parent='jawAdj',skipSelect=1)
    cmds.parentConstraint('headAdj',grp)
    for adj in lipList : self.createAdj(adj,grp,[0,0,0,0,0,0],'faceSpot')
    self.otherSideNode(adjList[1])
    self.otherSideNode(adjList[2])
    self.otherSideNode(adjList[3])
    self.posingSet(adjList,'faceAdj')
    crvCvList = [adjList[0],adjList[1],adjList[2],adjList[2],adjList[2],adjList[3],adjList[4],adjList[3]+'R',adjList[2]+'R',adjList[2]+'R',adjList[2]+'R',adjList[1]+'R',adjList[0]]
    self.guildCrv('crv_lipAdj',crvCvList,grp)
  else :
   if fclv < 2 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete('lipAdj_cons')
    
  # mouth round adj
  mouthList = ['noseUnder','noseAla','nasolabialFoldA','nasolabialFoldB','nasolabialFoldC','nasolabialFoldD']
  grp = 'mouthAdj_cons'
  adjList = [ x+'Adj' for x in mouthList ]
  if self.exCheck(adjList) == 0 :
   if fclv >= 3 :
    cmds.createNode('transform',name=grp,parent='faceAdj',skipSelect=1)
    cmds.parentConstraint('headAdj',grp)
    for adj in mouthList : self.createAdj(adj,grp,[0,0,0,0,0,0],'faceSpot')
    self.otherSideNode(adjList[1])
    #self.otherSideNode(adjList[2])
    #self.otherSideNode(adjList[3])
    self.posingSet(adjList,'faceAdj')
    crvCvList = [adjList[2],adjList[3],adjList[4],adjList[5]]
    self.guildCrv('crv_nasolabialFoldAdj',crvCvList,grp)
  else :
   if fclv < 2 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete(grp)

  # cheek adj
  grp = 'cheekAdj_cons'
  adjList = ['cheekAdj','nasalisAdj','gillAdj']
  if self.exCheck(adjList) == 0 :
   if fclv >= 3 :
    self.createAdj('chop','headAdj',[0,0,0,0,0,0],'none')
    cmds.createNode('transform',name=grp,parent='chopAdj',skipSelect=1)
    cmds.parentConstraint('headAdj',grp)
    self.createAdj('cheek',grp,[0,0,0,0,0,0],'faceSpot')
    self.createAdj('nasalis',grp,[0,0,0,0,0,0],'faceSpot')
    self.createAdj('gill',grp,[0,0,0,0,0,0],'faceSpot')
    pmaChop = cmds.createNode('plusMinusAverage',skipSelect=1)
    cmds.setAttr(pmaChop+'.operation',3)
    cmds.connectAttr('cheekAdj.translate',pmaChop+'.input3D[0]')
    cmds.connectAttr('nasalisAdj.translate',pmaChop+'.input3D[1]')
    cmds.connectAttr('gillAdj.translate',pmaChop+'.input3D[2]')
    cmds.connectAttr(pmaChop+'.output3D','chopAdj.translate')
    self.posingSet(adjList,'faceAdj')
  else :
   if fclv < 3 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete('chopAdj')
  
  # Advance eyelid adj
  advLid = ['canthusIn','uplidIn1','uplidOut1','lowlidIn1','lowlidOut1','canthusOut']
  grp = 'grp_advLidAdj'
  adjList = [ x+'Adj' for x in advLid ]
  if self.exCheck(adjList) == 0 :
   if fclv >= 3 :
    cmds.createNode('transform',name=grp,parent='lidAdj_cons',skipSelect=1)
    for adj in advLid : self.createAdj(adj,grp,[0,0,0,0,0,0],'faceSpot')
    self.posingSet(adjList,'faceAdj')
    crvCvList = [adjList[0],adjList[1],'uplidMainAdj',adjList[2],adjList[5]]
    self.guildCrv('crv_uplidAdj',crvCvList,grp)
    crvCvList = [adjList[0],adjList[3],'lowlidMainAdj',adjList[4],adjList[5]]
    self.guildCrv('crv_lowlidAdj',crvCvList,grp)
  else :
   if fclv < 3 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete(grp)
    
  # lying (under eyes) adj
  nameList = ['lyingA','lyingB','lyingC','lyingD']
  grp = 'grp_lyingAdj'
  adjList = [ x+'Adj' for x in nameList ]
  if self.exCheck(adjList) == 0 :
   if fclv >= 3 :
    cmds.createNode('transform',name=grp,parent='faceAdj',skipSelect=1)
    cmds.parentConstraint('headAdj',grp)
    for adj in nameList : self.createAdj(adj,grp,[0,0,0,0,0,0],'faceSpot')
    self.posingSet(adjList,'faceAdj')
    crvCvList = [adjList[0],adjList[1],adjList[2],adjList[3]]
    self.guildCrv('crv_lyingAdj',crvCvList,grp)
  else :
   if fclv < 2 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete(grp)
    
  # contour (face border) adj
  nameList = ['contourUpA','contourUpB','contourUpC','contourUpD','contourSideA','contourSideB','contourSideC','contourSideD','contourLowA','contourLowB','contourLowC','contourLowD']
  grp = 'grp_contourAdj'
  adjList = [ x+'Adj' for x in nameList ]
  if self.exCheck(adjList) == 0 :
   if fclv >= 3 :
    cmds.createNode('transform',name=grp,parent='faceAdj',skipSelect=1)
    cmds.parentConstraint('headAdj',grp)
    for adj in nameList : self.createAdj(adj,grp,[0,0,0,0,0,0],'faceSpot')
    self.otherSideNode(adjList[1])
    self.otherSideNode(adjList[2])
    self.otherSideNode(adjList[3])
    self.otherSideNode(adjList[4])
    self.otherSideNode(adjList[5])
    self.otherSideNode(adjList[6])
    self.otherSideNode(adjList[7])
    self.otherSideNode(adjList[8])
    self.otherSideNode(adjList[9])
    self.otherSideNode(adjList[10])
    self.posingSet(adjList,'faceAdj')
    crvCvList = [adjList[0],adjList[1],adjList[2],adjList[3],adjList[4],adjList[5],adjList[6],adjList[7],adjList[8],adjList[9],adjList[10],adjList[11],adjList[10]+'R',adjList[9]+'R',adjList[8]+'R',adjList[7]+'R',adjList[6]+'R',adjList[5]+'R',adjList[4]+'R',adjList[3]+'R',adjList[2]+'R',adjList[1]+'R',adjList[0]]
    self.guildCrv('crv_contourAdj',crvCvList,grp)
  else :
   if fclv < 2 :
    self.posingRem(adjList,'faceAdj')
    cmds.delete(grp)

# Shoulder, Arm Type adjuster module :  exsample part = ['shoulder','arm','elbow','wrist']
 def armAdjuster(self,part,hrc,*a):
  self.createAdj(part[0],hrc,[0,0,0,0,0,0])
  self.createAdj(part[1],part[0]+'Adj',[0,0,0,0,0,0])
  cmds.createNode('transform',name=part[2]+'Adj_consA',parent=part[1]+'Adj')
  cmds.createNode('transform',name=part[2]+'Adj_consB',parent=part[2]+'Adj_consA')
  cmds.createNode('transform',name=part[2]+'Adj_consC',parent=part[2]+'Adj_consA')
  self.createAdj(part[2],part[2]+'Adj_consB',[0,2,0,1,1,1])
  cmds.createNode('transform',name=part[3]+'Adj_trans1',parent=part[1]+'Adj')
  cmds.createNode('transform',name=part[3]+'Adj_trans2',parent=part[3]+'Adj_trans1')
  self.createAdj(part[3],part[3]+'Adj_trans2',[0,0,0,0,0,0])

  cmds.createNode('transform',name=part[2]+'Adj_consD',parent=part[2]+'Adj')
  cmds.aimConstraint(part[3]+'Adj',part[2]+'Adj_consD',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
  cmds.createNode('transform',name=part[3]+'Adj_cons',parent=part[3]+'Adj_trans2')
  cmds.orientConstraint(part[2]+'Adj_consD',part[3]+'Adj_cons')
  cmds.connectAttr(part[3]+'Adj_cons.rotate',part[3]+'Adj.jointOrient')

  cmds.aimConstraint(part[3]+'Adj',part[2]+'Adj_consA',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
  cmds.pointConstraint(part[3]+'Adj',part[2]+'Adj_consC')
  cmds.createNode('multiplyDivide',name='multiply_'+part[2]+'Adj_consB')
  cmds.connectAttr(part[2]+'Adj_consC.translate','multiply_'+part[2]+'Adj_consB.input1')
  cmds.setAttr('multiply_'+part[2]+'Adj_consB.input2',0.5,0.5,0.5)
  cmds.connectAttr('multiply_'+part[2]+'Adj_consB.output',part[2]+'Adj_consB.translate')
  cmds.createNode('multDoubleLinear',name='mdl_'+part[1]+'AdjSign_sz')
  cmds.curve(d=1,p=[(0,0,-.5),(0,0,.5),(1,0,-.5),(0,0,-.5),(1,0,.5),(1,0,-.5),(0,0,.5),(1,0,.5)],k=[0,1,2,3,4,5,6,7],name=part[1]+'AdjSign')
  cmds.parent(part[1]+'AdjSign',part[2]+'Adj_consA',relative=1)
  cmds.setAttr(part[1]+'AdjSign.template',1)
  cmds.connectAttr(part[2]+'Adj_consC.translateX',part[1]+'AdjSign.sx')
  cmds.connectAttr(part[2]+'Adj_consC.translateX','mdl_'+part[1]+'AdjSign_sz.input1')
  cmds.setAttr('mdl_'+part[1]+'AdjSign_sz.input2',0.5)
  cmds.connectAttr('mdl_'+part[1]+'AdjSign_sz.output',part[1]+'AdjSign.scaleZ')
  cmds.createNode('joint',name=part[2]+'AdjTemp',parent=part[2]+'Adj')
  cmds.pointConstraint(part[3]+'Adj',part[2]+'AdjTemp')
  cmds.setAttr(part[2]+'AdjTemp.radi',0)
  cmds.createNode('joint',name=part[1]+'AdjTemp',parent=part[1]+'Adj')
  cmds.pointConstraint(part[2]+'Adj',part[1]+'AdjTemp')
  cmds.setAttr(part[1]+'AdjTemp.radi',0)
  
# Leg Type adjuster module :  exsample part = ['hip','knee','ankle','4th']
# 4th can be null, if fill in, it'll have one more upper than hip
 def legAdjuster(self,part,hrc,*a):
   self.createAdj(part[0],hrc,[0,0,0,0,0,0])
   if len(part) > 3 :
    self.createAdj(part[3],hrc,[0,0,0,0,0,0])
    cmds.parent(part[0]+'Adj',part[3]+'Adj')
   cmds.createNode('transform',name=part[1]+'Adj_consA',parent=part[0]+'Adj')
   cmds.createNode('transform',name=part[1]+'Adj_consB',parent=part[1]+'Adj_consA')
   cmds.createNode('transform',name=part[1]+'Adj_consC',parent=part[1]+'Adj_consA')
   self.createAdj(part[1],part[1]+'Adj_consB',[2,0,0,1,1,1])
   cmds.createNode('transform',name=part[2]+'Adj_trans1',parent=part[0]+'Adj')
   cmds.createNode('transform',name=part[2]+'Adj_trans2',parent=part[2]+'Adj_trans1')
   self.createAdj(part[2],part[2]+'Adj_trans2',[0,0,0,0,0,0])

   cmds.aimConstraint(part[2]+'Adj',part[1]+'Adj_consA',aimVector=[0,-1,0],upVector=[0,1,0],worldUpType='none')
   cmds.pointConstraint(part[2]+'Adj',part[1]+'Adj_consC')
   cmds.createNode('multiplyDivide',name='multiply_'+part[1]+'Adj_consB')
   cmds.connectAttr(part[1]+'Adj_consC.translate','multiply_'+part[1]+'Adj_consB.input1')
   cmds.setAttr('multiply_'+part[1]+'Adj_consB.input2',0.5,0.5,0.5)
   cmds.connectAttr('multiply_'+part[1]+'Adj_consB.output',part[1]+'Adj_consB.translate')
   cmds.createNode('multDoubleLinear',name='mdl_'+part[0]+'AdjSign_sy')
   cmds.createNode('multDoubleLinear',name='mdl_'+part[0]+'AdjSign_sz')
   cmds.curve(d=1,p=[(0,0,-.5),(0,0,.5),(0,-1,-.5),(0,0,-.5),(0,-1,.5),(0,-1,-.5),(0,0,.5),(0,-1,.5)],k=[0,1,2,3,4,5,6,7],name=part[0]+'AdjSign')
   cmds.parent(part[0]+'AdjSign',part[1]+'Adj_consA',relative=1)
   cmds.setAttr(part[0]+'AdjSign.template',1)
   cmds.connectAttr(part[1]+'Adj_consC.translateY','mdl_'+part[0]+'AdjSign_sy.input1')
   cmds.setAttr('mdl_'+part[0]+'AdjSign_sy.input2',-1)
   cmds.connectAttr(part[1]+'Adj_consC.translateY','mdl_'+part[0]+'AdjSign_sz.input1')
   cmds.setAttr('mdl_'+part[0]+'AdjSign_sz.input2',-0.5)
   cmds.connectAttr('mdl_'+part[0]+'AdjSign_sy.output',part[0]+'AdjSign.scaleY')
   cmds.connectAttr('mdl_'+part[0]+'AdjSign_sz.output',part[0]+'AdjSign.scaleZ')
   cmds.createNode('joint',name=part[1]+'AdjTemp',parent=part[1]+'Adj')
   cmds.pointConstraint(part[2]+'Adj',part[1]+'AdjTemp')
   cmds.setAttr(part[1]+'AdjTemp.radi',0)
   cmds.createNode('joint',name=part[0]+'AdjTemp',parent=part[0]+'Adj')
   cmds.pointConstraint(part[1]+'Adj',part[0]+'AdjTemp')
   cmds.setAttr(part[0]+'AdjTemp.radi',0)
   cmds.createNode('transform',name=part[2]+'AdjOrient',parent=part[0]+'Adj')
   cmds.orientConstraint(hrc,part[2]+'AdjOrient')
   cmds.connectAttr(part[2]+'AdjOrient.rotate',part[2]+'Adj.jointOrient')

# finger adj module : thumb part
 def thumbAdjuster(self,name,hrc,axis,*a):
   cmds.createNode('transform',name=name+'0Adj_cons',parent=hrc)
   self.createAdj(name+'0',name+'0Adj_cons',[0,0,0,1,1,1])
   cmds.createNode('transform',name=name+'1_trans1',parent=hrc)
   cmds.createNode('transform',name=name+'1_trans2',parent=name+'1_trans1')
   self.createAdj(name+'1',name+'1_trans2',[0,0,0,0,0,0],'fingerPlane')
   cmds.createNode('joint',name=name+'0Temp',parent=name+'0Adj')
   cmds.setAttr(name+'0Temp.radius',0)
   cmds.pointConstraint(name+'1Adj',name+'0Temp')
   cmds.pointConstraint(name+'1Adj',name+'0Adj_cons')
   self.createAdj(name+'2',name+'1Adj',[0,0,2,1,1,0],'fingerPlane')
   cmds.createNode('transform',name=name+'0Adj_aCons',parent=name+'1Adj')
   cmds.aimConstraint(name+'2Adj',name+'0Adj_aCons',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
   cmds.orientConstraint(name+'0Adj_aCons',name+'0Adj_cons')
   self.createAdj(name+'3',name+'2Adj',[0,0,2,1,1,1])
   self.fingerPlaneConnect(name+'1Adj',name+'2Adj','xValue')
   self.fingerPlaneConnect(name+'2Adj',name+'3Adj','xValue')

# finger adj module : connect temp plane
 def fingerPlaneConnect(self,plane,target,value,*a):
  attr = '.tx'
  if value == 'zValue' : attr = '.tz'
  cmds.connectAttr(target+attr,plane+'.controlPoints[2].'+value)
  cmds.connectAttr(target+attr,plane+'.controlPoints[4].'+value)
  cmds.connectAttr(target+attr,plane+'.controlPoints[5].'+value)
  cmds.connectAttr(target+attr,plane+'.controlPoints[7].'+value)
  cmds.createNode('addDoubleLinear',name='adl_'+plane+'ShapeM')
  cmds.connectAttr(target+'.ty','adl_'+plane+'ShapeM.input1')
  cmds.setAttr('adl_'+plane+'ShapeM.input2',-.5)
  cmds.connectAttr('adl_'+plane+'ShapeM.output',plane+'.controlPoints[2].yValue')
  cmds.connectAttr('adl_'+plane+'ShapeM.output',plane+'.controlPoints[5].yValue')
  cmds.createNode('addDoubleLinear',name='adl_'+plane+'Shape')
  cmds.connectAttr(target+'.ty','adl_'+plane+'Shape.input1')
  cmds.setAttr('adl_'+plane+'Shape.input2',0.5)
  cmds.connectAttr('adl_'+plane+'Shape.output',plane+'.controlPoints[4].yValue')
  cmds.connectAttr('adl_'+plane+'Shape.output',plane+'.controlPoints[7].yValue')
  
# finger adj module : digit 0 part
 def digitAdjuster(self,gName,name,hrc,axis,*a):
  pAxis = [0,0,1]
  fPlane = 'fingerPlane'
  if axis == [0,0,1] :
   pAxis = [-1,0,0]
   fPlane = 'fingerPlaneZ'
  if gName != '' :
   cmds.circle(name=gName+'0Adj',normal=axis,radius=3.0)   # axis need to correct
   cmds.parent(gName+'0Adj',hrc,relative=1)
  for i in range(len(name)) :
   if gName != '' :
    cmds.createNode('transform',name=name[i]+'0Adj_cons',parent=hrc,skipSelect=1)
    self.createAdj(name[i]+'0',name[i]+'0Adj_cons',[0,0,0,1,1,1],'none')
    cmds.createNode('transform',name=name[i]+'0AdjPin',parent=gName+'0Adj',skipSelect=1)
    osv = 3 - (i+1)*(1.0/(len(name)+1))*6
    cmds.setAttr(name[i]+'0AdjPin.translate',pAxis[0]*osv,pAxis[1]*osv,pAxis[2]*osv,type="double3")
    cmds.pointConstraint(name[i]+'0AdjPin',name[i]+'0Adj_cons')
#									finger adj module : digit 1~4 part
   self.createAdj(name[i]+'1',hrc,[0,0,0,0,0,0],fPlane)
   if gName != '' :
    cmds.createNode('transform',name=name[i]+'1_trans1',parent=hrc,skipSelect=1)
    cmds.createNode('transform',name=name[i]+'1_trans2',parent=name[i]+'1_trans1',skipSelect=1)
    cmds.parent(name[i]+'1Adj',name[i]+'1_trans2',relative=1)
    cmds.createNode('joint',name=name[i]+'0Temp',parent=name[i]+'0Adj',skipSelect=1)
    cmds.setAttr(name[i]+'0Temp.radius',0)
    cmds.pointConstraint(name[i]+'1Adj',name[i]+'0Temp')

   if axis == [1,0,0] : attrStatus = [0,0,2,1,1,0] ; planeConnectValue = 'xValue'
   if axis == [0,0,1] : attrStatus = [2,0,0,0,1,1] ; planeConnectValue = 'zValue'
   self.createAdj(name[i]+'2',name[i]+'1Adj',attrStatus,fPlane)
   self.createAdj(name[i]+'3',name[i]+'2Adj',attrStatus,fPlane)
   self.createAdj(name[i]+'4',name[i]+'3Adj',attrStatus)
   self.fingerPlaneConnect(name[i]+'1Adj',name[i]+'2Adj',planeConnectValue)
   self.fingerPlaneConnect(name[i]+'2Adj',name[i]+'3Adj',planeConnectValue)
   self.fingerPlaneConnect(name[i]+'3Adj',name[i]+'4Adj',planeConnectValue)
  
 def toeAdjuster(self,name,knuckle,start,hrc,axis,*a):
  for i in range(knuckle+1):
   p = name+str(i+start-1)+'Adj'
   if i > 1 :
    cmds.createNode('transform',name='cons_'+name+str(i+start),parent=p,skipSelect=1)
    cmds.parentConstraint(name+str(start)+'Adj','cons_'+name+str(i+start))
    p = 'cons_'+name+str(i+start)
   if i == 0 : self.createAdj(name+str(i+start),hrc,[0,0,0,0,0,0],'fingerArrow')
   else : self.createAdj(name+str(i+start),p,[2,0,0,0,2,2])
   
  ap = cmds.createNode('transform',name='aCons_'+name+'Pin',parent=name+str(start)+'Adj',skipSelect=1)
  for i in range(5) :
   cmds.createNode('transform',name='pin_'+name+str(i),parent=ap,skipSelect=1)
   cmds.createNode('transform',name='v_'+name+str(i),parent=name+str(start)+'Adj',skipSelect=1)
   cmds.pointConstraint('pin_'+name+str(i),'v_'+name+str(i))
   cmds.connectAttr('v_'+name+str(i)+'.translate',name+str(start)+'AdjShape.controlPoints['+str(i)+']')

  cmds.aimConstraint(name+str(knuckle+start)+'Adj',ap,aimVector=[0,0,1],upVector=[0,1,0],worldUpType='none')
  cmds.pointConstraint(name+str(knuckle+start)+'Adj','pin_'+name+'2')
  cmds.createNode('multiplyDivide',name='mult_'+name,skipSelect=1)
  cmds.connectAttr('pin_'+name+'2.translateZ','mult_'+name+'.input1X')
  cmds.connectAttr('pin_'+name+'2.translateZ','mult_'+name+'.input1Y')
  cmds.connectAttr('pin_'+name+'2.translateZ','mult_'+name+'.input1Z')
  cmds.setAttr('mult_'+name+'.input2X',0.25)
  cmds.setAttr('mult_'+name+'.input2Y',-.25)
  cmds.setAttr('mult_'+name+'.input2Z',0.75)
  cmds.connectAttr('mult_'+name+'.outputX','pin_'+name+'0.ty')
  cmds.connectAttr('mult_'+name+'.outputX','pin_'+name+'1.ty')
  cmds.connectAttr('mult_'+name+'.outputZ','pin_'+name+'1.tz')
  cmds.connectAttr('mult_'+name+'.outputY','pin_'+name+'3.ty')
  cmds.connectAttr('mult_'+name+'.outputZ','pin_'+name+'3.tz')
  cmds.connectAttr('mult_'+name+'.outputY','pin_'+name+'4.ty')
  
# set adjuster default position
 def adjusterPosition(self,*a):
   av = cmds.optionMenu('aMenu',q=1,value=1) # Adjuster Variation
   adjList = [] ; adjDict = {}
   adjDict['rootAdj'] = (0,102.5,1.8)
   adjDict['chestAdj'] = (0,24.4,-2.4)
   adjDict['neckAdj'] = (0,17.6,-4.9)
   adjDict['headAdj'] = (0,14.15,3.9)
   adjDict['neckAdj'] = (0,17.6,-4.9)
   adjDict['topAdj'] = (0,16.4,0)
   # facial Adj
   adjDict['eyeAdj'] = (3.1,3.8,12.2)
   adjDict['sightAdj'] = (0,0,1.5)
   adjDict['browAAdj'] = (1.5,5.1,14.4)
   adjDict['browBAdj'] = (3.5,5.5,13.9)
   adjDict['uplidMainAdj'] = (3.2,4.4,13.7)
   adjDict['lowlidMainAdj'] = (3.2,3.2,13.7)
   adjDict['canthusInAdj'] = (1.8,3.3,13.4)
   adjDict['uplidIn1Adj'] = (2.4,4.2,13.6)
   adjDict['uplidOut1Adj'] = (4.1,4.1,13.5)
   adjDict['lowlidIn1Adj'] = (2.7,3.2,13.6)
   adjDict['lowlidOut1Adj'] = (4,3.3,13.4)
   adjDict['canthusOutAdj'] = (4.7,3.7,12.9)
   adjDict['thirdEyeAdj'] = (0,5.4,7.24)
   adjDict['thirdSightAdj'] = (0,0,2)
   adjDict['thirdUplidMainAdj'] = (0,5.76,8.93)
   adjDict['thirdLowlidMainAdj'] = (0,4.78,8.8)
   adjDict['jawAdj'] = (0,0.21,5.4)
   adjDict['jawTipAdj'] = (0,-5.1,8.4)
   adjDict['upLipMAdj'] = (0,-3.2,14.9)
   adjDict['upLipL1Adj'] = (1.3,-3.2,14.3)
   adjDict['cornerAdj'] = (2.3,-3.5,13.5)
   adjDict['loLipL1Adj'] = (1.3,-3.9,14.4)
   adjDict['loLipMAdj'] = (0,-4,14.6)
   adjDict['tongueAdj'] = (0,-2.4,4.9)
   adjDict['tongueTipAdj'] = (0,0.8,3.6)
   adjDict['cheekAdj'] = (3.5,3.42,8.8)
   adjDict['nasalisAdj'] = (1.75,1.85,9.9)
   adjDict['gillAdj'] = (5,-.42,6.64)
   adjDict['noseUnderAdj'] = (0,-2.2,9.1)
   adjDict['noseAlaAdj'] = (1.6,-1.4,8.2)
   adjDict['nasolabialFoldAAdj'] = (1.7,0,14.2)
   adjDict['nasolabialFoldBAdj'] = (3.2,-0.9,13.6)
   adjDict['nasolabialFoldCAdj'] = (3.9,-2.3,13.3)
   adjDict['nasolabialFoldDAdj'] = (3.5,-3.9,12.8)
   adjDict['lyingAAdj'] = (1.5,2.2,14)
   adjDict['lyingBAdj'] = (2.7,1.8,13.6)
   adjDict['lyingCAdj'] = (4.3,1.9,13.2)
   adjDict['lyingDAdj'] = (5.3,2.4,12.5)
   adjDict['contourUpAAdj'] = (0.0,10.4,13.4)
   adjDict['contourUpBAdj'] = (3.3,10.4,12.9)
   adjDict['contourUpCAdj'] = (5.9,9.7,10.7)
   adjDict['contourUpDAdj'] = (7,8.4,8.7)
   adjDict['contourSideAAdj'] = (7.7,6.4,6.5)
   adjDict['contourSideBAdj'] = (8,4,5.4)
   adjDict['contourSideCAdj'] = (7.8,1.4,5.6)
   adjDict['contourSideDAdj'] = (7.1,-1.8,5.9)
   adjDict['contourLowAAdj'] = (6.3,-4,7.1)
   adjDict['contourLowBAdj'] = (5,-5.8,9.5)
   adjDict['contourLowCAdj'] = (3.1,-6.9,12.6)
   adjDict['contourLowDAdj'] = (0.0,-7.2,14)
   # arm and leg adj
   adjDict['shoulderAdj'] = (1.3,14.6,-3.6)
   adjDict['armAdj'] = (19,0,-1.55)
   adjDict['elbowAdj'] = (0,0,0)
   adjDict['wristAdj'] = [(45.4,0,12.5),(0,0,-10)]
   adjDict['hipAdj'] = (8.98,-9.76,-1.8)
   adjDict['ankleAdj'] = (2.2,-83.6,-3)
   adjDict['ballAdj'] = (0,-6.6,11.7)
   adjDict['toeAdj'] = (0,-1.3,7) 
   # finger Adj
   adjDict['finger0Adj'] = (1.3,0,0)
   adjDict['thumb0Adj'] = (-6,-.1,0)
   adjDict['thumb1Adj'] = [(4.25,-1,6.8),(65,-50,-10)]
   adjDict['thumb2Adj'] = (3.2,0,0)
   adjDict['thumb3Adj'] = (3,0,0)
   adjDict['index1Adj'] = [(8.3,1.9,5.3),(0.5,-20,11)]
   adjDict['index2Adj'] = (3.7,0,0)
   adjDict['index3Adj'] = (2.3,0,0)
   adjDict['index4Adj'] = (2.4,0,0)
   adjDict['middle1Adj'] = [(8.8,1.9,2.86),(-9.6,-13,9.2)]
   adjDict['middle2Adj'] = (4.7,0,0)
   adjDict['middle3Adj'] = (2.5,0,0)
   adjDict['middle4Adj'] = (2.6,0,0)
   adjDict['ring1Adj'] = [(9.1,1.35,0.63),(-20,-8.3,4)]
   adjDict['ring2Adj'] = (4.1,0,0)
   adjDict['ring3Adj'] = (2.4,0,0)
   adjDict['ring4Adj'] = (2.5,0,0)
   adjDict['little1Adj'] = [(9,0.3,-1.2),(-28,-2,0)]
   adjDict['little2Adj'] = (3,0,0)
   adjDict['little3Adj'] = (2,0,0)
   adjDict['little4Adj'] = (2,0,0)
   # downBelow Adj
   adjDict['downBelowAdj'] = (0,-15,6)
   adjDict['penisAdj'] = (0,3,10)
   adjDict['scrotumAdj'] = (0,3,10)
   adjDict['nutAdj'] = (0,-1.5,0)
   # palm Adj
   adjDict['palmAdj'] = (0,-6.6,11.7)
   adjDict['fingerAdj'] = (0,-1.3,7)
   adjDict['palm2Adj'] = (0,-6.6,11.7)
   adjDict['finger2Adj'] = (0,-1.3,7)
   # tail Adj
   adjDict['tailAdj'] = (0,0,-10)
   adjDict['tailTipAdj'] = (0,-10,-60)
   # foot Adj
   adjDict['foot0Adj'] = (0,-6.8,4.6)
   adjDict['bigToe0Adj'] = (-2.7,-6.6,4.5)
   # foot Adj
   adjDict['earRootAdj'] = (7.5,3,7.4)
   adjDict['earAdj'] = (0,1.5,-0.8)
   adjDict['earInAdj'] = (-1,1.5,0.8)
   adjDict['earInTipAdj'] = (0,2,0)
   adjDict['earOutAdj'] = (1,1.5,0.8)
   adjDict['earOutTipAdj'] = (0,2,0)
   # torso around adj
   adjDict['abdomeFrontAdj'] = (0,0,10)
   adjDict['abdomeSideAdj'] = (14,0,0)
   adjDict['spine1FrontAdj'] = (0,0,10)
   adjDict['spine1SideAdj'] = (13,0,0)
   adjDict['spine2FrontAdj'] = (0,0,10)
   adjDict['spine2SideAdj'] = (14,0,0)
   adjDict['chestFrontAdj'] = (0,0,10)
   adjDict['chestSideAdj'] = (15,0,0)
   # adjDict[] = 
   adjDict['bigToe0Adj'] = [-2.2,-5.8,6]
   adjDict['bigToe1Adj'] = [-3.3,-7.5,13.1]
   adjDict['bigToe2Adj'] = [0,-.1,4.2]
   adjDict['bigToe3Adj'] = [0,0,7.1]
   adjDict['bigToe4Adj'] = [0,0,1]
   adjDict['indexToe1Adj'] = [-0.8,-7.2,13]
   adjDict['indexToe2Adj'] = [0,0.4,3.6]
   adjDict['indexToe3Adj'] = [0,-0.8,1.4]
   adjDict['indexToe4Adj'] = [0,-0.9,1.3]
   adjDict['middleToe1Adj'] = [0.7,-7.4,12.7]
   adjDict['middleToe2Adj'] = [0,0.4,3.1]
   adjDict['middleToe3Adj'] = [0,-0.8,1.7]
   adjDict['middleToe4Adj'] = [0,-0.6,1.2]
   adjDict['fourthToe1Adj'] = [2,-7.3,12.5]
   adjDict['fourthToe2Adj'] = [0,0,2]
   adjDict['fourthToe3Adj'] = [0,-0.6,1.5]
   adjDict['fourthToe4Adj'] = [0,-0.8,1.3]
   adjDict['littleToe1Adj'] = [3.4,-7.7,12.2]
   adjDict['littleToe2Adj'] = [0,-0.3,2]
   adjDict['littleToe3Adj'] = [0,-0.3,0.8]
   adjDict['littleToe4Adj'] = [0,-0.4,1.1]
   
   adjDict['backHoofAdj'] = [0,-1,0]
   adjDict['rearBallAdj'] = [0,-30,3.5]
   adjDict['rearToeAdj'] = [0,-2.4,3]
   adjDict['rearHoofAdj'] = [0,-3.6,1]

   adjDict['shoulder2Adj'] = (1.3,10,-3.6)
   adjDict['arm2Adj'] = (15,0,-1.55)
   adjDict['wrist2Adj'] = (45.4,0,12.5)
   adjDict['hip2Adj'] = (9,-9.8,-24)
   adjDict['knee2Adj'] = (0,0,0)
   adjDict['ankle2Adj'] = (2.2,-83.6,-3)
   adjDict['ball2Adj'] = (0,-6.6,11.7)
   adjDict['toe2Adj'] = (0,-1.3,7)

   adjList += [('finger20Adj',(1.3,0,0)),('thumb20Adj',(-6,-.1,0)),('thumb21Adj',(4.25,-1,6.8),(65,-50,-10)),('thumb22Adj',(3.2,0,0)),('thumb23Adj',(3,0,0))]
   adjList += [('index20Adj',(0,0,0)),('index21Adj',(8.3,1.9,5.3),(0.5,-20,11)),('index22Adj',(3.7,0,0)),('index23Adj',(2.3,0,0)),('index24Adj',(2.4,0,0))]
   adjList += [('middle20Adj',(0,0,0)),('middle21Adj',(8.8,1.9,2.86),(-9.6,-13,9.2)),('middle22Adj',(4.7,0,0)),('middle23Adj',(2.5,0,0)),('middle24Adj',(2.6,0,0))]
   adjList += [('ring20Adj',(0,0,0)),('ring21Adj',(9.1,1.35,0.63),(-20,-8.3,4)),('ring22Adj',(4.1,0,0)),('ring23Adj',(2.4,0,0)),('ring24Adj',(2.5,0,0))]
   adjList += [('little20Adj',(0,0,0)),('little21Adj',(9,0.3,-1.2),(-28,-2,0)),('little22Adj',(3,0,0)),('little23Adj',(2,0,0)),('little24Adj',(2,0,0))]
   adjList += [('wThumb0Adj',[0,0,0]),('wThumb1Adj',[0,0,0]),('wIndex0Adj',[0,0,0]),('wIndex1Adj',[0,0,0]),('wIndex2Adj',[0,0,0]),('wIndex3Adj',[0,0,0])]
   adjList += [('wMiddle0Adj',[0,0,0]),('wMiddle1Adj',[0,0,0]),('wMiddle2Adj',[0,0,0]),('wMiddle3Adj',[0,0,0])]
   adjList += [('wRing0Adj',[0,0,0]),('wRing1Adj',[0,0,0]),('wRing2Adj',[0,0,0]),('wRing3Adj',[0,0,0])]
   adjList += [('wLittle0Adj',[0,0,0]),('wLittle1Adj',[0,0,0]),('wLittle2Adj',[0,0,0]),('wLittle3Adj',[0,0,0])]
   adjList += [('rearPelvisAdj',[0,-11,-90]),('body1Adj',[0,-3,0]),('body2Adj',[0,-3.5,0]),('rearHipAdj',[8.98,-9.76,-1.8]),('rearAnkleAdj',[2.2,-72.3,-3])]
   adjList += [('rearTailAdj',(0,-0.8,-4.6)),('rearTailTipAdj',(0,-17.9,-60))]
	
   if av == 'Quadruped' :
    adjList += [('rootAdj',(0,76.53,-40.27)),('chestAdj',(0,-5.7,80.87)),('neckAdj',(0,-.7,8.3)),('headAdj',(0,5.5,22.4)),('topAdj',(0,8.5,0))]
    adjList += [('eyeAdj',(4.4,-2.8,12.8)),('browAAdj',(2.9,-1.2,16.2)),('browBAdj',(4.8,-0.8,14.8)),('uplidMainAdj',(4.8,-2.1,14.6)),('lowlidMainAdj',(4.9,-3.8,13.9))]
    adjList += [('jawAdj',(0,-8.9,4.8)),('jawTipAdj',(0,-12,5.7)),('upLidMAdj',(0,-14.6,18.6)),('upLidSAdj',(3.5,-15.6,15.8)),('cornerAdj',(4,-13.5,10.1)),('loLidSAdj',(3.3,-17.2,10.7)),('loLidMAdj',(0,-18.8,13.2))]
    adjList += [('shoulderAdj',(5.4,9.7,-0.2)),('armAdj',(2.8,-22.4,-9.9)),('wristAdj',(0,-44,10.2),(0,0,0))]
    adjList += [('thumb0Adj',(-3.2,-3.9,0),(-38.4,3.9,-17.1)),('thumb1Adj',(0,-4,0)),('thumb2Adj',(-4.8,-2.5,0)),('thumb3Adj',(-7.1,-3.1,0))]
    adjList += [('index1Adj',(-3.1,-10.3,1.3),(0,0,0)),('index2Adj',(0,-0.1,4.3)),('index3Adj',(0,-3.2,0.1)),('index4Adj',(0,-0.1,2.1))]
    adjList += [('middle1Adj',(-0.9,-10.2,2.4),(0,0,0)),('middle2Adj',(0,0.4,4.7)),('middle3Adj',(0,-3.9,0.5)),('middle4Adj',(0,0,2))]
    adjList += [('ring1Adj',(1.6,-10.2,2),(0,0,0)),('ring2Adj',(0,0.4,4.5)),('ring3Adj',(0,-3.8,0.4)),('ring4Adj',(0,-0.1,2.5))]
    adjList += [('little1Adj',(3.7,-10.3,0.2),(0,0,0)),('little2Adj',(0,-.1,4.1)),('little3Adj',(0,-3.2,0)),('little4Adj',(0,0,2.2))]
    adjList += [('hipAdj',(6.6,-4.7,-0.8)),('ankleAdj',(0,-53.3,-10.7)),('ballAdj',(0,-6.6,11.7)),('toeAdj',(0,-1.3,7))]
    adjList += [('indexToe1Adj',(-2.6,-14.4,2.8)),('indexToe2Adj',(0,-0.4,4.2)),('indexToe3Adj',(0,-3.4,0)),('indexToe4Adj',(0,-0.1,1,6))]
    adjList += [('middleToe1Adj',(-0.5,-14.5,3.8)),('middleToe2Adj',(0,0.2,5)),('middleToe3Adj',(0,-3.8,0.4)),('middleToe4Adj',(0,-0.1,1.5))]
    adjList += [('fourthToe1Adj',(1.9,-14.5,3.6)),('fourthToe2Adj',(0,0.2,4.8)),('fourthToe3Adj',(0,-3.9,-0.1)),('fourthToe4Adj',(0,0,1.6))]
    adjList += [('littleToe1Adj',(3.8,-14.4,2.4)),('littleToe2Adj',(0,-0.5,3.5)),('littleToe3Adj',(0,-3.3,0.2)),('littleToe4Adj',(0,0,1.5))]
    adjList += [('tailAdj',(0,-0.8,-4.6)),('tailTipAdj',(0,-17.9,-90.3))]

   if av == 'Bird' :
    adjList += [('rootAdj',(0,8.8,-4.2)),('chestAdj',(0,1.7,3.24)),('neckAdj',(0,1.24,2.5)),('headAdj',(0,4.3,0)),('topAdj',(0,2,0)),('tailAdj',(0,-.3,-.9))]
    adjList += [('eyeAdj',(0.6,1.5,1.2)),('browAAdj',(0.7,1.7,1.6)),('browBAdj',(0.8,1.8,1.3)),('uplidMainAdj',(0.9,1.7,1.3)),('lowlidMainAdj',(0.9,1.2,1.3))]
    adjList += [('cheekAdj',(0.86,1,1.5)),('nasalisAdj',(0.75,0.7,2)),('gillAdj',(0.88,0.4,1.7))]
    adjList += [('shoulderAdj',(0.85,1,1)),('armAdj',(1.6,0,0)),('elbowAdj',(0,0,0)),('wristAdj',(8.9,0.6,1.2),(0,0,-8.5))]
    adjList += [('thumb0Adj',(0.5,0,0.1),(0,20,0)),('thumb1Adj',(0.8,0,0))]
    adjList += [('index0Adj',(0.3,0,-0.1)),('index1Adj',(1.2,0,-0.5)),('index2Adj',(0.7,0,-0.3)),('index3Adj',(0.4,0,-0.2))]
    adjList += [('hipAdj',(1.8,-1,1.3)),('ankleAdj',(-.4,-7,0.5),(0,12.5,0)),('ballAdj',(0,-6.6,11.7)),('toeAdj',(0,-1.3,7))]
    adjList += [('jawAdj',(0,0.24,1.52)),('jawTipAdj',(0,-1.3,2.7)),('upLidMAdj',(0,0.27,4.75)),('upLidSAdj',(0.6,0.48,2.28)),('cornerAdj',(0.57,0.27,2.18)),('loLidSAdj',(0.55,0.05,2.3)),('loLidMAdj',(0,-1,4.2))]
    adjList += [('toeFinger0Adj',(0.05,-.3,0.2),(0,0,0),(0.15,0.15,0.15))]
    adjList += [('indexToe1Adj',(-.3,-0.5,0.6),(0,-32.5,0)),('indexToe2Adj',(0,-0.2,1)),('indexToe3Adj',(0,-0.1,0.7)),('indexToe4Adj',(0,0,0.5))]
    adjList += [('middleToe1Adj',(0,-0.5,0.7),(0,-2.5,0)),('middleToe2Adj',(0,-0.2,0.9)),('middleToe3Adj',(0,-0.1,1.3)),('middleToe4Adj',(0,0,0.5))]
    adjList += [('fourthToe1Adj',(0.4,-0.5,0.5),(0,27.5,0)),('fourthToe2Adj',(0,-0.2,0.9)),('fourthToe3Adj',(0,0,1.2)),('fourthToe4Adj',(0,0,0.5))]

   if len(a) == 0 :
    for x in adjDict.items() :
     if isinstance(x[1],tuple) :
      try : cmds.setAttr(x[0]+'.translate',x[1][0],x[1][1],x[1][2],type="double3")
      except : pass
     if isinstance(x[1],list) :
      try : cmds.setAttr(x[0]+'.translate',x[1][0][0],x[1][0][1],x[1][0][2],type="double3")
      except : pass
      try : cmds.setAttr(x[0]+'.rotate',x[1][1][0],x[1][1][1],x[1][1][2],type="double3")
      except : pass
      try : cmds.setAttr(x[0]+'.scale',x[1][2][0],x[1][2][1],x[1][2][2],type="double3")
      except : pass
   else :
    for x in a :
     t = adjDict.get(x,(0,0,0))
     try : cmds.setAttr(x+'.translate',t[0],t[1],t[2],type="double3")
     except : pass

##############################################################################################################
############################################## Joint Create Phase ############################################
##############################################################################################################
 def defineJoint(self,*a):
  self.joId = {'root':13000,'pelvis':13200,'pelvisL':13500
  ,'head':1500,'face':2000,'jaw':2800
  ,'neck':3500,'neck1':3510,'neck2':3520
  ,'chest':4200,'shoulderL':5200
  ,'spine2':12300,'spine1':12400,'spine0':12500
  ,'armL':7200,'armTw0L':7250,'armTw1L':7260,'armTw2L':7270,'armTw3L':7280,'armTw4L':7290
  ,'elbowL':7700,'elbowTw0L':7750,'elbowTw1L':7760,'elbowTw2L':7770,'elbowTw3L':7780,'elbowTw4L':7790
  ,'wristL':8200,'thumb0L':8400,'thumb1L':8410,'thumb2L':8420
  ,'index0L':8500,'index1L':8510,'index2L':8520,'index3L':8530
  ,'middle0L':8600,'middle1L':8610,'middle2L':8620,'middle3L':8630
  ,'ring0L':8700,'ring1L':8710,'ring2L':8720,'ring3L':8730
  ,'little0L':8800,'little1L':8810,'little2L':8820,'little3L':8830
  ,'hipL':14200,'hipTw0L':14250,'hipTw1L':14260,'hipTw2L':14270,'hipTw3L':14280,'hipTw4L':14290
  ,'kneeL':14700,'kneeTw0L':14750,'kneeTw1L':14760,'kneeTw2L':14770,'kneeTw3L':14780,'kneeTw4L':14790
  ,'ankleL':15200,'ballL':15450
  }
  
  self.rootJo = 'jo_root'
  self.pelvisJo = 'jo_pelvis'
  self.pelvisSplitJo = 'jo_pelvisL'
  self.downBelong = ['jo_penis','jo_penisTip','jo_scrotumL','jo_scrotumTipL']
  self.spineJo = ['jo_spine0','jo_spine1','jo_spine2','jo_spine3','jo_spine4','jo_spine5','jo_spine6','jo_spine7','jo_spine8','jo_spine9']
  self.spineFront = [ 'jcB02_spine0F','jcB12_spine1F','jcB22_spine2F','jcB32_spine3F','jcB42_spine4F','jcB52_spine5F','jcB62_spine6F','jcB72_spine7F','jcB82_spine8F','jcB92_spine9F' ]
  self.spineSide = [ 'jlB04_spine0L','jlB14_spine1L','jlB24_spine2L','jlB34_spine3L','jlB44_spine4L','jlB54_spine5L','jlB64_spine6L','jlB74_spine7L','jlB84_spine8L','jlB94_spine9L' ]
  self.tailJo = ['jo_tail0','jo_tail1','jo_tail2','jo_tail3','jo_tail4','jo_tail5','jo_tail6','jo_tail7','jo_tail8','jo_tail9']
  self.tailTip = 'jo_tailTip'
  self.chestJo = 'jo_chest'
  self.chestJoList = [self.chestJo]
  self.chestRound = ['jcC02_chestF','jlC04_chestL']
  self.neckJo = ['jo_neck','jo_neck1','jo_neck2','jo_neck3','jo_neck4','jo_neck5','jo_neck6','jo_neck7','jo_neck8','jo_neck9']
  self.headJo = 'jo_head'
  self.topJo = 'jo_top'
  self.faceJo = 'jo_face'
  self.browJo = ['jo_browM','jo_browL','jo_browMidL']
  
  self.eyeJo = 'jo_eyeL'
  self.specJo = ['jlF21_specAL','jlF22_specBL']
  self.uplidJo = ['jlF23_upLidRotL','jlF24_upLidL','jlF25_upLidHalfRotL','jlF26_upLidHalfL']
  self.lolidJo = ['jlF27_loLidRotL','jlF28_loLidL','jlF29_loLidHalfRotL','jlF30_loLidHalfL']
  self.thirdEyeJo = 'jcF20_thirdeye'


  self.lidJo = ['jo_upLidRotL','jo_upLidL','jo_loLidRotL','jo_loLidL']
  self.thirdLidJo = ['jo_thirdUpLidRot','jo_thirdUpLid','jo_thirdLoLidRotL','jo_thirdLoLidL']
  self.lidHalfJo = [['jlF25_upLidHalfRotL','jlF26_upLidHalfL','jlF29_loLidHalfRotL','jlF30_loLidHalfL'],[]]
  
  self.cheekJo = ['jo_cheekL','jo_nasalisL','jo_gillL']
  self.jawJo = ['jo_jaw','jo_jawTip']
  self.lipJo = ['jo_lipUp','jo_lipUpBL','jo_CornerL','jo_lipLoBL','jo_lipLo']
  self.tongueJo = ['jo_tongue0','jo_tongue1','jo_tongue2','jo_tongue3','jo_tongue4','jo_tongue5','jo_tongue6','jo_tongue7','jo_tongue8','jo_tongue9']
  self.tongueLJo = ['jcF90_tongue0L','jcF91_tongue1L','jcF92_tongue2L','jcF93_tongue3L','jcF94_tongue4L','jcF95_tongue5L','jcF96_tongue6L','jcF97_tongue7L','jcF98_tongue8L','jcF99_tongue9L']
  self.tongueRJo = ['jcF90_tongue0R','jcF91_tongue1R','jcF92_tongue2R','jcF93_tongue3R','jcF94_tongue4R','jcF95_tongue5R','jcF96_tongue6R','jcF97_tongue7R','jcF98_tongue8R','jcF99_tongue9R']
  self.tongueTipJo = 'jcF0A_tongueTip'
  self.earJo = ['jo_earRootL','jo_earL','jo_earInL','jo_earInTipL','jo_earOutL','jo_earOutTipL']

  self.bodyJo = ['jo_body0','jo_body1','jo_body2','jo_body3','jo_body4','jo_body5','jo_body6','jo_body7','jo_body8','jo_body9']
  self.rearPelvisJo = 'jo_rearPelvis'
  self.rearHipJo = 'jo_rearHipL' ; self.rearKneeJo = 'jo_rearKneeL' ; self.rearAnkleJo = 'jo_rearAnkleL'
  self.rearBallJo = 'jo_rearBallL' ; self.rearToeJo = 'jo_rearToeL' ; self.rearHoofJo = 'jo_rearHoofL'
  self.rearTailJo = ['jo_rearTail0','jo_rearTail1','jo_rearTail2','jo_rearTail3','jo_rearTail4','jo_rearTail5','jo_rearTail6','jo_rearTail7','jo_rearTail8','jo_rearTail9']
  self.rearTailTip = 'jo_rearTailTip'
  self.rearHipTwist = ['jo_rearHipTw0L','jo_rearHipTw1L','jo_rearHipTw2L','jo_rearHipTw3L','jo_rearHipTw4L']
  self.rearKneeTwist = ['jo_rearKneeTw0L','jo_rearKneeTw1L','jo_rearKneeTw2L','jo_rearKneeTw3L','jo_rearKneeTw4L']
  
  self.hipJo = ['jo_hipL','jo_hipR']
  self.hip2Jo = ['jo_hip2L','jo_hip2R']
  self.hipTwist = ['jo_hipTw0L','jo_hipTw1L','jo_hipTw2L','jo_hipTw3L','jo_hipTw4L']
  
  self.kneeJo = ['jo_kneeL','jo_kneeR']
  self.kneeOutJo = 'jlH10_kneeOutL'
  self.kneeTwist = ['jo_kneeTw0L','jo_kneeTw1L','jo_kneeTw2L','jo_kneeTw3L','jo_kneeTw4L']
  self.kneeFixJo = ['jlH10_kneeOutL','jlG90_kneePullL','jlH15_kneePushL']
  self.knee2Jo = ['jo_knee2L','jo_knee2R']
  
  self.ankleJo = ['jo_ankleL','jo_ankleR']
  self.ankle2Jo = ['jo_ankle2L','jo_ankle2R']
  
  self.ballJo = ['jo_ballL','jo_ballR']
  self.toeJo = ['jo_toeL','jo_toeR']
  self.shoe2Jo = ['jo_ball2L','jo_toe2L']
  self.bigToeJo = ['jo_bigToe0L','jo_bigToe1L','jo_bigToe2L','jo_bigToe3L']
  self.indexToeJo = ['jo_toeIndex0L','jo_toeIndex1L','jo_toeIndex2L','jo_toeIndex3L','jo_toeIndex4L']
  self.middleToeJo = ['jo_toeMiddle0L','jo_toeMiddle1L','jo_toeMiddle2L','jo_toeMiddle3L','jo_toeMiddle4L']
  self.fourthToeJo = ['jo_toeRing0L','jo_toeRing1L','jo_toeRing2L','jo_toeRing3L','jo_toeRing4L']
  self.littleToeJo = ['jo_toeLittle0L','jo_toeLittle1L','jo_toeLittle2L','jo_toeLittle3L','jo_toeLittle4L']

  self.bHoofJo = 'jo_backHoofL'
  self.bHoof2Jo = 'jo_backHoof2L'
  
  self.midLimbJo = ['jlL80_midHipL','jlL85_midKneeL','jlL90_midAnkleL']
  
  self.shoulderJo = ['jo_shoulderL','jo_shoulderR']
  self.shoulderTwist = 'jo_shoulderTwL'
  self.armJo = ['jo_armL','jo_armR']
  self.armTwist = ['jo_armTw0L','jo_armTw1L','jo_armTw2L','jo_armTw3L','jo_armTw4L']
  self.armFix = ['jlN05_armUpL','jlN06_armDnL','jlN07_armFtL','jlN08_armBkL','jlN09_armInL','jlN10_armOtL']
  self.elbowJo = ['jo_elbowL','jo_elbowR']
  self.elbowTwist = ['jo_elbowTw0L','jo_elbowTw1L','jo_elbowTw2L','jo_elbowTw3L','jo_elbowTw4L']
  self.elbowOutJo = 'jo_elbowOutL'
  self.elbowFixJo = ['jo_elbowOutL','jo_elbowPullL','jo_elbowPushL']
  self.wristJo = ['jo_wristL','jo_wristR']
  self.fShoeJo = ['jlR00_palmL','jlR50_fingerL']
  self.fHoofJo = ['jlR00_palmL','jlR50_fingerL','jlR90_frontHoofL']

  self.shoulder2Jo = ['jlM50_shoulder2L','jrM50_shoulder2R']
  self.elbow2Jo = ['jlP50_elbow2L','jrP50_elbow2R']
  self.viceElbowTwist = ['jlP55_viceElbow0L','jlP60_viceElbow1L','jlP65_viceElbow2L','jlP70_viceElbow3L','jlP75_viceElbow4L']
  self.arm2Jo = ['jlN50_arm2L','jrN50_arm2R']
  self.viceArmTwist = ['jlN55_viceArmTw0L','jlN60_viceArmTw1L','jlN65_viceArmTw2L','jlN70_viceArmTw3L','jlN75_viceArmTw4L']
  self.wrist2Jo = ['jlQ50_wrist2L','jrQ50_wrist2R']

  self.fShoe2Jo = ['jlR60_palm2L','jlR70_finger2L']
  self.fHoof2Jo = ['jlR50_palm2L','jlR70_finger2L','jlR90_frontHoof2L']

  self.thumbJo =  ['jo_thumb0L','jo_thumb1L','jo_thumb2L','jo_thumb3L']
  self.indexJo =  ['jo_index0L','jo_index1L','jo_index2L','jo_index3L','jo_index4L']
  self.middleJo = ['jo_middle0L','jo_middle1L','jo_middle2L','jo_middle3L','jo_middle4L']
  self.ringJo =   ['jo_ring0L','jo_ring1L','jo_ring2L','jo_ring3L','jo_ring4L']
  self.littleJo = ['jo_little0L','jo_little1L','jo_little2L','jo_little3L','jo_little4L']
  
  self.thumb2Jo = ['jlR60_thumb20L','jlR65_thumb21L','jlR70_thumb22L','jlR90_thumb23L']
  self.index2Jo = ['jlS60_index20L','jlS65_index21L','jlS70_index22L','jlS75_index23L','jlS80_index24L']
  self.middle2Jo = ['jlT60_middle20L','jlT65_middle21L','jlT70_middle22L','jlT75_middle23L','jlT80_middle24L']
  self.ring2Jo = ['jlU60_ring20L','jlS65_ring21L','jlU70_ring22L','jlU75_ring23L','jlU80_ring24L']
  self.little2Jo = ['jlV60_little20L','jlV65_little21L','jlV70_little22L','jlV75_little23L','jlV80_little24L']
  
  self.wThumbJo = ['jlR60_wThumb0L','jlR65_wThumb1L','jlR70_wThumb2L','jlR90_wThumb3L']
  self.wIndexJo = ['jlS60_wIndex0L','jlS65_wIndex1L','jlS70_wIndex2L','jlS75_wIndex3L','jlS80_wIndex4L']
  self.wMiddleJo = ['jlT60_wMiddle0L','jlT65_wMiddle1L','jlT70_wMiddle2L','jlT75_wMiddle3L','jlT80_wMiddle4L']
  self.wRingJo = ['jlU60_wRing0L','jlS65_wRing1L','jlU70_wRing2L','jlU75_wRing3L','jlU80_wRing4L']
  self.wLittleJo = ['jlV60_wLittle0L','jlV65_wLittle1L','jlV70_wLittle2L','jlV75_wLittle3L','jlV80_wLittle4L']
  
  self.arm2Wing1Jo = ['jlN55_arm2Wing10L','jlN56_arm2Wing11L','jlN57_arm2Wing12L','jlN58_arm2Wing13L']
  self.arm2Wing2Jo = ['jlN60_arm2Wing20L','jlN61_arm2Wing21L','jlN62_arm2Wing22L','jlN63_arm2Wing23L']
  self.arm2Wing3Jo = ['jlN65_arm2Wing30L','jlN66_arm2Wing31L','jlN67_arm2Wing32L','jlN68_arm2Wing33L']
  self.arm2Wing4Jo = ['jlN70_arm2Wing40L','jlN71_arm2Wing41L','jlN72_arm2Wing42L','jlN73_arm2Wing43L']

  if cmds.optionMenu('oMenu',q=1,value=1) == 'other' :
   pass

# create base hierachy
 def createHierachy(self,*a):
  self.defineCtrlAttr()
  if cmds.objExists('here') :
   sys.stderr.write('Hierachy exist.')
  else :
   if cmds.objExists('topAdj'): topPoint = 'topAdj'
   else :
    if self.topJo == '' : topPoint = self.headJo
    else : topPoint = self.topJo
   cmds.createNode('transform',name='here')
   self.ctrlAttrPara('here',[0,0,0,0,0,0,0,0,0,1])
   cmds.createNode('transform',name='ctrl_location',parent='here')
   self.ctrlAttrPara('ctrl_location',[1,1,1,1,1,1,1,1,1,0])
   cmds.createNode('transform',name='grp_geometry',parent='here')
   self.ctrlAttrPara('grp_geometry',[3,3,3,3,3,3,3,3,3,1])
   cmds.createNode('transform',name='grp_deformer',parent='here')
   self.ctrlAttrPara('grp_deformer',[3,3,3,3,3,3,3,3,3,1])
   cmds.createNode('transform',name='grp_facial',parent='here')
   self.ctrlAttrPara('grp_facial',[0,0,0,0,0,0,0,0,0,1])
   cmds.createNode('transform',name='grp_simulation',parent='here')
   self.ctrlAttrPara('grp_simulation',[2,2,2,2,2,2,2,2,2,1])
   cmds.createNode('transform',name='grp_temp',parent='here')
   if cmds.objExists(topPoint):
    x = cmds.xform(topPoint,q=1,ws=1,t=1)
    r = x[1]*0.5
    self.ctrlStar('ctrl_move',r,1,0,[1,1,1,1,1,1,1,1,1,0],[.4,.4,.4])
   else :
    self.ctrlCircle('ctrl_move',5,1,0,[1,1,1,1,1,1,1,1,1,0],[.4,.4,.4])
   self.ctrlAttrPara('ctrl_move',[1,1,1,1,1,1,1,1,1,0])
   cmds.parent('ctrl_move','ctrl_location')
   cmds.createNode('transform',name='ctrl_spin',parent='ctrl_move')
   cmds.reorder('ctrl_spin',front=1)
   self.ctrlAttrPara('ctrl_spin',[1,1,1,1,1,1,1,1,1,0])
   cmds.createNode('transform',name='ctrl_asset',parent='ctrl_spin')
   self.ctrlAttrPara('ctrl_asset',[0,0,0,0,0,0,0,0,0,2])
   if cmds.objExists(self.rootJo):
    cmds.parent(self.rootJo,'ctrl_spin')
    rootX = cmds.xform(self.pelvisJo,q=1,worldSpace=1,rotatePivot=1)
    cmds.xform('ctrl_spin',worldSpace=1,rotatePivot=[rootX[0],rootX[1],rootX[2]])
    cmds.xform('ctrl_spin',worldSpace=1,scalePivot=[rootX[0],rootX[1],rootX[2]])
   if cmds.objExists('rootAdj'):
    cmds.parent('rootAdj','grp_temp')

# Create amd Posing joints
 def createSkeleton(self,*a):
  topPos = 0.0
  if cmds.objExists('rootAdj') == 0 :
   sys.stderr.write('No adjsuter.')
   return 0
  else :
   for x in cmds.listRelatives('rootAdj',allDescendents=1,type='joint') :
    if x[-3:] == 'Adj' :
     ga = cmds.xform(x,q=1,worldSpace=1,translation=1)
     if ga[1] > topPos : topPos = ga[1]

  # 4 case in create and locating method
  # case len[x]=3 : simple point snap, 3 in list -> 1. most exist adj 2. create joint name 3. should parent joint
  # case len[x]=5, x[1] = list : multi adjustable joint, 4 in list, 2nd is list and upper then 4 argument, 4th is tail joint
  # case len[x]=4, len[x[3]]=0 : orient constraint
  # case len[x]=4, len[x[3]]=2 : rotate constraint then aim constraint -> aim=index2Adj, aimAxis = [1,0,0]
  # case len[x]=4, len[x[3]]=3 : specific hierachy aim constraint -> hrc=jcC00_chest, aim=armAdj, aimAxis = [1,0,0]
  # case len[x]=4, len[x[3]]=4 : specific hierachy aim constraint and ignore axis -> hrc=jcC00_chest, aim=armAdj, ignoreAxis = .tz, aimAxis = [1,0,0]
  allList = [ ('rootAdj',self.rootJo,'',[]) ]
  allList += [ ('chestAdj',self.spineJo,self.rootJo,self.chestJo,('gLine_spineRebuild','spineAdj','spine1Adj','spine2Adj')) ]
  allList += [ ('chestFrontAdj',self.spineFront,self.spineJo+self.chestJoList,self.chestRound[0],('gLine_chestFront','spineAdj','spine1FrontAdj','spine2FrontAdj')) ]
  allList += [ ('chestSideAdj',self.spineSide,self.spineJo+self.chestJoList,self.chestRound[1],('gLine_chestSide','spineAdj','spine1SideAdj','spine2SideAdj')) ]
  allList += [ ('rearPelvisAdj',self.bodyJo,self.rootJo,self.rearPelvisJo,('gLine_bodyRebuild','spineAdj','body1Adj','body2Adj')) ]
  allList += [ ('rearTailAdj',self.rearTailJo[0],self.rearPelvisJo) ]
  allList += [ ('rearTailTipAdj',self.rearTailJo,self.rearPelvisJo,self.rearTailTip,('gLine_rearTailRebuild', 'rearTailAdj', 'rearTail1Adj', 'rearTail2Adj',[0,0,-1])) ]
  #self.uplidJo
  neckDir = [0,1,0]
  if cmds.getAttr('neckAdj.tz')>cmds.getAttr('neckAdj.ty') : neckDir = [0,0,1]
  allList += [ ('headAdj',self.neckJo,self.chestJo,self.headJo,('gLine_neckRebuild','neckAdj','neck1Adj','neck2Adj',neckDir)) , ('topAdj',self.topJo,self.headJo) ]
  allList += [ ('faceAdj',self.faceJo,self.headJo) , ('browMAdj',self.browJo[0],self.faceJo) , ('browAAdj',self.browJo[1],self.faceJo) , ('browBAdj',self.browJo[2],self.faceJo) ]
  allList += [ ('eyeAdj',self.eyeJo,self.faceJo,['sightAdj',[0,0,1]]) , ('thirdEyeAdj',self.thirdEyeJo,self.faceJo,['thirdSightAdj',[0,0,1]]) ]
  allList += [ ('uplidMainAdj',(self.lidJo[0],self.lidJo[1]),self.faceJo,'eyeAdj') ] 
  allList += [ ('lowlidMainAdj',(self.lidJo[2],self.lidJo[3]),self.faceJo,'eyeAdj') ]
  allList += [ ('thirdUplidMainAdj',{self.thirdLidJo[0]:self.faceJo,self.thirdLidJo[1]:self.thirdLidJo[0]},self.rootJo) ]
  allList += [ ('thirdLowlidMainAdj',{self.thirdLidJo[2]:self.faceJo,self.thirdLidJo[3]:self.thirdLidJo[2]},self.rootJo) ]
  allList += [ ('cheekAdj',self.cheekJo[0],self.faceJo) , ('nasalisAdj',self.cheekJo[1],self.faceJo) , ('gillAdj',self.cheekJo[2],self.faceJo) ]
  allList += [ ('jawAdj',self.jawJo[0],self.faceJo) , ('jawTipAdj',self.jawJo[1],self.jawJo[0]) ]
  allList += [ ('upLipMAdj',self.lipJo[0],self.faceJo,('loLipMAdj',[0,-1,0])) , ('upLipL1Adj',self.lipJo[1],self.faceJo,[self.lipJo[0]]) , ('cornerAdj',self.lipJo[2],self.faceJo,[self.lipJo[0]]) , ('loLipL1Adj',self.lipJo[3],self.faceJo,[self.lipJo[0]]) , ('loLipMAdj',self.lipJo[4],self.faceJo,[self.lipJo[0]]) ]
  allList += [ ('earRootAdj',self.earJo[0],self.headJo,[]) , ('earAdj',self.earJo[1],self.earJo[0]) , ('earInAdj',self.earJo[2],self.earJo[1]) , ('earInTipAdj',self.earJo[3],self.earJo[2]) , ('earOutAdj',self.earJo[4],self.earJo[1]) , ('earOutTipAdj',self.earJo[5],self.earJo[4]) ]
  allList += [ ('tongueTipAdj',self.tongueJo,self.jawJo[0],self.tongueTipJo,('gLine_tongueRebuild', 'tongueAdj', 'tongue1Adj', 'tongue2Adj',[0,0,1])) ]
  
  allList += [ ('rootAdj',self.pelvisJo,self.rootJo) ]
  allList += [ ('tailAdj',self.tailJo[0],self.rootJo) ]
  allList += [ ('tailTipAdj',self.tailJo,self.pelvisJo,self.tailTip,('gLine_tailRebuild', 'tailAdj', 'tail1Adj', 'tail2Adj',[0,0,-1])) ]
  allList += [ ('downBelowAdj',self.downBelong[0],self.pelvisJo,['penisAdj',[0,-1,0]]) , ('penisAdj',self.downBelong[1],self.downBelong[0]) ]
  allList += [ ('scrotumAdj',self.downBelong[2],self.pelvisJo,['nutAdj',[0,-1,0]]) , ('nutAdj',self.downBelong[3],self.downBelong[2]) ]
  
  allList += [ ('hipAdj',self.hipJo[0],self.pelvisJo,['kneeAdj_consA','kneeAdj',[0,-1,0]]) , ('kneeAdj',self.kneeJo[0],self.hipJo[0],[self.kneeJo[0],'ankleAdj',[0,-1,0]]) , ('ankleAdj',self.ankleJo[0],self.kneeJo[0],[]) ]
  allList += [ ('ballAdj',self.ballJo[0],self.ankleJo[0]) , ('toeAdj',self.toeJo[0],self.ballJo[0]) ]
  allList += [ ('backHoofAdj',self.bHoofJo,self.toeJo[0]) ]
  allList += [ ('hip2Adj',self.hip2Jo[0],self.pelvisJo,['knee2Adj_consA','knee2Adj',[0,-1,0]]) , ('knee2Adj',self.knee2Jo[0],self.hip2Jo[0],[self.knee2Jo[0],'ankle2Adj',[0,-1,0]]) , ('ankle2Adj',self.ankle2Jo[0],self.knee2Jo[0],[]) ]
  allList += [ ('bigToe0Adj',self.bigToeJo[0],self.ankleJo[0],['bigToe1Adj',[0,0,1]]) , ('bigToe1Adj',self.bigToeJo[1],[self.bigToeJo[0],self.ankleJo[0]]) , ('bigToe2Adj',self.bigToeJo[2],[self.bigToeJo[1],self.ankleJo[0]],['bigToe3Adj',[0,0,1]]) , ('bigToe3Adj',self.bigToeJo[3],self.bigToeJo[2]) ]
  allList += [ ('indexToe0Adj',self.indexToeJo[0],self.ankleJo[0],[self.ankleJo[0],'indexToe1Adj','.tx',[0,0,1]]) , ('indexToe1Adj',self.indexToeJo[1],[self.indexToeJo[0],self.ankleJo[0]],['indexToe2Adj',[0,0,1]]) , ('indexToe2Adj',self.indexToeJo[2],self.indexToeJo[1],['indexToe3Adj',[0,0,1]]) , ('indexToe3Adj',self.indexToeJo[3],self.indexToeJo[2],['indexToe4Adj',[0,0,1]]) , ('indexToe4Adj',self.indexToeJo[4],self.indexToeJo[3]) ]
  allList += [ ('middleToe0Adj',self.middleToeJo[0],self.ankleJo[0]) , ('middleToe1Adj',self.middleToeJo[1],[self.middleToeJo[0],self.ankleJo[0]],['middleToe2Adj',[0,0,1]]) , ('middleToe2Adj',self.middleToeJo[2],self.middleToeJo[1],['middleToe3Adj',[0,0,1]]) , ('middleToe3Adj',self.middleToeJo[3],self.middleToeJo[2],['middleToe4Adj',[0,0,1]]) , ('middleToe4Adj',self.middleToeJo[4],self.middleToeJo[3]) ]
  allList += [ ('fourthToe0Adj',self.fourthToeJo[0],self.ankleJo[0]) , ('fourthToe1Adj',self.fourthToeJo[1],[self.fourthToeJo[0],self.ankleJo[0]],['fourthToe2Adj',[0,0,1]]) , ('fourthToe2Adj',self.fourthToeJo[2],self.fourthToeJo[1],['fourthToe3Adj',[0,0,1]]) , ('fourthToe3Adj',self.fourthToeJo[3],self.fourthToeJo[2],['fourthToe4Adj',[0,0,1]]) , ('fourthToe4Adj',self.fourthToeJo[4],self.fourthToeJo[3]) ]
  allList += [ ('littleToe0Adj',self.littleToeJo[0],self.ankleJo[0]) , ('littleToe1Adj',self.littleToeJo[1],[self.littleToeJo[0],self.ankleJo[0]],['littleToe2Adj',[0,0,1]]) , ('littleToe2Adj',self.littleToeJo[2],self.littleToeJo[1],['littleToe3Adj',[0,0,1]]) , ('littleToe3Adj',self.littleToeJo[3],self.littleToeJo[2],['littleToe4Adj',[0,0,1]]) , ('littleToe4Adj',self.littleToeJo[4],self.littleToeJo[3]) ]

  allList += [ ('rearHipAdj',self.rearHipJo,self.rearPelvisJo,['rearKneeAdj_consA','rearKneeAdj',[0,-1,0]]) , ('rearKneeAdj',self.rearKneeJo,self.rearHipJo,[self.rearKneeJo,'rearAnkleAdj',[0,-1,0]]) , ('rearAnkleAdj',self.rearAnkleJo,self.rearKneeJo,[]) ]
  allList += [ ('rearBallAdj',self.rearBallJo,self.rearAnkleJo) , ('rearToeAdj',self.rearToeJo,self.rearBallJo) , ('rearHoofAdj',self.rearHoofJo,self.rearToeJo) ]
  
  allList += [ ('arm2Wing10Adj',self.arm2Wing1Jo[0],self.arm2Jo[0],['arm2Wing11Adj',[0,-1,0]]) , ('arm2Wing11Adj',self.arm2Wing1Jo[1],self.arm2Wing1Jo[0],['arm2Wing12Adj',[0,-1,0]]) , ('arm2Wing12Adj',self.arm2Wing1Jo[2],self.arm2Wing1Jo[1],['arm2Wing13Adj',[0,-1,0]]) , ('arm2Wing13Adj',self.arm2Wing1Jo[3],self.arm2Wing1Jo[2]) ]
  allList += [ ('arm2Wing20Adj',self.arm2Wing2Jo[0],self.arm2Jo[0],['arm2Wing21Adj',[0,-1,0]]) , ('arm2Wing21Adj',self.arm2Wing2Jo[1],self.arm2Wing2Jo[0],['arm2Wing22Adj',[0,-1,0]]) , ('arm2Wing22Adj',self.arm2Wing2Jo[2],self.arm2Wing2Jo[1],['arm2Wing23Adj',[0,-1,0]]) , ('arm2Wing23Adj',self.arm2Wing2Jo[3],self.arm2Wing2Jo[2]) ]
  allList += [ ('arm2Wing30Adj',self.arm2Wing3Jo[0],self.arm2Jo[0],['arm2Wing31Adj',[0,-1,0]]) , ('arm2Wing31Adj',self.arm2Wing3Jo[1],self.arm2Wing3Jo[0],['arm2Wing32Adj',[0,-1,0]]) , ('arm2Wing32Adj',self.arm2Wing3Jo[2],self.arm2Wing3Jo[1],['arm2Wing33Adj',[0,-1,0]]) , ('arm2Wing33Adj',self.arm2Wing3Jo[3],self.arm2Wing3Jo[2]) ]
  allList += [ ('arm2Wing40Adj',self.arm2Wing4Jo[0],self.arm2Jo[0],['arm2Wing41Adj',[0,-1,0]]) , ('arm2Wing41Adj',self.arm2Wing4Jo[1],self.arm2Wing4Jo[0],['arm2Wing42Adj',[0,-1,0]]) , ('arm2Wing42Adj',self.arm2Wing4Jo[2],self.arm2Wing4Jo[1],['arm2Wing43Adj',[0,-1,0]]) , ('arm2Wing43Adj',self.arm2Wing4Jo[3],self.arm2Wing4Jo[2]) ]
  
  # arm ariel or ground decision
  armDir = [1,0,0] ; arm2Dir = [1,0,0] ; finDir = [1,0,0]

  tipY = cmds.xform('wristAdj',q=1,ws=1,bb=1)[1]
  if tipY < topPos/8.5 : armDir = [0,-1,0] ; finDir = [0,0,1]
  allList += [ ['shoulderAdj',self.shoulderJo[0],self.chestJo,[self.chestJo,'armAdj','.tz',armDir]] ]
  if armDir == [0,-1,0] : del allList[len(allList)-1][3]

  if cmds.objExists('wrist2Adj') :
   tipY = cmds.xform('wrist2Adj',q=1,ws=1,bb=1)[1]
   if tipY < topPos/8.5 : arm2Dir = [0,-1,0] ; finDir = [0,0,1]
   allList += [ ['shoulder2Adj',self.shoulder2Jo[0],self.chestJo,[self.chestJo,'arm2Adj','.tz',arm2Dir]] ]
   if arm2Dir == [0,-1,0] : del allList[len(allList)-1][3]

  allList += [ ('armAdj',self.armJo[0],self.shoulderJo[0],['elbowAdj_consA','elbowAdj',armDir]) , ('elbowAdj',self.elbowJo[0],self.armJo[0],[self.elbowJo[0],'wristAdj',armDir]) , ('wristAdj',self.wristJo[0],self.elbowJo[0],[]) ]
  allList += [ ('arm2Adj',self.arm2Jo[0],self.shoulder2Jo[0],['elbow2Adj_consA','elbow2Adj',arm2Dir]) , ('elbow2Adj',self.elbow2Jo[0],self.arm2Jo[0],[self.elbow2Jo[0],'wrist2Adj',arm2Dir]) , ('wrist2Adj',self.wrist2Jo[0],self.elbow2Jo[0],[]) ]
  allList += [ ('thumb0Adj',self.thumbJo[0],self.wristJo[0],['thumb1Adj',finDir]) , ('thumb1Adj',self.thumbJo[1],[self.thumbJo[0],self.wristJo[0]],['thumb2Adj',finDir]) , ('thumb2Adj',self.thumbJo[2],self.thumbJo[1],['thumb3Adj',finDir]) , ('thumb3Adj',self.thumbJo[3],self.thumbJo[2]) ]
  allList += [ ('index0Adj',self.indexJo[0],self.wristJo[0],[self.wristJo[0],'index1Adj','.tz',finDir]) , ('index1Adj',self.indexJo[1],[self.indexJo[0],self.wristJo[0]],['index2Adj',finDir]) , ('index2Adj',self.indexJo[2],self.indexJo[1],['index3Adj',finDir]) , ('index3Adj',self.indexJo[3],self.indexJo[2],['index4Adj',finDir]) , ('index4Adj',self.indexJo[4],self.indexJo[3]) ]
  allList += [ ('middle0Adj',self.middleJo[0],self.wristJo[0],[self.wristJo[0],'middle1Adj','.tz',finDir]) , ('middle1Adj',self.middleJo[1],[self.middleJo[0],self.wristJo[0]],['middle2Adj',finDir]) , ('middle2Adj',self.middleJo[2],self.middleJo[1],['middle3Adj',finDir]) , ('middle3Adj',self.middleJo[3],self.middleJo[2],['middle4Adj',finDir]) , ('middle4Adj',self.middleJo[4],self.middleJo[3]) ]
  allList += [ ('ring0Adj',self.ringJo[0],self.wristJo[0],[self.wristJo[0],'ring1Adj','.tz',finDir]) , ('ring1Adj',self.ringJo[1],[self.ringJo[0],self.wristJo[0]],['ring2Adj',finDir]) , ('ring2Adj',self.ringJo[2],self.ringJo[1],['ring3Adj',finDir]) , ('ring3Adj',self.ringJo[3],self.ringJo[2],['ring4Adj',finDir]) , ('ring4Adj',self.ringJo[4],self.ringJo[3]) ]
  allList += [ ('little0Adj',self.littleJo[0],self.wristJo[0],[self.wristJo[0],'little1Adj','.tz',finDir]) , ('little1Adj',self.littleJo[1],[self.littleJo[0],self.wristJo[0]],['little2Adj',finDir]) , ('little2Adj',self.littleJo[2],self.littleJo[1],['little3Adj',finDir]) , ('little3Adj',self.littleJo[3],self.littleJo[2],['little4Adj',finDir]) , ('little4Adj',self.littleJo[4],self.littleJo[3]) ]
  
  allList += [ ('thumb20Adj',self.thumb2Jo[0],self.wrist2Jo[0],['thumb21Adj',finDir]) , ('thumb21Adj',self.thumb2Jo[1],[self.thumb2Jo[0],self.wrist2Jo[0]],['thumb22Adj',finDir]) , ('thumb22Adj',self.thumb2Jo[2],self.thumb2Jo[1],['thumb23Adj',finDir]) , ('thumb23Adj',self.thumb2Jo[3],self.thumb2Jo[2]) ]
  allList += [ ('index20Adj',self.index2Jo[0],self.wrist2Jo[0],[self.wrist2Jo[0],'index21Adj','.tz',finDir]) , ('index21Adj',self.index2Jo[1],[self.index2Jo[0],self.wrist2Jo[0]],['index22Adj',finDir]) , ('index22Adj',self.index2Jo[2],self.index2Jo[1],['index23Adj',finDir]) , ('index23Adj',self.index2Jo[3],self.index2Jo[2],['index24Adj',finDir]) , ('index24Adj',self.index2Jo[4],self.index2Jo[3]) ]
  allList += [ ('middle20Adj',self.middle2Jo[0],self.wrist2Jo[0],[self.wrist2Jo[0],'middle21Adj','.tz',finDir]) , ('middle21Adj',self.middle2Jo[1],[self.middle2Jo[0],self.wrist2Jo[0]],['middle22Adj',finDir]) , ('middle22Adj',self.middle2Jo[2],self.middle2Jo[1],['middle23Adj',finDir]) , ('middle23Adj',self.middle2Jo[3],self.middle2Jo[2],['middle24Adj',finDir]) , ('middle24Adj',self.middle2Jo[4],self.middle2Jo[3]) ]
  allList += [ ('ring20Adj',self.ring2Jo[0],self.wrist2Jo[0],[self.wrist2Jo[0],'ring21Adj','.tz',finDir]) , ('ring21Adj',self.ring2Jo[1],[self.ring2Jo[0],self.wrist2Jo[0]],['ring22Adj',finDir]) , ('ring22Adj',self.ring2Jo[2],self.ring2Jo[1],['ring23Adj',finDir]) , ('ring23Adj',self.ring2Jo[3],self.ring2Jo[2],['ring24Adj',finDir]) , ('ring24Adj',self.ring2Jo[4],self.ring2Jo[3]) ]
  allList += [ ('little20Adj',self.little2Jo[0],self.wrist2Jo[0],[self.wrist2Jo[0],'little21Adj','.tz',finDir]) , ('little21Adj',self.little2Jo[1],[self.little2Jo[0],self.wrist2Jo[0]],['little22Adj',finDir]) , ('little22Adj',self.little2Jo[2],self.little2Jo[1],['little23Adj',finDir]) , ('little23Adj',self.little2Jo[3],self.little2Jo[2],['little24Adj',finDir]) , ('little24Adj',self.little2Jo[4],self.little2Jo[3]) ]

  allList += [ ('wThumb0Adj',self.wThumbJo[0],self.wrist2Jo[0],['wThumb1Adj',finDir]) , ('wThumb1Adj',self.wThumbJo[1],self.wThumbJo[0]) ]
  allList += [ ('wIndex0Adj',self.wIndexJo[0],self.wrist2Jo[0],['wIndex1Adj',finDir]) , ('wIndex1Adj',self.wIndexJo[1],self.wIndexJo[0]) , ('wIndex2Adj',self.wIndexJo[2],self.wIndexJo[1]) , ('wIndex3Adj',self.wIndexJo[3],self.wIndexJo[2]) , ('wIndex4Adj',self.wIndexJo[4],self.wIndexJo[3]) ]
  allList += [ ('wMiddle0Adj',self.wMiddleJo[0],self.wrist2Jo[0],['wMiddle1Adj',finDir]) , ('wMiddle1Adj',self.wMiddleJo[1],self.wMiddleJo[0]) , ('wMiddle2Adj',self.wMiddleJo[2],self.wMiddleJo[1]) , ('wMiddle3Adj',self.wMiddleJo[3],self.wMiddleJo[2]) , ('wMiddle4Adj',self.wMiddleJo[4],self.wMiddleJo[3]) ]
  allList += [ ('wRing0Adj',self.wRingJo[0],self.wrist2Jo[0],['wRing1Adj',finDir]) , ('wRing1Adj',self.wRingJo[1],self.wRingJo[0]) , ('wRing2Adj',self.wRingJo[2],self.wRingJo[1]) , ('wRing3Adj',self.wRingJo[3],self.wRingJo[2]) , ('wRing4Adj',self.wRingJo[4],self.wRingJo[3]) ]
  allList += [ ('wLittle0Adj',self.wLittleJo[0],self.wrist2Jo[0],['wLittle1Adj',finDir]) , ('wLittle1Adj',self.wLittleJo[1],self.wLittleJo[0]) , ('wLittle2Adj',self.wLittleJo[2],self.wLittleJo[1]) , ('wLittle3Adj',self.wLittleJo[3],self.wLittleJo[2]) , ('wLittle4Adj',self.wLittleJo[4],self.wLittleJo[3]) ]
  
  allList += [ ('midHipAdj',self.midLimbJo[0],self.spineJo[1],['midKneeAdj_consA','midKneeAdj',armDir]) , ('midKneeAdj',self.midLimbJo[1],self.midLimbJo[0],[self.midLimbJo[1],'midAnkleAdj',armDir]) , ('midAnkleAdj',self.midLimbJo[2],self.midLimbJo[1],[]) ]
  allList += [ ('palmAdj',self.fShoeJo[0],self.wristJo[0]) , ('fingerAdj',self.fShoeJo[1],self.fShoeJo[0]) , ('frontHoofAdj',self.fHoofJo[2],self.fShoeJo[1]) ]
  allList += [ ('palm2Adj',self.fShoe2Jo[0],self.wrist2Jo[0]) , ('finger2Adj',self.fShoe2Jo[1],self.fShoe2Jo[0]) , ('frontHoof2Adj',self.fHoof2Jo[2],self.fShoe2Jo[1]) ]
  allList += [ ('ball2Adj',self.shoe2Jo[0],self.ankle2Jo[0]) , ('toe2Adj',self.shoe2Jo[1],self.shoe2Jo[0]) , ('backHoof2Adj',self.bHoof2Jo,self.shoe2Jo[1]) ]
  

# create joint loop
  exList = []
  for x in allList :
   if cmds.objExists(x[0]) :
   #if self.exCheck(x[0]) :
    exList.append(x)
    if type(x[1]) == str :
     if cmds.objExists(x[1]) == 0 :
      if x[2] == '' : self.createJoint(x[1])
      else :
       if type(x[2]) != list : self.createJoint(x[1],x[2])
       else : # joint parent target will in order of exist joint in list
        for y in x[2] :
         if cmds.objExists(y) :
          self.createJoint(x[1],y)
          break
     else :
      xp = cmds.listRelatives(x[1],parent=1)[0]
      if type(x[2]) == str and x[2] != '' :
       if xp != x[2] : cmds.parent(x[1],x[2])
      if type(x[2]) == list and x[2] != '' :
       for y in x[2] :
        if cmds.objExists(y) :
          if xp != y : cmds.parent(x[1],y)
          break

 #allList += [ ('chestAdj',self.spineJo,self.rootJo,self.chestJo,('gLine_spineRebuild','spineAdj','spine1Adj','spine2Adj')) ]
 #allList += [ ('chestFrontAdj',self.spineFront,self.spineJo,self.chestRound[0],('gLine_chestFront','spineAdj','spine1FrontAdj','spine2FrontAdj')) ]
    if type(x[1]) == list :
     print x[0]
     pNum = cmds.getAttr(x[0]+'.jointNumber')
     if type(x[2]) == str : pList = x[1][:] ; pList.insert(0,x[2]) # define created joint parent to upper hierachy joint
     if type(x[2]) == list :
      pList = x[2][:] # or parent to specific joint in list = x[2]
      pList[pNum] = x[2][-1]
     for i in range(len(x[1])) :
      if i < pNum :
       if cmds.objExists(x[1][i]) == 0 : self.createJoint(x[1][i],pList[i])

     if cmds.objExists(x[3]) == 0 : self.createJoint(x[3],pList[pNum])
     elif cmds.objExists(x[3]) == 1 :
      xp = cmds.listRelatives(x[3],parent=1)[0]
      if xp != pList[pNum] :
       if type(x[2]) == str : cmds.parent(x[3],pList[pNum])

     for i in range(len(x[1])) :
      if i >= pNum :
       if cmds.objExists(x[1][i]) == 1 : cmds.delete(x[1][i])

    if type(x[1]) == tuple :
     for i,xx in enumerate(x[1]) :
      p = x[2]
      if xx != x[1][0] : p = x[1][i-1]
      if not cmds.objExists(xx) :
       self.createJoint(xx,p)
     
    if type(x[1]) == dict :
     print x[1]
     kList = x[1].keys()
     #kList.sort()
     print kList
     for i in range(len(x[1])) :
      if cmds.objExists(kList[i]) == 0 : self.createJoint(kList[i],x[1][kList[i]])

   else :
    if type(x[1]) == str and cmds.objExists(x[1]) == 1 :
     cmds.delete(x[1])
     if cmds.objExists(self.L2R(x[1])) :	
	  cmds.delete(self.L2R(x[1]))

# locate joints loop
  invis = [self.jawJo[1]]
  boxStyle = [self.faceJo]
  
  for x in exList :
   if type(x[1]) == str :
    cmds.xform(x[1],t=cmds.xform(x[0],q=1,ws=1,t=1),ws=1,a=1)
    cmds.setAttr(x[1]+'.rotate',0,0,0,type="double3")
    if x[1] == self.pelvisJo : cmds.setAttr(self.pelvisJo+'.ty',-0.01)
    if len(x) == 4 and len(x[3]) == 0 :
     cmds.xform(x[1],rotation=cmds.xform(x[0],q=1,ws=1,ro=1),ws=1,a=1)
    if len(x) == 4 and len(x[3]) == 1 :
     cmds.xform(x[1],rotation=cmds.xform(x[3][0],q=1,ws=1,ro=1),ws=1,a=1)
    if len(x) == 4 and len(x[3]) == 2 :
     if cmds.objExists(x[3][0]) :
      cmds.xform(x[1],rotation=cmds.xform(x[0],q=1,ws=1,ro=1),ws=1,a=1)
      tn = cmds.createNode('transform',parent=x[1])
      cmds.aimConstraint(x[3][0],tn,aimVector=x[3][1],upVector=[0,1,0],worldUpType='none')
      cmds.xform(x[1],rotation=cmds.xform(tn,q=1,ws=1,ro=1),ws=1,a=1)
      cmds.delete(tn)
    if len(x) == 4 and len(x[3]) == 3 :
     tn = cmds.createNode('transform',parent=x[3][0])
     cmds.delete(cmds.aimConstraint(x[3][1],tn,aimVector=x[3][2],upVector=[0,1,0],worldUpType='none'))
     if x[3][2] in [[1,0,0],[-1,0,0]]: cmds.setAttr(tn+'.rotateX',0)
     cmds.xform(x[1],rotation=cmds.xform(tn,q=1,ws=1,ro=1),ws=1,a=1)
     cmds.delete(tn)
    if len(x) == 4 and len(x[3]) == 4 :
     tn1 = cmds.createNode('transform',parent=x[3][0])
     cmds.xform(tn1,t=cmds.xform(x[0],q=1,ws=1,t=1),ws=1,a=1)
     tn2 = cmds.createNode('transform',parent=x[3][0])
     cmds.xform(tn2,t=cmds.xform(x[3][1],q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(tn2+x[3][2],cmds.getAttr(tn1+x[3][2]))
     cmds.aimConstraint(tn2,tn1,aimVector=x[3][3],upVector=[0,1,0],worldUpType='none')
     cmds.xform(x[1],rotation=cmds.xform(tn1,q=1,ws=1,ro=1),ws=1,a=1)
     cmds.delete(tn1,tn2)
   if x[1] in invis : cmds.setAttr(x[1]+'.drawStyle',2)
   if x[1] in boxStyle : cmds.setAttr(x[1]+'.drawStyle',1)

   if type(x[1]) == list :
    if len(x[1])>3 :
     spineList = []
     for y in x[1] :
      if cmds.objExists(y) :
       spineList.append(y)
     if cmds.objExists(x[4][1]) : 
      cmds.xform(x[1][0],t=cmds.xform(x[4][1],q=1,ws=1,t=1),ws=1,a=1)
      cmds.xform(x[1][0],ro=cmds.xform(x[4][2],q=1,ws=1,ro=1),ws=1,a=1)
     if len(spineList) == 2 :
      pos1 = cmds.xform(x[4][2],q=1,ws=1,t=1)
      pos2 = cmds.xform(x[0],q=1,ws=1,t=1)
      pos = [ (pos1[0]+pos2[0])/2 , (pos1[1]+pos2[1])/2 , (pos1[2]+pos2[2])/2 ]
      cmds.xform(spineList[1],t=pos,ws=1,a=1)
      cmds.xform(x[3],t=cmds.xform(x[0],q=1,ws=1,t=1),ws=1,a=1)
     if len(spineList) == 3 :
      cmds.xform(spineList[1],t=cmds.xform(x[4][2],q=1,ws=1,t=1),ro=cmds.xform(x[4][2],q=1,ws=1,ro=1),worldSpace=1,a=1)
      cmds.xform(spineList[2],t=cmds.xform(x[4][3],q=1,ws=1,t=1),ro=cmds.xform(x[4][2],q=1,ws=1,ro=1),worldSpace=1,a=1)
     if len(spineList) > 3 :
      tempList = []
      for i in range(len(spineList)) :
       if len(x[4])>4 :
        tmp = cmds.createNode('transform') ; tempList.append(tmp)
        cmds.xform(tmp,t=cmds.pointOnCurve(x[4][0],parameter=(1.0/(len(spineList))*(i+1)),position=1),ws=1,a=1)
        tempList.append(cmds.aimConstraint(tmp,spineList[i],aimVector=x[4][4],upVector=[0,1,0],worldUpType='none')[0])
       else : cmds.xform(spineList[i],ro=[0,0,0],ws=1,a=1)
       cmds.xform(spineList[i],t=cmds.pointOnCurve(x[4][0],parameter=(1.0/(len(spineList))*i),position=1),ws=1,a=1)
      cmds.delete(tempList)
     cmds.xform(x[3],t=cmds.xform(x[0],q=1,ws=1,t=1),ws=1,a=1)
     cmds.xform(x[3],ro=cmds.xform(x[0],q=1,ws=1,ro=1),ws=1,a=1)

   if type(x[1]) == dict :
    if x[0] == 'uplidMainAdj' and cmds.objExists('eyeAdj') and cmds.objExists('lowlidMainAdj') :
     kList = x[1].keys()
     kList.reverse()
     cmds.xform(kList[0],t=cmds.xform('eyeAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.delete(cmds.aimConstraint('uplidMainAdj',kList[0],aimVector=[0,0,1],upVector=[0,-1,0],worldUpType='object',worldUpObject='lowlidMainAdj'))
     self.freezeRotate(kList[0])
     cmds.xform(kList[1],t=cmds.xform('uplidMainAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(kList[0]+'.radius',0.25)
    if x[0] == 'lowlidMainAdj' and cmds.objExists('eyeAdj') and cmds.objExists('uplidMainAdj') :
     kList = x[1].keys()
     kList.sort()
     cmds.xform(kList[0],t=cmds.xform('eyeAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.delete(cmds.aimConstraint('lowlidMainAdj',kList[0],aimVector=[0,0,1],upVector=[0,1,0],worldUpType='object',worldUpObject='uplidMainAdj'))
     self.freezeRotate(kList[0])
     cmds.xform(kList[1],t=cmds.xform('lowlidMainAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(kList[0]+'.radius',0.25)
    if x[0] == 'thirdUplidMainAdj' and cmds.objExists('thirdEyeAdj') and cmds.objExists('thirdLowlidMainAdj') :
     kList = x[1].keys()
     #kList.reverse()
     cmds.xform(kList[0],t=cmds.xform('thirdEyeAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.delete(cmds.aimConstraint('thirdUplidMainAdj',kList[0],aimVector=[0,0,1],upVector=[0,-1,0],worldUpType='object',worldUpObject='thirdLowlidMainAdj'))
     self.freezeRotate(kList[0])
     cmds.xform(kList[1],t=cmds.xform('thirdUplidMainAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(kList[0]+'.radius',0.25)
    if x[0] == 'thirdLowlidMainAdj' and cmds.objExists('thirdEyeAdj') and cmds.objExists('thirdUplidMainAdj') :
     kList = x[1].keys()
     #kList.sort()
     cmds.xform(kList[0],t=cmds.xform('thirdEyeAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.delete(cmds.aimConstraint('thirdLowlidMainAdj',kList[0],aimVector=[0,0,1],upVector=[0,1,0],worldUpType='object',worldUpObject='thirdUplidMainAdj'))
     self.freezeRotate(kList[0])
     cmds.xform(kList[1],t=cmds.xform('thirdLowlidMainAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(kList[0]+'.radius',0.25)
    else :
     pass

   if type(x[1]) == tuple :
    if cmds.objExists(x[3]) :
     cmds.xform(x[1][0],t=cmds.xform('eyeAdj',q=1,ws=1,t=1),ws=1,a=1)
     cmds.delete(cmds.aimConstraint(x[0],x[1][0],aimVector=[0,0,1],upVector=[0,-1,0],worldUpType='object',worldUpObject='lowlidMainAdj'))
     self.freezeRotate(x[1][0])
     cmds.xform(x[1][1],t=cmds.xform(x[0],q=1,ws=1,t=1),ws=1,a=1)
     cmds.setAttr(x[1][0]+'.radius',0.25)

# if joint what will be ikHandle and have no rotate value
  sJoCd = [ [self.elbowJo[0],'.ry','.tx',self.wristJo[0]] , [self.kneeJo[0],'.rx','.ty',self.ankleJo[0]] ]
  for x in sJoCd :
   if round(cmds.getAttr(x[0]+x[1]),5) == 0 :
    ga = cmds.getAttr(x[0]+x[2]) + cmds.getAttr(x[3]+x[2])
    cmds.setAttr(x[0]+'.tz',ga*-.001)
    cmds.setAttr(x[3]+'.tz',ga*0.001)

# mirror joints
  leftJo = []
  rightJo = []
  leftParent = []
  rightParent = []
  matL = 'jl[A-Z]\d+_[a-zA-Z0-9]+L'
  natL = '\Ajo+_[a-zA-Z0-9]+L\Z'
  matC = 'jc[A-Z]\d+_[a-zA-Z0-9]+'
  matR = 'jr[A-Z]\d+_[a-zA-Z0-9]+R'
  aj = cmds.listRelatives(self.rootJo,allDescendents=1,type='joint')
  aj.reverse()
  for x in aj :
   if len(re.findall(matL,x)) > 0 :
    leftJo.append(x)
    xpj = cmds.listRelatives(x,parent=1)[0]
    leftParent.append(xpj)
    if len(re.findall(matC,xpj)) > 0 :
     rightParent.append(xpj)
    else :
     xpj = xpj[:-1]+'R'
     xpj = 'jr'+xpj[2:]
     rightParent.append(xpj)
    x = x[:-1]+'R'
    x = 'jr'+x[2:]
    rightJo.append(x)
    
   if len(re.findall(natL,x)) > 0 :
    print x
    leftJo.append(x)
    xpj = cmds.listRelatives(x,parent=1)[0]
    leftParent.append(xpj)
    if len(re.findall(natL,xpj)) > 0 :
     xpj = xpj[:-1]+'R'
     rightParent.append(xpj)
    else :
     rightParent.append(xpj)
    x = x[:-1]+'R'
    rightJo.append(x)
    print x

  print rightJo
  for i in range(len(leftJo)) :
   if leftParent[i] == rightParent[i] :
    self.rSideJoint(rightJo[i],rightParent[i],leftJo[i],'onRoot')
   else :
    self.rSideJoint(rightJo[i],rightParent[i],leftJo[i])

# connect inverse scale
  aj = cmds.listRelatives(self.rootJo,allDescendents=1,type='joint')
  for x in aj :
   if cmds.getAttr(x+'.inverseScale',settable=1) :
    p = cmds.listRelatives(x,parent=1)[0]
    if p != self.headJo :
     cmds.connectAttr(p+'.scale',x+'.inverseScale')
   else :
    p = cmds.listRelatives(x,parent=1)[0]
    ict = cmds.listConnections(x+'.inverseScale',s=1,d=0)
    if ict[0] != p :
     cmds.connectAttr(p+'.scale',x+'.inverseScale')
    if p == self.headJo :
     cmds.disconnectAttr(ict[0]+'.scale',x+'.inverseScale')

#lock preffered angle and set default translate value
  aj = cmds.listRelatives(self.rootJo,allDescendents=1,type='joint')
  aj.append(self.rootJo)
  for x in aj : cmds.setAttr(x+'.preferredAngle',lock=0)
  cmds.joint(self.rootJo,e=1,setPreferredAngles=1,children=1)
  for x in aj :
   cmds.setAttr(x+'.preferredAngle',lock=1)
   self.ctrlTransRem(x)

# add facial blendShape Attribute on grp_facial
  #self.jawJo = ['jcF50_jaw','jcF51_jawTip']
  fjo = []
  #fjo += [self.eyeJo,self.eyeJo] # add facial blendShape attribute on grp_facial
  #fjo += [self.uplidJo[1],self.uplidJo[1],self.uplidJo[1],self.uplidJo[1],self.uplidJo[1]]
  #fjo += [self.lolidJo[1],self.lolidJo[1],self.lolidJo[1],self.lolidJo[1],self.lolidJo[1]]
  fjo += [self.thirdLidJo[1],self.thirdLidJo[1],self.thirdLidJo[1],self.thirdLidJo[1],self.thirdLidJo[1]]
  fjo += [self.thirdLidJo[3],self.thirdLidJo[3],self.thirdLidJo[3],self.thirdLidJo[3],self.thirdLidJo[3]]
  fjo += [self.jawJo[0],self.jawJo[0],self.jawJo[0]]
  fjo += [self.browJo[1],self.browJo[1]]
  fjo += [self.lipJo[1],self.lipJo[2],self.lipJo[2],self.lipJo[2],self.lipJo[3]]
  fjo += [self.cheekJo[0],self.cheekJo[1]]
  attr = ['pupilDilated','pupilContract',]
  attr += ['uplidClose','uplidOpen','uplidRaise','uplidIn','uplidOut']
  attr += ['lolidTight','lolidOpen','lolidDepress','lolidIn','lolidOut']
  attr += ['uplidCloseThird','uplidOpenThird','uplidRaiseThird','uplidInThird','uplidOutThird']
  attr += ['lolidTightThird','lolidOpenThird','lolidDepressThird','lolidInThird','lolidOutThird']
  attr += ['jawOpen','jawStretch','jawDrop']
  attr += ['browRaise','browLower']
  attr += ['upLipRaise','cornerPull','cornerStretch','cornerDepress','loLipDepress']
  attr += ['cheekRaise','noseWrinkle']
  fjoDict = {}
  fjoDict[self.eyeJo] = ['pupilDilated','pupilContract',]
  fjoDict[self.lidJo[1]] = ['uplidClose','uplidOpen','uplidRaise','uplidIn','uplidOut']
  fjoDict[self.lidJo[3]] = ['lolidTight','lolidOpen','lolidDepress','lolidIn','lolidOut']
  for i,x in enumerate(fjo) :
   if self.L2R(x) != x :
    lrjo = [x,self.L2R(x)] ; s = ['L','R']
    for j in range(2) :
     if self.exCheck(lrjo[j]) and cmds.objExists('grp_facial.'+attr[i]+s[j])==0 :
      cmds.addAttr('grp_facial',longName=attr[i]+s[j],attributeType='double',keyable=1)
   else :
    if self.exCheck(x) and cmds.objExists('grp_facial.'+attr[i])==0 :
     cmds.addAttr('grp_facial',longName=attr[i],attributeType='double',keyable=1)
     
  for x in fjoDict.keys() :
   print x
   
# lip joint move with jaw
  self.createlipJoMovement()

  '''
# lip joint interacte
  if self.exCheck(self.lipJo) :
   lj = self.lipJo[:] # lip joint
   nn = ['lipUp','lipUpBL','cornerL','lipLoBL','lipLo','lipUpBR','cornerR','lipLoBR']
   num = [0,0.1,0.5,0.9,1,0.1,0.5,0.9]
   for i in range(len(lj)):
    t = cmds.createNode('transform',skipSelect=1,parent=lj[i])
    cmds.parent(t,self.jawJo[0])
    cmds.createNode('multMatrix',name='mX_'+nn[i],skipSelect=1)
    cmds.xform('mX_'+nn[i]+'.matrixIn[0]',matrix=cmds.getAttr(t+'.matrix'))
    cmds.setAttr('mX_'+nn[i]+'.matrixIn[0]',cmds.getAttr(t+'.matrix'),type='matrix')
    cmds.delete(t)
    cmds.connectAttr(self.jawJo[0]+'.matrix','mX_'+nn[i]+'.matrixIn[1]')
    cmds.createNode('multMatrix',name='mX_'+nn[i]+'2',skipSelect=1)
    cmds.connectAttr('mX_'+nn[i]+'.matrixSum','mX_'+nn[i]+'2'+'.matrixIn[0]')
    cmds.setAttr('mX_'+nn[i]+'2.matrixIn[1]',cmds.getAttr(lj[i]+'.inverseMatrix'),type='matrix')
    cmds.createNode('wtAddMatrix',name='mAdd_'+nn[i])
    cmds.connectAttr('mX_'+nn[i]+'2'+'.matrixSum','mAdd_'+nn[i]+'.wtMatrix[0].matrixIn')
    cmds.setAttr('mAdd_'+nn[i]+'.wtMatrix[0].weightIn',num[i])
    cmds.createNode('decomposeMatrix',name='dX_'+nn[i])
    cmds.connectAttr('mAdd_'+nn[i]+'.matrixSum','dX_'+nn[i]+'.inputMatrix')
    cmds.connectAttr('dX_'+nn[i]+'.outputTranslate',lj[i]+'.rotatePivotTranslate')
    cmds.connectAttr('dX_'+nn[i]+'.outputRotate',lj[i]+'.rotateAxis')
  '''

# connect height reference attribute
  if self.exCheck(['ctrl_move','topAdj']):
   if cmds.objExists('ctrl_move.height') == 0 :
    cmds.addAttr('ctrl_move',longName='height',attributeType='double',keyable=1)
    cmds.createNode('decomposeMatrix',name='xCons_height',skipSelect=1)
    cmds.connectAttr('topAdj.worldMatrix[0]','xCons_height.inputMatrix')
    cmds.createNode('multDoubleLinear',name='mdl_heightScale',skipSelect=1)
    cmds.connectAttr('xCons_height.outputTranslateY','mdl_heightScale.input1')
    cmds.connectAttr('ctrl_move.scaleY','mdl_heightScale.input2')
    cmds.connectAttr('mdl_heightScale.output','ctrl_move.height')
    cmds.setAttr('ctrl_move.height',keyable=0,channelBox=1)
  
# reaction with hierachy
  if cmds.objExists('ctrl_spin') and cmds.objExists(self.rootJo) :
   rp = cmds.listRelatives(self.rootJo,parent=1)
   if rp is None :
    cmds.parent(self.rootJo,'ctrl_spin')
   else :
    if rp[0] != 'ctrl_spin' : cmds.parent(self.rootJo,'ctrl_spin')
  cmds.setAttr('rootAdj.v',keyable=1,lock=0)
  cmds.setAttr('rootAdj.v',0)
  cmds.setAttr(self.rootJo+'.overrideEnabled',0)
  cmds.setAttr(self.rootJo+'.overrideDisplayType',0)
  cmds.setAttr(self.rootJo+'.v',1)
  sys.stderr.write('Create joints done.')
  
# Extra Joint Setup : lip joint move with jaw
 def createlipJoMovement(self,*a):
  self.xCons(self.faceJo,'xTrans_face')
  if cmds.objExists('crv_lipAdj') == 1 :
   cmds.duplicate('crv_lipAdj',name='crv_lipJo',renameChildren=1)
   cmds.parent('crv_lipJo','xTrans_face')
   cmds.makeIdentity('crv_lipJo',apply=True,translate=1,rotate=0,scale=0)
   cmds.parent('crv_lipJo','grp_facial')
   sk = cmds.skinCluster([self.headJo,self.jawJo[0]],'crv_lipJo',toSelectedBones=1,removeUnusedInfluence=0)
   cmds.setAttr('crv_lipJo.overrideEnabled',0)
   cmds.skinPercent(sk[0],'crv_lipJo.cv[0]',transformValue=[(self.headJo,1),(self.jawJo[0],0)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[1]',transformValue=[(self.headJo,1),(self.jawJo[0],0)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[2]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[3]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[4]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[5]',transformValue=[(self.headJo,0),(self.jawJo[0],1)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[6]',transformValue=[(self.headJo,0),(self.jawJo[0],1)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[7]',transformValue=[(self.headJo,0),(self.jawJo[0],1)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[8]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[9]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[10]',transformValue=[(self.headJo,.5),(self.jawJo[0],.5)])
   cmds.skinPercent(sk[0],'crv_lipJo.cv[11]',transformValue=[(self.headJo,1),(self.jawJo[0],0)])
   allLipJo = self.lipJo + [self.L2R(self.lipJo[3]),self.L2R(self.lipJo[2]),self.L2R(self.lipJo[1])]
   paraList = [11,0,2,4,5,6,8,10]
   for i,x in enumerate(allLipJo) :
    nn = x.split('_')[1] # node name
    poc = cmds.createNode('pointOnCurveInfo',name='poc_'+nn,skipSelect=1)
    cmds.setAttr(poc+'.parameter',paraList[i])
    cmds.connectAttr('crv_lipJo.local',poc+'.inputCurve')
    cmds.setAttr(x+'.translate',0,0,0,type='double3')
    cmds.connectAttr(poc+'.position',x+'.rotatePivotTranslate')
  pass

# Extra Joint : Elbow Out
 def createEyelidHalf(self,*a):
  jo = [self.lidHalfJo[0][0],self.lidHalfJo[0][1],self.lidHalfJo[0][2],self.lidHalfJo[0][3],self.L2R(self.lidHalfJo[0][0]),self.lidHalfJo[0][2]] ; exJo = []
  for x in jo :
   if cmds.objExists(x) :
    exJo.append(x)
  if len(exJo) == len(jo) :
   sys.stderr.write('There already exists.')
   cmds.select(jo,replace=1)
  elif len(exJo) > 0 :
   cmds.warning('Trouble.')
  else :
   self.xCons(self.faceJo,'xTrans_face')
   #list = [[self.uplidJo[2],self.uplidJo[3],self.uplidJo[0],'uplidHalfRotL','uplidHalfL',self.uplidJo[1]]]
   list = [[self.lidHalfJo[0][0],self.lidHalfJo[0][1],self.lidJo[0],'uplidHalfRotL','uplidHalfL',self.lidJo[1]]]
   list += [[self.lolidJo[2],self.lolidJo[3],self.lolidJo[0],'lolidHalfRotL','lolidHalfL',self.lolidJo[1]]]
   list += [[self.L2R(self.uplidJo[2]),self.L2R(self.uplidJo[3]),self.L2R(self.uplidJo[0]),'uplidHalfRotR','uplidHalfR',self.L2R(self.uplidJo[1])]]
   list += [[self.L2R(self.lolidJo[2]),self.L2R(self.lolidJo[3]),self.L2R(self.lolidJo[0]),'lolidHalfRotR','lolidHalfR',self.L2R(self.lolidJo[1])]]
   for y in list :
    cmds.createNode('joint',name=y[0],parent='xTrans_face')
    cmds.createNode('joint',name=y[1],parent=y[0])
    cmds.connectAttr(y[2]+'.translate',y[0]+'.translate')
    cmds.connectAttr(y[2]+'.jointOrient',y[0]+'.jointOrient')
    cmds.createNode('multDoubleLinear',name='mdl_'+y[3])
    cmds.connectAttr(y[2]+'.rotateX','mdl_'+y[3]+'.input1')
    cmds.setAttr('mdl_'+y[3]+'.input2',0.5)
    cmds.connectAttr('mdl_'+y[3]+'.output',y[0]+'.rotateX')
    cmds.createNode('multDoubleLinear',name='mdl_'+y[4])
    cmds.connectAttr(y[5]+'.translateZ','mdl_'+y[4]+'.input1')
    cmds.setAttr('mdl_'+y[4]+'.input2',0.5)
    cmds.connectAttr('mdl_'+y[4]+'.output',y[1]+'.translateZ')

 def createTongueExtra(self,*a):
  if cmds.objExists(self.tongueJo[0]) == 0 :
   cmds.warning('Trouble.')
  else :
   for i in range(1,len(self.tongueJo)) :
    if cmds.objExists(self.tongueJo[i]) :
     lt = cmds.createNode('joint',name=self.tongueLJo[i],parent=self.tongueJo[i])
     rt = cmds.createNode('joint',name=self.tongueRJo[i],parent=self.tongueJo[i])
     cj = self.tongueJo[i+1]
     if cmds.objExists(cj) == 0 :
      cj = self.tongueTipJo
     ga = cmds.getAttr(cj+'.translateZ')
     cmds.setAttr(lt+'.translateZ',ga*0.5)
     cmds.setAttr(lt+'.translateX',ga*0.5)
     cmds.setAttr(rt+'.translateZ',ga*0.5)
     cmds.setAttr(rt+'.translateX',ga*-.5)

 def createJointOut(self,dJo,joList,pJo,name,pName,*a): # oJo = self.kneeOutJo ; dJo = self.kneeJo ; name = 'knee' ; pName = 'hip'
  #ex = [joList[0],self.L2R(joList[0]),joList[1],self.L2R(joList[1]),joList[2],self.L2R(joList[2])]
  ex = [joList[0],self.L2R(joList[0])]
  exSel = ['vTrans_'+name+'RoL','vTrans_'+name+'RoR','cons_'+name+'OutL','cons_'+name+'OutR','pin_'+name+'RoL','pin_'+name+'RoR']
  #exSel += ['trans_'+name+'PullL','trans_'+name+'PullR','trans_'+name+'PushL','trans_'+name+'PushR']
  if self.exCheck(ex):
   cmds.showHidden(ex,above=1)
   cmds.select(exSel,replace=1)
   sys.stderr.write('There already exists.')
  else:
   side = ['L','R'] ; dir = [1,-1]
   for i in range(2):
    s = side[i]
    self.consCheck([name+s,pName+s])
    av = self.analyzeAxis(self.L2R(dJo,i))
    nr = 'noRo_'+name+s
    if cmds.objExists('noRo_'+name+s)==0:
     cmds.createNode('transform',name=nr,parent='xTrans_'+pName+s,skipSelect=1)
     cmds.connectAttr(self.L2R(dJo,i)+'.translate','noRo_'+name+s+'.translate')
    vt = cmds.createNode('transform',name='vTrans_'+name+'Ro'+s,parent=nr,skipSelect=1) # create drive value
    v = cmds.createNode('transform',name='v_'+name+'Ro'+s,parent=vt,skipSelect=1)
    pin = cmds.createNode('transform',name='pin_'+name+'Ro'+s,parent='xTrans_'+name+s,skipSelect=1)
    ga = cmds.getAttr(self.L2R(dJo,i)+'.translate'+av[0])
    cmds.setAttr(vt+'.translate'+av[0],ga/2)
    cmds.setAttr(pin+'.translate'+av[0],ga/2)
    cmds.pointConstraint(pin,v)
    joC = cmds.createNode('transform',name='cons_'+name+'Out'+s,parent=nr,skipSelect=1)
    joT = cmds.createNode('transform',name='trans_'+name+'Out'+s,parent=joC,skipSelect=1) # create joint hierarchy
    joX = cmds.createNode('transform',name='exp_'+name+'Out'+s,parent=joT,skipSelect=1)
    jo = cmds.createNode('joint',name=self.L2R(joList[0],i),parent=joX,skipSelect=1)
    cmds.addAttr(jo,longName='weightX',attributeType='double',defaultValue=0,keyable=1)
    cmds.addAttr(jo,longName='weightY',attributeType='double',defaultValue=0,keyable=1)
    cmds.addAttr(jo,longName='weightZ',attributeType='double',defaultValue=1,keyable=1)
    cmds.orientConstraint(self.L2R(pJo,i),self.L2R(dJo,i),joC,name='oCons_'+name+'Out'+s)
    cmds.setAttr('oCons_'+name+'Out'+s+'.interpType',2)
    cmds.setAttr(joT+'.tz',-av[2]) # set offset value
    mult = cmds.createNode('multiplyDivide',name='mult_'+name+s,skipSelect=1)
    cmds.connectAttr(v+'.translate'+av[0],mult+'.input1X')
    cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Y')
    cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Z')
    cmds.connectAttr(jo+'.weightX',mult+'.input2X')
    cmds.connectAttr(jo+'.weightY',mult+'.input2Y')
    cmds.connectAttr(jo+'.weightZ',mult+'.input2Z')
    cmds.connectAttr(mult+'.output',joX+'.translate')

    #joT = cmds.createNode('transform',name='trans_'+name+'Pull'+s,parent=nr,skipSelect=1) # create joint hierarchy
    #joC = cmds.createNode('transform',name='cons_'+name+'Pull'+s,parent=joT,skipSelect=1)
    #jo = cmds.createNode('joint',name=self.L2R(joList[1],i),parent=joC,skipSelect=1)
    #cmds.addAttr(jo,longName='weightX',attributeType='double',defaultValue=1,keyable=1)
    #cmds.addAttr(jo,longName='weightY',attributeType='double',defaultValue=0,keyable=1)
    #cmds.addAttr(jo,longName='weightZ',attributeType='double',defaultValue=0,keyable=1)
    #cmds.setAttr(joT+'.tx',-av[2]) # set offset value
    #cmds.setAttr(joT+'.tz',av[2]) # set offset value
    #mult = cmds.createNode('multiplyDivide',name='mult_'+name+'Pull'+s,skipSelect=1)
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1X')
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Y')
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Z')
    #cmds.connectAttr(jo+'.weightX',mult+'.input2X')
    #cmds.connectAttr(jo+'.weightY',mult+'.input2Y')
    #cmds.connectAttr(jo+'.weightZ',mult+'.input2Z')
    #cmds.connectAttr(mult+'.output',joC+'.translate')
	
    #joT = cmds.createNode('transform',name='trans_'+name+'Push'+s,parent='xTrans_'+name+s,skipSelect=1) # create joint hierarchy
    #joC = cmds.createNode('transform',name='cons_'+name+'Push'+s,parent=joT,skipSelect=1)
    #jo = cmds.createNode('joint',name=self.L2R(joList[2],i),parent=joC,skipSelect=1)
    #cmds.addAttr(jo,longName='weightX',attributeType='double',defaultValue=-1,keyable=1)
    #cmds.addAttr(jo,longName='weightY',attributeType='double',defaultValue=0,keyable=1)
    #cmds.addAttr(jo,longName='weightZ',attributeType='double',defaultValue=0,keyable=1)
    #cmds.setAttr(joT+'.tx',av[2]) # set offset value
    #cmds.setAttr(joT+'.tz',av[2]) # set offset value
    #mult = cmds.createNode('multiplyDivide',name='mult_'+name+'Push'+s,skipSelect=1)
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1X')
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Y')
    #cmds.connectAttr(v+'.translate'+av[0],mult+'.input1Z')
    #cmds.connectAttr(jo+'.weightX',mult+'.input2X')
    #cmds.connectAttr(jo+'.weightY',mult+'.input2Y')
    #cmds.connectAttr(jo+'.weightZ',mult+'.input2Z')
    #cmds.connectAttr(mult+'.output',joC+'.translate')
	
#self.elbowFixJo
   cmds.select(ex,replace=1)

# Extra Joint : Arm Twist
 def createArmTwist(self,*a):
  joList = [(self.armJo[0],self.elbowJo[0]),(self.wristJo[0],self.wristJo[0])]
  joList += [(self.L2R(self.armJo[0]),self.L2R(self.elbowJo[0])),(self.L2R(self.wristJo[0]),self.L2R(self.wristJo[0]))]
  joList += [(self.arm2Jo[0],self.elbow2Jo[0]),(self.wrist2Jo[0],self.wrist2Jo[0])]
  joList += [(self.L2R(self.arm2Jo[0]),self.L2R(self.elbow2Jo[0])),(self.L2R(self.wrist2Jo[0]),self.L2R(self.wrist2Jo[0]))]
  nList = ['upperarmTwistL','wristTwistL','upperarmTwistR','wristTwistR','upperarm2TwistL','wrist2TwistL','upperarm2TwistR','wrist2TwistR']
  selList = [] ; ctList = [] # createList
  xList = ['shoulderL','elbowL','shoulderR','elbowR','viceShoulderL','viceElbowL','viceShoulderR','viceElbowR']
  twList = [self.armTwist,self.elbowTwist,self.L2R(self.armTwist),self.L2R(self.elbowTwist)]
  twList += [self.viceArmTwist,self.viceElbowTwist,self.L2R(self.viceArmTwist),self.L2R(self.viceElbowTwist)]
  for i,x in enumerate(joList):
   if self.exCheck(x):
    if self.exCheck('cons_'+nList[i]): selList.append('cons_'+nList[i])
    else:
     self.consCheck(xList[i])
     self.createTwist(nList[i],'xTrans_'+xList[i],x[0],x[1],twList[i])
     if x[0]!=x[1] : cmds.connectAttr(x[0]+'.scaleX','cons_'+nList[i]+'.scaleX')
     else : self.connectKneeOffset(nList[i],'xTrans_'+xList[i])
     ctList.append('cons_'+nList[i])

  if len(ctList)>0 :
   cmds.select(ctList,replace=1) ; cmds.showHidden(ctList,above=1)
   sys.stderr.write('Create twist joint.')
  else :
   cmds.select(selList,replace=1) ; cmds.showHidden(selList,above=1)
   sys.stderr.write('There already exists.')

# Extra Joint : Leg Twist
 def createLegTwist(self,*a):
  joList = [(self.hipJo[0],self.kneeJo[0]),(self.ankleJo[0],self.ankleJo[0])]
  joList += [(self.L2R(self.hipJo[0]),self.L2R(self.kneeJo[0])),(self.L2R(self.ankleJo[0]),self.L2R(self.ankleJo[0]))]
  joList += [(self.rearHipJo,self.rearKneeJo),(self.rearAnkleJo,self.rearAnkleJo)]
  joList += [(self.L2R(self.rearHipJo),self.L2R(self.rearKneeJo)),(self.L2R(self.rearAnkleJo),self.L2R(self.rearAnkleJo))]
  nList = ['thighTwistL','ankleTwistL','thighTwistR','ankleTwistR','rearThighTwistL','rearAnkleTwistL','rearThighTwistR','rearAnkleTwistR']
  selList = [] ; ctList = [] # create
  xList= ['pelvis','kneeL','pelvisR','kneeR','rearPelvis','rearKneeL','rearPelvisR','rearKneeR']
  twList = [self.hipTwist,self.kneeTwist,self.L2R(self.hipTwist),self.L2R(self.kneeTwist),self.rearHipTwist,self.rearKneeTwist,self.L2R(self.rearHipTwist),self.L2R(self.rearKneeTwist)]
  for i,x in enumerate(joList):
   if self.exCheck(x):
    if self.exCheck('cons_'+nList[i]): selList.append('cons_'+nList[i])
    else:
     self.consCheck(xList[i])
     self.createTwist(nList[i],'xTrans_'+xList[i],x[0],x[1],twList[i])
     if x[0]!=x[1] : cmds.connectAttr(x[0]+'.scaleX','cons_'+nList[i]+'.scaleX')
     else : self.connectKneeOffset(nList[i],'xTrans_'+xList[i])
     ctList.append('cons_'+nList[i])

  if len(ctList)>0 :
   cmds.select(ctList,replace=1) ; cmds.showHidden(ctList,above=1)
   sys.stderr.write('Create twist joint.')
  else :
   cmds.select(selList,replace=1) ; cmds.showHidden(selList,above=1)
   sys.stderr.write('There already exists.')
 
# Extra Joint : Finger Assist
 def createFingerAssist(self,*a):
  self.createAssistA('jo_thumb1L','jo_thumb1OutL','xCons_thumb1L')
  self.createAssistA('jo_thumb2L','jo_thumb2OutL','xCons_thumb2L')
  self.createAssistA('jo_index1L','jo_index1OutL','xCons_index1L')
  self.createAssistA('jo_index2L','jo_index2OutL','xCons_index2L')
  self.createAssistA('jo_index3L','jo_index3OutL','xCons_index3L')
  self.createAssistA('jo_middle1L','jo_middle1OutL','xCons_middle1L')
  self.createAssistA('jo_middle2L','jo_middle2OutL','xCons_middle2L')
  self.createAssistA('jo_middle3L','jo_middle3OutL','xCons_middle3L')
  self.createAssistA('jo_ring1L','jo_ring1OutL','xCons_ring1L')
  self.createAssistA('jo_ring2L','jo_ring2OutL','xCons_ring2L')
  self.createAssistA('jo_ring3L','jo_ring3OutL','xCons_ring3L')
  self.createAssistA('jo_little1L','jo_little1OutL','xCons_little1L')
  self.createAssistA('jo_little2L','jo_little2OutL','xCons_little2L')
  self.createAssistA('jo_little3L','jo_little3OutL','xCons_little3L')
  self.createAssistA('jo_thumb1R','jo_thumb1OutR','xCons_thumb1R')
  self.createAssistA('jo_thumb2R','jo_thumb2OutR','xCons_thumb2R')
  self.createAssistA('jo_index1R','jo_index1OutR','xCons_index1R')
  self.createAssistA('jo_index2R','jo_index2OutR','xCons_index2R')
  self.createAssistA('jo_index3R','jo_index3OutR','xCons_index3R')
  self.createAssistA('jo_middle1R','jo_middle1OutR','xCons_middle1R')
  self.createAssistA('jo_middle2R','jo_middle2OutR','xCons_middle2R')
  self.createAssistA('jo_middle3R','jo_middle3OutR','xCons_middle3R')
  self.createAssistA('jo_ring1R','jo_ring1OutR','xCons_ring1R')
  self.createAssistA('jo_ring2R','jo_ring2OutR','xCons_ring2R')
  self.createAssistA('jo_ring3R','jo_ring3OutR','xCons_ring3R')
  self.createAssistA('jo_little1R','jo_little1OutR','xCons_little1R')
  self.createAssistA('jo_little2R','jo_little2OutR','xCons_little2R')
  self.createAssistA('jo_little3R','jo_little3OutR','xCons_little3R')

# Extra Joint : Pelvis Seperate
 def createCutPelvis(self,*a):
  ex = [self.pelvisSplitJo,self.L2R(self.pelvisSplitJo)]
  exSel = ['cons_pelvisJoL','cons_pelvisJoR']
  if self.exCheck(ex):
   cmds.showHidden(ex,above=1)
   cmds.select(exSel,replace=1)
   sys.stderr.write('There already exists.')
  else:
   side = ['L','R'] ; dir = [1,-1] ; sSide = ['','R']
   self.consCheck('pelvis')
   if cmds.objExists('xTrans_pelvisR')==0:
    cmds.createNode('transform',name='xTrans_pelvisR',parent='xTrans_pelvis',skipSelect=1)
    cmds.setAttr('xTrans_pelvisR.rotateX',-180)
   
   for i in range(2):
    s = side[i]
    cmds.createNode('transform',name='cons_pelvisJo'+s,parent='xTrans_pelvis'+sSide[i],skipSelect=1)
    cmds.createNode('transform',name='trans_pelvisJo'+s,parent='cons_pelvisJo'+s,skipSelect=1)
    cmds.createNode('joint',name=self.L2R(self.pelvisSplitJo,i),parent='trans_pelvisJo'+s)
    cmds.aimConstraint(self.L2R(self.hipJo[0],i),'cons_pelvisJo'+s,aimVector=[0,-1,0],upVector=[0,0,1],worldUpType='none')
    cmds.setAttr('trans_pelvisJo'+s+'.translateY',-1.0)

# Extra Joint : Shoulder IK
 def createShoulderIk(self,*a):
  self.xCons('jcC00_chest','xTrans_chest')
  shoulderIkNameList=['jo_shoulderIkL','jo_shoulderIkR']
  shoulderJoList=['jlM00_shoulderL','jrM00_shoulderR']
  shoulderIkJoList=['jlM20_shoulderIkL','jrM20_shoulderIkR']
  armJoList=['jlN00_armL','jrN00_armR']
  shoulderIkTipList=['jlM25_shoulderIkTipL','jrM25_shoulderIkTipR']
  for i in range(len(shoulderIkJoList)):
   if cmds.objExists(shoulderIkJoList[i])==1:
    cmds.showHidden(shoulderIkJoList[i],above=1)
    sys.stderr.write('shoulderIK already exist, set visibility on.')
   else :
    cmds.createNode('transform',name=shoulderIkNameList[i]+'_trans',parent='xTrans_chest')
    cmds.connectAttr(shoulderJoList[i]+'.t',shoulderIkNameList[i]+'_trans.t')
    cmds.createNode('joint',name=shoulderIkJoList[i],parent=shoulderIkNameList[i]+'_trans')
    if shoulderIkJoList[i][-1] == 'L' : cmds.aimConstraint(armJoList[i],shoulderIkJoList[i],aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
    if shoulderIkJoList[i][-1] == 'R' : cmds.aimConstraint(armJoList[i],shoulderIkJoList[i],aimVector=[-1,0,0],upVector=[0,-1,0],worldUpType='none')
    cmds.createNode('joint',name=shoulderIkTipList[i],parent=shoulderIkJoList[i])
    cmds.pointConstraint(armJoList[i],shoulderIkTipList[i])
    cmds.setAttr(shoulderIkTipList[i]+'.v',0)
    cmds.setAttr(shoulderIkJoList[i]+'.displayHandle',1)
    if shoulderIkJoList[i][-1] == 'L' : cmds.setAttr(shoulderIkJoList[i]+'.selectHandleX',1)
    if shoulderIkJoList[i][-1] == 'R' : cmds.setAttr(shoulderIkJoList[i]+'.selectHandleX',-1)
    if shoulderIkJoList[i][-1] == 'L' :  cmds.setAttr(shoulderIkJoList[i]+'.selectHandleY',1)
    if shoulderIkJoList[i][-1] == 'R' :  cmds.setAttr(shoulderIkJoList[i]+'.selectHandleY',-1)
  cmds.select(shoulderIkJoList,r=1)

 def createAxisFix(self,axis,dir,sAxis,*a):
  sls = cmds.ls(selection=1)
  sll = cmds.ls(selection=1,long=1)
  #self.consCheck('armL')
  dirName = {1:'Plus',-1:'Minus'} ; sideName = {}
  if axis=='X' : osAxis1 = 'Z' ; osAxis2 = 'Y' ; sideName = {1:'Fore',-1:'Back'}
  if axis=='Y' : osAxis1 = 'Z' ; osAxis2 = 'X' ; sideName = {1:'Out',-1:'In'}
  if axis=='Z' : osAxis1 = 'Y' ; osAxis2 = 'X' ; sideName = {1:'Up',-1:'Low'}
  
  for i,x in enumerate(sls) : # each selection's loop ....?
   xp = cmds.listRelatives(sll[i],parent=1)[0] # x's parent
   pn = xp[6:-1]+'Tip'+sideName[dir]+xp[-1] # parent name
   xn = x[6:-1]+sideName[dir]+x[-1] # x(seletion) = joint name
   sxn = x[6:-1]+sAxis+x[-1] # sub x(seletion) name

   self.consCheck(x[6:])
   if cmds.objExists('pos_'+x[6:])==0 :
    self.consCheck(xp[6:])
    cmds.createNode('transform',name='pos_'+x[6:],parent='xTrans_'+xp[6:],skipSelect=1)
    cmds.connectAttr(sll[i]+'.translate','pos_'+x[6:]+'.translate')

   n = [pn,xn] ; p = [xp[6:],x[6:]]
   hrc = ['pos_'+x[6:],'xTrans_'+x[6:]] ; mv = [-1,1] ; lr = 1
   if self.joBelong(x) == 'R' : lr = -1
   for j in range(2) : # two side joint's loop
    cmds.createNode('transform',name='trans_'+n[j],parent=hrc[j],skipSelect=1)
    cmds.createNode('transform',name='cons_'+n[j],parent='trans_'+n[j],skipSelect=1)
    cmds.createNode('joint',name='jo_'+n[j],parent='cons_'+n[j],skipSelect=1) # create joint is here !
    cmds.setAttr('trans_'+n[j]+'.translate'+osAxis1,dir*lr,lock=1)
    cmds.setAttr('trans_'+n[j]+'.translate'+osAxis2,mv[j]*lr,lock=1)
    cmds.createNode('plusMinusAverage',name='plus_'+n[j],skipSelect=1)
    cmds.connectAttr('plus_'+n[j]+'.output3D','cons_'+n[j]+'.translate')

    v = [xn,sxn] ; ax=[axis,sAxis]
    for ii in range(2) :
     da = sll[i]+'.quat'+ax[ii]
     if cmds.objExists(da) == 0 : self.quatRot(x,ax[ii])
     if cmds.objExists(da+'0') : da = da+'0'
     if cmds.objExists('mdl_'+v[ii])==0 :
      cmds.createNode('multDoubleLinear',name='mdl_'+v[ii],skipSelect=1)
      cmds.connectAttr(da,'mdl_'+v[ii]+'.input1')
      cmds.setAttr('mdl_'+v[ii]+'.input2',0.1*dir)
     cd = cmds.createNode('condition',name='cd_'+n[j][0:-1]+ax[ii]+x[-1],skipSelect=1)
     cmds.connectAttr(cd+'.outColor','plus_'+n[j]+'.input3D['+str(ii)+']')
     cmds.connectAttr(da,cd+'.firstTerm')
     if dir == 1 : cmds.setAttr(cd+'.operation',3)
     if dir == -1 : cmds.setAttr(cd+'.operation',5)
	
     pm = ['Weight','Opposite'] ; tfa = ['.colorIfTrue','.colorIfFalse']
     for ij in range(2) : # condition plus the minus multiply node's loop
      mult = cmds.createNode('multiplyDivide',name='mult_'+n[j][0:-1]+ax[ii]+dirName[mv[ij]]+x[-1],skipSelect=1)
      cmds.connectAttr('mdl_'+v[ii]+'.output',mult+'.input1X')
      cmds.connectAttr('mdl_'+v[ii]+'.output',mult+'.input1Y')
      cmds.connectAttr('mdl_'+v[ii]+'.output',mult+'.input1Z')

      for ji,xyz in enumerate(['X','Y','Z']) :
       an = ax[ii].lower()+pm[ij]+xyz # attribute name
       cmds.addAttr('jo_'+n[j],longName=an,attributeType='double',keyable=1)
       cmds.connectAttr('jo_'+n[j]+'.'+an,mult+'.input2'+xyz)
      cmds.connectAttr(mult+'.output',cd+tfa[ij])

 def createAssistA(self,jo,n,xCons,*a): # for finger additional joint
  self.xCons(jo,xCons)
  cmds.createNode('transform',name=n+'_transA',parent=xCons)
  cmds.createNode('transform',name=n+'_transB',parent=n+'_transA')
  child = cmds.listRelatives(jo,children=1)
  cmds.createNode('multDoubleLinear',name='mdl_'+jo+'Tx_trans')  
  cmds.connectAttr(child[0]+'.tx','mdl_'+jo+'Tx_trans.input1')
  cmds.setAttr('mdl_'+jo+'Tx_trans.input2',0.2)
  cmds.connectAttr('mdl_'+jo+'Tx_trans.output',n+'_transA.ty')
  cmds.createNode('joint',name=n,parent=n+'_transB')
  cmds.createNode('multDoubleLinear',name='mdl_'+jo+'Tx')
  cmds.connectAttr(jo+'.rz','mdl_'+jo+'Tx.input1')
  rate = cmds.getAttr(child[0]+'.tx') / 80
  cmds.setAttr('mdl_'+jo+'Tx.input2',rate)
  cmds.connectAttr('mdl_'+jo+'Tx.output',n+'_transB.tx')

 def createAssistB(self,n,nOut,vp,p,j,jo,dir,*a): # no use ?
  cmds.createNode('transform',name=n+'_roV_trans',parent=vp)
  cmds.createNode('transform',name=n+'_roV',parent=n+'_roV_trans')
  cmds.createNode('transform',name=n+'_ro_trans',parent=vp)
  cmds.createNode('transform',name=n+'_ro',parent=n+'_ro_trans')
  if dir == 'x' : cmds.setAttr(n+'_roV_trans.tx',5)
  if dir == 'x' : cmds.setAttr(n+'_ro.tx',5)
  if dir == 'y' : cmds.setAttr(n+'_roV_trans.ty',-5)
  if dir == 'y' : cmds.setAttr(n+'_ro.ty',-5)
  cmds.orientConstraint(j,n+'_ro_trans')
  cmds.pointConstraint(n+'_ro',n+'_roV')
  cmds.createNode('transform',name=nOut+'_trans',parent=p)
  cmds.createNode('joint',name=jo,parent=nOut+'_trans')
  if dir == 'x' :
   cmds.setAttr(nOut+'_trans.tz',-.5)
   cmds.createNode('multDoubleLinear',name='mdl_'+nOut+'Tx')
   cmds.createNode('multDoubleLinear',name='mdl_'+nOut+'Tz')
   cmds.connectAttr(n+'_roV.tx','mdl_'+nOut+'Tx.input1')
   cmds.connectAttr(n+'_roV.tx','mdl_'+nOut+'Tz.input1')
   cmds.setAttr('mdl_'+nOut+'Tx.input2',0.5)
   cmds.setAttr('mdl_'+nOut+'Tz.input2',0.5)
   cmds.connectAttr('mdl_'+nOut+'Tx.output',jo+'.tx')
   cmds.connectAttr('mdl_'+nOut+'Tz.output',jo+'.tz')
  if dir == 'y' :
   cmds.setAttr(nOut+'_trans.tz',0.5)
   cmds.createNode('multDoubleLinear',name='mdl_'+nOut+'Ty')
   cmds.createNode('multDoubleLinear',name='mdl_'+nOut+'Tz')
   cmds.connectAttr(n+'_roV.ty','mdl_'+nOut+'Ty.input1')
   cmds.connectAttr(n+'_roV.ty','mdl_'+nOut+'Tz.input1')
   cmds.setAttr('mdl_'+nOut+'Ty.input2',0.5)
   cmds.setAttr('mdl_'+nOut+'Tz.input2',0.5)
   cmds.connectAttr('mdl_'+nOut+'Ty.output',jo+'.ty')
   cmds.connectAttr('mdl_'+nOut+'Tz.output',jo+'.tz')

 def createTwist(self,n,p,tj,dir,jq,*a): # extra joint : twist process
  # exsample :
  # n = 'shoulderLTwist' ; p = 'xCons_shoulderL' ; tj = 'jlN00_armL' ; dir = 'jlP00_elbowL'
  # jq = ['jlN20_armLTw0','jlN30_armLTw1','jlN40_armLTw2','jlN50_armLTw3','jlN60_armLTw4']
  # if it's tail end tj == dir

  axis = self.analyzeAxis(dir)
  handleAttr = '.selectHandleY'
  if axis[0]=='Y': handleAttr = '.selectHandleZ'
  if axis[0]=='Z': handleAttr = '.selectHandleX'

  cmds.createNode('transform',name='cons_'+n,parent=p,skipSelect=1)
  cmds.createNode('transform',name='exp_'+n,parent='cons_'+n,skipSelect=1)
  if tj!= dir :
   cmds.pointConstraint(tj,'cons_'+n)
   cmds.connectAttr(tj+'.scale','cons_'+n+'.scale')
  else :
   cmds.matchTransform('exp_'+n,dir,pivots=1)
  cmds.aimConstraint(dir,'cons_'+n,aimVector=axis[1],upVector=[0,1,0],worldUpType='none')
  cmds.createNode('transform',name=n,parent='exp_'+n,skipSelect=1)
  cmds.createNode('multMatrix',name='xMult_'+n,skipSelect=1)
  cmds.connectAttr(tj+'.worldMatrix[0]','xMult_'+n+'.matrixIn[0]')
  cmds.connectAttr(p+'.worldInverseMatrix[0]','xMult_'+n+'.matrixIn[1]')
  cmds.createNode('decomposeMatrix',name='xCons_'+n,skipSelect=1)
  cmds.connectAttr('xMult_'+n+'.matrixSum','xCons_'+n+'.inputMatrix')
  cmds.createNode('quatToEuler',name='q2e_'+n,parent='exp_'+n,skipSelect=1)
  cmds.connectAttr('xCons_'+n+'.outputQuat'+axis[0],'q2e_'+n+'.inputQuat'+axis[0])
  cmds.connectAttr('xCons_'+n+'.outputQuatW','q2e_'+n+'.inputQuatW')
  cmds.connectAttr('q2e_'+n+'.outputRotate'+axis[0],n+'.rotate'+axis[0])

  transWeight = [0.025,0.25,0.5,0.75,0.975] ; ma = ['','X','Y','Z']
  for i,x in enumerate(jq) :
   jp = cmds.createNode('transform',name='cons_'+x[3:],parent='exp_'+n,skipSelect=1) # joint parent
   #cmds.createNode('joint',name=x,parent=jp,skipSelect=1)
   self.createJoint(x,jp)
   
   cmds.setAttr(x+'.displayHandle',1)
   cmds.setAttr(x+handleAttr,axis[2]*3)
   pmv = cmds.createNode('plusMinusAverage',name='plus_'+x[3:],skipSelect=1) #new
   mult = cmds.createNode('multiplyDivide',name='mult_'+x[3:]+'Trans',skipSelect=1) #new
   cmds.connectAttr(dir+'.translate',mult+'.input1') #new
   cmds.setAttr(mult+'.input2',transWeight[i],transWeight[i],transWeight[i],type='double3') # new
   cmds.connectAttr(mult+'.output',jp+'.translate')
   if axis[0] == 'X' : cmds.transformLimits(n,ry=(0,0),rz=(0,0),ery=(1,1),erz=(1,1))
   if axis[1] == 'Y' : cmds.transformLimits(n,rx=(0,0),rz=(0,0),erx=(1,1),erz=(1,1))
   if axis[2] == 'Z' : cmds.transformLimits(n,rx=(0,0),ry=(0,0),erx=(1,1),ery=(1,1))
   if i == 1 : cmds.createNode('multiplyDivide',name='mult_'+n+'Rot',skipSelect=1)
   if i in [1,2,3]:
    cmds.connectAttr(n+'.rotate'+axis[0],'mult_'+n+'Rot.input1'+ma[i])
    cmds.setAttr('mult_'+n+'Rot.input2'+ma[i],transWeight[i])
    cmds.connectAttr('mult_'+n+'Rot.output'+ma[i],'cons_'+x[3:]+'.rotate'+axis[0])
   if i == 4 : cmds.connectAttr(n+'.rotate'+axis[0],'cons_'+x[3:]+'.rotate'+axis[0])

##############################################################################################################
############################################## Generate Controller ###########################################
##############################################################################################################

 def chDefine(self,*a): # charactor height
  bbJo = [ self.rootJo,self.chestJo,self.neckJo[0],self.headJo,self.topJo,self.shoulderJo[0],self.armJo[0],self.wristJo[0],self.indexJo[1],self.pelvisJo,self.kneeJo[0],self.ankleJo[0],self.ballJo[0],self.middleToeJo[0],self.middleToeJo[1] ]
  bbGrp = cmds.createNode('transform',skipSelect=1)
  for x in bbJo :
   if cmds.objExists(x):
    tLoc = cmds.createNode('transform',parent=bbGrp,skipSelect=1)
    cmds.matchTransform(tLoc,x)
    if self.joBelong(x) == 'L' :
     tLoc = cmds.createNode('transform',parent=bbGrp,skipSelect=1)
     cmds.matchTransform(tLoc,self.L2R(x))
  bb = cmds.xform(bbGrp,q=1,bb=1)
  cmds.delete(bbGrp)
  bb_x = bb[3] - bb[0] ; bb_y = bb[4] - bb[1] ; bb_z = bb[5] - bb[2]
  ch = max(bb_x,bb_y,bb_z) * 0.15
  ctrlDir = 1
  if bb_z > bb_y : ctrlDir = 2
  return ch,ctrlDir

 def defineCtrlAttr(self,*a):
 # color arrange note [H,0.5,0.5], [H,0.72,0.32], [H,0.94,0.14]
 # 0.000 red     : arm, hand
 # 0.111 orange  : 2nd arm, 2nd hand
 # 0.222 yellow  : finger
 # 0.333 green   : torso, head
 # 0.444 cyan    : head parts <- new define
 # 0.555 blue    : 2nd leg, 2nd foot
 # 0.666 indigo  : leg, foot
 # 0.777 purple  : facial
 # 0.888 magenta : wing
  self.ctrlPos = {
  'torso':     ['rRect',0,0,0,4,1.6]
  ,'waist':    ['rect',0,42,0,2.5,1]
  ,'chest':    ['chest',0,80,0,2,2]
  ,'neck':     ['rect',0,110,0,1.2,0.5]
  ,'head':     ['moon',0,160,0,1.2,2.4]
  ,'pelvis':   ['trig',0,-35,0,3,2,0]
  ,'shoulderL':['trig',40,92,0,1.8,1.7]
  ,'upperarmL':['rect',85,85,0,3,0.75]
  ,'forearmL': ['rect',150,85,0,3,0.75]
  ,'wristL':   ['circ',105,-52,0,1.2,1.2]
  ,'elbowL':   ['rect',135,25,45,1,1]
  ,'handL':    ['rect',135,-52,0,1.5,1.5]
  ,'thighL':   ['rect',25,-75,0,1,3]
  ,'shankL':   ['rect',25,-140,0,1,3]
  ,'ankleL':   ['rect',25,-190,0,1.2,1.2]
  ,'kneeL':    ['rect',55,-110,0,1,1]
  ,'heelL':    ['rect',55,-162,0,0.8,0.8]
  ,'legL':     ['rect',55,-190,0,1.5,1.5]
  ,'toeL':     ['trig',40,-215,0,1,1]
  
  ,'fingerL': ['rect',120,-85,0,2,1]
  ,'thumb0L': ['trig',90,-85,0,0.7,1.4]
  ,'thumb1L': ['trig',90,-105,0,0.7,1.4]
  ,'thumb2L': ['trig',90,-125,0,0.7,1.4]
  ,'index1L': ['trig',108,-108,0,0.7,1.4]
  ,'index2L': ['trig',108,-128,0,0.7,1.4]
  ,'index3L': ['trig',108,-148,0,0.7,1.4]
  ,'middle1L': ['trig',121,-108,0,0.7,1.4]
  ,'middle2L': ['trig',121,-128,0,0.7,1.4]
  ,'middle3L': ['trig',121,-148,0,0.7,1.4]
  ,'ring1L': ['trig',135,-108,0,0.7,1.4]
  ,'ring2L': ['trig',135,-128,0,0.7,1.4]
  ,'ring3L': ['trig',135,-148,0,0.7,1.4]
  ,'little1L': ['trig',149,-108,0,0.7,1.4]
  ,'little2L': ['trig',149,-128,0,0.7,1.4]
  ,'little3L': ['trig',149,-148,0,0.7,1.4]
  
  ,'jaw':['moon',0,160,0,1,1.2]
  ,'eyeL':['rect',20,195,0,0.25,0.2]
  ,'browL':['rect',20,210,0,0.25,0.2]
  ,'glabella':['rect',0,155,0,0.25,0.2]
  ,'upLidL':['moon',20,200,180,1,1]
  ,'loLidL':['moon',20,190,0,1,1]
  ,'cheekL':['rect',12,135,0,0.25,0.2]
  ,'nasalisL':['rect',4,135,0,0.25,0.2]
  ,'gillL':['rect',0,140,0,0.25,0.2]
  ,'upLip':['rect',0,130,0,0.25,0.2]
  ,'uplipL':['rect',4,130,0,0.25,0.2]
  ,'cornerL':['rect',8,125,0,0.25,0.2]
  ,'loLipL':['rect',4,120,0,0.25,0.2]
  ,'loLip':['rect',0,120,0,0.25,0.2]
  
  ,'ribcage':['rect',0,-250,0,1,1]
  ,'belly':['rect',0,-275,0,1,1]
  ,'rearPelvis':['rect',0,-300,0,1,1]
  }
  for x,y in self.ctrlPos.items():
   if x[-1] == 'L' :
    r = x[:-1]+'R'
    self.ctrlPos[r] = y[:]
    self.ctrlPos[r][1] = self.ctrlPos[r][1] * -1

 def createCtrl(self,*a):

  ov = cmds.optionMenu('oMenu',q=1,value=1)
  self.defineCtrlAttr()

  if cmds.objExists(self.rootJo) == 0 :
   sys.stderr.write('No Joints.')
   return;
  self.deleteCtrl()
  self.createHierachy()
  ch = self.chDefine()[0]
  ctrlDir = self.chDefine()[1]
  cmds.setAttr(self.rootJo+'.v',0)
  
  #ctrlDir = 1 # which is Y
  #if bb_z > bb_y : ctrlDir = 2
  if cmds.objExists('ctrl_move.bodyCtrlVisibility') == 0 : cmds.addAttr('ctrl_move',longName='bodyCtrlVisibility',attributeType='bool',keyable=1)
  if cmds.objExists('ctrl_move.faceCtrlVisibility') == 0 : cmds.addAttr('ctrl_move',longName='faceCtrlVisibility',attributeType='bool',keyable=1)
  cmds.setAttr('ctrl_move.bodyCtrlVisibility',1,keyable=0,channelBox=1)
  cmds.setAttr('ctrl_move.faceCtrlVisibility',1,keyable=0,channelBox=1)

# Root Controller
  if self.exCheck([self.rootJo]):
   cs = 1.0
   if cmds.objExists('ctrlParameter.torsoCtrlScale') : cs = cmds.getAttr('ctrlParameter.torsoCtrlScale')
   self.ctrlArc(ch*1.4*cs,ch*0.25*cs,-90,340,ch*0.1*cs,ctrlDir,'ctrl_torso',3,[1,1,1,1,1,1,0,0,0,0],[0.3,0.4,0.4])
   cmds.parent('ctrlTrans_torso','ctrl_asset')
   cmds.matchTransform('ctrlTrans_torso',self.rootJo,position=1)
   cmds.matchTransform('ctrl_torso',self.rootJo,rotation=1)
   cmds.parentConstraint('ctrl_torso',self.rootJo)
   self.ctrlAttrPara('ctrlTrans_torso',[3,3,3,3,3,3,3,3,3,1])
   cmds.createNode('transform',name='ctrlConsY_torse',parent='ctrlCons_torso',skipSelect=1)
   cmds.setAttr('ctrlConsY_torse.rotateOrder',2)
   cmds.pointConstraint('ctrl_torso','ctrlConsY_torse')
   cmds.orientConstraint('ctrl_torso','ctrlConsY_torse',skip=['x','z'])
   cmds.connectAttr('ctrl_move.bodyCtrlVisibility','ctrlTrans_torso.v')

# Pelvis Controller
  if self.exCheck([self.hipJo[0]]):
   ga = cmds.getAttr(self.hipJo[0]+'.translate')[0]
   ctrlSize = [1.4,0.7,1.1]
   if ctrlDir == 2 : temp = ctrlSize[1] ; ctrlSize[1] = ctrlSize[2] ; ctrlSize[2] = temp
   #self.ctrlSquare('ctrl_pelvis',ch*ctrlSize[0],ch*ctrlSize[1],ch*ctrlSize[2],0,[0,0,0,1,1,1,0,0,0,0],[0.01,0.05,0.01])
   self.ctrlPrism('ctrl_pelvis',ch*ctrlSize[0],ch*ctrlSize[1],ch*ctrlSize[2],'-y',0,[0,0,0,1,1,1,0,0,0,0],self.ctrlPos['pelvis'][6])
   #self.ctrlOffset('ctrl_pelvis',[0,ga[1],ga[2]])
   cmds.createNode('transform',name='pin_pelvis',parent='ctrl_pelvis',skipSelect=1)
   cmds.setAttr('pin_pelvis.ty', cmds.getAttr(self.pelvisJo+'.ty'))
   cmds.parent('ctrl_pelvis','ctrlConsY_torse',relative=1)
   cmds.parentConstraint('pin_pelvis',self.pelvisJo)
   cmds.createNode('transform',name='cons_limbsFollowPelvis',parent='ctrlTrans_torso')
   cmds.setAttr("cons_limbsFollowPelvis.rotateOrder",3)
   cmds.orientConstraint('pin_pelvis','cons_limbsFollowPelvis',skip=['x','z'])   
 
# downBelong Controller
  if self.exCheck(self.downBelong):
   lst = self.downBelong[2] ; rst = self.L2R(self.downBelong[2])
   cmds.createNode('transform',name='cons_downBelong',parent='ctrl_pelvis')
   cmds.parentConstraint(self.pelvisJo,'cons_downBelong')
   ga = cmds.getAttr(self.downBelong[1]+'.ty')
   self.ctrlSquare('ctrl_penis',ga/2,ga,ga/2,2,[1,1,1,1,1,1,1,1,1,0],self.colour(0.333,2))
   self.ctrlOffset('ctrl_penis',[0,ga/2,0])
   cmds.parent('ctrlTrans_penis','cons_downBelong')
   cmds.matchTransform('ctrlTrans_penis',self.downBelong[0])
   cmds.parentConstraint('ctrl_penis',self.downBelong[0])
   ga = cmds.getAttr(self.downBelong[3]+'.ty')
   self.ctrlSquare('ctrl_scrotum',ga*2,ga*1.2,ga*1.2,2,[1,1,1,1,1,1,1,1,1,0],self.colour(0.333,2))
   self.ctrlOffset('ctrl_scrotum',[0,ga*0.6,0])
   cmds.parent('ctrlTrans_scrotum','cons_downBelong')
   cmds.delete(cmds.pointConstraint(lst,rst,'ctrlTrans_scrotum'))
   cmds.matchTransform('ctrlTrans_scrotum',self.downBelong[2],rotation=1)
   cmds.setAttr('ctrlTrans_scrotum.rz',0)
   cmds.createNode('transform',name='pin_scrotumL',parent='ctrl_scrotum')
   cmds.createNode('transform',name='pin_scrotumR',parent='ctrl_scrotum')
   cmds.matchTransform('pin_scrotumL',lst)
   cmds.matchTransform('pin_scrotumR',rst)
   cmds.parentConstraint('pin_scrotumL',lst)
   cmds.parentConstraint('pin_scrotumR',rst)
 
# Spine Controller
  if self.exCheck([self.spineJo[0],self.chestJo]):
   joNum = 10
   for x in self.spineJo :
    if cmds.objExists(x) == 0 :
     joNum = self.spineJo.index(x)
     break

   if joNum == 3 :
    ga = cmds.getAttr(self.spineJo[1]+'.ty')
    self.ctrlSquare('ctrl_waist',ch*1.5,ch*.2,ch*1.0,1,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))
    self.ctrlOffset('ctrl_waist',[0,ga,0])
    cmds.parent('ctrlTrans_waist','ctrl_torso',relative=1)
    cmds.matchTransform('ctrlTrans_waist',self.spineJo[0],position=1)
    #cmds.orientConstraint('ctrlTrans_waist','ctrl_waist',self.spineJo[0])
    #cmds.orientConstraint('ctrl_waist',self.spineJo[1])
    self.ctrlAttrPara('ctrlTrans_waist',[3,3,3,3,3,3,3,3,3,1])

    ga = cmds.getAttr(self.chestJo+'.ty') ; cs = 1
    if cmds.objExists('ctrlParameter.chestCtrlScale') : cs = cmds.getAttr('ctrlParameter.chestCtrlScale')
    #self.ctrlSquare('ctrl_chest',ch*1.75*cs,ch*.2*cs,ch*1.5*cs,1,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))
    self.ctrlHexagon('ctrl_chest',ch*1.75*cs,ch*.3*cs,ch*1.5*cs,'y',1,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))

    self.ctrlOffset('ctrl_chest',[0,ga,0])
    cmds.parent('ctrlTrans_chest','ctrl_waist',relative=1)
    x = cmds.xform(self.spineJo[2],q=1,ws=1,t=1)
    cmds.move(x[0],x[1],x[2],'ctrlTrans_chest',ws=1,a=1)
    #cmds.orientConstraint('ctrlTrans_chest','ctrl_chest',self.spineJo[2])
    #cmds.orientConstraint('ctrl_chest',self.chestJo)
	
    cmds.createNode('transform',name='oCons_chestTrans',parent='ctrlTrans_chest',skipSelect=1)
    cmds.createNode('transform',name='v_chestTrans',parent='oCons_chestTrans',skipSelect=1)
    cmds.orientConstraint('ctrlTrans_waist','oCons_chestTrans')
    cmds.pointConstraint('ctrl_chest','v_chestTrans')
	
    cmds.createNode('transform',name='rot_spine0',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('transform',name='rot_spine1',parent='rot_spine0',skipSelect=1)
    cmds.createNode('transform',name='rot_spine2',parent='rot_spine1',skipSelect=1)
    cmds.createNode('transform',name='rot_chest',parent='rot_spine2',skipSelect=1)
    cmds.orientConstraint('ctrlTrans_waist','ctrl_waist','rot_spine0')
    cmds.matchTransform('rot_spine1',self.spineJo[1])
    cmds.matchTransform('rot_spine2',self.spineJo[2])
    cmds.matchTransform('rot_chest',self.chestJo)
    cmds.orientConstraint('ctrl_waist','rot_spine1')
    cmds.orientConstraint('ctrl_waist','ctrl_chest','rot_spine2')
    cmds.createNode('transform',name='v_spine1',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('transform',name='v_spine2',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('transform',name='v_chest',parent='ctrlTrans_waist',skipSelect=1)
    cmds.pointConstraint('rot_spine1','v_spine1')
    cmds.pointConstraint('rot_spine2','v_spine2')
    cmds.pointConstraint('rot_chest','v_chest')
    cmds.createNode('transform',name='pin_spine1',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('transform',name='pin_spine2',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('transform',name='pin_chest',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('plusMinusAverage',name='plus_spine1',skipSelect=1)
    cmds.createNode('plusMinusAverage',name='plus_spine2',skipSelect=1)
    cmds.createNode('plusMinusAverage',name='plus_chest',skipSelect=1)
    cmds.connectAttr('v_spine1.translate','plus_spine1.input3D[0]')
    cmds.connectAttr('v_spine2.translate','plus_spine2.input3D[0]')
    cmds.connectAttr('v_chest.translate','plus_chest.input3D[0]')
    cmds.connectAttr('plus_spine1.output3D','pin_spine1.translate')
    cmds.connectAttr('plus_spine2.output3D','pin_spine2.translate')
    cmds.connectAttr('plus_chest.output3D','pin_chest.translate')
    cmds.createNode('multiplyDivide',name='mult_spine1Pin',skipSelect=1)
    cmds.connectAttr('ctrl_waist.translate','mult_spine1Pin.input1')
    cmds.setAttr('mult_spine1Pin.input2',0.5,0.5,0.5,type='double3')
    cmds.connectAttr('mult_spine1Pin.output','plus_spine1.input3D[1]')
    cmds.createNode('multiplyDivide',name='mult_spine2PinA',skipSelect=1)
    cmds.connectAttr('ctrl_waist.translate','mult_spine2PinA.input1')
    cmds.setAttr('mult_spine2PinA.input2',0.79,0.79,0.79,type='double3')
    cmds.connectAttr('mult_spine2PinA.output','plus_spine2.input3D[1]')
    cmds.createNode('multiplyDivide',name='mult_spine2PinB',skipSelect=1)
    cmds.connectAttr('v_chestTrans.translate','mult_spine2PinB.input1')
    cmds.setAttr('mult_spine2PinB.input2',0.5,0.5,0.5,type='double3')
    cmds.connectAttr('mult_spine2PinB.output','plus_spine2.input3D[2]')
    cmds.connectAttr('ctrl_waist.translate','plus_chest.input3D[1]')
    cmds.connectAttr('v_chestTrans.translate','plus_chest.input3D[2]')
    cmds.aimConstraint('ctrlTrans_waist','pin_spine1',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
    cmds.aimConstraint('pin_spine1','pin_spine2',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
    cmds.aimConstraint('pin_spine2','pin_chest',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
    cmds.createNode('transform',name='len_spine1',parent='pin_spine1',skipSelect=1)
    cmds.createNode('transform',name='len_spine2',parent='pin_spine2',skipSelect=1)
    cmds.createNode('transform',name='len_chest',parent='pin_chest',skipSelect=1)
    cmds.pointConstraint('ctrlTrans_waist','len_spine1')
    cmds.pointConstraint('pin_spine1','len_spine2')
    cmds.pointConstraint('pin_spine2','len_chest')
	
    cmds.createNode('joint',name='jo_spine0Rot',parent='ctrlTrans_waist',skipSelect=1)
    cmds.createNode('joint',name='jo_spine0Aim',parent='jo_spine0Rot',skipSelect=1)
    cmds.createNode('joint',name='jo_spine1Rot',parent='jo_spine0Aim',skipSelect=1)
    cmds.createNode('joint',name='jo_spine1Aim',parent='jo_spine1Rot',skipSelect=1)
    cmds.createNode('joint',name='jo_spine2Rot',parent='jo_spine1Aim',skipSelect=1)
    cmds.createNode('joint',name='jo_spine2Aim',parent='jo_spine2Rot',skipSelect=1)
    cmds.createNode('joint',name='jo_chestRot',parent='jo_spine2Aim',skipSelect=1)
    cmds.connectAttr('jo_spine0Aim.scale','jo_spine1Rot.inverseScale')
    cmds.connectAttr('jo_spine1Aim.scale','jo_spine2Rot.inverseScale')
    cmds.connectAttr('jo_spine2Aim.scale','jo_chestRot.inverseScale')
    cmds.setAttr('jo_spine0Rot.v',0)
    cmds.orientConstraint('ctrlTrans_waist','ctrl_waist','jo_spine0Rot')
    cmds.aimConstraint('pin_spine1','jo_spine0Aim',aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
    cmds.matchTransform('jo_spine1Rot',self.spineJo[1])
    cmds.orientConstraint('ctrl_waist','jo_spine1Rot')
    cmds.aimConstraint('pin_spine2','jo_spine1Aim',aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
    cmds.matchTransform('jo_spine2Rot',self.spineJo[2])
    cmds.orientConstraint('ctrl_waist','ctrl_chest','jo_spine2Rot')
    cmds.aimConstraint('pin_chest','jo_spine2Aim',aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
    cmds.matchTransform('jo_chestRot',self.chestJo)
    cmds.createNode('multiplyDivide',name='mult_spineLen',skipSelect=1)
    cmds.setAttr('mult_spineLen.operation',2)
    cmds.connectAttr('len_spine1.translateX','mult_spineLen.input1X')
    cmds.connectAttr('len_spine2.translateX','mult_spineLen.input1Y')
    cmds.connectAttr('len_chest.translateX','mult_spineLen.input1Z')
    cmds.setAttr('mult_spineLen.input2X',cmds.getAttr('len_spine1.translateX'))
    cmds.setAttr('mult_spineLen.input2Y',cmds.getAttr('len_spine2.translateX'))
    cmds.setAttr('mult_spineLen.input2Z',cmds.getAttr('len_chest.translateX'))
    cmds.addAttr('ctrl_chest',longName='stretchable',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
    cmds.createNode('blendColors',name='bColor_spineScaleY',skipSelect=1)
    cmds.connectAttr('ctrl_chest.stretchable','bColor_spineScaleY.blender')
    cmds.connectAttr('mult_spineLen.outputX','bColor_spineScaleY.color1R')
    cmds.connectAttr('mult_spineLen.outputY','bColor_spineScaleY.color1G')
    cmds.connectAttr('mult_spineLen.outputZ','bColor_spineScaleY.color1B')
    cmds.setAttr('bColor_spineScaleY.color2',1,1,1,type='double3')
    cmds.connectAttr('bColor_spineScaleY.outputR','jo_spine0Aim.scaleY')
    cmds.connectAttr('bColor_spineScaleY.outputG','jo_spine1Aim.scaleY')
    cmds.connectAttr('bColor_spineScaleY.outputB','jo_spine2Aim.scaleY')
	
    cmds.createNode('transform',name='pin_spine0Jo',parent='jo_spine0Aim')
    cmds.matchTransform('pin_spine0Jo',self.spineJo[0])
    cmds.orientConstraint('pin_spine0Jo',self.spineJo[0])
    cmds.createNode('transform',name='pin_spine1Jo',parent='jo_spine1Aim')
    cmds.matchTransform('pin_spine1Jo',self.spineJo[1])
    cmds.orientConstraint('pin_spine1Jo',self.spineJo[1])
    cmds.createNode('transform',name='pin_spine2Jo',parent='jo_spine2Aim')
    cmds.matchTransform('pin_spine2Jo',self.spineJo[2])
    cmds.orientConstraint('pin_spine2Jo',self.spineJo[2])
    cmds.orientConstraint('ctrl_chest',self.chestJo)
    cmds.createNode('multiplyDivide',name='mult_spine1Trans',skipSelect=1)
    ga = cmds.getAttr(self.spineJo[1]+'.translate')[0]
    cmds.setAttr('mult_spine1Trans.input1',ga[0],ga[1],ga[2])
    cmds.connectAttr('jo_spine0Aim.scaleY','mult_spine1Trans.input2X')
    cmds.connectAttr('jo_spine0Aim.scaleY','mult_spine1Trans.input2Y')
    cmds.connectAttr('jo_spine0Aim.scaleY','mult_spine1Trans.input2Z')
    cmds.connectAttr('mult_spine1Trans.output',self.spineJo[1]+'.translate')
    cmds.createNode('multiplyDivide',name='mult_spine2Trans',skipSelect=1)
    ga = cmds.getAttr(self.spineJo[2]+'.translate')[0]
    cmds.setAttr('mult_spine2Trans.input1',ga[0],ga[1],ga[2])
    cmds.connectAttr('jo_spine1Aim.scaleY','mult_spine2Trans.input2X')
    cmds.connectAttr('jo_spine1Aim.scaleY','mult_spine2Trans.input2Y')
    cmds.connectAttr('jo_spine1Aim.scaleY','mult_spine2Trans.input2Z')
    cmds.connectAttr('mult_spine2Trans.output',self.spineJo[2]+'.translate')
    cmds.createNode('multiplyDivide',name='mult_chestTrans',skipSelect=1)
    ga = cmds.getAttr(self.chestJo+'.translate')[0]
    cmds.setAttr('mult_chestTrans.input1',ga[0],ga[1],ga[2])
    cmds.connectAttr('jo_spine2Aim.scaleY','mult_chestTrans.input2X')
    cmds.connectAttr('jo_spine2Aim.scaleY','mult_chestTrans.input2Y')
    cmds.connectAttr('jo_spine2Aim.scaleY','mult_chestTrans.input2Z')
    cmds.connectAttr('mult_chestTrans.output',self.chestJo+'.translate')

   if joNum in [4,5,6,7,8,9,10] :
    self.spineCtrl(ch,['pelvis','abdomen','waist','chest'],ctrlDir,'ctrl_torso',joNum,self.spineJo,self.chestJo)

   if joNum >= 11 :
    ctrlSize = [2.25,0.2,2]
    if ctrlDir == 2 : ctrlSize = [2.25,2,0.2]
    self.ctrlSquare('ctrl_chest',ch*ctrlSize[0],ch*ctrlSize[1],ch*ctrlSize[2],1,[1,1,1,1,1,1,0,0,0,0],[0.01,0.05,0.01])
    cmds.matchTransform('ctrlTrans_chest',self.chestJo)
    cmds.parent('ctrlTrans_chest','ctrl_torso')
 
   cmds.createNode('transform',name='cons_limbsFollowChest',parent='ctrlTrans_torso')
   cmds.setAttr("cons_limbsFollowChest.rotateOrder",3)
   cmds.orientConstraint('ctrl_chest','cons_limbsFollowChest',skip=['x','z'])
 
# extra body 's Controller
  if self.exCheck([self.rearPelvisJo,self.bodyJo[0]]):
   exJoNum = 10
   for x in self.bodyJo :
    if cmds.objExists(x) == 0 :
     exJoNum = self.bodyJo.index(x)
     break
   self.spineCtrl(ch,['pelvis','ribcage','belly','rearPelvis'],2,'ctrlConsY_torse',exJoNum,self.bodyJo,self.rearPelvisJo) # ctrlDir=2
   cmds.createNode('transform',name='grp_rearPelvisCons',parent='ctrl_asset')
   cmds.addAttr('ctrl_rearPelvis',longName='follow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
   cmds.createNode('transform',name='followPin_rearPelvis',parent='ctrlTrans_torso',skipSelect=1)
   cmds.matchTransform('followPin_rearPelvis','ctrl_rearPelvis')
   cmds.parentConstraint('followPin_rearPelvis','ctrlTrans_rearPelvis','ctrlCons_rearPelvis',name='pCons_rearPelvis')
   cmds.connectAttr('ctrl_rearPelvis.follow','pCons_rearPelvis.ctrlTrans_rearPelvisW1')
   cmds.createNode('reverse',name='rvs_rearPelvis',skipSelect=1)
   cmds.connectAttr('ctrl_rearPelvis.follow','rvs_rearPelvis.inputX')
   cmds.connectAttr('rvs_rearPelvis.outputX','pCons_rearPelvis.followPin_rearPelvisW0')
   cmds.parentConstraint(self.rearPelvisJo,'grp_rearPelvisCons')

# Head and Neck Controller
  joNum = 10
  for x in self.neckJo :
   if cmds.objExists(x) == 0 :
    joNum = self.neckJo.index(x)
    break
  cmds.createNode('transform',name='grp_chestCons',parent='ctrl_asset')
  cmds.connectAttr('ctrl_move.bodyCtrlVisibility','grp_chestCons.v')
  cmds.parentConstraint(self.chestJo,'grp_chestCons')

  if joNum == 3 :
   cmds.createNode('transform',name='ctrlTrans_neck',parent='ctrl_chest')
   cmds.xform('ctrlTrans_neck',ws=1,t=cmds.xform(self.neckJo[0],q=1,ws=1,t=1))
   self.ctrlArc(ch*0.5,ch*0.1,90,350,ch*0.1,1,'ctrl_head',2,[1,1,1,1,1,1,1,1,1,0],self.colour(0.333,0))
   self.ctrlOffset('ctrl_head',[0,cmds.getAttr(self.topJo+'.ty')*1.25,cmds.getAttr(self.topJo+'.tz')*1.25])
   aa = ['FKIK','FK_rotateFixed','IK_fixed','IK_fixedFollowTorso','autoStretch'] ; aad = [1,0,0,0,0]
   for i in range(len(aa)) : cmds.addAttr('ctrl_head',longName=aa[i],attributeType='double',minValue=0,maxValue=1.0,defaultValue=aad[i],keyable=1)
   cmds.createNode('reverse',name='rvs_headCtrl')
   cmds.connectAttr('ctrl_head.FKIK','rvs_headCtrl.inputX')
   cmds.createNode('transform',name='follow_Head',parent='ctrlTrans_head')
   x = cmds.xform(self.headJo,q=1,ws=1,t=1)
   cmds.move(0,x[1],x[2],'ctrlTrans_head',ws=1,a=1)
   cmds.createNode('blendColors',name='bColor_headTrans')
   cmds.createNode('blendColors',name='bColor_headRot')
   cmds.connectAttr('ctrl_head.FKIK','bColor_headTrans.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_headRot.blender')
   cmds.connectAttr('bColor_headTrans.output','ctrlCons_head.translate')
   cmds.connectAttr('bColor_headRot.output','ctrlCons_head.rotate')
   cmds.createNode('transform',name='follow0_headOnTorso',parent='ctrl_torso')
   cmds.createNode('transform',name='follow0_headOnMove',parent='ctrlTrans_torso')
   cmds.matchTransform('follow0_headOnTorso','follow_Head')
   cmds.matchTransform('follow0_headOnMove','follow_Head')
   cmds.parentConstraint('follow0_headOnTorso','follow0_headOnMove','follow_Head',name='pCons_headFollow')
   cmds.connectAttr('ctrl_head.IK_fixedFollowTorso','pCons_headFollow.follow0_headOnTorsoW0')
   cmds.connectAttr('ctrl_head.IK_fixedFollowTorso','rvs_headCtrl.inputZ')
   cmds.connectAttr('rvs_headCtrl.outputZ','pCons_headFollow.follow0_headOnMoveW1')
   cmds.setAttr('pCons_headFollow.interpType',2)
   cmds.createNode('multiplyDivide',name='mult_headTrans')
   cmds.createNode('multiplyDivide',name='mult_headRot')
   cmds.connectAttr('follow_Head.translate','mult_headTrans.input1')
   cmds.connectAttr('follow_Head.rotate','mult_headRot.input1')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headTrans.input2X')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headTrans.input2Y')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headTrans.input2Z')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headRot.input2X')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headRot.input2Y')
   cmds.connectAttr('ctrl_head.IK_fixed','mult_headRot.input2Z')
   cmds.connectAttr('mult_headTrans.output','bColor_headTrans.color1')
   cmds.connectAttr('mult_headRot.output','bColor_headRot.color1')
   
   cmds.createNode('transform',name='v_head',parent='ctrlTrans_head') # make neck1 neck2 and move with headCtrl
   cmds.parentConstraint('ctrl_head','v_head')
   cc = ['',[0.15,0.35,0.15],[0.2,0.4,0.2]] # ctrl color
   for i in range(1,3) :
    self.ctrlCrystal('ctrl_neck'+str(i),ch*0.4,ch*0.4,2,[1,1,1,1,1,1,0,0,0,0],cc[i])
    cmds.xform('ctrlTrans_neck'+str(i),t=cmds.xform(self.neckJo[i],q=1,ws=1,t=1))
    cmds.createNode('multiplyDivide',name='mult_neck'+str(i)+'Trans')
    cmds.createNode('multiplyDivide',name='mult_neck'+str(i)+'Rot')
    cmds.connectAttr('v_head.translate','mult_neck'+str(i)+'Trans.input1')
    cmds.connectAttr('v_head.rotate','mult_neck'+str(i)+'Rot.input1')
    cmds.connectAttr('mult_neck'+str(i)+'Trans.output','ctrlCons_neck'+str(i)+'.translate')
    cmds.connectAttr('mult_neck'+str(i)+'Rot.output','ctrlCons_neck'+str(i)+'.rotate')

   cmds.createNode('joint',name='jo_neck0_oCons',parent='ctrlTrans_neck')
   cmds.createNode('joint',name='jo_neck0_aCons',parent='jo_neck0_oCons')
   cmds.connectAttr('jo_neck0_oCons.scale','jo_neck0_aCons.inverseScale')
   cmds.createNode('joint',name='jo_neck1_oCons',parent='jo_neck0_aCons')
   cmds.connectAttr('jo_neck0_aCons.scale','jo_neck1_oCons.inverseScale')
   cmds.createNode('joint',name='jo_neck1_aCons',parent='jo_neck1_oCons')
   cmds.connectAttr('jo_neck1_oCons.scale','jo_neck1_aCons.inverseScale')
   cmds.createNode('joint',name='jo_neck2_oCons',parent='jo_neck1_aCons')
   cmds.connectAttr('jo_neck1_aCons.scale','jo_neck2_oCons.inverseScale')
   cmds.createNode('joint',name='jo_neck2_aCons',parent='jo_neck2_oCons')
   cmds.connectAttr('jo_neck2_oCons.scale','jo_neck2_aCons.inverseScale')
   cmds.createNode('joint',name='jo_neck3_oCons',parent='jo_neck2_aCons')
   cmds.connectAttr('jo_neck2_aCons.scale','jo_neck3_oCons.inverseScale')
   cmds.setAttr('jo_neck0_oCons.v',0)

   cmds.aimConstraint('ctrl_neck1','jo_neck0_aCons',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.xform('jo_neck1_oCons',ws=1,t=cmds.xform('ctrl_neck1',q=1,ws=1,t=1))
   cmds.orientConstraint('ctrl_neck1','jo_neck1_oCons')
   cmds.aimConstraint('ctrl_neck2','jo_neck1_aCons',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.xform('jo_neck2_oCons',ws=1,t=cmds.xform('ctrl_neck2',q=1,ws=1,t=1))
   cmds.orientConstraint('ctrl_neck2','jo_neck2_oCons')
   cmds.aimConstraint('ctrl_head','jo_neck2_aCons',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.xform('jo_neck3_oCons',ws=1,t=cmds.xform('ctrl_head',q=1,ws=1,t=1))
   neckTotalLength = cmds.getAttr('jo_neck1_oCons.ty') + cmds.getAttr('jo_neck2_oCons.ty') + cmds.getAttr('jo_neck3_oCons.ty')
   neck1Rate = cmds.getAttr('jo_neck1_oCons.ty') / neckTotalLength
   neck2Rate = (cmds.getAttr('jo_neck1_oCons.ty')+cmds.getAttr('jo_neck2_oCons.ty')) / neckTotalLength
   cmds.setAttr('mult_neck1Trans.input2',neck1Rate,neck1Rate,neck1Rate)
   cmds.setAttr('mult_neck2Trans.input2',neck2Rate,neck2Rate,neck2Rate)
   cmds.setAttr('mult_neck1Rot.input2',neck1Rate,neck1Rate,neck1Rate)
   cmds.setAttr('mult_neck2Rot.input2',neck2Rate,neck2Rate,neck2Rate)

   cmds.createNode('transform',name='aCons_neck0_len',parent='ctrlTrans_neck')
   cmds.createNode('transform',name='pin_neck0_len',parent='aCons_neck0_len')
   cmds.createNode('transform',name='aCons_neck1_len',parent='pin_neck0_len')
   cmds.createNode('transform',name='pin_neck1_len',parent='aCons_neck1_len')
   cmds.createNode('transform',name='aCons_neck2_len',parent='pin_neck1_len')
   cmds.createNode('transform',name='pin_neck2_len',parent='aCons_neck2_len')
   cmds.aimConstraint('ctrl_neck1','aCons_neck0_len',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.aimConstraint('ctrl_neck2','aCons_neck1_len',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.aimConstraint('ctrl_head','aCons_neck2_len',aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
   cmds.pointConstraint('ctrl_neck1','pin_neck0_len')
   cmds.pointConstraint('ctrl_neck2','pin_neck1_len')
   cmds.pointConstraint('ctrl_head','pin_neck2_len')

   cmds.createNode('multiplyDivide',name='divide_neck0')
   cmds.createNode('multiplyDivide',name='divide_neck1')
   cmds.createNode('multiplyDivide',name='divide_neck2')
   cmds.setAttr('divide_neck0.operation',2)
   cmds.setAttr('divide_neck1.operation',2)
   cmds.setAttr('divide_neck2.operation',2)
   cmds.connectAttr('pin_neck0_len.translateY','divide_neck0.input1X')
   cmds.connectAttr('pin_neck1_len.translateY','divide_neck1.input1X')
   cmds.connectAttr('pin_neck2_len.translateY','divide_neck2.input1X')
   cmds.setAttr('divide_neck0.input2X',cmds.getAttr('pin_neck0_len.ty'))
   cmds.setAttr('divide_neck1.input2X',cmds.getAttr('pin_neck1_len.ty'))
   cmds.setAttr('divide_neck2.input2X',cmds.getAttr('pin_neck2_len.ty'))
   cmds.createNode('blendColors',name='bColor_neck')
   cmds.connectAttr('ctrl_head.autoStretch','bColor_neck.blender')
#   cmds.connectAttr('divide_neck0.outputX','jo_neck0_aCons.sy')
#   cmds.connectAttr('divide_neck1.outputX','jo_neck1_aCons.sy')
#   cmds.connectAttr('divide_neck2.outputX','jo_neck2_aCons.sy')
   cmds.connectAttr('divide_neck0.outputX','bColor_neck.color1R')
   cmds.connectAttr('divide_neck1.outputX','bColor_neck.color1G')
   cmds.connectAttr('divide_neck2.outputX','bColor_neck.color1B')
   cmds.setAttr('bColor_neck.color2',1,1,1,type="double3")
   cmds.connectAttr('bColor_neck.outputR','jo_neck0_aCons.sy')
   cmds.connectAttr('bColor_neck.outputG','jo_neck1_aCons.sy')
   cmds.connectAttr('bColor_neck.outputB','jo_neck2_aCons.sy')

   cmds.createNode('transform',name='pin_neck0',parent=self.neckJo[0])
   cmds.createNode('transform',name='pin_neck1',parent=self.neckJo[1])
   cmds.createNode('transform',name='pin_neck2',parent=self.neckJo[2])
   cmds.parent('pin_neck0','jo_neck0_aCons')
   cmds.parent('pin_neck1','jo_neck1_aCons')
   cmds.parent('pin_neck2','jo_neck2_aCons')
   cmds.createNode('multMatrix',name='multX_neck0')
   cmds.createNode('multMatrix',name='multX_neck1')
   cmds.createNode('multMatrix',name='multX_neck2')
   cmds.createNode('multMatrix',name='multX_head')
   cmds.createNode('transform',name='scaleMatrix_neck0',parent='ctrlTrans_neck')
   cmds.createNode('transform',name='scaleMatrix_neck1',parent='ctrlTrans_neck')
   cmds.createNode('transform',name='scaleMatrix_neck2',parent='ctrlTrans_neck')
   cmds.connectAttr(self.neckJo[0]+'.scale','scaleMatrix_neck0.scale')
   cmds.connectAttr(self.neckJo[1]+'.scale','scaleMatrix_neck1.scale')
   cmds.connectAttr(self.neckJo[2]+'.scale','scaleMatrix_neck2.scale')
   cmds.connectAttr('pin_neck0.worldMatrix[0]','multX_neck0.matrixIn[0]')
   cmds.connectAttr('pin_neck1.worldMatrix[0]','multX_neck1.matrixIn[0]')
   cmds.connectAttr('pin_neck2.worldMatrix[0]','multX_neck2.matrixIn[0]')
   cmds.connectAttr(self.chestJo+'.worldInverseMatrix[0]','multX_neck0.matrixIn[1]')
   cmds.connectAttr(self.neckJo[0]+'.worldInverseMatrix[0]','multX_neck1.matrixIn[1]')
   cmds.connectAttr(self.neckJo[1]+'.worldInverseMatrix[0]','multX_neck2.matrixIn[1]')
   cmds.connectAttr(self.neckJo[2]+'.worldInverseMatrix[0]','multX_head.matrixIn[1]')
   cmds.connectAttr('ctrl_head.worldMatrix[0]','multX_head.matrixIn[0]')
   cmds.connectAttr('scaleMatrix_neck0.matrix','multX_neck1.matrixIn[2]')
   cmds.connectAttr('scaleMatrix_neck1.matrix','multX_neck2.matrixIn[2]')
   cmds.connectAttr('scaleMatrix_neck2.matrix','multX_head.matrixIn[2]')
   cmds.createNode('decomposeMatrix',name='dm_neck0')
   cmds.createNode('decomposeMatrix',name='dm_neck1')
   cmds.createNode('decomposeMatrix',name='dm_neck2')
   cmds.createNode('decomposeMatrix',name='dm_head')
   cmds.connectAttr('multX_neck0.matrixSum','dm_neck0.inputMatrix')
   cmds.connectAttr('multX_neck1.matrixSum','dm_neck1.inputMatrix')
   cmds.connectAttr('multX_neck2.matrixSum','dm_neck2.inputMatrix')
   cmds.connectAttr('multX_head.matrixSum','dm_head.inputMatrix')
   
   cmds.createNode('blendColors',name='bColor_neck1Ro')
   cmds.createNode('blendColors',name='bColor_neck2Ro')
   cmds.createNode('blendColors',name='bColor_neck3Ro')
   cmds.createNode('blendColors',name='bColor_neck1S')
   cmds.createNode('blendColors',name='bColor_neck2S')
   cmds.createNode('blendColors',name='bColor_neck3S')
   cmds.createNode('blendColors',name='bColor_neck1Sr')
   cmds.createNode('blendColors',name='bColor_neck2Sr')
   cmds.createNode('blendColors',name='bColor_neck3Sr')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck1Ro.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck2Ro.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck3Ro.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck1S.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck2S.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck3S.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck1Sr.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck2Sr.blender')
   cmds.connectAttr('ctrl_head.FKIK','bColor_neck3Sr.blender')
   cmds.connectAttr('dm_neck0.outputRotate','bColor_neck1Ro.color1')
   cmds.connectAttr('dm_neck1.outputRotate','bColor_neck2Ro.color1')
   cmds.connectAttr('dm_neck2.outputRotate','bColor_neck3Ro.color1')
   cmds.connectAttr('dm_neck0.outputScale','bColor_neck1S.color1')
   cmds.connectAttr('dm_neck1.outputScale','bColor_neck2S.color1')
   cmds.connectAttr('dm_neck2.outputScale','bColor_neck3S.color1')
   cmds.connectAttr('dm_neck0.outputShear','bColor_neck1Sr.color1')
   cmds.connectAttr('dm_neck1.outputShear','bColor_neck2Sr.color1')
   cmds.connectAttr('dm_neck2.outputShear','bColor_neck3Sr.color1')
   cmds.connectAttr('bColor_neck1Ro.output',self.neckJo[0]+'.rotate')
   cmds.connectAttr('bColor_neck2Ro.output',self.neckJo[1]+'.rotate')
   cmds.connectAttr('bColor_neck3Ro.output',self.neckJo[2]+'.rotate')
   cmds.connectAttr('bColor_neck1S.output',self.neckJo[0]+'.scale')
   cmds.connectAttr('bColor_neck2S.output',self.neckJo[1]+'.scale')
   cmds.connectAttr('bColor_neck3S.output',self.neckJo[2]+'.scale')
   cmds.connectAttr('bColor_neck1Sr.output',self.neckJo[0]+'.shear')
   cmds.connectAttr('bColor_neck2Sr.output',self.neckJo[1]+'.shear')
   cmds.connectAttr('bColor_neck3Sr.output',self.neckJo[2]+'.shear')
   cmds.connectAttr('dm_head.outputRotate',self.headJo+'.rotate')
   cmds.connectAttr('dm_head.outputScale',self.headJo+'.scale')
   cmds.connectAttr('dm_head.outputShear',self.headJo+'.shear')

   cmds.parent('ctrlTrans_neck1','ctrlTrans_neck')
   cmds.parent('ctrlTrans_neck2','ctrlTrans_neck')
   cmds.parent('ctrlTrans_head','ctrl_chest')
   
   
   self.ctrlCircle('ctrl_neckFk0',ch*0.45,ctrlDir,2,[0,0,0,1,1,1,1,1,1,0],self.colour(0.333,1))
   self.ctrlCircle('ctrl_neckFk1',ch*0.4,ctrlDir,2,[0,0,0,1,1,1,1,1,1,0],self.colour(0.333,1))
   self.ctrlCircle('ctrl_neckFk2',ch*0.35,ctrlDir,2,[0,0,0,1,1,1,1,1,1,0],self.colour(0.333,1))
   cmds.parent('ctrlTrans_neckFk0','ctrlTrans_neck')
   cmds.parent('ctrlTrans_neckFk1','ctrl_neckFk0')
   cmds.parent('ctrlTrans_neckFk2','ctrl_neckFk1')
   cmds.matchTransform('ctrlTrans_neckFk0',self.neckJo[0])
   cmds.matchTransform('ctrlTrans_neckFk1',self.neckJo[1])
   cmds.matchTransform('ctrlTrans_neckFk2',self.neckJo[2])
   cmds.createNode('transform',name='pin_fkHead',parent='ctrl_neckFk2')
   cmds.matchTransform('pin_fkHead',self.headJo)
   cmds.createNode('transform',name='v_fkHead',parent='ctrlTrans_head')
   cmds.parentConstraint('pin_fkHead','v_fkHead')
   cmds.createNode('multiplyDivide',name='mult_headFxTrans')
   cmds.createNode('multiplyDivide',name='mult_headFxRot')
   cmds.connectAttr('v_fkHead.translate','mult_headFxTrans.input1')
   cmds.connectAttr('v_fkHead.rotate','mult_headFxRot.input1')
   cmds.connectAttr('ctrl_head.FK_rotateFixed','rvs_headCtrl.inputY')
   cmds.connectAttr('rvs_headCtrl.outputX','mult_headFxTrans.input2X')
   cmds.connectAttr('rvs_headCtrl.outputX','mult_headFxTrans.input2Y')
   cmds.connectAttr('rvs_headCtrl.outputX','mult_headFxTrans.input2Z')
   cmds.connectAttr('rvs_headCtrl.outputY','mult_headFxRot.input2X')
   cmds.connectAttr('rvs_headCtrl.outputY','mult_headFxRot.input2Y')
   cmds.connectAttr('rvs_headCtrl.outputY','mult_headFxRot.input2Z')
   cmds.connectAttr('mult_headFxTrans.output','bColor_headTrans.color2')
   cmds.connectAttr('mult_headFxRot.output','bColor_headRot.color2')
   # FKIK switch process
   cmds.createNode('multiplyDivide',name='mult_headFkRvs') 
   cmds.createNode('multDoubleLinear',name='mdl_headFkRvs')
   cmds.connectAttr('ctrl_head.translate','mult_headFkRvs.input1')
   cmds.connectAttr('rvs_headCtrl.outputX','mdl_headFkRvs.input1')
   cmds.setAttr('mdl_headFkRvs.input2',-1)
   cmds.connectAttr('mdl_headFkRvs.output','mult_headFkRvs.input2X')
   cmds.connectAttr('mdl_headFkRvs.output','mult_headFkRvs.input2Y')
   cmds.connectAttr('mdl_headFkRvs.output','mult_headFkRvs.input2Z')
   cmds.connectAttr('mult_headFkRvs.output','ctrl_head.rotatePivotTranslate')
   cmds.connectAttr('ctrl_head.FKIK','ctrlTrans_neck1.v')
   cmds.connectAttr('ctrl_head.FKIK','ctrlTrans_neck2.v')
   cmds.connectAttr('rvs_headCtrl.outputX','ctrlTrans_neckFk0.v')
   
   cmds.connectAttr('ctrl_neckFk0.rotate','bColor_neck1Ro.color2')
   cmds.connectAttr('ctrl_neckFk1.rotate','bColor_neck2Ro.color2')
   cmds.connectAttr('ctrl_neckFk2.rotate','bColor_neck3Ro.color2')
   cmds.connectAttr('ctrl_neckFk0.scale','bColor_neck1S.color2')
   cmds.connectAttr('ctrl_neckFk1.scale','bColor_neck2S.color2')
   cmds.connectAttr('ctrl_neckFk2.scale','bColor_neck3S.color2')
   cmds.connectAttr('ctrl_neckFk0.shear','bColor_neck1Sr.color2')
   cmds.connectAttr('ctrl_neckFk1.shear','bColor_neck2Sr.color2')
   cmds.connectAttr('ctrl_neckFk2.shear','bColor_neck3Sr.color2')

  if joNum == 2 :
   if self.topJo != '' :
    tmp = cmds.createNode('transform',parent=self.neckJo[0])
    cmds.matchTransform(tmp,self.topJo)
    ga = cmds.getAttr(tmp+'.translate')[0]
    print ga
    cmds.delete(tmp)
   else : ga = ( cmds.getAttr(self.neckJo[1]+'.ty') + cmds.getAttr(self.headJo+'.ty') + cmds.getAttr(self.neckJo[0]+'.ty') ) * 1.25
   self.ctrlArc(ch*0.5,ch*0.1,90,350,ch*0.1,1,'ctrl_head',2,[1,1,1,1,1,1,1,1,1,0],self.colour(0.333,0))
   self.ctrlOffset('ctrl_head',[0,ga[1]*1.2,ga[2]*1.2])
   cmds.addAttr('ctrl_head',longName='rotateWeight',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0.5,keyable=1)
   cmds.addAttr('ctrl_head',longName='follow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
   cmds.addAttr('ctrl_head',longName='neckLength',attributeType='double',minValue=0.1,defaultValue=1,keyable=1)
   cmds.addAttr('ctrl_head',longName='stretchable',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.parent('ctrlTrans_head','grp_chestCons')
   x = cmds.xform(self.neckJo[0],q=1,ws=1,t=1)
   cmds.move(0,x[1],x[2],'ctrlTrans_head',ws=1,a=1)
   self.ctrlAttrPara('ctrlTrans_head',[3,3,3,3,3,3,3,3,3,1])

   self.ctrlCircle('ctrl_neck',ch*0.6,1,2,[0,0,0,1,1,1,0,0,0,0],self.colour(0.333,0))
   #ga = cmds.getAttr(self.neckJo[1]+'.translate')
   #self.ctrlOffset('ctrl_neck',[ga[0][0],ga[0][1],ga[0][2]])
   cmds.parent('ctrlTrans_neck','grp_chestCons',relative=1)
   x = cmds.xform(self.neckJo[0],q=1,ws=1,t=1)
   cmds.move(x[0],x[1],x[2],'ctrlTrans_neck',ws=1,a=1)
   self.ctrlAttrPara('ctrlTrans_neck',[3,3,3,3,3,3,3,3,3,1])
   self.ctrlCircle('ctrl_neck2',ch*0.6,1,2,[0,0,0,1,1,1,0,0,0,0],self.colour(0.333,0))
   #ga = cmds.getAttr(self.headJo+'.translate')
   #self.ctrlOffset('ctrl_neck2',[ga[0][0]*0.5,ga[0][1]*0.5,ga[0][2]*0.5])
   cmds.parent('ctrlTrans_neck2','ctrl_neck',relative=1)
   x = cmds.xform(self.neckJo[1],q=1,ws=1,t=1)
   cmds.move(x[0],x[1],x[2],'ctrlTrans_neck2',ws=1,a=1)
   
   cmds.createNode('transform',name='pin_head_head',parent='ctrl_head',skipSelect=1)
   x = cmds.xform(self.headJo,q=1,ws=1,ro=1)
   cmds.rotate(x[0],x[1],x[2],'pin_head_head',ws=1,a=1)

   cmds.orientConstraint('pin_head_head',self.headJo)
   cmds.orientConstraint('ctrl_neck',self.neckJo[0])
   cmds.orientConstraint('ctrl_neck2',self.neckJo[1])
   cmds.createNode('plusMinusAverage',name='plus_neckScale',skipSelect=1)
   cmds.createNode('plusMinusAverage',name='plus_neck2Scale',skipSelect=1)
   cmds.connectAttr('ctrl_neck.scale','plus_neckScale.input3D[0]')
   cmds.connectAttr('ctrl_neck2.scale','plus_neck2Scale.input3D[0]')
   #cmds.connectAttr('plus_neckScale.output3D','jcD00_neck.scale')
   #cmds.connectAttr('plus_neck2Scale.output3D','jcD10_neck1.scale')
   cmds.connectAttr('plus_neckScale.output3D',self.neckJo[0]+'.scale')
   cmds.connectAttr('plus_neck2Scale.output3D',self.neckJo[1]+'.scale')

   cmds.createNode('setRange',name='range_neckCons',skipSelect=1)
   cmds.connectAttr('ctrl_head.rotateWeight','range_neckCons.valueX')
   cmds.connectAttr('ctrl_head.rotateWeight','range_neckCons.valueY')
   cmds.connectAttr('ctrl_head.rotateWeight','range_neckCons.valueZ')
   cmds.setAttr('range_neckCons.maxX',2)
   cmds.setAttr('range_neckCons.maxY',1)
   cmds.setAttr('range_neckCons.maxZ',1)
   cmds.setAttr('range_neckCons.oldMinZ',0.5)
   cmds.setAttr('range_neckCons.oldMaxX',0.5)
   cmds.setAttr('range_neckCons.oldMaxY',0.5)
   cmds.setAttr('range_neckCons.oldMaxZ',1)
   cmds.createNode('reverse',name='rev_neckCons',skipSelect=1)
   cmds.connectAttr('range_neckCons.outValueZ','rev_neckCons.inputX')
   cmds.createNode('multDoubleLinear',name='mdl_neckCons',skipSelect=1)
   cmds.connectAttr('rev_neckCons.outputX','mdl_neckCons.input1')
   cmds.setAttr('mdl_neckCons.input2',2)
   
# new method develop
   cmds.createNode('transform',name='rot_neck',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('transform',name='rot_neck2',parent='rot_neck',skipSelect=1)
   cmds.createNode('transform',name='rot_head',parent='rot_neck2',skipSelect=1)
   cmds.matchTransform('rot_neck2',self.neckJo[1])
   cmds.matchTransform('rot_head',self.headJo)
   cmds.orientConstraint('ctrlTrans_head','ctrl_head','rot_neck',name='oCons_neckRot')
   cmds.orientConstraint('ctrlTrans_head','ctrl_head','rot_neck2',name='oCons_neckRot2')
   cmds.connectAttr('range_neckCons.outValueX','oCons_neckRot.ctrlTrans_headW0')
   cmds.connectAttr('range_neckCons.outValueY','oCons_neckRot2.ctrlTrans_headW0')
   cmds.connectAttr('rev_neckCons.outputX','oCons_neckRot.ctrl_headW1')
   cmds.connectAttr('mdl_neckCons.output','oCons_neckRot2.ctrl_headW1')
   cmds.createNode('transform',name='v_neckRot2',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('transform',name='v_headRot',parent='ctrlTrans_head',skipSelect=1)
   cmds.pointConstraint('rot_neck2','v_neckRot2')
   cmds.pointConstraint('rot_head','v_headRot')

   cmds.createNode('transform',name='pin_neck2',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('transform',name='pin_head',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('plusMinusAverage',name='plus_neck2Pin',skipSelect=1)
   cmds.createNode('plusMinusAverage',name='plus_headPin',skipSelect=1)
   cmds.connectAttr('plus_neck2Pin.output3D','pin_neck2.translate')
   cmds.connectAttr('plus_headPin.output3D','pin_head.translate')

   cmds.connectAttr('v_neckRot2.translate','plus_neck2Pin.input3D[0]')
   cmds.createNode('multiplyDivide',name='mult_neckRot2',skipSelect=1)
   cmds.connectAttr('ctrl_head.translate','mult_neckRot2.input1')
   cmds.setAttr('mult_neckRot2.input2',0.5,0.5,0.5,type='double3')
   cmds.connectAttr('mult_neckRot2.output','plus_neck2Pin.input3D[1]')
   cmds.connectAttr('v_headRot.translate','plus_headPin.input3D[0]')
   cmds.connectAttr('ctrl_head.translate','plus_headPin.input3D[1]')
   
   cmds.createNode('transform',name='len_neck2',parent='pin_neck2',skipSelect=1)
   cmds.createNode('transform',name='len_head',parent='pin_head',skipSelect=1)
   cmds.aimConstraint('ctrlTrans_head','pin_neck2',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
   cmds.pointConstraint('ctrlTrans_head','len_neck2')
   cmds.aimConstraint('pin_neck2','pin_head',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
   cmds.pointConstraint('pin_neck2','len_head')
   cmds.createNode('multiplyDivide',name='dvd_neckLen',skipSelect=1)
   cmds.setAttr('dvd_neckLen.operation',2)
   cmds.connectAttr('len_neck2.translateX','dvd_neckLen.input1X')
   cmds.connectAttr('len_head.translateX','dvd_neckLen.input1Y')
   cmds.setAttr('dvd_neckLen.input2X',cmds.getAttr('len_neck2.translateX'))
   cmds.setAttr('dvd_neckLen.input2Y',cmds.getAttr('len_head.translateX'))
   
   cmds.createNode('blendColors',name='bColor_neckLen',skipSelect=1)
   cmds.connectAttr('ctrl_head.stretchable','bColor_neckLen.blender')
   cmds.connectAttr('dvd_neckLen.outputX','bColor_neckLen.color1R')
   cmds.connectAttr('dvd_neckLen.outputY','bColor_neckLen.color1G')
   cmds.setAttr('bColor_neckLen.color2R',1)
   cmds.setAttr('bColor_neckLen.color2G',1)

   cmds.createNode('joint',name='jo_neckRot',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('joint',name='jo_neckAim',parent='jo_neckRot',skipSelect=1)
   cmds.createNode('joint',name='jo_neck2Rot',parent='jo_neckAim',skipSelect=1)
   cmds.connectAttr('jo_neckAim.scale','jo_neck2Rot.inverseScale')
   cmds.createNode('joint',name='jo_neck2Aim',parent='jo_neck2Rot',skipSelect=1)
   cmds.createNode('joint',name='jo_headPos',parent='jo_neck2Aim',skipSelect=1)
   cmds.setAttr('jo_neckRot.v',0)
   cmds.aimConstraint('pin_neck2','jo_neckAim',aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
   cmds.matchTransform('jo_neck2Rot',self.neckJo[1],position=1)
   cmds.aimConstraint('pin_head','jo_neck2Aim',aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
   cmds.matchTransform('jo_headPos',self.headJo,position=1)
   cmds.createNode('transform',name='pin_neckCtrl',parent='jo_neckAim',skipSelect=1)
   cmds.createNode('transform',name='pin_neck2Ctrl',parent='jo_neck2Aim',skipSelect=1)
   cmds.matchTransform('pin_neckCtrl',self.neckJo[0])
   cmds.matchTransform('pin_neck2Ctrl',self.neckJo[1])
   cmds.connectAttr('bColor_neckLen.outputR','jo_neckAim.scaleY')
   cmds.connectAttr('bColor_neckLen.outputG','jo_neck2Aim.scaleY')
   cmds.orientConstraint('ctrlTrans_head','ctrl_head','jo_neck2Rot')
   
   cmds.parentConstraint('pin_neckCtrl','ctrlCons_neck')
   cmds.orientConstraint('pin_neck2Ctrl','ctrlCons_neck2')
   cmds.createNode('multiplyDivide',name='mult_neck1Trans',skipSelect=1)
   ga = cmds.getAttr(self.neckJo[1]+'.translate')[0]
   cmds.setAttr('mult_neck1Trans.input1',ga[0],ga[1],ga[2],type='double3')
   cmds.createNode('multDoubleLinear',name='mdl_neckScale',skipSelect=1)
   cmds.connectAttr('ctrl_head.neckLength','mdl_neckScale.input1')
   cmds.connectAttr('jo_neckAim.scaleY','mdl_neckScale.input2')
   #cmds.connectAttr('jo_neckAim.scaleY','mult_neck1Trans.input2X')
   #cmds.connectAttr('jo_neckAim.scaleY','mult_neck1Trans.input2Y')
   #cmds.connectAttr('jo_neckAim.scaleY','mult_neck1Trans.input2Z')
   cmds.connectAttr('mdl_neckScale.output','mult_neck1Trans.input2X')
   cmds.connectAttr('mdl_neckScale.output','mult_neck1Trans.input2Y')
   cmds.connectAttr('mdl_neckScale.output','mult_neck1Trans.input2Z')
   cmds.connectAttr('mult_neck1Trans.output','ctrlTrans_neck2.translate')
   cmds.connectAttr('mult_neck1Trans.output',self.neckJo[1]+'.translate')
   cmds.createNode('multiplyDivide',name='mult_headTrans',skipSelect=1)
   ga = cmds.getAttr(self.headJo+'.translate')[0]
   cmds.setAttr('mult_headTrans.input1',ga[0],ga[1],ga[2],type='double3')
   cmds.createNode('multDoubleLinear',name='mdl_headScale',skipSelect=1)
   cmds.connectAttr('ctrl_head.neckLength','mdl_headScale.input1')
   cmds.connectAttr('jo_neck2Aim.scaleY','mdl_headScale.input2')
   #cmds.connectAttr('jo_neck2Aim.scaleY','mult_headTrans.input2X')
   #cmds.connectAttr('jo_neck2Aim.scaleY','mult_headTrans.input2Y')
   #cmds.connectAttr('jo_neck2Aim.scaleY','mult_headTrans.input2Z')
   cmds.connectAttr('mdl_headScale.output','mult_headTrans.input2X')
   cmds.connectAttr('mdl_headScale.output','mult_headTrans.input2Y')
   cmds.connectAttr('mdl_headScale.output','mult_headTrans.input2Z')
   cmds.connectAttr('mult_headTrans.output',self.headJo+'.translate')
   
#  Head Ctrl Rotate Follow
   cmds.createNode('transform',name='ctrlCons_head0',parent='ctrlTrans_head',skipSelect=1)
   cmds.orientConstraint('ctrlTrans_torso','ctrlCons_head0')
   cmds.createNode('multiplyDivide',name='multiply_neckFollow',skipSelect=1)
   cmds.connectAttr('ctrlCons_head0.rotate','multiply_neckFollow.input1')
   cmds.createNode('reverse',name='rev_neckFollow',skipSelect=1)
   cmds.connectAttr('ctrl_head.follow','rev_neckFollow.inputX')
   cmds.connectAttr('rev_neckFollow.outputX','multiply_neckFollow.input2X')
   cmds.connectAttr('rev_neckFollow.outputX','multiply_neckFollow.input2Y')
   cmds.connectAttr('rev_neckFollow.outputX','multiply_neckFollow.input2Z')
   cmds.connectAttr('multiply_neckFollow.output','ctrlCons_head.rotate')
#  Head Ctrl Scale
   cmds.connectAttr('ctrl_head.scale',self.headJo+'.scale')
   cmds.createNode('addDoubleLinear',name='adl_headScaleX',skipSelect=1)
   cmds.createNode('addDoubleLinear',name='adl_headScaleY',skipSelect=1)
   cmds.createNode('addDoubleLinear',name='adl_headScaleZ',skipSelect=1)
   cmds.setAttr('adl_headScaleX.input1',-1)
   cmds.setAttr('adl_headScaleY.input1',-1)
   cmds.setAttr('adl_headScaleZ.input1',-1)
   cmds.connectAttr('ctrl_head.scaleX','adl_headScaleX.input2')
   cmds.connectAttr('ctrl_head.scaleY','adl_headScaleY.input2')
   cmds.connectAttr('ctrl_head.scaleZ','adl_headScaleZ.input2')

   cmds.createNode('multiplyDivide',name='multiply_neck2Scale')
   cmds.connectAttr('adl_headScaleX.output','multiply_neck2Scale.input1X')
   cmds.connectAttr('adl_headScaleY.output','multiply_neck2Scale.input1Y')
   cmds.connectAttr('adl_headScaleZ.output','multiply_neck2Scale.input1Z')
   cmds.setAttr('multiply_neck2Scale.input2',0.666,0.666,0.666,type='double3')
   cmds.connectAttr('multiply_neck2Scale.output','plus_neck2Scale.input3D[2]')

   cmds.createNode('multiplyDivide',name='multiply_neckScale',skipSelect=1)
   cmds.connectAttr('adl_headScaleX.output','multiply_neckScale.input1X')
   cmds.connectAttr('adl_headScaleY.output','multiply_neckScale.input1Y')
   cmds.connectAttr('adl_headScaleZ.output','multiply_neckScale.input1Z')
   cmds.setAttr('multiply_neckScale.input2',0.333,0.333,0.333,type='double3')
   cmds.connectAttr('multiply_neckScale.output','plus_neckScale.input3D[2]')

  if joNum > 3 :
   cmds.createNode('transform',name='ctrlTrans_neck',parent='ctrl_chest')
   cmds.xform('ctrlTrans_neck',ws=1,t=cmds.xform(self.neckJo[0],q=1,ws=1,t=1))
   ga = cmds.getAttr(self.topJo+'.ty') * 1.25
   self.ctrlArc(ch*0.5,ch*0.1,90,350,ch*0.1,1,'ctrl_head',2,[1,1,1,1,1,1,1,1,1,0],[0.25,0.45,0.25])
   self.ctrlOffset('ctrl_head',[0,ga,0])
   cmds.addAttr('ctrl_head',longName='rotateFixed',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.addAttr('ctrl_head',longName='translateFixed',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=0)
   cmds.addAttr('ctrl_head',longName='stretchable',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
   cmds.matchTransform('ctrlTrans_head',self.headJo,position=1)
   cmds.createNode('transform',name='follow_head',parent='ctrlTrans_head',skipSelect=1)
   cmds.createNode('transform',name='follow0_head',parent='ctrlCons_torso',skipSelect=1)
   cmds.matchTransform('follow0_head','follow_head')
   cmds.parentConstraint('follow0_head','follow_head')
   cmds.createNode('multiplyDivide',name='mult_headRotFix')
   cmds.createNode('multiplyDivide',name='mult_headTransFix')
   cmds.connectAttr('follow_head.rotate','mult_headRotFix.input1')
   cmds.connectAttr('follow_head.translate','mult_headTransFix.input1')
   cmds.connectAttr('ctrl_head.rotateFixed','mult_headRotFix.input2X')
   cmds.connectAttr('ctrl_head.rotateFixed','mult_headRotFix.input2Y')
   cmds.connectAttr('ctrl_head.rotateFixed','mult_headRotFix.input2Z')
   cmds.connectAttr('ctrl_head.translateFixed','mult_headTransFix.input2X')
   cmds.connectAttr('ctrl_head.translateFixed','mult_headTransFix.input2Y')
   cmds.connectAttr('ctrl_head.translateFixed','mult_headTransFix.input2Z')
   cmds.connectAttr('mult_headRotFix.output','ctrlCons_head.rotate')
   cmds.connectAttr('mult_headTransFix.output','ctrlCons_head.translate')
   
   cs = ['ctrl_pelvis','ctrl_abdomen','ctrl_waist','ctrl_chest']
   self.ctrlCrystal('ctrl_neck1',ch*0.4,ch*0.4,2,[1,1,1,1,1,1,0,0,0,0],[0.01,0.05,0.01])
   self.ctrlCrystal('ctrl_neck2',ch*0.4,ch*0.4,2,[1,1,1,1,1,1,0,0,0,0],[0.01,0.05,0.01])
   div = float(joNum)/3
   pCons1 = cmds.pointConstraint(self.neckJo[int(div)],self.neckJo[int(div)+1],'ctrlTrans_neck1')
   cmds.setAttr(pCons1[0]+'.'+self.neckJo[int(div)]+'W0',1-(div%1))
   cmds.setAttr(pCons1[0]+'.'+self.neckJo[int(div)+1]+'W1',(div%1))
   pCons2 = cmds.pointConstraint(self.neckJo[int(div*2)],self.neckJo[int(div*2)+1],'ctrlTrans_neck2')
   cmds.setAttr(pCons2[0]+'.'+self.neckJo[int(div*2)]+'W0',1-((div*2)%1))
   cmds.setAttr(pCons2[0]+'.'+self.neckJo[int(div*2)+1]+'W1',((div*2)%1))
   cmds.delete(pCons1,pCons2)
   cmds.parent('ctrlTrans_neck1','ctrlTrans_neck')
   cmds.parent('ctrlTrans_neck2','ctrlTrans_neck')
   cmds.parent('ctrlTrans_head','ctrl_chest')
   cmds.orientConstraint('ctrl_head',self.headJo)
   
   cmds.createNode('transform',name='v_headCtrl',parent='ctrlTrans_head')
   cmds.pointConstraint('ctrl_head','v_headCtrl')
   cmds.orientConstraint('ctrl_head','v_headCtrl')
   cmds.createNode('multiplyDivide',name='mult_neck1Cons',skipSelect=1)
   cmds.createNode('multiplyDivide',name='mult_neck2Cons',skipSelect=1)
   cmds.createNode('multDoubleLinear',name='mdl_neck1Cons',skipSelect=1)
   cmds.createNode('multDoubleLinear',name='mdl_neck2Cons',skipSelect=1)
   cmds.connectAttr('v_headCtrl.translate','mult_neck1Cons.input1')
   cmds.connectAttr('v_headCtrl.translate','mult_neck2Cons.input1')
   cmds.connectAttr('v_headCtrl.rotateZ','mdl_neck1Cons.input1')
   cmds.connectAttr('v_headCtrl.rotateZ','mdl_neck2Cons.input1')
   cmds.setAttr('mult_neck1Cons.input2',1.0/3,1.0/3,1.0/3)
   cmds.setAttr('mult_neck2Cons.input2',2.0/3,2.0/3,2.0/3)
   cmds.setAttr('mdl_neck1Cons.input2',1.0/3)
   cmds.setAttr('mdl_neck2Cons.input2',2.0/3)
   cmds.connectAttr('mult_neck1Cons.output','ctrlCons_neck1.translate')
   cmds.connectAttr('mult_neck2Cons.output','ctrlCons_neck2.translate')
   cmds.connectAttr('mdl_neck1Cons.output','ctrlCons_neck1.rotateZ')
   cmds.connectAttr('mdl_neck2Cons.output','ctrlCons_neck2.rotateZ')
   
   self.curveCtrled('crv_neckCtrl',['ctrlTrans_neck','ctrl_neck1','ctrl_neck2','ctrl_head'],1)
   cmds.duplicate('crv_neckCtrl',name='crv_neckCtrlBase',renameChildren=1)
   sp = cmds.listRelatives('crv_neckCtrlBase',shapes=1)[0]
   cmds.rename(sp,'crv_neckCtrlBaseShape')

   joPos = []
   for i in range(joNum) :
    joPos.append(cmds.xform(self.neckJo[i],q=1,ws=1,t=1))
   joPos.append(cmds.xform(self.headJo,q=1,ws=1,t=1))
   cmds.curve(ep=joPos,name='crv_neck')
   sp = cmds.listRelatives('crv_neck',shapes=1)[0]
   cmds.rename(sp,'crv_neckShape')
   cmds.setAttr('crv_neck.v',0)
   cmds.parent('crv_neck','ctrlTrans_neck')
   w = cmds.wire('crv_neck',dds=[(0,100)])[0]
   cmds.connectAttr('crv_neckCtrlShape.worldSpace[0]',w+'.deformedWire[0]')
   cmds.connectAttr('crv_neckCtrlBaseShape.worldSpace[0]',w+'.baseWire[0]')
   rCrv = cmds.rebuildCurve('crv_neck',name='crv_neckRe',constructionHistory=1,rpo=0,rt=0,end=1,keepRange=0,kcp=0,kep=1,kt=0,spans=20,d=3,tol=0.01)
   cmds.setAttr('crv_neckRe.v',0)
   cmds.parent('crv_neckRe','ctrlTrans_neck')
   dCrv = cmds.createNode('detachCurve',name='dCrv_neck')
   cmds.connectAttr(rCrv[1]+'.outputCurve',dCrv+'.inputCurve')
   ci = cmds.createNode('curveInfo',name='crvInfo_neck')
   cmds.connectAttr(rCrv[1]+'.outputCurve',ci+'.inputCurve')
   cmds.createNode('multiplyDivide',name='divide_neck',skipSelect=1)
   cmds.connectAttr('crvInfo_neck.arcLength','divide_neck.input2X')
   cmds.setAttr('divide_neck.input1X',cmds.getAttr('crvInfo_neck.arcLength'))
   cmds.setAttr('divide_neck.operation',2)
   cmds.createNode('blendTwoAttr',name='b2a_neck')
   cmds.connectAttr('ctrl_head.stretchable','b2a_neck.attributesBlender')
   cmds.setAttr('b2a_neck.input[1]',1)
   cmds.connectAttr('divide_neck.outputX','b2a_neck.input[0]')
   cmds.createNode('condition',name='cd_neck',skipSelect=1)
   cmds.setAttr('cd_neck.operation',3)
   cmds.connectAttr('b2a_neck.output','cd_neck.firstTerm')
   cmds.connectAttr('b2a_neck.output','cd_neck.colorIfFalseR')
   cmds.setAttr('cd_neck.secondTerm',1)
   cmds.setAttr('cd_neck.colorIfTrueR',1)
   cmds.connectAttr('cd_neck.outColorR','dCrv_neck.parameter[0]')
   cmds.connectAttr(dCrv+'.outputCurve[0]','crv_neckReShape.create',f=1)

    #for i in range(1,joNum) :
   cs = ['ctrlTrans_neck','ctrl_neck1','ctrl_neck2','ctrl_head'] # repeat
   dvd = ''
   for i in range(0,joNum+1) :
    vn = cmds.createNode('transform',name='pos_neck'+str(i),parent='ctrlTrans_neck',skipSelect=1)
    poc = cmds.createNode('pointOnCurveInfo',name='poc_neck'+str(i))
    cmds.connectAttr('crv_neckReShape.worldSpace[0]',poc+'.inputCurve')
    cmds.setAttr(poc+'.parameter',1.0/joNum*i)
    cmds.setAttr(poc+'.turnOnPercentage',1)
    cmds.connectAttr(poc+'.position',vn+'.translate')
    cmds.setAttr(vn+'.inheritsTransform',0)
    quotient = int(( 3.0 / joNum * i )//1)
    remainder = ( 3.0 / joNum * i ) % 1
    if remainder == 0 :
     oCons = cmds.orientConstraint(cs[quotient],'pos_neck'+str(i))
    else :
     oCons = cmds.orientConstraint(cs[quotient],cs[quotient+1],'pos_neck'+str(i))
     cmds.setAttr(oCons[0]+'.'+cs[quotient]+'W0',1-remainder)
     cmds.setAttr(oCons[0]+'.'+cs[quotient+1]+'W1',remainder)
    cmds.setAttr(oCons[0]+'.interpType',2)
    cmds.createNode('transform',name='aim_neck'+str(i),parent='pos_neck'+str(i),skipSelect=1)
    cmds.createNode('transform',name='pin_neck'+str(i),parent='aim_neck'+str(i))
    cmds.createNode('transform',name='len_neck'+str(i),parent='aim_neck'+str(i))
    cmds.addAttr('len_neck'+str(i),longName='rate',attributeType='double')
    if i > 0 :
     cmds.aimConstraint('pos_neck'+str(i),'aim_neck'+str(i-1),aimVector=[0,0,1],upVector=[0,1,0],worldUpType='none')
     cmds.pointConstraint('pos_neck'+str(i),'len_neck'+str(i-1))
    if i % 3 == 1 :
     dvd = cmds.createNode('multiplyDivide',name='divide_neckLen'+str(i))
     cmds.setAttr(dvd+'.operation',2)
     cAttr = 'X'
    elif i % 3 == 2 : cAttr = 'Y'
    else : cAttr = 'Z'
    if i > 0 :
     cmds.connectAttr('len_neck'+str(i-1)+'.translateZ',dvd+'.input1'+cAttr)
     cmds.setAttr(dvd+'.input2'+cAttr,cmds.getAttr('len_neck'+str(i-1)+'.translateZ'))
     cmds.connectAttr(dvd+'.output'+cAttr,'len_neck'+str(i-1)+'.rate')
	
   for i in range(0,joNum) :
    self.ctrlCircle('ctrl_neckFK'+str(i),ch*0.4,1,2,[1,1,1,1,1,1,0,0,0,0],[0.01,0.05,0.01])
    cmds.matchTransform('ctrlTrans_neckFK'+str(i),self.neckJo[i])
    if i == 0 : cmds.parent('ctrlTrans_neckFK'+str(i),'ctrlTrans_neck')
    else : cmds.parent('ctrlTrans_neckFK'+str(i),'ctrl_neckFK'+str(i-1))
	
   nJoL = self.neckJo[:] ; nJoL.append(self.headJo)
   for i in range(joNum+1) :
    pJo = nJoL[i]
    if i == joNum : pJo = self.headJo
    cmds.matchTransform('pin_neck'+str(i),pJo)
    if i < joNum : cmds.orientConstraint('pin_neck'+str(i),pJo)
    cmds.pointConstraint('pin_neck'+str(i),pJo)
    if pJo != self.headJo : cmds.connectAttr('len_neck'+str(i)+'.rate',pJo+'.scaleY')
   
# fixed head special ctrl
  fhsc = 0
  if fhsc == 1 :
   joN = ['jo_fixedHeadIk0','jo_fixedHeadIk1','jo_fixedHeadIk2','jo_fixedHeadIk3']
   joP = ['ctrl_torso',joN[0],joN[1],joN[2]]
   cnt = ['ctrlTrans_waist','ctrlTrans_chest','ctrlTrans_neck','ctrlTrans_head']
   for i in range(len(joN)) :
    cmds.createNode('joint',name=joN[i],parent=joP[i],skipSelect=1)
   cmds.matchTransform('jo_fixedHeadIk1','ctrl_chest')
   cmds.matchTransform('jo_fixedHeadIk2','ctrlTrans_neck')
   cmds.matchTransform('jo_fixedHeadIk3','ctrl_head')
   cmds.ikHandle(startJoint='jo_fixedHeadIk0',endEffector='jo_fixedHeadIk3',priority=2,weight=1,solver='ikSCsolver',sticky='sticky',name='ik_fixedHead')
   self.ctrlSquare('ctrl_fixedHead',ch*1.1,ch*1.1,ch*1.1,1,[1,1,1,1,1,1,0,0,0,0],[0.3,0.3,0.3])
   cmds.addAttr('ctrl_head',longName='fixedHeadCtrl',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.parent('ctrlTrans_fixedHead','ctrlTrans_torso')
   cmds.matchTransform('ctrlTrans_fixedHead',self.headJo)
   cmds.parent('ik_fixedHead','ctrl_fixedHead')
   cmds.setAttr('ik_fixedHead.v',0)
   cmds.setAttr('jo_fixedHeadIk0.v',0)
   self.ctrlAttrPara('ik_fixedHead',[3,3,3,3,3,3,3,3,3,1])
   for i in range(len(joN)) :
    md = cmds.createNode('multiplyDivide',name='mult_'+joN[i][3:],skipSelect=1)
    cmds.connectAttr(joN[i]+'.rotate',md+'.input1')
    cmds.connectAttr('ctrl_head.fixedHeadCtrl',md+'.input2X')
    cmds.connectAttr('ctrl_head.fixedHeadCtrl',md+'.input2Y')
    cmds.connectAttr('ctrl_head.fixedHeadCtrl',md+'.input2Z')
    if i in [0,1] : cmds.connectAttr(md+'.output',cnt[i]+'.rotate')
    if i == 3 :
     #cmds.pointConstraint('ctrl_fixedHead',cnt[i])
     #cmds.orientConstraint(joN[i],cnt[i])
	 #cmds.orientConstraint('ctrl_fixedHead','follow0_head')
     pCons = cmds.parentConstraint('ctrlTrans_torso','ctrl_fixedHead','follow0_head',maintainOffset=1)[0]
     cmds.createNode('reverse',name='rvs_fixedHead')
     cmds.connectAttr('ctrl_head.fixedHeadCtrl','rvs_fixedHead.inputX')
     cmds.connectAttr('rvs_fixedHead.outputX',pCons+'.ctrlTrans_torsoW0')
     cmds.connectAttr('ctrl_head.fixedHeadCtrl',pCons+'.ctrl_fixedHeadW1')
   cmds.connectAttr('ctrl_head.fixedHeadCtrl','ctrl_head.translateFixed')
   cmds.connectAttr('ctrl_head.fixedHeadCtrl','ctrlTrans_fixedHead.v')

# Pelvis Auto Retate
  par = 0
  if par == 1 :
   cmds.addAttr('ctrl_pelvis',longName='rotateFollow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.addAttr('ctrl_pelvis',longName='twistFollow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.createNode('transform',name='aim_pelvisRot',parent='ctrl_torso_trans')
   cmds.pointConstraint('ctrl_heelL_pin','ctrl_heelR_pin','aim_pelvisRot')
   cmds.aimConstraint('ctrl_heelL_pin','aim_pelvisRot',aimVector=[1,0,0],upVector=[0,1,0],worldUpType='object',worldUpObject='ctrl_torso')
   cmds.setAttr('aim_pelvisRot.rotateOrder',4)
   cmds.createNode('transform',name='dri_pelvisRot',parent='ctrl_torso')
   cmds.aimConstraint('aim_pelvisRot','dri_pelvisRot',aimVector=[0,-1,0],upVector=[0,0,1],worldUpType='none')
   cmds.createNode('multiplyDivide',name='multiply_pelvisFollow')
   cmds.connectAttr('dri_pelvisRot.rotate','multiply_pelvisFollow.input1')
   cmds.connectAttr('ctrl_pelvis.rotateFollow','multiply_pelvisFollow.input2X')
   cmds.connectAttr('ctrl_pelvis.rotateFollow','multiply_pelvisFollow.input2Y')
   cmds.connectAttr('ctrl_pelvis.rotateFollow','multiply_pelvisFollow.input2Z')
   cmds.connectAttr('multiply_pelvisFollow.output','ctrl_pelvis_consA.rotate')
   cmds.createNode('multDoubleLinear',name='mdl_pelvisFollow')
   cmds.connectAttr('aim_pelvisRot.rotateY','mdl_pelvisFollow.input1')
   cmds.connectAttr('ctrl_pelvis.twistFollow','mdl_pelvisFollow.input2')
   cmds.connectAttr('mdl_pelvisFollow.output','ctrl_pelvis_consB.rotateY')

# ear Controller
  elif self.exCheck([self.earJo[0],self.L2R(self.earJo[0])]) :
   side = ['L','R'] ; ctrlDir = [1,-1]
   rJo = [self.earJo[0],self.L2R(self.earJo[0])] ; eJo = [self.earJo[1],self.L2R(self.earJo[1])]
   iJo = [self.earJo[2],self.L2R(self.earJo[2])] ; oJo = [self.earJo[4],self.L2R(self.earJo[4])]
   itJo = [self.earJo[3],self.L2R(self.earJo[3])] ; otJo = [self.earJo[5],self.L2R(self.earJo[5])]
   cmds.createNode('transform',name='cons_earCtrl',parent='ctrl_head')
   cmds.parentConstraint(self.headJo,'cons_earCtrl')
   for i in range(2) :
    s = side[i]
    self.ctrlCircle('ctrl_ear'+s,ch*0.25,1,1,[1,1,1,1,1,1,0,0,0,0],[0.3,0.4,0.1])
    cmds.parent('ctrlTrans_ear'+s,'cons_earCtrl')
    cmds.matchTransform('ctrlTrans_ear'+s,eJo[i])
    cmds.parentConstraint('ctrl_ear'+s,eJo[i])
    cmds.createNode('transform',name='pin_earRootBase'+s,parent='ctrlTrans_ear'+s)
    cmds.createNode('transform',name='pin_earRoot'+s,parent='ctrl_ear'+s)
    cmds.matchTransform('pin_earRootBase'+s,rJo[i])
    cmds.matchTransform('pin_earRoot'+s,rJo[i])
    cmds.parentConstraint('pin_earRootBase'+s,'pin_earRoot'+s,rJo[i],name='pCons_earRoot'+s)
    cmds.setAttr('pCons_earRoot'+s+'.interpType',2)
    self.ctrlCircle('ctrl_earIn'+s,ch*0.15,1,1,[1,1,1,1,1,1,0,0,0,0],[0.3,0.4,0.1])
    self.ctrlOffset('ctrl_earIn'+s,[ch*-.15*ctrlDir[i],0,0])
    cmds.parent('ctrlTrans_earIn'+s,'ctrl_ear'+s)
    cmds.matchTransform('ctrlTrans_earIn'+s,iJo[i])
    cmds.parentConstraint('ctrl_earIn'+s,iJo[i])
    self.ctrlCircle('ctrl_earOut'+s,ch*0.15,1,1,[1,1,1,1,1,1,0,0,0,0],[0.3,0.4,0.1])
    self.ctrlOffset('ctrl_earOut'+s,[ch*0.15*ctrlDir[i],0,0])
    cmds.parent('ctrlTrans_earOut'+s,'ctrl_ear'+s)
    cmds.matchTransform('ctrlTrans_earOut'+s,oJo[i])
    cmds.parentConstraint('ctrl_earOut'+s,oJo[i])
    self.ctrlCircle('ctrl_earEnd'+s,ch*0.15,0,1,[1,1,1,1,1,1,0,0,0,0],[0.3,0.4,0.1])
    self.ctrlOffset('ctrl_earEnd'+s,[0,ch*0.15*ctrlDir[i],0])
    cmds.parent('ctrlTrans_earEnd'+s,'ctrl_ear'+s,relative=1)
    cmds.delete(cmds.pointConstraint(itJo[i],otJo[i],'ctrlTrans_earEnd'+s))
    cmds.connectAttr('ctrl_earEnd'+s+'.rotate',itJo[i]+'.rotate')
    cmds.connectAttr('ctrl_earEnd'+s+'.rotate',otJo[i]+'.rotate')
    cmds.createNode('transform',name='pin_earInJo'+s,parent='ctrl_earEnd'+s)
    cmds.createNode('transform',name='pin_earOutJo'+s,parent='ctrl_earEnd'+s)
    cmds.matchTransform('pin_earInJo'+s,itJo[i])
    cmds.matchTransform('pin_earOutJo'+s,otJo[i])
    cmds.pointConstraint('pin_earInJo'+s,itJo[i])
    cmds.pointConstraint('pin_earOutJo'+s,otJo[i])
   
# tail Controller
  if self.exCheck([self.tailJo[0]]) :
   if self.exCheck([self.tailJo[0],self.tailJo[1]]) :
    self.pipeCtrl(ch*1.5,'',2,self.tailJo,self.tailTip,'tail','ctrl_pelvis',[0,0.03,0])
   else :
    self.ctrlCircle('ctrl_tail',ch*0.4,2,2,[1,1,1,1,1,1,1,1,1,0],[0,0.03,0])
    cmds.matchTransform('ctrlTrans_tail',self.tailJo[0])
    cmds.parentConstraint('ctrl_tail',self.tailJo[0])	
    cmds.parent('ctrlTrans_tail','ctrl_pelvis')
  if self.exCheck([self.rearTailJo[0]]) :
   self.pipeCtrl(ch*1.5,'',2,self.rearTailJo,self.rearTailTip,'rearTail','ctrl_rearPelvis',[0,0.03,0])
   
# facial Controller
  if self.exCheck([self.faceJo]) :
   #self.ctrlCircle('ctrl_facial',ch*1.0,2,2,[2,2,2,2,2,2,2,2,2,0],[0.1,0.1,0.1])
   cmds.createNode('transform',name='ctrlTrans_facial',skipSelect=1)
   cmds.createNode('transform',name='ctrlCons_facial',parent='ctrlTrans_facial')
   cmds.createNode('transform',name='ctrl_facial',parent='ctrlCons_facial')
   cmds.xform('ctrlTrans_facial',worldSpace=1,translation=cmds.xform(self.faceJo,q=1,worldSpace=1,translation=1))
   cmds.parent('ctrlTrans_facial','ctrl_asset')
   cmds.parentConstraint(self.faceJo,'ctrlCons_facial')
   cmds.connectAttr('ctrl_move.faceCtrlVisibility','ctrlTrans_facial.v')
   self.ctrlAttrPara('ctrl_facial',[2,2,2,2,2,2,2,2,2,0])
   cmds.createNode('transform',name='cons_facialRig',parent='ctrlTrans_facial',skipSelect=1)
   cmds.parentConstraint(self.faceJo,'cons_facialRig')
   cmds.connectAttr('ctrl_head.scale','cons_facialRig.scale')
  
# EyesAim Controller
  eyeList = [self.eyeJo,self.L2R(self.eyeJo),self.thirdEyeJo]
  if self.anyCheck(eyeList):
   nList = ['eyeL','eyeR','eyeThird']
   lidList = [[self.lidJo[1],self.lidJo[3]],[self.L2R(self.lidJo[1]),self.L2R(self.lidJo[3])],[self.thirdLidJo[1],self.thirdLidJo[3]]]
   rotX = [0,-180,0] ; aVec = [[0,0,1],[0,0,-1],[0,0,1]] ; aUp = [[0,1,0],[0,-1,0],[0,1,0]]
   for i in range(len(eyeList)):
    if self.exCheck(eyeList[i]):
     if self.exCheck('ctrl_head'):
      cmds.connectAttr('ctrl_head.scale',eyeList[i]+'.scale')
	  
     x = cmds.xform(eyeList[i],q=1,worldSpace=1,translation=1)
     eyeAngle = 0
     #self.ctrlCircle('ctrl_'+nList[i],ch*0.03,2,2,[1,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35])
     self.ctrlLocator('ctrl_'+nList[i],ch*0.05,2,[1,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35])
     #cmds.addAttr('ctrl_eyeL',longName='irisScale',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
     #cmds.addAttr('ctrl_eyeL',longName='pupilScale',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
     cmds.parent('ctrlTrans_'+nList[i],'ctrl_facial')
     tn = cmds.createNode('transform',parent=eyeList[i],skipSelect=1)
     if nList[i][-1] == 'R' : cmds.setAttr(tn+'.rotateX',180)
     cmds.setAttr(tn+'.translateZ',cmds.getAttr(lidList[i][0]+'.translateZ')+cmds.getAttr(lidList[i][1]+'.translateZ'))
     cmds.matchTransform('ctrlTrans_'+nList[i],tn)
     cmds.delete(tn)
     os = cmds.createNode('transform',name='ctrlAim_'+nList[i]+'Os',parent='ctrl_facial')
     cmds.createNode('transform',name='ctrlAim_'+nList[i],parent=os)
     cmds.matchTransform(os,eyeList[i],position=1)
     cmds.setAttr(os+'.rotateX',rotX[i])
     cmds.aimConstraint('ctrl_'+nList[i],'ctrlAim_'+nList[i],aimVector=aVec[i],upVector=aUp[i],worldUpType='none')
     cmds.connectAttr('ctrlAim_'+nList[i]+'.rotate',eyeList[i]+'.rotate')
   
   x = cmds.xform(eyeList[0],q=1,worldSpace=1,translation=1)
   if eyeAngle < 50 :
    self.ctrlSquare('ctrl_eyesAim',ch*.2,ch*.2,ch*.2,2,[1,1,1,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    self.ctrlLocator('ctrl_eyesAimL',ch*.5,2,[1,1,1,0,0,0,0,0,0,0],[0.3,0.1,0.3])
    self.ctrlLocator('ctrl_eyesAimR',ch*.5,2,[1,1,1,0,0,0,0,0,0,0],[0.3,0.1,0.3])
    cmds.parent('ctrlTrans_eyesAimL','ctrlTrans_eyesAimR','ctrl_eyesAim')
    cmds.createNode('transform',name='aim_eyeL',parent='ctrlTrans_eyesAim')
    cmds.createNode('transform',name='aim_eyeR',parent='ctrlTrans_eyesAim')
    cmds.xform('ctrlTrans_eyesAim',worldSpace=1,translation=[0,x[1],x[2]+ch*3])
    cmds.xform('ctrlTrans_eyesAimL',worldSpace=1,translation=[x[0],x[1],x[2]+ch*3])
    cmds.xform('ctrlTrans_eyesAimR',worldSpace=1,translation=[-x[0],x[1],x[2]+ch*3])
    cmds.delete(cmds.pointConstraint(eyeList[0],'aim_eyeL'))
    cmds.delete(cmds.pointConstraint(eyeList[1],'aim_eyeR'))
    cmds.aimConstraint('ctrl_eyesAimL','aim_eyeL',aimVector=[0,0,1],upVector=[0,1,0],worldUpType='none')
    cmds.aimConstraint('ctrl_eyesAimR','aim_eyeR',aimVector=[0,0,1],upVector=[0,1,0],worldUpType='none')
    cmds.xform('ctrlCons_eyeL',rotatePivot=cmds.xform(eyeList[0],q=1,translation=1,worldSpace=1),worldSpace=1)
    cmds.xform('ctrlCons_eyeR',rotatePivot=cmds.xform(eyeList[1],q=1,translation=1,worldSpace=1),worldSpace=1)
    cmds.connectAttr('aim_eyeL.rotate','ctrlCons_eyeL.rotate')
    cmds.connectAttr('aim_eyeR.rotate','ctrlCons_eyeR.rotate')
    cmds.parent('ctrlTrans_eyesAim','ctrl_facial')
  
# brow Controller self.browJo = ['jcF05_browM','jlF10_browL','jlF15_browMidL']
  if self.exCheck(self.browJo):
   
   ctrl = ['glabella','browL','browR']
   #ctrl = ['ctrl_glabella','ctrl_browL','ctrl_browMidL','ctrl_browTailL']
   loc = [self.browJo[0],self.browJo[1],self.L2R(self.browJo[1])]
   exCd = [self.browJo[0],self.browJo[1],self.L2R(self.browJo[1])]
   posA = cmds.xform(self.browJo[0],q=1,worldSpace=1,translation=1)
   posB = cmds.xform(self.browJo[1],q=1,worldSpace=1,translation=1)
   dis = math.sqrt( math.pow(posA[0]-posB[0],2) + math.pow(posA[1]-posB[1],2) + math.pow(posA[2]-posB[2],2) )
   size = [0.015,0.02,0.02]
   
   for i in range(len(ctrl)):
    if cmds.objExists(exCd[i]):
     self.ctrlCircle('ctrl_'+ctrl[i],ch*size[i],2,1,[0,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35])
     cmds.parent('ctrlTrans_'+ctrl[i],'ctrl_facial')
     cmds.matchTransform('ctrlTrans_'+ctrl[i],loc[i],position=1)
     cmds.setAttr('ctrlTrans_'+ctrl[i]+'.translateZ',cmds.getAttr('ctrlTrans_'+ctrl[i]+'.translateZ')*1.05)
     cmds.setAttr('ctrlTrans_'+ctrl[i]+'.scale',dis*0.5,dis*0.5,dis*0.5)
   
   weight = [ [ ['ctrl_glabella',[0,1,0]],['ctrl_browL',[0,0.4,0]],['ctrl_browR',[0,0.4,0]] ] ]
   weight += [ [ ['ctrl_glabella',[0,0.5,0]],['ctrl_browL',[0.08,0.92,0],[0.5,0.5,0]] ] ]
   weight += [ [ ['ctrl_browL',[0,0.5,0],[0.5,0.5,0]] ] ]
   for i in range(len(self.browJo)):
    js = self.joBelong(self.browJo[i])
    if self.browJo[i][-1] != 'L' : sideList = ['']
    else : sideList = ['L','R']
    for side in sideList :
     jo = self.browJo[i]
     if side == 'R' : jo = self.L2R(jo)
     pma = cmds.createNode('plusMinusAverage',name=jo.replace('jo_','plus_'),skipSelect=1)
     cmds.setAttr(pma+'.input3D[0].input3Dx',cmds.getAttr(jo+'.translateX'))
     cmds.setAttr(pma+'.input3D[0].input3Dy',cmds.getAttr(jo+'.translateY'))
     cmds.setAttr(pma+'.input3D[0].input3Dz',cmds.getAttr(jo+'.translateZ'))
     #cmds.connectAttr(pma+'.output3D',jo+'.translate')
     print jo
     for j,w in enumerate(weight[i]) :
      txm = 1
      if side == 'R' : w[0] = self.L2R(w[0]) ; txm = -1
      if len(w) == 2 :
       mult = cmds.createNode('multiplyDivide',skipSelect=1)
       cmds.connectAttr(w[0]+'.translate',mult+'.input1')
       cmds.setAttr(mult+'.input2',w[1][0],w[1][1],w[1][2],type='double3')
       cmds.connectAttr(mult+'.output',pma+'.input3D['+str(j+1)+']')
      if len(w) == 3 :
       cd = cmds.createNode('condition')
       cmds.connectAttr(w[0]+'.translateY',cd+'.firstTerm')
       cmds.setAttr(cd+'.operation',3)
       cmds.connectAttr(cd+'.outColor',pma+'.input3D['+str(j+1)+']')
       upm = cmds.createNode('multiplyDivide',skipSelect=1)
       dnm = cmds.createNode('multiplyDivide',skipSelect=1)
       cmds.connectAttr(upm+'.output',cd+'.colorIfTrue')
       cmds.connectAttr(dnm+'.output',cd+'.colorIfFalse')
       cmds.connectAttr(w[0]+'.translateY',upm+'.input1X')
       cmds.connectAttr(w[0]+'.translateY',upm+'.input1Y')
       cmds.connectAttr(w[0]+'.translateY',upm+'.input1Z')
       cmds.connectAttr(w[0]+'.translateY',dnm+'.input1X')
       cmds.connectAttr(w[0]+'.translateY',dnm+'.input1Y')
       cmds.connectAttr(w[0]+'.translateY',dnm+'.input1Z')
       cmds.setAttr(upm+'.input2',w[1][0]*txm,w[1][1],w[1][2],type='double3')
       cmds.setAttr(dnm+'.input2',w[2][0]*txm,w[2][1],w[2][2],type='double3')

   for s in ['L','R']:
    if cmds.objExists('grp_facial.browLower'+s):
     cmds.createNode('clamp',name='clp_upLidY'+s)
     cmds.connectAttr('ctrl_brow'+s+'.translateY','clp_upLidY'+s+'.inputR')
     cmds.connectAttr('ctrl_brow'+s+'.translateY','clp_upLidY'+s+'.inputG')
     cmds.setAttr('clp_upLidY'+s+'.minR',0)
     cmds.setAttr('clp_upLidY'+s+'.maxR',1)
     cmds.setAttr('clp_upLidY'+s+'.minG',-1)
     cmds.setAttr('clp_upLidY'+s+'.maxG',0)
     cmds.connectAttr('clp_upLidY'+s+'.outputR','grp_facial.browRaise'+s)
     cmds.createNode('multDoubleLinear',name='mdl_browLower'+s)
     cmds.connectAttr('clp_upLidY'+s+'.outputG','mdl_browLower'+s+'.input1')
     cmds.setAttr('mdl_browLower'+s+'.input2',-1)
     cmds.connectAttr('mdl_browLower'+s+'.output','grp_facial.browLower'+s)
	   
# eyelid Controller
  lidsList = [[self.lidJo[0],self.lidJo[1],self.lidJo[2],self.lidJo[3]]]
  lidsList.append(self.L2R([self.lidJo[0],self.lidJo[1],self.lidJo[2],self.lidJo[3]]))
  lidsList.append([self.thirdLidJo[0],self.thirdLidJo[1],self.thirdLidJo[2],self.thirdLidJo[3]])
  sideList = ['L','R','Third']
  openAttr = ['upperLidOpenRotate','upperLidOpenRotate','thirdUpLidOpenRotate']
  lowOpenAttr = ['lowerLidOpenRotate','lowerLidOpenRotate','thirdLoLidOpenRotate']
  eyeList = [self.eyeJo,self.L2R(self.eyeJo),self.thirdEyeJo]
  for i,x in enumerate(lidsList) :
   if self.exCheck(x) :
    upLidRo = x[0] ; upLidJo = x[1] ; loLidRo = x[2] ; loLidJo = x[3] ; s = sideList[i]
    tt = cmds.createNode('transform',parent=upLidRo,skipSelect=1) # prepare uplid ctrl position
    cmds.setAttr(tt+'.translateZ',cmds.getAttr(upLidJo+'.tz')*1.8)
    self.ctrlCircleH('ctrl_upLid'+s,ch*.025,2,0,2,[0,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35]) # generate uplid ctrl
    cmds.matchTransform('ctrlTrans_upLid'+s,tt,position=1)
    cmds.transformLimits('ctrl_upLid'+s,enableTranslationY=[1,1],translationY=[-1,0.5],enableTranslationX=[1,1],translationX=[-.5,0.5])

    cmds.parent(tt,loLidRo,relative=1) # prepare lolid ctrl position
    cmds.setAttr(tt+'.translateZ',cmds.getAttr(loLidJo+'.tz')*1.8)
    self.ctrlCircleH('ctrl_loLid'+s,ch*.02,2,180,2,[0,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35]) # generate lolid ctrl
    cmds.transformLimits('ctrl_loLid'+s,enableTranslationY=[1,1],translationY=[-.5,0.5],enableTranslationX=[1,1],translationX=[-.5,0.5])
    cmds.matchTransform('ctrlTrans_loLid'+s,tt,position=1)
    loPlus = cmds.createNode('plusMinusAverage',name='plus_lodLid'+s,skipSelect=1)
    cmds.connectAttr(loPlus+'.output3D','ctrlCons_loLid'+s+'.translate')

    cmds.delete(cmds.aimConstraint('ctrl_loLid'+s,'ctrlTrans_upLid'+s,aimVector=[0,-1,0],upVector=[0,1,0],worldUpType='none'))
    cmds.delete(cmds.aimConstraint('ctrl_upLid'+s,'ctrlTrans_loLid'+s,aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none'))
    cmds.parent('ctrlTrans_upLid'+s,'ctrlTrans_loLid'+s,'ctrl_facial')	
    cmds.orientConstraint(upLidRo,tt)
    ag = cmds.getAttr(tt+'.rotateX') # angle between uplidJo and lolidJo
    cmds.delete(tt)
    dis = self.distance('ctrl_upLid'+s,'ctrl_loLid'+s) # distance between uplidJo and lolidJo
    cmds.setAttr('ctrlTrans_upLid'+s+'.scale',dis,dis,dis)
    cmds.setAttr('ctrlTrans_loLid'+s+'.scale',dis,dis,dis)
    self.ctrlAttrPara('ctrlTrans_upLid'+s,[3,3,3,3,3,3,3,3,3,1])
    self.ctrlAttrPara('ctrlTrans_loLid'+s,[3,3,3,3,3,3,3,3,3,1])
    self.ctrlScale('ctrl_upLid'+s,1/dis)
    self.ctrlScale('ctrl_loLid'+s,1/dis)
    if cmds.objExists('ctrlParameter.'+openAttr[i]):
     agOp = cmds.getAttr('ctrlParameter.'+openAttr[i])
     agUp = ag + cmds.getAttr('ctrlParameter.'+openAttr[i])
     dis = dis * (agUp/ag)
     #vDef = (ag-agUp)/agUp	
     vDef = agOp/abs(agUp)
     cmds.setAttr('ctrl_upLid'+s+'.ty',vDef)
     self.ctrlTransRem('ctrl_upLid'+s)
    else: agUp = ag ; vDef = 0
    if cmds.objExists('ctrlParameter.'+lowOpenAttr[i]):
     agCl = cmds.getAttr('ctrlParameter.'+lowOpenAttr[i])
     agDn = ag - agCl
     lvDef = -agCl/agDn
     cmds.setAttr('ctrl_loLid'+s+'.ty',lvDef)
     self.ctrlTransRem('ctrl_loLid'+s)
    else: agDn = ag ; lvDef = 0

    cmds.createNode('addDoubleLinear',name='adl_uplidDef'+s,skipSelect=1)
    cmds.connectAttr('ctrl_upLid'+s+'.ty','adl_uplidDef'+s+'.input1')
    cmds.setAttr('adl_uplidDef'+s+'.input2',-vDef)
    cmds.createNode('addDoubleLinear',name='adl_uplid'+s,skipSelect=1)
    cmds.connectAttr('adl_uplidDef'+s+'.output','adl_uplid'+s+'.input1')
    cmds.connectAttr('ctrlCons_upLid'+s+'.ty','adl_uplid'+s+'.input2')
    #cmds.connectAttr('adl_uplid'+s+'.output',self.faceJo + '.' + bsAttrs[0] + s)
    cmds.createNode('multDoubleLinear',name='mdl_uplid'+s)
    #cmds.connectAttr('adl_uplid'+s+'.output','mdl_uplid'+s+'.input1') not now, do it after lid effect
    cmds.setAttr('mdl_uplid'+s+'.input2',agUp)
    cmds.connectAttr('mdl_uplid'+s+'.output',upLidRo+'.rotateX')

    cmds.createNode('addDoubleLinear',name='adl_lolidDef'+s,skipSelect=1)
    cmds.connectAttr('ctrl_loLid'+s+'.ty','adl_lolidDef'+s+'.input1')
    cmds.setAttr('adl_lolidDef'+s+'.input2',-lvDef)
    cmds.createNode('addDoubleLinear',name='adl_lolid'+s,skipSelect=1)
    cmds.connectAttr('adl_lolidDef'+s+'.output','adl_lolid'+s+'.input1')
    cmds.connectAttr('ctrlCons_loLid'+s+'.ty','adl_lolid'+s+'.input2')
    #cmds.connectAttr('adl_lolid'+s+'.output',self.faceJo + '.' + bsAttrs[1] + s)
    cmds.createNode('multDoubleLinear',name='mdl_lolid'+s) # multiply angle value
    cmds.connectAttr('adl_lolid'+s+'.output','mdl_lolid'+s+'.input1')
    cmds.setAttr('mdl_lolid'+s+'.input2',agDn)
    cmds.connectAttr('mdl_lolid'+s+'.output',loLidRo+'.rotateX')

    cmds.addAttr('ctrl_upLid'+s,longName='lowerEffect',attributeType='double',min=0,max=1.0,defaultValue=0.2,keyable=1)
    cmds.createNode('multDoubleLinear',name='mdl_upEffect'+s,skipSelect=1)
    cmds.connectAttr('adl_uplidDef'+s+'.output','mdl_upEffect'+s+'.input1')
    cmds.connectAttr('ctrl_upLid'+s+'.lowerEffect','mdl_upEffect'+s+'.input2')
    cmds.createNode('multDoubleLinear',name='mdl_upEfMinus'+s,skipSelect=1)
    cmds.connectAttr('mdl_upEffect'+s+'.output','mdl_upEfMinus'+s+'.input1')
    cmds.setAttr('mdl_upEfMinus'+s+'.input2',-1)
    #cmds.connectAttr('mdl_upEfMinus'+s+'.output','ctrlCons_loLid'+s+'.ty')
    cmds.connectAttr('mdl_upEfMinus'+s+'.output',loPlus+'.input3D[0].input3Dy')
	
    cmds.createNode('addDoubleLinear',name='adl_loEfUpper'+s,skipSelect=1)
    cmds.connectAttr('mdl_upEfMinus'+s+'.output','adl_loEfUpper'+s+'.input1')
    cmds.connectAttr('adl_uplid'+s+'.output','adl_loEfUpper'+s+'.input2')
    cmds.connectAttr('adl_loEfUpper'+s+'.output','mdl_uplid'+s+'.input1')
	
    if cmds.objExists(eyeList[i]): # eyeball affect eyelid
     lidList = ['ctrl_upLid'+s,'ctrl_loLid'+s] ; nList = ['uplid','lolid'] ; dvList=[0.7,0.5]
     fAttrList = ['ctrlCons_upLid'+s+'.ty',loPlus+'.input3D[1].input3Dy']
     for j in range(2):
      cmds.addAttr(lidList[j],longName='eyeballAffect',attributeType='double',min=0,max=1.0,defaultValue=dvList[j],keyable=1)
      mAmp = cmds.createNode('multDoubleLinear',name='mdl_'+nList[j]+'AffectAmp'+s,skipSelect=1)
      cmds.connectAttr(eyeList[i]+'.rotateX',mAmp+'.input1')
      cmds.setAttr(mAmp+'.input2',1.0/ag)
      mWt = cmds.createNode('multDoubleLinear',name='mdl_'+nList[j]+'AffectWeight'+s,skipSelect=1)
      cmds.connectAttr(mAmp+'.output',mWt+'.input1')
      cmds.connectAttr(lidList[j]+'.eyeballAffect',mWt+'.input2')
      mDrop = cmds.createNode('multDoubleLinear',name='mdl_'+nList[j]+'AffectDrop'+s,skipSelect=1)
      cmds.connectAttr(mWt+'.output',mDrop+'.input1')
      if j == 0 :
       adl = cmds.createNode('addDoubleLinear',name='adl_'+nList[j]+'Affect'+s,skipSelect=1)
       cmds.connectAttr(lidList[j]+'.translateY',adl+'.input1')
       cmds.setAttr(adl+'.input2',1)
       cmds.connectAttr(adl+'.output',mDrop+'.input2')
      else :
       mdl = cmds.createNode('multDoubleLinear',name='mdl_'+nList[j]+'AffectDropV'+s,skipSelect=1)
       cmds.connectAttr(lidList[j]+'.translateY',mdl+'.input1')
       cmds.setAttr(mdl+'.input2',2)
       rvs = cmds.createNode('reverse',name='rvs_'+nList[j]+'AffectDropV'+s,skipSelect=1)
       cmds.connectAttr(mdl+'.output',rvs+'.inputX')
       cmds.connectAttr(rvs+'.outputX',mDrop+'.input2')
      cmds.connectAttr(mDrop+'.output',fAttrList[j])

    if self.anyCheck(['grp_facial.uplidClose'+s,'grp_facial.uplidOpen'+s,'grp_facial.uplidRaise'+s]):# bs attributes connect 
     srg = cmds.createNode('setRange',name='srg_uplidUpDnAttr'+s,skipSelect=1)
     cmds.connectAttr('adl_loEfUpper'+s+'.output',srg+'.valueX')
     cmds.connectAttr('adl_uplid'+s+'.output',srg+'.valueY')
     cmds.connectAttr('adl_uplid'+s+'.output',srg+'.valueZ')
     cmds.setAttr(srg+'.oldMinX',(1-(vDef*-1))*-1)
     cmds.setAttr(srg+'.oldMaxX',0)
     cmds.setAttr(srg+'.oldMinY',0)
     cmds.setAttr(srg+'.oldMaxY',-vDef)
     cmds.setAttr(srg+'.oldMinZ',-vDef)
     cmds.setAttr(srg+'.oldMaxZ',-vDef+0.5)
     cmds.setAttr(srg+'.max',1,1,1,type='double3')
     if cmds.objExists('grp_facial.uplidClose'+s):
      rvs = cmds.createNode('reverse',name='rvs_uplidCloseBs'+s,skipSelect=1)
      cmds.connectAttr(srg+'.outValueX',rvs+'.inputX')
      cmds.connectAttr(rvs+'.outputX','grp_facial.uplidClose'+s)
     if cmds.objExists('grp_facial.uplidOpen'+s):
      cmds.connectAttr(srg+'.outValueY','grp_facial.uplidOpen'+s)
     if cmds.objExists('grp_facial.uplidRaise'+s):
      cmds.connectAttr(srg+'.outValueZ','grp_facial.uplidRaise'+s)
	 
    if self.anyCheck(['grp_facial.lolidTight'+s,'grp_facial.lolidOpen'+s,'grp_facial.lolidDepress'+s]):
     srg = cmds.createNode('setRange',name='srg_lolipUpDnAttr'+s,skipSelect=1)
     cmds.connectAttr('adl_lolid'+s+'.output',srg+'.valueX')
     cmds.connectAttr('adl_lolid'+s+'.output',srg+'.valueY')
     cmds.connectAttr('adl_lolid'+s+'.output',srg+'.valueZ')
     cmds.setAttr(srg+'.oldMinX',lvDef)
     cmds.setAttr(srg+'.oldMaxX',0.5)
     cmds.setAttr(srg+'.oldMinY',-lvDef)
     cmds.setAttr(srg+'.oldMaxY',0)
     cmds.setAttr(srg+'.oldMinZ',-lvDef-0.5)
     cmds.setAttr(srg+'.oldMaxZ',-lvDef)
     cmds.setAttr(srg+'.max',1,1,1,type='double3')
     if cmds.objExists('grp_facial.lolidTight'+s):
      cmds.connectAttr(srg+'.outValueX','grp_facial.lolidTight'+s)
     if cmds.objExists('grp_facial.lolidOpen'+s):
      cmds.connectAttr(srg+'.outValueY',rvs+'.inputY')
      cmds.connectAttr(rvs+'.outputY','grp_facial.lolidOpen'+s)
     if cmds.objExists('grp_facial.lolidDepress'+s):
      cmds.connectAttr(srg+'.outValueZ',rvs+'.inputZ')
      cmds.connectAttr(rvs+'.outputZ','grp_facial.lolidDepress'+s)

    if cmds.objExists(eyeList[i]):
     cmds.createNode('addDoubleLinear',name='adl_eyeBallY0'+s,skipSelect=1)
     cmds.connectAttr(eyeList[i]+'.rotateY','adl_eyeBallY0'+s+'.input1')
     cmds.setAttr('adl_eyeBallY0'+s+'.input2',cmds.getAttr(eyeList[i]+'.rotateY')*-1)
     atList = ['grp_facial.uplidIn'+s,'grp_facial.lolidIn'+s,'grp_facial.uplidOut'+s,'grp_facial.lolidOut'+s]
     nList = ['uplidIn','lolidIn','uplidOut','lolidOut']
     mvList = [1.0/ag*0.5,1.0/ag*0.5,1.0/ag*-.5,1.0/ag*-.5]
     for j in range(4):
      if cmds.objExists(atList[j]):
       mult = cmds.createNode('multDoubleLinear',name='mdl_'+nList[j]+'Bs'+s,skipSelect=1)
       cmds.connectAttr('adl_eyeBallY0'+s+'.output',mult+'.input1')
       cmds.setAttr(mult+'.input2',mvList[j])
       cmds.connectAttr(mult+'.output',atList[j])

# Jaw Controller
  if self.exCheck([self.jawJo[0],self.jawJo[1]]) :
   tt = cmds.createNode('transform',parent=self.jawJo[0])
   cmds.aimConstraint(self.jawJo[1],tt,aimVector=[0,0,1],upVector=[0,1,0],worldUpType='none')
   ttt = cmds.createNode('transform',parent=tt)
   cmds.delete(cmds.pointConstraint(self.jawJo[1],ttt))
   cmds.setAttr(ttt+'.translateZ',cmds.getAttr(ttt+'.translateZ')*1.2)
   self.ctrlCircle('ctrl_jaw',ch*0.1,2,2,[1,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35])
   cmds.matchTransform('ctrlTrans_jaw',ttt)
   cmds.setAttr('ctrlTrans_jaw.rotateX',cmds.getAttr('ctrlTrans_jaw.rotateX')*0.5)
   cmds.delete(tt,ttt)
   cmds.createNode('transform',name='pin_jawTrans',parent='cons_facialRig',skipSelect=1)
   cmds.createNode('transform',name='pin_jaw',parent='pin_jawTrans',skipSelect=1)
   cmds.matchTransform('pin_jawTrans',self.headJo)
   cmds.matchTransform('pin_jaw',self.jawJo[0])
   cmds.parentConstraint('pin_jaw',self.jawJo[0])
   cmds.createNode('multiplyDivide',name='multiply_jawRot')
   cmds.connectAttr('ctrl_jaw.ty','multiply_jawRot.input1X')
   cmds.connectAttr('ctrl_jaw.tx','multiply_jawRot.input1Y')
   cmds.connectAttr('ctrl_jaw.tx','multiply_jawRot.input1Z')
   cmds.setAttr('multiply_jawRot.input2X',-5)
   cmds.setAttr('multiply_jawRot.input2Y',2.5)
   cmds.setAttr('multiply_jawRot.input2Z',0.1)
   cmds.connectAttr('multiply_jawRot.outputY','pin_jaw.rotateY')
   cmds.connectAttr('multiply_jawRot.outputZ','pin_jaw.translateX')
   
   cmds.createNode('multDoubleLinear',name='mdl_jawTy',skipSelect=1)
   cmds.connectAttr('ctrl_jaw.ty','mdl_jawTy.input1')
   cmds.setAttr('mdl_jawTy.input2',-1)
   cmds.createNode('setRange',name='rag_jaw',skipSelect=1)
   cmds.connectAttr('mdl_jawTy.output','rag_jaw.valueX')
   cmds.connectAttr('mdl_jawTy.output','rag_jaw.valueY')
   cmds.connectAttr('mdl_jawTy.output','rag_jaw.valueZ')
   cmds.setAttr('rag_jaw.maxX',30)
   cmds.setAttr('rag_jaw.maxY',10)
   cmds.setAttr('rag_jaw.maxZ',20)
   cmds.setAttr('rag_jaw.oldMinZ',2)
   cmds.setAttr('rag_jaw.oldMaxX',6)
   cmds.setAttr('rag_jaw.oldMaxY',2)
   cmds.setAttr('rag_jaw.oldMaxZ',6)
   cmds.connectAttr('rag_jaw.outValueY','pin_jaw.rotateX')
   cmds.connectAttr('rag_jaw.outValueZ','pin_jawTrans.rotateX')
   cmds.parent('ctrlTrans_jaw','ctrl_facial')
   
   if self.exCheck(['grp_facial.jawOpen','grp_facial.jawStretch','grp_facial.jawDrop']):# bs attributes connect 
    cmds.createNode('setRange',name='srg_jawBs',skipSelect=1)
    cmds.connectAttr('mdl_jawTy.output','srg_jawBs.valueX')
    cmds.connectAttr('mdl_jawTy.output','srg_jawBs.valueY')
    cmds.connectAttr('mdl_jawTy.output','srg_jawBs.valueZ')
    cmds.setAttr('srg_jawBs.max',1,1,1)
    cmds.setAttr('srg_jawBs.oldMin',0,2,0)
    cmds.setAttr('srg_jawBs.oldMax',2,5,6)
    cmds.connectAttr('srg_jawBs.outValueX','grp_facial.jawOpen')
    cmds.connectAttr('srg_jawBs.outValueY','grp_facial.jawStretch')
    cmds.connectAttr('srg_jawBs.outValueZ','grp_facial.jawDrop')
   
   if self.exCheck(self.lipJo) :
    #if cmds.objExists('xCons_jaw') == 0 :
     #cmds.createNode('transform',name='xCons_jaw',parent='grp_deformer')
     #self.xCons(self.jawJo[0],'xCons_jaw')

    lj = self.lipJo[:] # lid joint
    lj.append(self.L2R(self.lipJo[1]))
    lj.append(self.L2R(self.lipJo[2]))
    lj.append(self.L2R(self.lipJo[3]))
    ctrl = ['upLip','upLipL','cornerL','loLipL','loLip','upLipR','cornerR','loLipR']
    wt = [0,0.2,0.5,0.8,1,0.2,0.5,0.8]
    xv = [0,0.025,0.1,0.025,0,-.025,-.1,-.025] # x offset value
    zv = [0,-.05,-.15,-.05,0,-.05,-.15,-.05] # z offset value
    for i in range(len(lj)):
     self.ctrlLocator('ctrl_'+ctrl[i],ch*0.1,1,[1,1,1,1,1,1,0,0,0,0],[0.35,0.1,0.35])
     cmds.matchTransform('ctrlTrans_'+ctrl[i],lj[i],position=1,rotation=1)
     cmds.createNode('transform',name='pin_'+ctrl[i],parent='ctrl_'+ctrl[i])
     cmds.parent('ctrlTrans_'+ctrl[i],'ctrl_facial')
     if i >= 5 :
      cmds.setAttr('ctrlTrans_'+ctrl[i]+'.rotateX',cmds.getAttr('ctrlTrans_'+ctrl[i-4]+'.rotateX'))
      cmds.setAttr('ctrlTrans_'+ctrl[i]+'.rotateY',cmds.getAttr('ctrlTrans_'+ctrl[i-4]+'.rotateY')*-1)
      cmds.setAttr('ctrlTrans_'+ctrl[i]+'.rotateZ',cmds.getAttr('ctrlTrans_'+ctrl[i-4]+'.rotateZ')*-1)
      cmds.setAttr('ctrlTrans_'+ctrl[i]+'.scaleX',-1)
      cmds.matchTransform('pin_'+ctrl[i],lj[i])
     cmds.createNode('multMatrix',name='xMult_'+lj[i])
     cmds.connectAttr('pin_'+ctrl[i]+'.worldMatrix[0]','xMult_'+lj[i]+'.matrixIn[0]')
     cmds.connectAttr('ctrl_facial.worldInverseMatrix[0]','xMult_'+lj[i]+'.matrixIn[1]')
     cmds.createNode('decomposeMatrix',name='xCons_'+lj[i])
     cmds.connectAttr('xMult_'+lj[i]+'.matrixSum','xCons_'+lj[i]+'.inputMatrix')
     cmds.connectAttr('xCons_'+lj[i]+'.outputTranslate',lj[i]+'.translate')
     cmds.connectAttr('xCons_'+lj[i]+'.outputRotate',lj[i]+'.rotate')
     #cmds.parentConstraint('pin_'+ctrl[i],lj[i])
 
     cmds.createNode('transform',name='ctrlCons_'+ctrl[i]+'Jaw',skipSelect=1,parent='ctrlTrans_'+ctrl[i])
     cmds.parent('ctrl_'+ctrl[i],'ctrlCons_'+ctrl[i]+'Jaw')
     t = cmds.createNode('transform',skipSelect=1,parent=self.jawJo[0])
     #cmds.matchTransform(t,'ctrl_'+ctrl[i])
     cmds.matchTransform(t,'ctrlTrans_'+ctrl[i])
     cmds.createNode('multMatrix',name='xMult_'+ctrl[i]+'A',skipSelect=1)
     cmds.setAttr('xMult_'+ctrl[i]+'A.matrixIn[0]',cmds.getAttr(t+'.matrix'),type='matrix')
     cmds.delete(t)
     cmds.connectAttr(self.jawJo[0]+'.matrix','xMult_'+ctrl[i]+'A.matrixIn[1]')
     cmds.createNode('multMatrix',name='xMult_'+ctrl[i]+'B',skipSelect=1)
     cmds.connectAttr('xMult_'+ctrl[i]+'A.matrixSum','xMult_'+ctrl[i]+'B.matrixIn[0]')
     cmds.setAttr('xMult_'+ctrl[i]+'B.matrixIn[1]',cmds.getAttr('ctrlTrans_'+ctrl[i]+'.inverseMatrix'),type='matrix')
     cmds.createNode('wtAddMatrix',name='xAdd_'+ctrl[i])
     cmds.connectAttr('xMult_'+ctrl[i]+'B.matrixSum','xAdd_'+ctrl[i]+'.wtMatrix[0].matrixIn')
     cmds.setAttr('xAdd_'+ctrl[i]+'.wtMatrix[0].weightIn',wt[i])
     cmds.createNode('decomposeMatrix',name='xCons_'+ctrl[i])
     cmds.connectAttr('xAdd_'+ctrl[i]+'.matrixSum','xCons_'+ctrl[i]+'.inputMatrix')
     cmds.connectAttr('xCons_'+ctrl[i]+'.outputTranslateY','ctrlCons_'+ctrl[i]+'Jaw.translateY')
     cmds.connectAttr('xCons_'+ctrl[i]+'.outputRotate','ctrlCons_'+ctrl[i]+'Jaw.rotate')
     if xv[i] != 0 :
      cmds.createNode('multDoubleLinear',name='mdl_'+ctrl[i]+'X')
      cmds.connectAttr('ctrl_jaw.translateY','mdl_'+ctrl[i]+'X.input1')
      cmds.setAttr('mdl_'+ctrl[i]+'X.input2',xv[i])
      cmds.createNode('addDoubleLinear',name='adl_'+ctrl[i]+'X')
      cmds.connectAttr('xCons_'+ctrl[i]+'.outputTranslateX','adl_'+ctrl[i]+'X.input1')
      cmds.connectAttr('mdl_'+ctrl[i]+'X.output','adl_'+ctrl[i]+'X.input2')
      cmds.connectAttr('adl_'+ctrl[i]+'X.output','ctrlCons_'+ctrl[i]+'Jaw.translateX')
     else :
      cmds.connectAttr('xCons_'+ctrl[i]+'.outputTranslateX','ctrlCons_'+ctrl[i]+'Jaw.translateX')
     if xv[i] != 0 :
      cmds.createNode('multDoubleLinear',name='mdl_'+ctrl[i]+'Z')
      cmds.connectAttr('ctrl_jaw.translateY','mdl_'+ctrl[i]+'Z.input1')
      cmds.setAttr('mdl_'+ctrl[i]+'Z.input2',zv[i])
      cmds.createNode('addDoubleLinear',name='adl_'+ctrl[i]+'Z')
      cmds.connectAttr('xCons_'+ctrl[i]+'.outputTranslateZ','adl_'+ctrl[i]+'Z.input1')
      cmds.connectAttr('mdl_'+ctrl[i]+'Z.output','adl_'+ctrl[i]+'Z.input2')
      cmds.connectAttr('adl_'+ctrl[i]+'Z.output','ctrlCons_'+ctrl[i]+'Jaw.translateZ')
     else :
      cmds.connectAttr('xCons_'+ctrl[i]+'.outputTranslateZ','ctrlCons_'+ctrl[i]+'Jaw.translateZ')

# Cheek Controller self.cheekJo = ['jlF35_cheekL','jlF40_nasalisL','jlF45_gillL']
  if self.exCheck(self.cheekJo):
   x1 = cmds.xform(self.cheekJo[0],q=1,t=1,worldSpace=1)
   x2 = cmds.xform(self.cheekJo[1],q=1,t=1,worldSpace=1)
   dis = math.pow((x1[0]-x2[0]),2) + math.pow((x1[1]-x2[1]),2) + math.pow((x1[2]-x2[2]),2)
   dis = math.sqrt(dis)
   sa = [180,0] ; nsa = [90,-90]
   for i,s in enumerate(['L','R']) :
    self.ctrlCircleH('ctrl_cheek'+s,ch*0.02,2,sa[i],2,[0,1,0,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    cmds.parent('ctrlTrans_cheek'+s,'ctrl_facial')
    cmds.matchTransform('ctrlTrans_cheek'+s,self.L2R(self.cheekJo[0],i))
    cmds.setAttr('ctrlTrans_cheek'+s+'.translateZ',cmds.getAttr('ctrlTrans_cheek'+s+'.translateZ')*1.05)
    cmds.setAttr('ctrlTrans_cheek'+s+'.scale',dis*.5,dis*.5,dis*.5,type='double3')
    cmds.createNode('clamp',name='clp_cheekY'+s)
    cmds.connectAttr('ctrl_cheek'+s+'.translateY','clp_cheekY'+s+'.inputR')
    cmds.connectAttr('ctrl_cheek'+s+'.translateY','clp_cheekY'+s+'.inputG')
    cmds.setAttr('clp_cheekY'+s+'.minR',0)
    cmds.setAttr('clp_cheekY'+s+'.maxR',1)
    cmds.setAttr('clp_cheekY'+s+'.minG',-1)
    cmds.setAttr('clp_cheekY'+s+'.maxG',0)
    cmds.connectAttr('clp_cheekY'+s+'.outputR','grp_facial.cheekRaise'+s)
	
    self.ctrlCircleH('ctrl_nasalis'+s,ch*0.02,2,nsa[i],2,[0,1,1,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    cmds.parent('ctrlTrans_nasalis'+s,'ctrl_facial')
    cmds.matchTransform('ctrlTrans_nasalis'+s,self.L2R(self.cheekJo[1],i))
    cmds.setAttr('ctrlTrans_nasalis'+s+'.rotateY',45)
    cmds.setAttr('ctrlTrans_nasalis'+s+'.scale',dis*.5,dis*.5,dis*.5,type='double3')
    cmds.setAttr('ctrl_nasalis'+s+'.translateZ',dis*0.1,lock=1,keyable=0,channelBox=0)
    cmds.connectAttr('ctrl_nasalis'+s+'.translateY','clp_cheekY'+s+'.inputB')
    cmds.setAttr('clp_cheekY'+s+'.minB',0)
    cmds.setAttr('clp_cheekY'+s+'.maxB',1)
    cmds.connectAttr('clp_cheekY'+s+'.outputB','grp_facial.noseWrinkle'+s)
  
# corner Controller self.lipJo = ['jcF60_lipUp','jlF65_lipUpBL','jlF70_CornerL','jlF75_lipLoBL','jcF80_lipLo']
  if self.exCheck(self.lipJo):
   csa = [-90,-90] ; usa = [-30,210] ; lsa = [210,-30] ; ctrlDir = [1,-1]
   #cLoc = [self.lipJo[2],self.L2R(self.lipJo[2])]
   cLoc = ['ctrlTrans_cornerL','ctrlTrans_cornerR']
   uLoc = [self.lipJo[1],self.L2R(self.lipJo[1])]
   lLoc = [self.lipJo[3],self.L2R(self.lipJo[3])]
   cav = [ [-1,0,0],[-1,0,0] ]
   x1 = cmds.xform(self.lipJo[0],q=1,t=1,worldSpace=1)
   x2 = cmds.xform(self.lipJo[2],q=1,t=1,worldSpace=1)
   dis = math.pow((x1[0]-x2[0]),2) + math.pow((x1[1]-x2[1]),2) + math.pow((x1[2]-x2[2]),2)
   dis = math.sqrt(dis)
   for i,s in enumerate(['L','R']) :
    self.ctrlCircleH('ctrl_mouthCorner'+s,ch*0.02,2,csa[i],2,[1,1,1,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    cmds.parent('ctrlTrans_mouthCorner'+s,'ctrl_facial')
    cmds.matchTransform('ctrlTrans_mouthCorner'+s,cLoc[i])
    tt = cmds.createNode('transform')
    cmds.pointConstraint(self.L2R(self.lipJo[1],i),self.L2R(self.lipJo[3],i),tt)
    cmds.aimConstraint(tt,'ctrlCons_mouthCorner'+s,aimVector=cav[i],upVector=[0,1,0],worldUpType='none')
    cmds.delete(tt)

    cmds.setAttr('ctrlCons_mouthCorner'+s+'.rotateX',0)
    cmds.setAttr('ctrlCons_mouthCorner'+s+'.rotateZ',0)
    cmds.setAttr('ctrl_mouthCorner'+s+'.translateZ',dis*0.03,lock=1,keyable=0,channelBox=0)
    cmds.setAttr('ctrlCons_mouthCorner'+s+'.scale',dis*.3,dis*.3,dis*.3,type='double3')
	
    self.ctrlCircleH('ctrl_uplip'+s,ch*0.02,2,usa[i],2,[1,1,1,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    self.ctrlCircleH('ctrl_lolip'+s,ch*0.02,2,lsa[i],2,[1,1,1,0,0,0,0,0,0,0],[0.35,0.1,0.35])
    cmds.parent('ctrlTrans_uplip'+s,'ctrl_facial')
    cmds.parent('ctrlTrans_lolip'+s,'ctrl_facial')
    cmds.matchTransform('ctrlTrans_uplip'+s,uLoc[i])
    cmds.matchTransform('ctrlTrans_lolip'+s,lLoc[i])
    cmds.setAttr('ctrlCons_uplip'+s+'.rotateY',cmds.getAttr('ctrlCons_mouthCorner'+s+'.rotateY'))
    cmds.setAttr('ctrlCons_lolip'+s+'.rotateY',cmds.getAttr('ctrlCons_mouthCorner'+s+'.rotateY'))
    cmds.setAttr('ctrlCons_uplip'+s+'.scale',dis*.3,dis*.3,dis*.3,type='double3')
    cmds.setAttr('ctrlCons_lolip'+s+'.scale',dis*.3,dis*.3,dis*.3,type='double3')
    cmds.setAttr('ctrl_uplip'+s+'.translateZ',dis*0.03,lock=1,keyable=0,channelBox=0)
    cmds.setAttr('ctrl_lolip'+s+'.translateZ',dis*0.03,lock=1,keyable=0,channelBox=0)

    if cmds.objExists('grp_facial.cornerPull'+s) :
     cmds.createNode('clamp',name='clp_cornerX'+s)
     cmds.createNode('clamp',name='clp_cornerY'+s)
     cmds.connectAttr('ctrl_mouthCorner'+s+'.translateX','clp_cornerX'+s+'.inputR')
     cmds.connectAttr('ctrl_mouthCorner'+s+'.translateX','clp_cornerX'+s+'.inputG')
     cmds.connectAttr('ctrl_mouthCorner'+s+'.translateY','clp_cornerY'+s+'.inputR')
     cmds.connectAttr('ctrl_mouthCorner'+s+'.translateY','clp_cornerY'+s+'.inputG')
     cmds.setAttr('clp_cornerX'+s+'.minR',0)
     cmds.setAttr('clp_cornerX'+s+'.maxR',1)
     cmds.setAttr('clp_cornerX'+s+'.minG',-1)
     cmds.setAttr('clp_cornerX'+s+'.maxG',0)
     cmds.setAttr('clp_cornerY'+s+'.minR',0)
     cmds.setAttr('clp_cornerY'+s+'.maxR',1)
     cmds.setAttr('clp_cornerY'+s+'.minG',-1)
     cmds.setAttr('clp_cornerY'+s+'.maxG',0)
     cmds.connectAttr('clp_cornerX'+s+'.outputR','grp_facial.cornerStretch'+s)
     cmds.createNode('multDoubleLinear',name='mult_cornerPull'+s+'Bs')
     cmds.connectAttr('clp_cornerX'+s+'.outputR','mult_cornerPull'+s+'Bs.input1')
     cmds.connectAttr('clp_cornerY'+s+'.outputR','mult_cornerPull'+s+'Bs.input2')
     cmds.connectAttr('mult_cornerPull'+s+'Bs.output','grp_facial.cornerPull'+s)
     cmds.createNode('multDoubleLinear',name='mult_cornerDepress'+s+'Bs')
     cmds.connectAttr('clp_cornerX'+s+'.outputR','mult_cornerDepress'+s+'Bs.input1')
     cmds.connectAttr('clp_cornerY'+s+'.outputR','mult_cornerDepress'+s+'Bs.input2')
     cmds.connectAttr('mult_cornerDepress'+s+'Bs.output','grp_facial.cornerDepress'+s)

# tongue Controller
  if self.exCheck([self.tongueTipJo]):
   joList = [] ; md = ''
   for i,x in enumerate(self.tongueJo) :
    if cmds.objExists(x) :
     joList.append(x)
   joList.append(self.tongueTipJo)
   cmds.createNode('transform',name='cons_tongueCtrl',parent='ctrl_asset')
   cmds.parentConstraint(self.jawJo,'cons_tongueCtrl')
   self.ctrlSquare('ctrl_tongue',ch*0.32,ch*0.32,ch*0.32,1,[2,2,2,2,2,2,0,0,0,0],[0.3,0.1,0.3])
   cmds.addAttr('ctrl_tongue',longName='FKIK',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.parent('ctrlTrans_tongue','cons_tongueCtrl')
   cmds.matchTransform('ctrlTrans_tongue',self.tongueJo[0],position=1)
   for i,x in enumerate(joList) :
    if x != joList[-1] : cl = cmds.getAttr(joList[i+1]+'.tz') # ctrl length
    cci = (i+1) * 0.04 # ctrl color increase
    if x == joList[-1] : self.ctrlSquare('ctrl_tongueFK'+str(i),ch*0.2,ch*0.1,ch*0.025,1,[0,0,1,0,0,0,0,0,0,0],[0.3+cci+0.04,0.1+cci+0.04,0.3+cci+0.04])
    elif i == 0 : self.ctrlPlay('ctrl_tongueFK'+str(i),ch*0.2,ch*0.1,'z',cl,2,[0,0,0,1,1,1,0,0,0,0],[0.3+cci,0.1+cci,0.3+cci])
    else : self.ctrlPlay('ctrl_tongueFK'+str(i),ch*0.2,ch*0.1,'z',cl,2,[0,0,1,1,1,1,0,0,0,0],[0.3+cci,0.1+cci,0.3+cci])
    cp = 'ctrl_tongueFK'+str(i-1) # ctrl parent
    if i == 0 : cp = 'ctrl_tongue'
    cmds.parent('ctrlTrans_tongueFK'+str(i),cp,relative=1)
    if x != joList[-1] : cmds.matchTransform('ctrlTrans_tongueFK'+str(i),x)
    else : cmds.matchTransform('ctrlTrans_tongueFK'+str(i),x,position=1)
    cmds.createNode('transform',name='v_tongueFK'+str(i),parent=cp,skipSelect=1)
    cmds.orientConstraint('ctrl_tongueFK'+str(i),'v_tongueFK'+str(i))
    cmds.createNode('blendColors',name='bColor_'+x[6:])
    #cmds.connectAttr('v_tongueFK'+str(i)+'.rotate',x+'.rotate')
    cmds.connectAttr('ctrl_tongue.FKIK','bColor_'+x[6:]+'.blender')
    cmds.connectAttr('v_tongueFK'+str(i)+'.rotate','bColor_'+x[6:]+'.color2')
    cmds.connectAttr('bColor_'+x[6:]+'.output',x+'.rotate')
	
    cmds.createNode('joint',name='jo_tongueIk'+str(i),skipSelect=1)
    if i == 0 : cmds.parent('jo_tongueIk'+str(i),'ctrl_tongue',relative=1)
    else :
     cmds.parent('jo_tongueIk'+str(i),'jo_tongueIk'+str(i-1),relative=1)
     cmds.connectAttr('jo_tongueIk'+str(i-1)+'.scale','jo_tongueIk'+str(i)+'.inverseScale')
    cmds.connectAttr('jo_tongueIk'+str(i)+'.rotate','bColor_'+x[6:]+'.color1')
    #cmds.connectAttr('jo_tongueIk'+str(i)+'.scaleZ',bd+'.color1'+bda)
    cmds.matchTransform('jo_tongueIk'+str(i),x)
	
    if i % 3 == 1 :
     md = cmds.createNode('multiplyDivide',name='mult_tongueScaleRate'+str(i))
     bd = cmds.createNode('blendColors',name='bColor_tongueScale'+str(i))
     cmds.setAttr(md+'.operation',2)
     cmds.connectAttr('ctrl_tongue.FKIK',bd+'.blender')
     mda = 'X' ; bda = 'R'
    elif i % 3 == 2 : mda = 'Y' ; bda = 'G'
    else : mda = 'Z' ; bda = 'B'
    if i > 0 :
     cmds.connectAttr('ctrl_tongueFK'+str(i)+'.tz',md+'.input1'+mda)
     cmds.setAttr(md+'.input2'+mda,cmds.getAttr(x+'.tz'))
     cmds.createNode('addDoubleLinear',name='adl_tongue'+str(i)+'Sz')
     cmds.connectAttr(md+'.output'+mda,'adl_tongue'+str(i)+'Sz.input1')
     cmds.setAttr('adl_tongue'+str(i)+'Sz.input2',1)
     #cmds.connectAttr('adl_tongue'+str(i)+'Sz.output',joList[i-1]+'.scaleZ')
     cmds.connectAttr('adl_tongue'+str(i)+'Sz.output',bd+'.color2'+bda)
     cmds.connectAttr('jo_tongueIk'+str(i-1)+'.scaleZ',bd+'.color1'+bda)
     cmds.connectAttr(bd+'.output'+bda,joList[i-1]+'.scaleZ')

   ikh = cmds.ikHandle(startJoint='jo_tongueIk'+str(0),endEffector='jo_tongueIk'+str(len(joList)-1),sol='ikSplineSolver',createCurve=1,numSpans=2,parentCurve=0)
   cmds.delete(ikh[0])
   cmds.parent(ikh[2],'ctrl_tongue')
   #cmds.makeIdentity(ikh[2],apply=True,translate=1,rotate=0,scale=0)
   self.stripCtrl(ch,'tongueIk','jo_tongueIk'+str(0),'jo_tongueIk'+str(len(joList)-1),ikh[2],'rb_ascJFZ','+z','ctrl_tongue',[0.3,0.1,0.3])
   
   cmds.connectAttr('ctrl_tongue.FKIK','grp_tongueIkCtrl.v')
   cmds.setAttr('jo_tongueIk0.v',0)
   cmds.connectAttr('ctrl_tongue.FKIK',ikh[2]+'.v')
   cmds.setAttr(ikh[2]+'.template',1)
   cmds.createNode('reverse',name='rvs_tongueCtrl')
   cmds.connectAttr('ctrl_tongue.FKIK','rvs_tongueCtrl.inputX')
   cmds.connectAttr('rvs_tongueCtrl.outputX','ctrlTrans_tongueFK0.v')
  #self.tongueLJo = ['jcF90_tongue0L','jcF91_tongue1L','jcF92_tongue2L','jcF93_tongue3L','jcF94_tongue4L','jcF95_tongue5L','jcF96_tongue6L','jcF97_tongue7L','jcF98_tongue8L','jcF99_tongue9L']
   cmds.createNode('transform',name='cons_tongueSide',parent='ctrl_tongue',skipSelect=1)
   #cmds.parentConstraint(joList[0],'cons_tongueSide',maintainOffset=1)
   cmds.pointConstraint(joList[0],'cons_tongueSide')
   cmds.orientConstraint(self.jawJo[0],'cons_tongueSide',maintainOffset=1)
   
   if self.exCheck([self.tongueLJo[1],self.tongueRJo[1]]):
    for i in range(1,len(joList)-1):
     if cmds.objExists(joList[i]):
      cmds.createNode('transform',name='cons_tongueSide'+str(i),parent='ctrl_tongue')
      #cmds.delete(cmds.parentConstraint(joList[i],'cons_tongueSide'+str(i)))
      cmds.createNode('transform',name='v_tongueSide'+str(i),parent='cons_tongueSide')
      cmds.parentConstraint(joList[i],'v_tongueSide'+str(i))
      cmds.connectAttr('v_tongueSide'+str(i)+'.translate','cons_tongueSide'+str(i)+'.translate')
      cmds.connectAttr('v_tongueSide'+str(i)+'.rotate','cons_tongueSide'+str(i)+'.rotate')
      cci = (i+1) * 0.03
      self.ctrlPlay('ctrl_tongueL'+str(i),ch*0.05,ch*0.05,'x',cl,2,[1,1,1,1,1,1,0,0,0,0],[0.17+cci,0+cci,0.17+cci])
      self.ctrlPlay('ctrl_tongueR'+str(i),ch*0.05,ch*0.05,'x',-cl,2,[1,1,1,1,1,1,0,0,0,0],[0.17+cci,0+cci,0.17+cci])
      cmds.parent('ctrlTrans_tongueL'+str(i),'cons_tongueSide'+str(i))
      cmds.parent('ctrlTrans_tongueR'+str(i),'cons_tongueSide'+str(i))
      cmds.matchTransform('ctrlTrans_tongueL'+str(i),self.tongueLJo[i])
      cmds.matchTransform('ctrlTrans_tongueR'+str(i),self.tongueRJo[i])
      cmds.createNode('transform',name='v_tongueL'+str(i),parent='cons_tongueSide'+str(i))
      cmds.createNode('transform',name='v_tongueR'+str(i),parent='cons_tongueSide'+str(i))
      cmds.parentConstraint('ctrl_tongueL'+str(i),'v_tongueL'+str(i))
      cmds.parentConstraint('ctrl_tongueR'+str(i),'v_tongueR'+str(i))
      cmds.connectAttr('v_tongueL'+str(i)+'.translate',self.tongueLJo[i]+'.translate')
      cmds.connectAttr('v_tongueR'+str(i)+'.translate',self.tongueRJo[i]+'.translate')
      cmds.connectAttr('v_tongueL'+str(i)+'.rotate',self.tongueLJo[i]+'.rotate')
      cmds.connectAttr('v_tongueR'+str(i)+'.rotate',self.tongueRJo[i]+'.rotate')
	
# limd Controllers
  self.defineBType()
  if self.anyCheck([self.hipJo[0],self.hipJo[1],self.hip2Jo[0],self.shoulder2Jo[0]]) :
   #cmds.createNode('transform',name='grp_chestCons',parent='ctrl_asset')
   #cmds.parentConstraint(self.chestJo,'grp_chestCons')
   sdc = ['shoulderL','shoulderR'] ; sdc2 = ['shoulder2L','shoulder2R']

   for i in range(2) :
    limbList = [] ; bTypeDict = {}
    print self.L2R([self.pelvisJo,self.hipJo[0],self.kneeJo[0],self.ankleJo[0]],i)
    limbList.append([self.L2R([self.pelvisJo,self.hipJo[0],self.kneeJo[0],self.ankleJo[0]],i),['ctrl_pelvis','cons_limbsFollowPelvis','pelvis','thigh','shank','ankle','leg','knee'],0.0,'legCtrlScale'])
    limbList.append([self.L2R([self.shoulderJo[0],self.armJo[0],self.elbowJo[0],self.wristJo[0]],i),['grp_chestCons','cons_limbsFollowChest','shoulder','upperarm','forearm','wrist','hand','elbow'],0.666,'armCtrlScale'])
    limbList.append([self.L2R([self.pelvisJo,self.hip2Jo[0],self.knee2Jo[0],self.ankle2Jo[0]],i),['ctrl_pelvis','ctrlTrans_torso','pelvis2','thigh2','shank2','ankle2','leg2','knee2'],0.0,'leg2CtrlScale'])
    limbList.append([self.L2R([self.shoulder2Jo[0],self.arm2Jo[0],self.elbow2Jo[0],self.wrist2Jo[0]],i),['grp_chestCons','ctrlTrans_torso','shoulder2','upperarm2','forearm2','wrist2','hand2','elbow2'],0.777,'arm2CtrlScale'])
    #limbList.append([self.L2R([self.rearPelvisJo,self.rearHipJo,self.rearKneeJo,self.rearAnkleJo],i),['ctrl_rearPelvis','ctrlTrans_torso','rearPelvis','rearThigh','rearShank','rearAnkle','rearLeg','rearKnee'],0.888,'rearLegCtrlScale'])
    limbList.append([self.L2R([self.rearPelvisJo,self.rearHipJo,self.rearKneeJo,self.rearAnkleJo],i),['grp_rearPelvisCons','ctrlTrans_torso','rearPelvis','rearThigh','rearShank','rearAnkle','rearLeg','rearKnee'],0.888,'rearLegCtrlScale'])
	

    for x in limbList :
     if self.exCheck(x[0]):
      side = x[0][1][-1]
      dir = self.analyzeAxis(x[0][2])[3]
      bType = ''
      bJo = []
      bCtrl = []
      bEx = []
      bLen = int(0)
      ad = cmds.listRelatives(x[0][3],allDescendents=1,type='joint')
      #for y in bTypeDict[self.L2R(x[0][3],i)] :
      for y in self.bTypeDic[self.L2R(x[0][3],i)] :
       if self.existCompare(y[1],ad) and bLen < len(y[1]) :
        bType = y[0]
        bJo = y[1]
        bCtrl = y[2]
        bLen = 0+len(y[1])
        print bLen
        try : bEx = y[3]
        except : pass
      if cmds.objExists('ctrlParameter.'+x[3]) : cScale = cmds.getAttr('ctrlParameter.'+x[3])
      else : cScale = 1.0
      self.limbCtrl(ch,side,dir,x[0][0],x[0][1],x[0][2],x[0][3],x[1][0],x[1][1],x[1][2],x[1][3],x[1][4],x[1][5],x[1][6],x[1][7],bType,bJo,bCtrl,bEx,x[2],cScale)
      print bType

# if shoulder and viceShoulder at same point they constraint togather
    if cmds.objExists('ctrl_'+sdc2[i]):
     sdc1t = cmds.xform('ctrl_'+sdc[i],q=1,ws=1,t=1) ; sdc2t = cmds.xform('ctrl_'+sdc2[i],q=1,ws=1,t=1)
     if round(sdc1t[0],3) == round(sdc2t[0],3) and round(sdc1t[1],3) == round(sdc2t[1],3) and round(sdc1t[2],3) == round(sdc2t[2],3) :
      cmds.parentConstraint('ctrlTrans_'+sdc[i],'ctrl_'+sdc[i],'ctrlCons_'+sdc2[i],mo=1,name='pCons_'+sdc2[i])
      cmds.addAttr('ctrl_'+sdc2[i],longName='follow',attributeType='double',min=0,max=1,defaultValue=1,keyable=1)
      cmds.connectAttr('ctrl_'+sdc2[i]+'.follow','pCons_'+sdc2[i]+'.ctrl_'+sdc[i]+'W1')
      cmds.createNode('reverse',name='rvs_'+sdc2[i])
      cmds.connectAttr('ctrl_'+sdc2[i]+'.follow','rvs_'+sdc2[i]+'.inputX')
      cmds.connectAttr('rvs_'+sdc2[i]+'.outputX','pCons_'+sdc2[i]+'.ctrlTrans_'+sdc[i]+'W0')
      #if cmds.objExists(sdc2[i]+'.FKIK'):
      # cmds.addAttr(sdc[i],longName='FKIK2',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
      # cmds.connectAttr(sdc[i]+'.FKIK2',sdc2[i]+'.FKIK')
      #if cmds.objExists(sdc2[i]+'.bendCtrl'): cmds.connectAttr(sdc[i]+'.bendCtrl',sdc2[i]+'.bendCtrl')
      #cmds.setAttr(sdc2[i]+'Shape.v',0)

# torso around Controllers
  if self.anyCheck(self.spineFront+self.spineSide):
   cmds.createNode('transform',name='grp_torsoAround',parent='ctrl_asset')
   fjoList = self.spineFront + [self.chestRound[0]] ; sjoList = self.spineSide + [self.chestRound[1]]
   fCtrl = [] ; lCtrl = [] ; rCtrl = []
   for i in range(len(fjoList)) :
    fjo = fjoList[i] ; ljo = sjoList[i] ; rjo = self.L2R(sjoList[i])
    if self.exCheck([fjo,ljo,rjo]) :
     suffix = str(i)
     cmds.createNode('transform',name='cons_around'+str(i),parent='grp_torsoAround')
     if i < len(self.spineFront) : cmds.parentConstraint(self.spineJo[i],'cons_around'+str(i))
     else :
      cmds.parentConstraint(self.chestJo,'cons_around'+str(i))
      suffix = 'Chest'
     h = max(abs(cmds.getAttr(fjo+'.ty')),abs(cmds.getAttr(fjo+'.tz')))
     w = cmds.getAttr(ljo+'.tx')*2
     fCtrlDir = 2
     if abs(cmds.getAttr(fjo+'.ty')) > abs(cmds.getAttr(fjo+'.tz')) : fCtrlDir = 1
     joList = [ljo,fjo,rjo] ; os = [(w*0.2,0,0),(0,w*-.2,0),(w*-.2,0,0)]
     side = ['L','F','R'] ; ctrlW = [w*0.2,h*0.2,w*0.2] ; ctrlH = [h*0.2,w*0.2,h*0.2] ; ctrlD = [0,fCtrlDir,0]
     for j in range(3) :
      self.ctrlSquareRC('ctrl_spine'+suffix+side[j],ctrlW[j],ctrlH[j],ctrlD[j],2,[1,1,1,1,1,1,0,0,0,0],[0.22,0.33,0.2])
      self.ctrlOffset('ctrl_spine'+suffix+side[j],os[j])
      cmds.parent('ctrlTrans_spine'+suffix+side[j],'cons_around'+str(i))
      cmds.matchTransform('ctrlTrans_spine'+suffix+side[j],joList[j])
      cmds.parentConstraint('ctrl_spine'+suffix+side[j],joList[j])
      cmds.scaleConstraint('ctrl_spine'+suffix+side[j],joList[j])
     fCtrl.append('spine'+suffix+'F') ; lCtrl.append('spine'+suffix+'L') ; rCtrl.append('spine'+suffix+'R')

   cmds.addAttr('ctrl_chest',longName='breath',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
   cmds.createNode('multiplyDivide',name='mult_breathChestF')
   cmds.connectAttr('ctrl_chest.breath','mult_breathChestF.input1X')
   cmds.connectAttr('ctrl_chest.breath','mult_breathChestF.input1Y')
   cmds.connectAttr('ctrl_chest.breath','mult_breathChestF.input1Z')
   tyv = cmds.getAttr(self.chestRound[0]+'.ty') * 0.1
   tzv = cmds.getAttr(self.chestRound[0]+'.ty') * -.1
   if ctrlDir == 2 : pass
   cmds.setAttr('mult_breathChestF.input2X',tyv)
   cmds.setAttr('mult_breathChestF.input2Y',tzv)
   cmds.connectAttr('mult_breathChestF.outputX','ctrlCons_spineChestF.translateY')
   cmds.connectAttr('mult_breathChestF.outputY','ctrlCons_spineChestF.translateZ')
   cmds.createNode('multDoubleLinear',name='mdl_breathChestF',skipSelect=1)
   cmds.connectAttr('ctrl_chest.breath','mdl_breathChestF.input1')
   cmds.setAttr('mdl_breathChestF.input2',0.25)
   cmds.createNode('addDoubleLinear',name='adl_breathChestF')
   cmds.connectAttr('mdl_breathChestF.output','adl_breathChestF.input1')
   cmds.setAttr('adl_breathChestF.input2',1)
   cmds.connectAttr('adl_breathChestF.output','ctrlCons_spineChestF.scaleX')
   cmds.createNode('multDoubleLinear',name='mdl_'+fCtrl[-2])
   cmds.connectAttr('ctrl_chest.breath','mdl_'+fCtrl[-2]+'.input1')
   cmds.setAttr('mdl_'+fCtrl[-2]+'.input2',tyv*0.5)
   cmds.connectAttr('mdl_'+fCtrl[-2]+'.output','ctrlCons_'+fCtrl[-2]+'.translateY')
   if len(fCtrl)>4 :
    cmds.addAttr('ctrl_waist',longName='breath',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
    cmds.addAttr('ctrl_abdomen',longName='breath',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
    num = len(fCtrl)-1
    for i in range(1,len(lCtrl)-1) :
     r1 = min((240.0/num*i),180)
     w1 = math.sin(math.radians(r1))
     r2 = max(0,(240.0/num*i-60))
     w2 = math.sin(math.radians(r2))
     if r1 == 180 : w1 = 0
     if r2 == 180 : w2 = 0
     s = ['L','R'] ; mv = [1,-1]
     for j,ctrl in enumerate([lCtrl[i],rCtrl[i]]) :
      ga = cmds.getAttr(self.L2R(self.spineSide[i],j)+'.translate')[0]
      if cmds.objExists('plus_'+ctrl) == 0 :
       cmds.createNode('plusMinusAverage',name='plus_'+ctrl)
       cmds.connectAttr('plus_'+ctrl+'.output3D','ctrlCons_'+ctrl+'.translate')
      if w1 > 0 :
       mult1 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'Abdomen')
       cmds.connectAttr('ctrl_abdomen.breath',mult1+'.input1')
       cmds.setAttr(mult1+'.input2',w1)
       mult2 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'AbdomenTx')
       cmds.connectAttr(mult1+'.output',mult2+'.input1')
       cmds.setAttr(mult2+'.input2',ga[0]*0.2)
       cmds.connectAttr(mult2+'.output','plus_'+ctrl+'.input3D[0].input3Dx')
       mult3 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'AbdomenTy')
       cmds.connectAttr(mult1+'.output',mult3+'.input1')
       cmds.setAttr(mult3+'.input2',ga[1]*0.1*mv[j])
       cmds.connectAttr(mult3+'.output','plus_'+ctrl+'.input3D[0].input3Dy')
      if w2 > 0 :
       mult4 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'waist')
       cmds.connectAttr('ctrl_waist.breath',mult4+'.input1')
       cmds.setAttr(mult4+'.input2',w2)
       mult5 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'waistTx')
       cmds.connectAttr(mult4+'.output',mult5+'.input1')
       cmds.setAttr(mult5+'.input2',ga[0]*0.2)
       cmds.connectAttr(mult5+'.output','plus_'+ctrl+'.input3D[1].input3Dx')
       mult6 = cmds.createNode('multDoubleLinear',name='mdl_'+ctrl+'waistTy')
       cmds.connectAttr(mult4+'.output',mult6+'.input1')
       cmds.setAttr(mult6+'.input2',ga[1]*0.1*mv[j])
       cmds.connectAttr(mult6+'.output','plus_'+ctrl+'.input3D[1].input3Dy')
	
# free and bend at twist Controller
  if self.anyCheck(['upperarmTwistL','wristTwistL','upperarmTwistR','wristTwistR','thighTwistL','kneeTwistL','thighTwistR','kneeTwistR','upperarm2TwistL','upperarm2TwistR']):
   swList = ['ctrl_shoulderL','ctrl_shoulderR','ctrl_pelvisL','ctrl_pelvisR','ctrl_shoulder2L','ctrl_shoulder2R']
   pJo = [(self.armJo[0],self.elbowJo[0]),(self.L2R(self.armJo[0]),self.L2R(self.elbowJo[0])),(self.hipJo[0],self.kneeJo[0]),(self.L2R(self.hipJo[0]),self.L2R(self.kneeJo[0])),(self.arm2Jo[0],self.elbow2Jo[0]),(self.L2R(self.arm2Jo[0]),self.L2R(self.elbow2Jo[0]))]
   twList = [self.armTwist+self.elbowTwist,self.L2R(self.armTwist)+self.L2R(self.elbowTwist),self.hipTwist+self.kneeTwist,self.L2R(self.hipTwist)+self.L2R(self.kneeTwist),self.viceArmTwist+self.viceElbowTwist,self.L2R(self.viceArmTwist)+self.L2R(self.viceElbowTwist)]
   midCtrl = ['freeElbowL','freeElbowR','freeKneeL','freeKneeR','freeViceElbowL','freeViceElbowR']
   midJo = [self.elbowJo[0],self.L2R(self.elbowJo[0]),self.kneeJo[0],self.L2R(self.kneeJo[0]),self.elbow2Jo[0],self.L2R(self.elbow2Jo[0])]
   tailJo = [self.wristJo[0],self.L2R(self.wristJo[0]),self.ankleJo[0],self.L2R(self.ankleJo[0]),self.wrist2Jo[0],self.L2R(self.wrist2Jo[0])]
   consN = [('upperarmTwistL','wristTwistL'),('upperarmTwistR','wristTwistR'),('thighTwistL','ankleTwistL'),('thighTwistR','ankleTwistR'),('upperarm2TwistL','wrist2TwistL'),('upperarm2TwistR','wrist2TwistR')]
   bendCtrl = [('bendArmL','bendforearmL'),('bendArmR','bendforearmR'),('bendThighL','bendShinkL'),('bendThighR','bendShinkR'),('viceBendArmL','viceBendforearmL'),('viceBendArmR','viceBendforearmR')]
   cColor = [0.66666,0.66666,0,0,0.77777,0.77777]
   for i,x in enumerate(twList) :
    print i
    if self.exCheck(x):
     cmds.addAttr(swList[i],longName='bendCtrl',attributeType='bool',defaultValue=0,keyable=1)
     cmds.setAttr(swList[i]+'.bendCtrl',keyable=0,channelBox=1)
     ad1 = [1,0,0] ; ad2 = [-1,0,0] # aim direction
     axis = 'X'
     if abs(cmds.getAttr(midJo[i]+'.ty')) > abs(cmds.getAttr(midJo[i]+'.tx')) : 
      axis = 'Y' ; ad1 = [0,1,0] ; ad2 = [0,-1,0]
      if cmds.getAttr(midJo[i]+'.ty') < 0 : ad1 = [0,-1,0] ; ad2 = [0,1,0]
     elif cmds.getAttr(midJo[i]+'.tx') < 0 : ad1 = [-1,0,0] ; ad2 = [1,0,0]

     self.ctrlLocator('ctrl_'+midCtrl[i],ch*1,1,[1,1,1,0,0,0,0,0,0,0],self.colour(cColor[i],2))
     cmds.parent('ctrlTrans_'+midCtrl[i],swList[i],relative=1)
     cmds.pointConstraint(midJo[i],'ctrlTrans_'+midCtrl[i])
     cmds.orientConstraint(pJo[i][0],'ctrlTrans_'+midCtrl[i])
     cmds.connectAttr(swList[i]+'.bendCtrl','ctrlTrans_'+midCtrl[i]+'.v')

     ad = [ad1,ad2]
     for j in [0,1] :
      trans = cmds.createNode('transform',name='trans_'+consN[i][j]+'Ctrl',parent=swList[i])
      aCons = cmds.createNode('transform',name='aCons_'+consN[i][j]+'Ctrl',parent=trans)
      sCons = cmds.createNode('transform',name='sCons_'+consN[i][j]+'Ctrl',parent=aCons)
      if j == 0 : cmds.pointConstraint(pJo[i][j],trans)
      if j == 1 : cmds.parentConstraint(pJo[i][j],trans)
      lenCons = cmds.createNode('transform',name='len_'+consN[i][j]+'Ctrl',parent=aCons)
      if j == 1 :
      #cmds.matchTransform(aCons,tailJo[i],position=1)
       cmds.pointConstraint(tailJo[i],aCons)
       cmds.matchTransform(sCons,midJo[i])
       cmds.matchTransform(sCons,tailJo[i],pivots=1)
      cmds.aimConstraint('ctrl_'+midCtrl[i],aCons,aimVector=ad[j],upVector=[0,1,0],worldUpType='none')
      cmds.pointConstraint('ctrl_'+midCtrl[i],lenCons)
      dvd = cmds.createNode('multiplyDivide',name='dvd_'+midCtrl[i])
      cmds.setAttr(dvd+'.operation',2)
      cmds.connectAttr(lenCons+'.translate'+axis,dvd+'.input1X')
      cmds.setAttr(dvd+'.input2X',cmds.getAttr(lenCons+'.translate'+axis))
      cmds.connectAttr(dvd+'.outputX',sCons+'.scale'+axis)
      cmds.connectAttr(swList[i]+'.bendCtrl',trans+'.v')
	 
      self.ctrlLocator('ctrl_'+bendCtrl[i][j],ch*1,0,[1,1,1,0,0,0,1,1,1,0],self.colour(cColor[i],2)) # create one of bend ctrl
      cmds.addAttr('ctrl_'+bendCtrl[i][j],longName='autoTwist',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
	
      twJo = x[0+j*5:5+j*5] ; po = []
      for k,z in enumerate(twJo) :
       pc = cmds.createNode('transform',name='pinCons_'+z[3:],parent=sCons,skipSelect=1)
       p = cmds.listRelatives(z,parent=1)[0]
       cmds.connectAttr(p+'.translate',pc+'.translate')
       cmds.createNode('multiplyDivide',name='mult_'+z[3:]+'Off')
       cmds.connectAttr(p+'.rotate','mult_'+z[3:]+'Off.input1') # auto twist switch function
       cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.autoTwist','mult_'+z[3:]+'Off.input2X')
       cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.autoTwist','mult_'+z[3:]+'Off.input2Y')
       cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.autoTwist','mult_'+z[3:]+'Off.input2Z')
       cmds.connectAttr('mult_'+z[3:]+'Off.outputX',pc+'.rotateX')
       cmds.connectAttr('mult_'+z[3:]+'Off.outputY',pc+'.rotateY')
       cmds.connectAttr('mult_'+z[3:]+'Off.outputZ',pc+'.rotateZ')
       cmds.disconnectAttr('mult_'+z[3:]+'Off.output'+axis,pc+'.rotate'+axis) # turn to connect ctrl rotate to twist value
       cmds.createNode('addDoubleLinear',name='adl_'+z[3:],skipSelect=1)
       cmds.createNode('multDoubleLinear',name='mdl_'+z[3:]+'Ramp',skipSelect=1)
       cmds.connectAttr('mult_'+z[3:]+'Off.output'+axis,'adl_'+z[3:]+'.input1')
       cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.rotate'+axis,'mdl_'+z[3:]+'Ramp.input1')
       cmds.setAttr('mdl_'+z[3:]+'Ramp.input2',k*0.25)
       cmds.connectAttr('mdl_'+z[3:]+'Ramp.output','adl_'+z[3:]+'.input2')
       cmds.connectAttr('adl_'+z[3:]+'.output',pc+'.rotate'+axis) # pin constraint back to twist joint
       pin = cmds.createNode('transform',name='pin_'+z[3:],parent=pc,skipSelect=1)
       po += [pin]
       cmds.parentConstraint(pin,z)
       cmds.scaleConstraint(pin,z)
	  
      #self.ctrlLocator('ctrl_'+bendCtrl[i][j],ch*1,0,[1,1,1,0,0,0,1,1,1,0],[0.2,0.2,0.15]) # move to upper
      cmds.setAttr('ctrl_'+bendCtrl[i][j]+'.rotate'+axis,channelBox=1,lock=0)
      cmds.setAttr('ctrl_'+bendCtrl[i][j]+'.rotate'+axis,keyable=1)
      cmds.setAttr('ctrl_'+bendCtrl[i][j]+'.scale'+axis,lock=1,keyable=0,channelBox=0)
      cmds.parent('ctrl_'+bendCtrl[i][j],cmds.listRelatives(po[2],parent=1)[0],relative=1)
      #for z in twJo : cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.scale',z+'.scale')
      for z in po : cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.scale',z+'.scale')
      cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.translate',po[2]+'.translate')
      mult = cmds.createNode('multiplyDivide',name='mult_'+bendCtrl[i][j],skipSelect=1)
      cmds.connectAttr('ctrl_'+bendCtrl[i][j]+'.translate',mult+'.input1')
      cmds.setAttr(mult+'.input2',0.7,0.7,0.7,type='double3')
      cmds.connectAttr(mult+'.output',po[1]+'.translate')
      cmds.connectAttr(mult+'.output',po[3]+'.translate')
      cmds.aimConstraint(po[1],po[0],aimVector=ad1,upVector=[0,1,0],worldUpType='none')
      cmds.aimConstraint(po[2],po[1],aimVector=ad1,upVector=[0,1,0],worldUpType='none')
      cmds.aimConstraint(po[2],po[3],aimVector=ad2,upVector=[0,1,0],worldUpType='none')
      cmds.aimConstraint(po[3],po[4],aimVector=ad2,upVector=[0,1,0],worldUpType='none')

     cmds.connectAttr('exp_'+consN[i][1]+'.rotate',sCons+'.rotate')
     cmds.addAttr(swList[i],longName='twistValue',attributeType='double',keyable=1)
     cmds.setAttr(swList[i]+'.twistValue',keyable=0,channelBox=1)
     cmds.connectAttr(consN[i][0]+'.rotate'+axis,swList[i]+'.twistValue')
	
# Hair Controller
  if self.anyCheck(['crv_frontHair1','crv_leftHair1','crv_rightHair1','crv_leftburns1','crv_rightburns1','crv_topHair1','crv_backHair1','crv_bottomHair1']):
   hPart = ['frontHair','leftHair','rightHair','leftburns','rightburns','topHair','backHair','bottomHair']
   self.consCheck('head')
   cmds.createNode('transform',name='cons_hairCtrl',parent='ctrl_head',skipSelect=1)
   cmds.parentConstraint(self.headJo,'cons_hairCtrl')
   for hp in hPart:
    cnList = ['crv_'+hp+str(0),'crv_'+hp+str(1),'crv_'+hp+str(2),'crv_'+hp+str(3)]
    if self.anyCheck(cnList):
     hairNum = 0
     for i in range(1,100):
      cn = 'crv_'+hp+str(i)
      if cmds.objExists(cn):
       hairNum = hairNum + 1
       sp = cmds.listRelatives(cn,shapes=1)[0]
       cvn = cmds.getAttr(sp+'.spans')+cmds.getAttr(sp+'.degree')
       #len = cmds.arclen(cn)
       #if (len/cvn) > 3 : pass
       cGrp = cmds.createNode('transform',name='grp_'+hp+str(i)+'Ctrl',parent='cons_hairCtrl',skipSelect=1)
       cmds.createNode('transform',name='pin_'+cn[4:]+'0',parent=cGrp,skipSelect=1)
       cmds.xform('pin_'+cn[4:]+'0',ws=1,t=cmds.xform(sp+'.cv[0]',q=1,worldSpace=1,t=1))
       colorH = 0.444 + (((i%5)-2)*0.03) ; colorL = 2-(1-(i%2))
       self.ctrlSquare('ctrl_'+cn[4:],ch*0.1,ch*0.1,ch*0.1,2,[1,1,1,0,0,0,0,0,0,0],self.colour(colorH,colorL))
       cmds.parent('ctrlTrans_'+cn[4:],cGrp)
       cmds.xform('ctrlTrans_'+cn[4:],ws=1,t=cmds.xform(sp+'.cv['+str(cvn-1)+']',q=1,worldSpace=1,t=1))
       for j in range(1,cvn):
        ctrl = 'ctrl_'+cn[4:]+str(j) ; ctrlT = 'ctrlTrans_'+cn[4:]+str(j)
        self.ctrlLocator(ctrl,ch*0.1,2,[1,1,1,0,0,0,0,0,0,0],self.colour(colorH,colorL))
        cmds.parent(ctrlT,cGrp)
        cmds.xform(ctrlT,ws=1,t=cmds.xform(sp+'.cv['+str(j)+']',q=1,worldSpace=1,t=1))
        cmds.createNode('transform',name='v_'+cn[4:]+str(j),parent=cGrp,skipSelect=1)
        cmds.pointConstraint(ctrl,'v_'+cn[4:]+str(j))
        cmds.connectAttr('v_'+cn[4:]+str(j)+'.translate',sp+'.controlPoints['+str(j)+']')
        cmds.createNode('transform',name='pv_'+cn[4:]+str(j),parent=ctrl,skipSelect=1)
        consSource = 'ctrl_'+cn[4:]+str(j-1)
        if j == 1 : consSource = 'pin_'+cn[4:]+'0'
        cmds.pointConstraint(consSource,'pv_'+cn[4:]+str(j))
        cmds.connectAttr('pv_'+cn[4:]+str(j)+'.translate',ctrl+'Shape.controlPoints[9]')
        # cmds.addAttr(ctrl,longName='stretchable',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
        # for k in range(1,(cvn-1)):
        # cmds.addAttr(ctrl,longName='ctrl'+str(k)+'follow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
	
# MT4 wing specific rig
  if self.exCheck([self.arm2Wing1Jo[0],self.arm2Wing2Jo[0],self.arm2Wing3Jo[0],self.arm2Wing4Jo[0]]) :
   sd = ['L','R']
   for j,s in enumerate(sd) :
    cmds.createNode('transform',name='grp_arm2Wing'+s+'Ctrl',parent='ctrl_shoulder2'+s)
    cmds.parentConstraint(self.arm2Jo[j],'grp_arm2Wing'+s+'Ctrl')
    self.ctrlSphere('ctrl_armWingUni'+s,ch*0.5,1,[0,0,0,1,1,1,0,0,0,0],[0.2,0.4,0.3])
    cmds.parent('ctrlTrans_armWingUni'+s,'grp_arm2Wing'+s+'Ctrl',relative=1)
    ga = cmds.getAttr(self.elbow2Jo[j]+'.translateX')
    cmds.move(ga*0.5,ga*0.5,0,'ctrlTrans_armWingUni'+s,relative=True, objectSpace=True)
    cmds.setAttr('ctrlTrans_armWingUni'+s+'.rotateY',-90)
    aj = self.arm2Wing1Jo[:3] + self.arm2Wing2Jo[:3] + self.arm2Wing3Jo[:3] + self.arm2Wing4Jo[:3]
    if s == 'R' : aj = self.L2R(self.arm2Wing1Jo[:3]) + self.L2R(self.arm2Wing2Jo[:3]) + self.L2R(self.arm2Wing3Jo[:3]) + self.L2R(self.arm2Wing4Jo[:3])
    for i,x in enumerate(aj) :
     cs = (ch*0.5)+(i*1) ; lenM = 2
     if s == 'R' : lenM = -2
     self.ctrlFingerY('ctrl_armWing2'+str(i)+s,cs,cs*lenM,2,[0,0,0,1,1,1,0,0,0,0],[0.2,0.4,0.3])
     cmds.matchTransform('ctrlTrans_armWing2'+str(i)+s,x)
     if i in [0,3,6,9] :
      cmds.parent('ctrlTrans_armWing2'+str(i)+s,'grp_arm2Wing'+s+'Ctrl')
      m = cmds.createNode('multiplyDivide')
      cmds.connectAttr('ctrl_armWingUni'+s+'.rotate',m+'.input1')
      v = ((float(i)/3)+1)/4
      cmds.setAttr(m+'.input2X',v)
      cmds.setAttr(m+'.input2Y',v)
      cmds.setAttr(m+'.input2Z',v)
      cmds.connectAttr(m+'.output','ctrlCons_armWing2'+str(i)+s+'.rotate')
     else : cmds.parent('ctrlTrans_armWing2'+str(i)+s,'ctrl_armWing2'+str(i-1)+s)
     cmds.parentConstraint('ctrl_armWing2'+str(i)+s,x)

# bashira specific rig
  if cmds.objExists(self.jawJo[0]+'.split') :
   cmds.addAttr('ctrl_jaw',longName='splite',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   cmds.connectAttr('ctrl_jaw.splite',self.jawJo[0]+'.split')
  if cmds.objExists('ctrlParameter.legFollowEnable') :
   cmds.setAttr('ctrl_legL.follow',1)
   cmds.setAttr('ctrl_legR.follow',1)
	 
  cmds.setAttr('grp_deformer.v',0)
  sys.stderr.write('Create ctrl done.')

 def spineCtrl(self,ch,ctrlName,ctrlDir,pCtrl,joNum,spineJo,tailJo,*a): # ch = character height
# ctrlName=['pelvis','abdomen','waist','chest'], pCtrl='ctrl_torso', spineJo=self.spineJo, tailJo=self.chestJo
  ctrlSize = [2.25,0.2,2] ; cs = 1
  axis = self.analyzeAxis(spineJo[1])
  if ctrlDir == 2 : temp = ctrlSize[1] ; ctrlSize[1] = ctrlSize[2] ; ctrlSize[2] = temp
  self.ctrlHexagon('ctrl_'+ctrlName[3],ch*1.75*cs,ch*.3*cs,ch*1.5*cs,'z',2,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))
  cmds.addAttr('ctrl_'+ctrlName[3],longName='stretchable',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
  cmds.matchTransform('ctrlTrans_'+ctrlName[3],tailJo)
  cmds.setAttr('ctrl_'+ctrlName[0]+'.translateX',lock=0,keyable=1)
  cmds.setAttr('ctrl_'+ctrlName[0]+'.translateY',lock=0,keyable=1)
  cmds.setAttr('ctrl_'+ctrlName[0]+'.translateZ',lock=0,keyable=1)
  
  self.ctrlSquare('ctrl_'+ctrlName[1],ch*ctrlSize[0],ch*ctrlSize[1],ch*ctrlSize[2],2,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))
  self.ctrlSquare('ctrl_'+ctrlName[2],ch*ctrlSize[0],ch*ctrlSize[1],ch*ctrlSize[2],2,[1,1,1,1,1,1,0,0,0,0],self.colour(0.333,1))
  div = float(joNum)/3
  pCons1 = cmds.pointConstraint(spineJo[int(div)],spineJo[int(div)+1],'ctrlTrans_'+ctrlName[1])
  cmds.setAttr(pCons1[0]+'.'+spineJo[int(div)]+'W0',1-(div%1))
  cmds.setAttr(pCons1[0]+'.'+spineJo[int(div)+1]+'W1',(div%1))
  pCons2 = cmds.pointConstraint(spineJo[int(div*2)],spineJo[int(div*2)+1],'ctrlTrans_'+ctrlName[2])
  cmds.setAttr(pCons2[0]+'.'+spineJo[int(div*2)]+'W0',1-((div*2)%1))
  cmds.setAttr(pCons2[0]+'.'+spineJo[int(div*2)+1]+'W1',((div*2)%1))
  cmds.delete(pCons1,pCons2)
  cmds.parent('ctrlTrans_'+ctrlName[1],pCtrl)
  cmds.parent('ctrlTrans_'+ctrlName[2],pCtrl)
  cmds.parent('ctrlTrans_'+ctrlName[3],pCtrl)
  cmds.orientConstraint('ctrl_'+ctrlName[3],tailJo)
  
  cmds.createNode('transform',name='v_'+ctrlName[3]+'Pos',parent='ctrlTrans_'+ctrlName[3])
  cmds.pointConstraint('ctrl_'+ctrlName[3],'v_'+ctrlName[3]+'Pos')
  cmds.orientConstraint('ctrl_'+ctrlName[3],'v_'+ctrlName[3]+'Pos')
  cmds.createNode('wtAddMatrix',name='xAdd_'+ctrlName[1]+'Cons')
  cmds.createNode('wtAddMatrix',name='xAdd_'+ctrlName[2]+'Cons')
  #cmds.connectAttr(pCtrl+'.matrix','xAdd_'+ctrlName[1]+'Cons.wtMatrix[0].matrixIn')
  #cmds.connectAttr(pCtrl+'.matrix','xAdd_'+ctrlName[2]+'Cons.wtMatrix[0].matrixIn')
  cmds.connectAttr('ctrl_'+ctrlName[0]+'.matrix','xAdd_'+ctrlName[1]+'Cons.wtMatrix[0].matrixIn')
  cmds.connectAttr('ctrl_'+ctrlName[0]+'.matrix','xAdd_'+ctrlName[2]+'Cons.wtMatrix[0].matrixIn')
  cmds.connectAttr('v_'+ctrlName[3]+'Pos.matrix','xAdd_'+ctrlName[1]+'Cons.wtMatrix[1].matrixIn')
  cmds.connectAttr('v_'+ctrlName[3]+'Pos.matrix','xAdd_'+ctrlName[2]+'Cons.wtMatrix[1].matrixIn')
  cmds.setAttr('xAdd_'+ctrlName[1]+'Cons.wtMatrix[0].weightIn',1.0/3*2)
  cmds.setAttr('xAdd_'+ctrlName[1]+'Cons.wtMatrix[1].weightIn',1.0/3)
  cmds.setAttr('xAdd_'+ctrlName[2]+'Cons.wtMatrix[0].weightIn',1.0/3)
  cmds.setAttr('xAdd_'+ctrlName[2]+'Cons.wtMatrix[1].weightIn',1.0/3*2)
  cmds.createNode('decomposeMatrix',name='xCons_'+ctrlName[1]+'Cons')
  cmds.createNode('decomposeMatrix',name='xCons_'+ctrlName[2]+'Cons')
  cmds.connectAttr('xAdd_'+ctrlName[1]+'Cons.matrixSum','xCons_'+ctrlName[1]+'Cons.inputMatrix')
  cmds.connectAttr('xAdd_'+ctrlName[2]+'Cons.matrixSum','xCons_'+ctrlName[2]+'Cons.inputMatrix')
  cmds.connectAttr('xCons_'+ctrlName[1]+'Cons.outputTranslate','ctrlCons_'+ctrlName[1]+'.translate')
  cmds.connectAttr('xCons_'+ctrlName[1]+'Cons.outputRotateZ','ctrlCons_'+ctrlName[1]+'.rotateZ')
  cmds.connectAttr('xCons_'+ctrlName[2]+'Cons.outputTranslate','ctrlCons_'+ctrlName[2]+'.translate')
  cmds.connectAttr('xCons_'+ctrlName[2]+'Cons.outputRotateZ','ctrlCons_'+ctrlName[2]+'.rotateZ')
  
  pPos = []
  for x in ctrlName :
   cmds.createNode('transform',name='v_'+x+'Ctrl',parent=pCtrl,skipSelect=1)
   cmds.pointConstraint('ctrl_'+x,'v_'+x+'Ctrl')
   pPos.append(cmds.xform('ctrl_'+x,q=1,ws=1,t=1))
  cCrv = 'crv_'+ctrlName[3]+'Ctrl'
  cmds.curve(d=3,p=pPos,k=[0,0,0,1,1,1],name=cCrv)
  sp = cmds.listRelatives(cCrv,shapes=1)[0]
  cmds.rename(sp,cCrv+'Shape') ; cmds.setAttr(cCrv+'.v',0)
  cmds.parent(cCrv,pCtrl) ; cmds.makeIdentity(cCrv,apply=1,t=1,r=1,pn=1)
  for i,x in enumerate(ctrlName) : cmds.connectAttr('v_'+x+'Ctrl.translate',cCrv+'Shape.controlPoints['+str(i)+']')

  joPos = []
  for i in range(joNum) : joPos.append(cmds.xform(spineJo[i],q=1,ws=1,t=1))
  joPos.append(cmds.xform(tailJo,q=1,ws=1,t=1))
  crv = 'crv_'+ctrlName[3]
  cmds.curve(ep=joPos,name=crv)
  sp = cmds.listRelatives(crv,shapes=1)[0]
  cmds.rename(sp,crv+'Shape') ; cmds.parent(crv,pCtrl) ; cmds.setAttr(crv+'.v',0)  
  cmds.wire(crv,w=cCrv,dropoffDistance=[0,100])
  rCrv = cmds.rebuildCurve(crv,name=crv+'Re',constructionHistory=1,rpo=0,rt=0,end=1,keepRange=0,kcp=0,kep=1,kt=0,spans=20,d=3,tol=0.01)
  cmds.setAttr(crv+'Re.v',0)
  #cmds.setAttr('crv_spineRe.inheritsTransform',0)
  cmds.parent(crv+'Re',pCtrl)
  dCrv = cmds.createNode('detachCurve',name='dCrv_'+ctrlName[3],skipSelect=1)
  cmds.connectAttr(rCrv[1]+'.outputCurve',dCrv+'.inputCurve')
  ci = cmds.createNode('curveInfo',name='crvInfo_'+ctrlName[3],skipSelect=1)
  cmds.connectAttr(rCrv[1]+'.outputCurve',ci+'.inputCurve')
  dvd = cmds.createNode('multiplyDivide',name='dvd_'+ctrlName[3],skipSelect=1)
  cmds.connectAttr(ci+'.arcLength',dvd+'.input2X')
  cmds.setAttr(dvd+'.input1X',cmds.getAttr(ci+'.arcLength'))
  cmds.setAttr(dvd+'.operation',2)
  b2a = cmds.createNode('blendTwoAttr',name='b2a_'+ctrlName[3])
  cmds.connectAttr('ctrl_'+ctrlName[3]+'.stretchable',b2a+'.attributesBlender')
  cmds.setAttr(b2a+'.input[1]',1)
  cmds.connectAttr(dvd+'.outputX',b2a+'.input[0]')
  cd = cmds.createNode('condition',name='cd_'+ctrlName[3],skipSelect=1)
  cmds.setAttr(cd+'.operation',3)
  cmds.connectAttr(b2a+'.output',cd+'.firstTerm')
  cmds.connectAttr(b2a+'.output',cd+'.colorIfFalseR')
  cmds.setAttr(cd+'.secondTerm',1)
  cmds.setAttr(cd+'.colorIfTrueR',1)
  cmds.connectAttr(cd+'.outColorR',dCrv+'.parameter[0]')
  cmds.connectAttr(dCrv+'.outputCurve[0]',crv+'ReShape.create',f=1)

  for i in range(0,joNum+1) :
   vn = cmds.createNode('transform',name='pos_'+ctrlName[3]+str(i),parent='ctrl_torso',skipSelect=1)
   poc = cmds.createNode('pointOnCurveInfo',name='poc_'+ctrlName[3]+str(i),skipSelect=1)
   cmds.connectAttr(crv+'ReShape.worldSpace[0]',poc+'.inputCurve')
   cmds.setAttr(poc+'.parameter',1.0/joNum*i)
   cmds.setAttr(poc+'.turnOnPercentage',1)
   cmds.connectAttr(poc+'.position',vn+'.translate')
   cmds.setAttr(vn+'.inheritsTransform',0)
   quotient = int(( 3.0 / joNum * i )//1)
   remainder = ( 3.0 / joNum * i ) % 1
   if remainder == 0 :
    oCons = cmds.orientConstraint('ctrl_'+ctrlName[quotient],vn)
   else :
    oCons = cmds.orientConstraint('ctrl_'+ctrlName[quotient],'ctrl_'+ctrlName[quotient+1],vn)
    cmds.setAttr(oCons[0]+'.ctrl_'+ctrlName[quotient]+'W0',1-remainder)
    cmds.setAttr(oCons[0]+'.ctrl_'+ctrlName[quotient+1]+'W1',remainder)
   cmds.setAttr(oCons[0]+'.interpType',2)
   cmds.createNode('transform',name='aim_'+ctrlName[3]+str(i),parent=vn,skipSelect=1)
   if i > 0 : cmds.aimConstraint(vn,'aim_'+ctrlName[3]+str(i-1),aimVector=axis[1],upVector=[0,1,0],worldUpType='none')
   cmds.createNode('transform',name='pin_'+ctrlName[3]+str(i),parent='aim_'+ctrlName[3]+str(i),skipSelect=1)

  for i in range(joNum+1) :
   pJo = spineJo[i]
   if i == joNum : pJo = tailJo
   cmds.matchTransform('pin_'+ctrlName[3]+str(i),pJo)
   if i < joNum : cmds.orientConstraint('pin_'+ctrlName[3]+str(i),pJo)
   cmds.pointConstraint('pin_'+ctrlName[3]+str(i),pJo)
  
 def defineBType(self,*a):
  self.bTypeDic = {}
  for i in range(2) :
   self.bTypeDic[self.L2R(self.wristJo[0],i)] = [['finger'],['palm'],['wing']]
   self.bTypeDic[self.L2R(self.wristJo[0],i)][0].append(self.L2R([self.thumbJo[0],self.thumbJo[1],self.thumbJo[2],self.indexJo[0],self.indexJo[1],self.indexJo[2],self.indexJo[3],self.middleJo[0],self.middleJo[1],self.middleJo[2],self.middleJo[3],self.ringJo[0],self.ringJo[1],self.ringJo[2],self.ringJo[3],self.littleJo[0],self.littleJo[1],self.littleJo[2],self.littleJo[3],self.indexJo[4],self.middleJo[4],self.ringJo[4],self.littleJo[4]],i))
   self.bTypeDic[self.L2R(self.wristJo[0],i)][0].append(['finger','thumb0','thumb1','thumb2','index0','index1','index2','index3','middle0','middle1','middle2','middle3','ring0','ring1','ring2','ring3','little0','little1','little2','little3'])
   self.bTypeDic[self.L2R(self.wristJo[0],i)][1].append(self.L2R([self.thumbJo[0],self.thumbJo[1],self.thumbJo[2],self.thumbJo[3],self.indexJo[1],self.indexJo[2],self.indexJo[3],self.indexJo[4],self.middleJo[1],self.middleJo[2],self.middleJo[3],self.middleJo[4],self.ringJo[1],self.ringJo[2],self.ringJo[3],self.ringJo[4],self.littleJo[1],self.littleJo[2],self.littleJo[3],self.littleJo[4]],i))
   self.bTypeDic[self.L2R(self.wristJo[0],i)][1].append(['plam','thumb0','thumb1','thumb2','thumbClaw','index1','index2','index3','indexClaw','middle1','middle2','middle3','middleClaw','ring1','ring2','ring3','ringClaw','little1','little2','little3','littleClaw'])
   self.bTypeDic[self.L2R(self.wristJo[0],i)][2].append(self.L2R(self.thumbJo[0],self.thumbJo[1],self.indexJo[0],self.indexJo[1],self.indexJo[2],self.indexJo[3],i))
   self.bTypeDic[self.L2R(self.wristJo[0],i)][2].append(['finger','thumb','digit1','digit2'])
   
   self.bTypeDic[self.L2R(self.ankleJo[0],i)] = [['shoe'],['toe'],['paw'],['web'],['hoof']]
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][0].append(self.L2R([self.ballJo[0],self.toeJo[0]],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][0].append(['heel','toe'])
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][0].append(self.L2R(['grp_legRotatePivotL','pv_tipToeL','pv_tipHeelL'],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][1].append(self.L2R([self.bigToeJo[0],self.bigToeJo[1],self.bigToeJo[2],self.bigToeJo[3],self.indexToeJo[0],self.indexToeJo[1],self.indexToeJo[2],self.indexToeJo[3],self.indexToeJo[4],self.middleToeJo[0],self.middleToeJo[1],self.middleToeJo[2],self.middleToeJo[3],self.middleToeJo[4],self.fourthToeJo[0],self.fourthToeJo[1],self.fourthToeJo[2],self.fourthToeJo[3],self.fourthToeJo[4],self.littleToeJo[0],self.littleToeJo[1],self.littleToeJo[2],self.littleToeJo[3],self.littleToeJo[4]],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][1].append(['heel','toe','bigToe','indexToe','middleToe','fourthToe','littleToe'])
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][2].append(self.L2R([self.indexToeJo[1],self.indexToeJo[2],self.indexToeJo[3],self.indexToeJo[4],self.middleToeJo[1],self.middleToeJo[2],self.middleToeJo[3],self.middleToeJo[4],self.fourthToeJo[1],self.fourthToeJo[2],self.fourthToeJo[3],self.fourthToeJo[4],self.littleToeJo[1],self.littleToeJo[2],self.littleToeJo[3],self.littleToeJo[4]],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][2].append(['heel','indexToe1','indexToe2','indexToe3','indexToe4','middleToe1','middleToe2','middleToe3','middleToe4','fourthToe1','fourthToe2','fourthToe3','fourthToe4','littleToe1','littleToe2','littleToe3','littleToe4'])
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][3].append(self.L2R([self.indexToeJo[1],self.indexToeJo[2],self.indexToeJo[3],self.indexToeJo[4],self.middleToeJo[1],self.middleToeJo[2],self.middleToeJo[3],self.middleToeJo[4],self.fourthToeJo[1],self.fourthToeJo[2],self.fourthToeJo[3],self.fourthToeJo[4]],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][3].append(['heel','web','indexToe','middleToe','littleToe'])
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][4].append(self.L2R([self.ballJo[0],self.toeJo[0],self.bHoofJo],i))
   self.bTypeDic[self.L2R(self.ankleJo[0],i)][4].append(['ball','toe','backHoof'])
   
   self.bTypeDic[self.L2R(self.wrist2Jo[0],i)] = [['finger']]
   self.bTypeDic[self.L2R(self.wrist2Jo[0],i)][0].append(self.L2R([self.thumb2Jo[0],self.thumb2Jo[1],self.thumb2Jo[2],self.index2Jo[0],self.index2Jo[1],self.index2Jo[2],self.index2Jo[3],self.middle2Jo[0],self.middle2Jo[1],self.middle2Jo[2],self.middle2Jo[3],self.ring2Jo[0],self.ring2Jo[1],self.ring2Jo[2],self.ring2Jo[3],self.little2Jo[0],self.little2Jo[1],self.little2Jo[2],self.little2Jo[3],self.index2Jo[4],self.middle2Jo[4],self.ring2Jo[4],self.little2Jo[4]],i))
   self.bTypeDic[self.L2R(self.wrist2Jo[0],i)][0].append(['finger2','thumb20','thumb21','thumb22','index20','index21','index22','index23','middle20','middle21','middle22','middle23','ring20','ring21','ring22','ring23','little20','little21','little22','little23'])
   self.bTypeDic[self.L2R(self.rearAnkleJo,i)] = [['hoof']]
   self.bTypeDic[self.L2R(self.rearAnkleJo,i)][0].append(self.L2R([self.rearBallJo,self.rearToeJo,self.rearHoofJo],i))
   self.bTypeDic[self.L2R(self.rearAnkleJo,i)][0].append(['rearBall','rearToe','rearHoof'])

# Limb ctrl Process Module
 def limbCtrl(self,ch,side,dir,pJo,sJo,mJo,eJo,pCtrl,fk0Ctrl,fCtrl,sCtrl,mCtrl,eCtrl,ikCtrl,pvCtrl,bType,bJo,bCtrl,bEx,color,cScale,*a): # ch = character height
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  #cr = colorsys.hsv_to_rgb(color,0.5,0.5) ; colorM = [cr[0],cr[1],cr[2]]
  #cr = colorsys.hsv_to_rgb(color+0.02,0.6,0.4) ; colorFK = [cr[0],cr[1],cr[2]]
  #cr = colorsys.hsv_to_rgb(color-0.01,0.6,0.4) ; colorIK = [cr[0],cr[1],cr[2]]
  #cr = colorsys.hsv_to_rgb(color-0.02,0.8,0.05) ; colorEx = [cr[0],cr[1],cr[2]]
  ch = ch * cScale
  #x180 = 1

  ctrlStartAngle = 0 ; ctrlOffsetDir = 1 ; ctrlRadius = 1.0 ; sweepAngel = 40
  fCtrlAxis = 1 ; fCtrlOffset = [0,cmds.getAttr(pJo+'.ty')*ctrlOffsetDir,0]
  if side == 'R' : ctrlStartAngle = 180 ; ctrlOffsetDir = -1
  if self.joBelong(pJo) in ['L','R'] :
   fCtrlAxis = 0 ; ctrlRadius = 0.6 ; sweepAngel = 60
   fCtrlOffset = [cmds.getAttr(sJo+'.tx'),0,cmds.getAttr(sJo+'.tz')]

# first,previous Ctrl create : pelvis or shoulder
  if fCtrl == 'shoulder2' : ctrlStartAngle = ctrlStartAngle - 60 # temp : BSK special 
  self.ctrlArc(ch*ctrlRadius,ch*0.2,ctrlStartAngle,sweepAngel,ch*0.3,fCtrlAxis,'ctrl_'+fCtrl+side,2,[1,1,1,1,1,1,0,0,0,0],self.colour(color,0))
  self.ctrlOffset('ctrl_'+fCtrl+side,fCtrlOffset)
  cmds.parent('ctrlTrans_'+fCtrl+side,pCtrl,relative=1)
  cmds.xform('ctrlTrans_'+fCtrl+side,t=cmds.xform(pJo,q=1,ws=1,t=1),ws=1,a=1)
  if side == 'R' : cmds.setAttr('ctrlTrans_'+fCtrl+side+'.rotateX',-180)
  if self.joBelong(pJo) in ['L','R'] :
   cmds.orientConstraint('ctrl_'+fCtrl+side,pJo,mo=1)
   cmds.pointConstraint('ctrl_'+fCtrl+side,pJo)

# ikCtrl create : leg or hand
  self.ctrlSquare('ctrl_'+ikCtrl+side,ch*.6,ch*.6,ch*.8,3,[1,1,1,1,1,1,0,0,0,0],self.colour(color,0))
  if cmds.objExists('ctrlParameter.ikCtrlNulling') and cmds.getAttr('ctrlParameter.ikCtrlNulling') :
   cmds.createNode('joint',name='ctrl_'+ikCtrl+side+'Jo',parent='ctrl_'+ikCtrl+side+'_P',skipSelect=1)
   cmds.setAttr('ctrl_'+ikCtrl+side+'Jo.drawStyle',2)
   cmds.parent('ctrlShape_'+ikCtrl+side,'ctrl_'+ikCtrl+side+'Jo',s=1,r=1)
   cmds.delete('ctrl_'+ikCtrl+side)
   cmds.rename('ctrl_'+ikCtrl+side+'Jo','ctrl_'+ikCtrl+side)
  cmds.createNode('transform',name='ctrlRot_'+ikCtrl+side,parent='ctrl_'+ikCtrl+side,skipSelect=1)
  cmds.createNode('transform',name='pin_'+ikCtrl+side,parent='ctrlRot_'+ikCtrl+side,skipSelect=1)
  if side == 'R' : cmds.setAttr('pin_'+ikCtrl+side+'.rotateX',-180)
  cmds.xform('ctrlTrans_'+ikCtrl+side,t=cmds.xform(eJo,q=1,ws=1,t=1),ws=1,a=1)
  #x = cmds.xform(eJo,q=1,ws=1,ro=1)
  #cmds.xform('ctrl_'+ikCtrl+side,ro=[0,x[1],0],ws=1,a=1)
  cmds.delete(cmds.orientConstraint(eJo,'ctrl_'+ikCtrl+side))
  if side == 'R' :
   ga = cmds.getAttr('ctrl_'+ikCtrl+'L.rotate')[0]
   if cmds.objExists('ctrlDro_'+ikCtrl+'L') : ga = cmds.getAttr('ctrlDro_'+ikCtrl+'L.rotate')[0]
   cmds.setAttr('ctrl_'+ikCtrl+side+'.rotate',ga[0],-ga[1],-ga[2],type='double3')
  self.ctrlDefaultRotate('ctrl_'+ikCtrl+side)

  if cmds.objExists('ctrlParameter.ikCtrlNulling') and cmds.getAttr('ctrlParameter.ikCtrlNulling') :
   ga = cmds.getAttr('ctrl_'+ikCtrl+side+'.rotate')[0]
   cmds.setAttr('ctrl_'+ikCtrl+side+'.jointOrient',ga[0],ga[1],ga[2],type='double3')
   cmds.setAttr('ctrl_'+ikCtrl+side+'.rotateX',0)
   cmds.setAttr('ctrl_'+ikCtrl+side+'.rotateY',0)
   cmds.setAttr('ctrl_'+ikCtrl+side+'.rotateZ',0)

  cmds.ikHandle(startJoint=sJo,endEffector=eJo, p=2, w=1,solver='ikRPsolver',sticky='sticky',name='ik_'+ikCtrl+side)
  #cmds.parent('ik_'+ikCtrl+side,'ctrl_'+ikCtrl+side)
  cmds.parent('ik_'+ikCtrl+side,'pin_'+ikCtrl+side) # 20180821 try for plam type branch ctrl
  cmds.setAttr('ik_'+ikCtrl+side+'.translate',lock=1)
  cmds.setAttr('ik_'+ikCtrl+side+'.v',0)
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='ikTwist',attributeType='double',defaultValue=0,keyable=1)
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.ikTwist','ik_'+ikCtrl+side+'.twist')

# ikCtrl follow
  cmds.createNode('transform',name='follow_'+ikCtrl+side,parent='ctrlTrans_'+ikCtrl+side,skipSelect=1)
  cmds.createNode('transform',name='followPin_'+ikCtrl+side,parent='ctrl_torso',skipSelect=1)
  cmds.matchTransform('followPin_'+ikCtrl+side,'ctrlTrans_'+ikCtrl+side)
  cmds.parentConstraint('followPin_'+ikCtrl+side,'follow_'+ikCtrl+side)
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='follow',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
  cmds.createNode('multiplyDivide',name='mult_'+ikCtrl+'FollowTrans'+side,skipSelect=1)
  cmds.createNode('multiplyDivide',name='mult_'+ikCtrl+'FollowRot'+side,skipSelect=1)
  cmds.connectAttr('follow_'+ikCtrl+side+'.translate','mult_'+ikCtrl+'FollowTrans'+side+'.input1')
  cmds.connectAttr('follow_'+ikCtrl+side+'.rotate','mult_'+ikCtrl+'FollowRot'+side+'.input1')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowTrans'+side+'.input2X')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowTrans'+side+'.input2Y')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowTrans'+side+'.input2Z')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowRot'+side+'.input2X')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowRot'+side+'.input2Y')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.follow','mult_'+ikCtrl+'FollowRot'+side+'.input2Z')
  cmds.connectAttr('mult_'+ikCtrl+'FollowTrans'+side+'.output','ctrlCons_'+ikCtrl+side+'.translate')
  cmds.connectAttr('mult_'+ikCtrl+'FollowRot'+side+'.output','ctrlCons_'+ikCtrl+side+'.rotate')
  
# pivot Ctrl create : knee or elbow
  tt = cmds.createNode('transform',parent=sJo,skipSelect=1)
  cmds.delete(cmds.aimConstraint(eJo,tt,aimVector=[1,0,0],upVector=[0,1,0],worldUpType='object',worldUpObject=mJo))
  ttt = cmds.createNode('transform',parent=eJo)
  cmds.parent(ttt,tt)
  osValue = cmds.getAttr(ttt+'.translateX')
  cmds.setAttr(ttt+'.translateX',osValue*0.5)
  cmds.setAttr(ttt+'.translateY',osValue*1.0)
  x = cmds.xform(ttt,q=1,ws=1,t=1)
  cmds.delete(tt,ttt)
  
  self.ctrlLocator('ctrl_'+pvCtrl+side,ch*.5,2,[1,1,1,0,0,0,0,0,0,0],self.colour(color,0))
  cmds.move(x[0],x[1],x[2],'ctrlTrans_'+pvCtrl+side,ws=1,a=1)
  cmds.poleVectorConstraint('ctrl_'+pvCtrl+side,'ik_'+ikCtrl+side)
  cmds.createNode('transform',name='ctrlEnvv_'+pvCtrl+side,parent='ctrl_'+pvCtrl+side,skipSelect=1)
  cmds.pointConstraint(mJo,'ctrlEnvv_'+pvCtrl+side)
  cmds.connectAttr('ctrlEnvv_'+pvCtrl+side+'.translate','ctrl_'+pvCtrl+side+'.controlPoints[9]')
  cmds.parent('ctrlTrans_'+pvCtrl+side,'ctrlTrans_'+fCtrl+side)
  cmds.createNode('transform',name='aimCons_'+pvCtrl+side,parent=pCtrl)
  cmds.pointConstraint(sJo,'aimCons_'+pvCtrl+side)
  cmds.aimConstraint('pin_'+ikCtrl+side,'aimCons_'+pvCtrl+side,aimVector=[0,-1,0],upVector=[0,1,0],worldUpType='none')
  cmds.createNode('transform',name='followPin_'+pvCtrl+side,parent='aimCons_'+pvCtrl+side,skipSelect=1)
  cmds.matchTransform('followPin_'+pvCtrl+side,'ctrlTrans_'+pvCtrl+side)

  # make follow switch
  cmds.addAttr('ctrl_'+pvCtrl+side,longName='follow',attributeType='double',minValue=-1.0,maxValue=1.0,defaultValue=1,keyable=1)
  cmds.createNode('transform',name='follow_'+pvCtrl+side,parent='ctrlTrans_'+pvCtrl+side) 
  cmds.pointConstraint('followPin_'+pvCtrl+side,'follow_'+pvCtrl+side)
  cmds.createNode('transform',name='hold_'+pvCtrl+side,parent='ctrlTrans_'+pvCtrl+side)
  cmds.createNode('transform',name='holdPin_'+pvCtrl+side,parent='ctrlTrans_torso',skipSelect=1)
  cmds.matchTransform('holdPin_'+pvCtrl+side,'hold_'+pvCtrl+side)
  cmds.parentConstraint('holdPin_'+pvCtrl+side,'hold_'+pvCtrl+side)

  cd = cmds.createNode('condition',name='cd_'+pvCtrl+'follow'+side)
  cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow',cd+'.firstTerm')
  cmds.setAttr(cd+'.operation',3)
  cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow',cd+'.colorIfTrueR')
  mdl = cmds.createNode('multDoubleLinear',name='mdl_'+pvCtrl+'follow'+side)
  cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow',mdl+'.input1')
  cmds.setAttr(mdl+'.input2',-1)
  cmds.connectAttr(mdl+'.output',cd+'.colorIfFalseR')
  cmds.setAttr(cd+'.colorIfTrueG',1)
  cmds.setAttr(cd+'.colorIfFalseG',0)
  bColor = cmds.createNode('blendColors',name='bColor_'+pvCtrl+'follow'+side)
  bColorR = cmds.createNode('blendColors',name='bColor_'+pvCtrl+'followRo'+side)
  cmds.connectAttr(cd+'.outColorG',bColor+'.blender')
  cmds.connectAttr(cd+'.outColorG',bColorR+'.blender')
  cmds.connectAttr('follow_'+pvCtrl+side+'.t',bColor+'.color1')
  cmds.connectAttr('hold_'+pvCtrl+side+'.t',bColor+'.color2')
  cmds.connectAttr('follow_'+pvCtrl+side+'.rotate',bColorR+'.color1')
  cmds.connectAttr('hold_'+pvCtrl+side+'.rotate',bColorR+'.color2')
  
  mult = cmds.createNode('multiplyDivide',name='mult_'+pvCtrl+side+'Follow')
  multR = cmds.createNode('multiplyDivide',name='mult_'+pvCtrl+side+'FollowRo')
  #cmds.connectAttr('follow_'+pvCtrl+side+'.t','multiply_'+pvCtrl+side+'Follow.input1')
  cmds.connectAttr(bColor+'.output',mult+'.input1')
  cmds.connectAttr(bColorR+'.output',multR+'.input1')
  #cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow','multiply_'+pvCtrl+side+'Follow.input2X')
  #cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow','multiply_'+pvCtrl+side+'Follow.input2Y')
  #cmds.connectAttr('ctrl_'+pvCtrl+side+'.follow','multiply_'+pvCtrl+side+'Follow.input2Z')
  cmds.connectAttr(cd+'.outColorR',mult+'.input2X')
  cmds.connectAttr(cd+'.outColorR',mult+'.input2Y')
  cmds.connectAttr(cd+'.outColorR',mult+'.input2Z')
  cmds.connectAttr(cd+'.outColorR',multR+'.input2X')
  cmds.connectAttr(cd+'.outColorR',multR+'.input2Y')
  cmds.connectAttr(cd+'.outColorR',multR+'.input2Z')
  #cmds.connectAttr('multiply_'+pvCtrl+side+'Follow.output','ctrlCons_'+pvCtrl+side+'.t')
  cmds.connectAttr(mult+'.output','ctrlCons_'+pvCtrl+side+'.t')
  cmds.connectAttr(multR+'.output','ctrlCons_'+pvCtrl+side+'.rotate')
  dv = 0
  if dir in ['+y','-y'] : dv = 1
  cmds.addAttr('ctrl_'+fCtrl+side,longName='FKIK',attributeType='double',minValue=0,maxValue=1.0,keyable=1,defaultValue=dv)
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ik_'+ikCtrl+side+'.ikBlend')

# fkCtrl create
  self.ctrlSphere('ctrl_'+sCtrl+side,ch*0.9,2,[0,0,0,1,1,1,1,1,1,0],self.colour(color,1))
  if cmds.objExists('ctrlParameter.fkCtrlOpenTrans') and cmds.getAttr('ctrlParameter.fkCtrlOpenTrans') :
   cmds.setAttr('ctrl_'+sCtrl+side+'.translateX',keyable=1,lock=0)
   cmds.setAttr('ctrl_'+sCtrl+side+'.translateY',keyable=1,lock=0)
   cmds.setAttr('ctrl_'+sCtrl+side+'.translateZ',keyable=1,lock=0)
  cmds.createNode('transform',name='pin_'+sCtrl+side,parent='ctrl_'+sCtrl+side)
  cmds.addAttr('ctrl_'+sCtrl+side,longName='follow',attributeType='double',minValue=0,maxValue=1.0,keyable=1)
  cmds.parent('ctrlTrans_'+sCtrl+side,'ctrl_'+fCtrl+side)
  cmds.xform('ctrlTrans_'+sCtrl+side,t=cmds.xform(sJo,q=1,ws=1,t=1),a=1,ws=1)
  cmds.xform('ctrlTrans_'+sCtrl+side,ro=cmds.xform(sJo,q=1,ws=1,ro=1),a=1,ws=1)
  cmds.createNode('transform',name='follow0_'+sCtrl+side,parent=sJo,skipSelect=1)
  cmds.parent('follow0_'+sCtrl+side,fk0Ctrl)
  cmds.orientConstraint('follow0_'+sCtrl+side,'ctrlCons_'+sCtrl+side,name='oCons_'+sCtrl+side)
  cmds.orientConstraint('ctrlTrans_'+sCtrl+side,'ctrlCons_'+sCtrl+side)
  cmds.setAttr('oCons_'+sCtrl+side+'.interpType',2)
  cmds.connectAttr('ctrl_'+sCtrl+side+'.follow','oCons_'+sCtrl+side+'.ctrlTrans_'+sCtrl+side+'W1')
  cmds.createNode('reverse',name='rvs_'+sCtrl+side+'Follow')
  cmds.connectAttr('ctrl_'+sCtrl+side+'.follow','rvs_'+sCtrl+side+'Follow.inputX')
  cmds.connectAttr('rvs_'+sCtrl+side+'Follow.outputX','oCons_'+sCtrl+side+'.follow0_'+sCtrl+side+'W0')
  cmds.parentConstraint('pin_'+sCtrl+side,sJo)
  if cmds.objExists('jo_'+sCtrl+'Twist'+side): cmds.orientConstraint('ctrl_'+sCtrl+side,'jo_'+sCtrl+'Twist'+side)
  self.ctrlSphere('ctrl_'+mCtrl+side,ch*0.8,1,[0,0,0,1,1,1,1,1,1,0],self.colour(color,1))
  cmds.createNode('transform',name='pin_'+mCtrl+side,parent='ctrl_'+mCtrl+side,skipSelect=1)
  cmds.parent('ctrlTrans_'+mCtrl+side,'ctrl_'+sCtrl+side)
  cmds.xform('ctrlTrans_'+mCtrl+side,t=cmds.xform(mJo,q=1,ws=1,t=1),a=1,ws=1)
  cmds.xform('ctrlTrans_'+mCtrl+side,ro=cmds.xform(sJo,q=1,ws=1,ro=1),a=1,ws=1)
  if cmds.objExists('ctrlParameter.fkCtrlNulling') and cmds.getAttr('ctrlParameter.fkCtrlNulling'):
   cmds.xform('ctrlTrans_'+mCtrl+side,ro=cmds.xform(mJo,q=1,ws=1,ro=1),a=1,ws=1)
  else :
   cmds.xform('ctrl_'+mCtrl+side,ro=cmds.xform(mJo,q=1,ws=1,ro=1),a=1,ws=1)
  cmds.orientConstraint('pin_'+mCtrl+side,mJo,name='oCons_'+mJo,weight=0)
  dvd = cmds.createNode('multiplyDivide',name='dvd_'+mCtrl+'Ivs'+side,skipSelect=1)
  cmds.setAttr(dvd+'.operation',2)
  cmds.setAttr(dvd+'.input1',1,1,1,type='double3')
  cmds.connectAttr('ctrl_'+sCtrl+side+'.scale',dvd+'.input2')
  cmds.connectAttr(dvd+'.output','ctrlTrans_'+mCtrl+side+'.scale')
  self.ctrlSphere('ctrl_'+eCtrl+side,ch*0.7,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,1))
  cmds.createNode('transform',name='pin_'+eCtrl+side,parent='ctrl_'+eCtrl+side,skipSelect=1)
  cmds.parent('ctrlTrans_'+eCtrl+side,'ctrl_'+mCtrl+side,relative=1)
  cmds.xform('ctrlTrans_'+eCtrl+side,t=cmds.xform(eJo,q=1,ws=1,t=1),a=1,ws=1)
  if cmds.objExists('ctrlParameter.fkCtrlNulling') and cmds.getAttr('ctrlParameter.fkCtrlNulling'):
   cmds.xform('ctrlTrans_'+eCtrl+side,ro=cmds.xform(eJo,q=1,ws=1,ro=1),a=1,ws=1)
  else :
   cmds.xform('ctrl_'+eCtrl+side,ro=cmds.xform(eJo,q=1,ws=1,ro=1),a=1,ws=1)
  cons = cmds.orientConstraint('pin_'+eCtrl+side,eJo)[0]
  dvd = cmds.createNode('multiplyDivide',name='dvd_'+eCtrl+'Ivs'+side,skipSelect=1)
  cmds.setAttr(dvd+'.operation',2)
  cmds.setAttr(dvd+'.input1',1,1,1,type='double3')
  cmds.connectAttr('ctrl_'+mCtrl+side+'.scale',dvd+'.input2')
  cmds.connectAttr(dvd+'.output','ctrlTrans_'+eCtrl+side+'.scale')
  if cmds.objExists('jo_'+eCtrl+'Twist'+side): cmds.orientConstraint('ctrl_'+eCtrl+side,'jo_'+eCtrl+'Twist'+side)
  
# FK IK integration
  cmds.orientConstraint('pin_'+ikCtrl+side,eJo)
  cmds.setAttr(cons+'.interpType',2)
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ctrlCons_'+ikCtrl+side+'.v')
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ctrlCons_'+pvCtrl+side+'.v')
  cmds.createNode('reverse',name='rvs_'+ikCtrl+side+'FKIK',skipSelect=1)
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','rvs_'+ikCtrl+side+'FKIK.inputX')
  cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX','ctrlCons_'+sCtrl+side+'.v')
  cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX','oCons_'+mJo+"."+'pin_'+mCtrl+side+'W0')
  cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX',cons+'.'+'pin_'+eCtrl+side+'W0')
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK',cons+'.'+'pin_'+ikCtrl+side+'W1')
  if cmds.objExists('bColor_'+eCtrl+'Twist'+side):
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','bColor_'+eCtrl+'Twist'+side+'.blender')
  if cmds.objExists('bColor_'+sCtrl+'Twist'+side):
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','bColor_'+sCtrl+'Twist'+side+'.blender')
  cmds.connectAttr('ctrl_move.bodyCtrlVisibility','ctrlTrans_'+ikCtrl+side+'.v')
  cmds.connectAttr('ctrl_move.bodyCtrlVisibility','ctrlTrans_'+pvCtrl+side+'.v')
  cmds.connectAttr('ctrl_move.bodyCtrlVisibility','ctrlTrans_'+sCtrl+side+'.v')

# Stretch Function
  cmds.createNode('transform',name='lenCons_'+ikCtrl+side,parent='ctrl_'+fCtrl+side)
  cmds.delete(cmds.pointConstraint(sJo,'lenCons_'+ikCtrl+side))
  cmds.createNode('transform',name='len_'+ikCtrl+side,parent='lenCons_'+ikCtrl+side)
  cmds.createNode('transform',name='lenPin_'+ikCtrl+side,parent='pin_'+ikCtrl+side)
  cmds.aimConstraint('lenPin_'+ikCtrl+side,'lenCons_'+ikCtrl+side,aimVector=[1,0,0],upVector=[0,1,0],worldUpType='none')
  cmds.pointConstraint('lenPin_'+ikCtrl+side,'len_'+ikCtrl+side)

  cmds.createNode('multiplyDivide',name='mult_'+ikCtrl+side+'_len')
  cmds.setAttr('mult_'+ikCtrl+side+'_len.operation',2)
  cmds.connectAttr('len_'+ikCtrl+side+'.tx','mult_'+ikCtrl+side+'_len.input1X')
  
  ga = cmds.getAttr(mJo+'.ty') + cmds.getAttr(eJo+'.ty')
  if dir in ['+x','-x'] : ga = cmds.getAttr(mJo+'.tx') + cmds.getAttr(eJo+'.tx')
  mla = cmds.createNode('multDoubleLinear',name='mdl_'+ikCtrl+'LenAdj'+side,skipSelect=1)
  #cmds.setAttr('mult_'+ikCtrl+side+'_len.input2X',abs(ga))
  cmds.setAttr(mla+'.input1',abs(ga))
  cmds.setAttr(mla+'.input2',1)
  cmds.connectAttr(mla+'.output','mult_'+ikCtrl+side+'_len.input2X')
  cmds.createNode('condition',name='cd_'+ikCtrl+side+'_len')
  cmds.connectAttr('mult_'+ikCtrl+side+'_len.outputX','cd_'+ikCtrl+side+'_len.firstTerm')
  cmds.connectAttr('mult_'+ikCtrl+side+'_len.outputX','cd_'+ikCtrl+side+'_len.colorIfTrueR')
  cmds.connectAttr('mult_'+ikCtrl+side+'_len.outputX','cd_'+ikCtrl+side+'_len.colorIfFalseG')
  cmds.setAttr('cd_'+ikCtrl+side+'_len.secondTerm',1)
  cmds.setAttr('cd_'+ikCtrl+side+'_len.operation',3)
  cmds.setAttr('cd_'+ikCtrl+side+'_len.colorIfTrueG',1)
  
  cmds.createNode('addDoubleLinear',name='adl_'+ikCtrl+side+'_len')
  cmds.connectAttr('cd_'+ikCtrl+side+'_len.outColorR','adl_'+ikCtrl+side+'_len.input1')
  cmds.setAttr('adl_'+ikCtrl+side+'_len.input2',-1)
  cmds.createNode('multDoubleLinear',name='mdl_'+ikCtrl+side+'_len')
  cmds.connectAttr('adl_'+ikCtrl+side+'_len.output','mdl_'+ikCtrl+side+'_len.input1')
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='lengthAdjust',attributeType='double',minValue=0.1,defaultValue=1,keyable=1)
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='autoStretch',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='stretchShrink',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.autoStretch','mdl_'+ikCtrl+side+'_len.input2')
  cmds.createNode('multDoubleLinear',name='mdl_'+ikCtrl+side+'_shrinkA')
  cmds.connectAttr('mdl_'+ikCtrl+side+'_len.output','mdl_'+ikCtrl+side+'_shrinkA.input1')
  cmds.setAttr('mdl_'+ikCtrl+side+'_shrinkA.input2',-1)
  cmds.createNode('multDoubleLinear',name='mdl_'+ikCtrl+side+'_shrinkB')
  cmds.connectAttr('mdl_'+ikCtrl+side+'_shrinkA.output','mdl_'+ikCtrl+side+'_shrinkB.input1')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.stretchShrink','mdl_'+ikCtrl+side+'_shrinkB.input2')

  plusA = cmds.createNode('plusMinusAverage',name='plus_'+sJo[3:]+'Scale',skipSelect=1)
  plusB = cmds.createNode('plusMinusAverage',name='plus_'+mJo[3:]+'Scale',skipSelect=1)
  bca = cmds.createNode('blendColors',name='bColor_'+sJo[3:]+'Scale',skipSelect=1)
  bcb = cmds.createNode('blendColors',name='bColor_'+mJo[3:]+'Scale',skipSelect=1)
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK',bca+'.blender')
  cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK',bcb+'.blender')
  cmds.connectAttr('ctrl_'+sCtrl+side+'.scale',bca+'.color2')
  cmds.connectAttr('ctrl_'+mCtrl+side+'.scale',bcb+'.color2')
  axisAttr = 'input3Dx' ; otherAttr = 'input3Dy' ; otherScale = 'scaleY'
  if dir in ['+y','-y'] : axisAttr = 'input3Dy' ; otherAttr = 'input3Dx' ; otherScale = 'scaleX'
  
  #cmds.connectAttr('ctrl_'+ikCtrl+side+'.scale',plusA+'.input3D[0]')
  #cmds.connectAttr('ctrl_'+ikCtrl+side+'.scale',plusB+'.input3D[0]')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.lengthAdjust',plusA+'.input3D[0].'+axisAttr)
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.lengthAdjust',plusB+'.input3D[0].'+axisAttr)
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.lengthAdjust',mla+'.input2')
  
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.'+otherScale,plusA+'.input3D[0].'+otherAttr)
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.'+otherScale,plusB+'.input3D[0].'+otherAttr)

  cmds.connectAttr('ctrl_'+ikCtrl+side+'.scaleZ',plusA+'.input3D[0].input3Dz')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.scaleZ',plusB+'.input3D[0].input3Dz')

  cmds.connectAttr('mdl_'+ikCtrl+side+'_len.output',plusA+'.input3D[1].'+axisAttr)
  cmds.connectAttr('mdl_'+ikCtrl+side+'_len.output',plusB+'.input3D[1].'+axisAttr)
  cmds.connectAttr('mdl_'+ikCtrl+side+'_shrinkB.output',plusA+'.input3D[1].'+otherAttr)
  cmds.connectAttr('mdl_'+ikCtrl+side+'_shrinkB.output',plusB+'.input3D[1].'+otherAttr)
  cmds.connectAttr('mdl_'+ikCtrl+side+'_shrinkB.output',plusA+'.input3D[1].input3Dz')
  cmds.connectAttr('mdl_'+ikCtrl+side+'_shrinkB.output',plusB+'.input3D[1].input3Dz')
  cmds.connectAttr(plusA+'.output3D',bca+'.color1')
  cmds.connectAttr(plusB+'.output3D',bcb+'.color1')
  cmds.connectAttr(bca+'.output',sJo+'.scale')
  cmds.connectAttr(bcb+'.output',mJo+'.scale')
  
  cmds.connectAttr('cd_'+ikCtrl+side+'_len.outColorG','aimCons_'+pvCtrl+side+'.scaleY') # connect to pivet ctrl aim constraint's scale


  # make ik pop function
  cmds.addAttr('ctrl_'+ikCtrl+side,longName='reduceIkPop',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
  cmds.createNode('transform',name='os_'+ikCtrl+'Pop'+side,parent='lenCons_'+ikCtrl+side,skipSelect=1)
  cmds.createNode('transform',name='pin_'+ikCtrl+'Pop'+side,parent='lenCons_'+ikCtrl+side,skipSelect=1)
  cmds.createNode('multDoubleLinear',name='mdl_'+ikCtrl+'Pop'+side,skipSelect=1)
  cmds.connectAttr('os_'+ikCtrl+'Pop'+side+'.tx','mdl_'+ikCtrl+'Pop'+side+'.input1')
  cmds.connectAttr('ctrl_'+ikCtrl+side+'.reduceIkPop','mdl_'+ikCtrl+'Pop'+side+'.input2')
  cmds.connectAttr('mdl_'+ikCtrl+'Pop'+side+'.output','pin_'+ikCtrl+'Pop'+side+'.tx')
  cmds.pointConstraint('pin_'+ikCtrl+'Pop'+side,'ctrlCons_'+sCtrl+side)
  #cmds.connectAttr('mult_'+ikCtrl+side+'_len.outputX',sr+'.valueX')
  cmds.setDrivenKeyframe('os_'+ikCtrl+'Pop'+side+'.tx',currentDriver='mult_'+ikCtrl+side+'_len.outputX',driverValue=0.958,value=0)
  cmds.setDrivenKeyframe('os_'+ikCtrl+'Pop'+side+'.tx',currentDriver='mult_'+ikCtrl+side+'_len.outputX',driverValue=0.9857,value=abs(ga)*-.007827)
  cmds.setDrivenKeyframe('os_'+ikCtrl+'Pop'+side+'.tx',currentDriver='mult_'+ikCtrl+side+'_len.outputX',driverValue=0.993,value=abs(ga)*-.0057)
  cmds.setDrivenKeyframe('os_'+ikCtrl+'Pop'+side+'.tx',currentDriver='mult_'+ikCtrl+side+'_len.outputX',driverValue=1.0,value=0)
  
  #self.ctrlDefaultRotate('ctrl_'+ikCtrl+side)
  self.ctrlDefaultRotate('ctrl_'+sCtrl+side)
  self.ctrlDefaultRotate('ctrl_'+mCtrl+side)
  self.ctrlDefaultRotate('ctrl_'+eCtrl+side)
  cmds.parent('ctrlTrans_'+ikCtrl+side,'ctrl_asset')
#  cmds.reorder('ctrl_legL_trans',front=1)

# if branch is Wing
  if bType == 'wing' :   
   self.ctrlSphere('ctrl_'+bCtrl[0]+side,ch*1,2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+bCtrl[0]+side,'ctrl_asset')
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,bJo[2])
   cmds.parentConstraint(eJo,'ctrlCons_'+bCtrl[0]+side,maintainOffset=1)
   cmds.parentConstraint('ctrl_'+bCtrl[0]+side,bJo[2])
   
   self.ctrlLocator('ctrl_'+bCtrl[1]+side,ch*0.6,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+bCtrl[1]+side,'ctrlCons_'+bCtrl[0]+side)
   cmds.matchTransform('ctrlTrans_'+bCtrl[1]+side,bJo[0])
   cmds.parentConstraint('ctrl_'+bCtrl[1]+side,bJo[0])
   self.ctrlCircle('ctrl_'+bCtrl[2]+side,ch*0.5,0,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   self.ctrlCircle('ctrl_'+bCtrl[3]+side,ch*0.25,0,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+bCtrl[2]+side,'ctrl_'+bCtrl[0]+side)
   cmds.parent('ctrlTrans_'+bCtrl[3]+side,'ctrl_'+bCtrl[2]+side)
   cmds.matchTransform('ctrlTrans_'+bCtrl[2]+side,bJo[3])
   cmds.matchTransform('ctrlTrans_'+bCtrl[3]+side,bJo[4])
   cmds.parentConstraint('ctrl_'+bCtrl[2]+side,bJo[3])
   cmds.parentConstraint('ctrl_'+bCtrl[3]+side,bJo[4])

# if branch is Shoe
  if bType == 'shoe' :
   if ov == 'default' :
    if self.exCheck([self.ankleJo[0],self.ballJo[0],self.toeJo[0]]) :
     if cmds.objExists('grp_legRotatePivotL') == 0 :
      #self.legRotatePreset()
      pass
   ballJo = bJo[0]
   toeJo = bJo[1]
   heelCtrl = bCtrl[0]
   toeCtrl = bCtrl[1]
   pivotGrp = bEx[0]
   fPivot = bEx[1]
   bPivot = bEx[2]
   tm = 1 ; rx = 0
   if side == 'R' : tm = -1 ; rx = -180
   self.legPivotCirclePreset(ch)

   self.ctrlArc(ch*1.2,ch*0.08,-90,20,ch*0.2,0,'ctrl_'+heelCtrl+side,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+heelCtrl+side,'ctrl_'+ikCtrl+side,relative=1)
   cmds.ikHandle(startJoint=eJo,endEffector=ballJo, p=2, w=1,solver='ikRPsolver',sticky='sticky',name='ik_'+heelCtrl+side)
   cmds.parent('ik_'+heelCtrl+side,'pin_'+ikCtrl+side)
   cmds.setAttr('ik_'+heelCtrl+side+'.translate',lock=1)
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ik_'+heelCtrl+side+'.ikBlend')

   self.ctrlArc(ch*0.7,ch*0.06,90*tm,20,ch*0.15,0,'ctrl_'+toeCtrl+side,2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+toeCtrl+side,'ctrl_'+fCtrl+side,relative=1)
   cmds.createNode('transform',name='pin_'+toeCtrl+side,parent='ctrl_'+toeCtrl+side,skipSelect=1)
   cmds.pointConstraint(ballJo,'ctrlCons_'+toeCtrl+side)
   cmds.ikHandle(startJoint=ballJo,endEffector=toeJo, p=2, w=1,solver='ikRPsolver',sticky='sticky',name='ik_'+toeCtrl+side)
   cmds.setAttr('ik_'+heelCtrl+side+'.v',0)
   cmds.setAttr('ik_'+toeCtrl+side+'.v',0)
   cmds.orientConstraint('ctrl_'+eCtrl+side,'pin_'+toeCtrl+side,'ctrlCons_'+toeCtrl+side,name='oCons_'+toeCtrl+side)
   cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX','oCons_'+toeCtrl+side+'.ctrl_'+eCtrl+side+'W0')
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','oCons_'+toeCtrl+side+'.pin_'+toeCtrl+side+'W1')
   cmds.parent('ik_'+toeCtrl+side,'ctrl_'+toeCtrl+side)
   cmds.setAttr('ik_'+toeCtrl+side+'.translate',lock=1)

   self.ctrlSphere('ctrl_'+heelCtrl+'TipRotate'+side,ch*0.3,0,[1,1,1,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrl_'+heelCtrl+'TipRotate'+side,'ctrl_'+ikCtrl+side,relative=1)
   
   self.heelCtrl(ch,heelCtrl,side,'ctrl_'+ikCtrl+side,'crv_'+heelCtrl+'PivotCircle',bJo[0],'pin_'+toeCtrl+side)
   
   cmds.addAttr('ctrl_'+ikCtrl+side,longName='ballPivot',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   vtp = cmds.createNode('transform',name='v_'+ikCtrl+'ballPivot'+side,parent='ctrl_'+ikCtrl+side+'_P',skipSelect=1)
   cmds.matchTransform(vtp,ballJo)
   mult = cmds.createNode('multiplyDivide',name='mult_'+ikCtrl+'ballPivot'+side)
   cmds.connectAttr(vtp+'.translate',mult+'.input1')
   cmds.connectAttr('ctrl_'+ikCtrl+side+'.ballPivot',mult+'.input2X')
   cmds.connectAttr('ctrl_'+ikCtrl+side+'.ballPivot',mult+'.input2Y')
   cmds.connectAttr('ctrl_'+ikCtrl+side+'.ballPivot',mult+'.input2Z')
   cmds.connectAttr(mult+'.output','ctrl_'+ikCtrl+side+'.rotatePivot')

# if branch is Toe
  if bType == 'toe' :

   ballJo = bJo[0]
   toeJo = bJo[1]
   heelCtrl = bCtrl[0]
   toeCtrl = bCtrl[1]
   #pivotGrp = bEx[0]
   #fPivot = bEx[1]
   #bPivot = bEx[2]
   tm = 1 ; rx = 0
   if side == 'R' : tm = -1 ; rx = -180
   self.legPivotCirclePreset(ch)
   
   tg = cmds.createNode('transform',skipSelect=1)
   cmds.matchTransform(tg,self.ankleJo[0])
   heelPivot = '' ; maxZ = 0.0
   for x in [bJo[1],bJo[5],bJo[15],bJo[20]] :
    cmds.createNode('transform',name='t_'+x,parent=tg,skipSelect=1)
    cmds.matchTransform('t_'+x,x)
    if cmds.getAttr('t_'+x+'.translateZ') > maxZ :
     heelPivot = x ; maxZ = cmds.getAttr('t_'+x+'.translateZ')
   cmds.delete(tg)
   
   cs = 1.0
   if cmds.objExists('ctrlParameter.shoulderCtrlOffset'): cs = cmds.getAttr('ctrlParameter.shoulderCtrlOffset')
   self.ctrlArc(ch*0.9*cs,ch*0.08*cs,-90,30,ch*0.2*cs,0,'ctrl_'+heelCtrl+side,0,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrl_'+heelCtrl+side,'ctrl_'+ikCtrl+side,relative=1)
   self.ctrlSphere('ctrl_'+heelCtrl+'TipRotate'+side,ch*0.3,0,[1,1,1,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrl_'+heelCtrl+'TipRotate'+side,'ctrl_'+ikCtrl+side,relative=1)
   cmds.setAttr('ctrl_'+heelCtrl+'TipRotate'+side+'.translateZ',ch*-.3)
   cmds.setAttr('ctrl_'+heelCtrl+'TipRotate'+side+'.translateY',ch*-.2)
   
   self.ctrlArc(ch*0.7,ch*0.06,90*tm,20,ch*0.15,0,'ctrl_'+toeCtrl+side,2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+toeCtrl+side,'ctrl_'+fCtrl+side)
   cmds.pointConstraint(heelPivot,'ctrlTrans_'+toeCtrl+side)
   cmds.createNode('transform',name='pin_'+toeCtrl+side,parent='ctrl_'+toeCtrl+side,skipSelect=1)
   cmds.orientConstraint('pin_'+eCtrl+side,'pin_'+toeCtrl+side,'ctrlCons_'+toeCtrl+side,name='oCons_'+toeCtrl+side)
   cmds.setAttr('oCons_'+toeCtrl+side+'.interpType',2)
   cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX','oCons_'+toeCtrl+side+'.pin_'+eCtrl+side+'W0')
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','oCons_'+toeCtrl+side+'.pin_'+toeCtrl+side+'W1')
   
   self.heelCtrl(ch,heelCtrl,side,'ctrl_'+ikCtrl+side,'crv_'+heelCtrl+'PivotCircle',bJo[5],'pin_'+toeCtrl+side)
   
   cmds.orientConstraint('ctrl_'+toeCtrl+side,bJo[1],mo=1)
   cmds.orientConstraint('ctrl_'+toeCtrl+side,bJo[5],mo=1)
   cmds.orientConstraint('ctrl_'+toeCtrl+side,bJo[10],mo=1)
   cmds.orientConstraint('ctrl_'+toeCtrl+side,bJo[15],mo=1)
   cmds.orientConstraint('ctrl_'+toeCtrl+side,bJo[20],mo=1)
   
   if cmds.objExists('ctrlParameter.CirqusRequest'):
    cmds.addAttr('ctrl_'+ikCtrl+side,longName='ballTwist',attributeType='double',minValue=-180,maxValue=180.0,keyable=1)
    cmds.addAttr('ctrl_'+ikCtrl+side,longName='ballRoll',attributeType='double',minValue=0,maxValue=180.0,keyable=1)
   #cc = cmds.createNode('transform',name='ctrlCons_'+heelCtrl+side,parent=cb,skipSelect=1)
   #cTip = cmds.createNode('transform',name='ctrlCons_'+ikCtrl+'Tip'+side,parent=cc,skipSelect=1)
    roll = cmds.createNode('transform',name='ctrlCons_'+heelCtrl+'Roll'+side,parent=cc,skipSelect=1)
    cmds.parent(cTip,roll)
    cmds.matchTransform(roll,cc,pivots=1)
    cmds.connectAttr('ctrl_'+ikCtrl+side+'.ballRoll',roll+'.rotateX')
    twist = cmds.createNode('transform',name='ctrlCons_'+ikCtrl+'Twist'+side,parent=cTip,skipSelect=1)
    cmds.parent(hp,twist)
    cmds.connectAttr('ctrl_'+ikCtrl+side+'.ballTwist',twist+'.rotateY')
    ct4 = cmds.createNode('transform',name='ctrlRotD_'+toeCtrl+side,parent=ct,skipSelect=1)
    cmds.parent(pt,ct4)
    cmds.matchTransform(twist,'ctrl_'+toeCtrl+side,pivots=1)
    cmds.connectAttr(twist+'.rotate',ct4+'.rotate')

# if branch is Finger
  if bType == 'finger' :

   if ov == 'default' :
    if self.exCheck([self.wristJo[0],self.thumbJo[0],self.indexJo[0],self.middleJo[0],self.ringJo[0],self.littleJo[0]]) :
     if cmds.objExists('grp_fingerPoseJo') == 0 :
      self.fingerPosePreset()

   gCtrl = bCtrl[0]
   #fingerPoseList = cmds.listRelatives('grp_fingerPoseJo',parent=0,children=1,type='joint')
   poseFolder = 'grp_'+gCtrl+'PoseJo' ; fingerPoseList = []
   if cmds.objExists(poseFolder) : fingerPoseList = cmds.listRelatives('grp_'+gCtrl+'PoseJo',parent=0,children=1,type='joint')
   #for i in range(len(fingerPoseList)) : fingerPoseList[i] = fingerPoseList[i].replace('_wristL','')
   for i in range(len(fingerPoseList)) : fingerPoseList[i] = fingerPoseList[i].split('_')[0]

   ctrlStartAngle = 0 ; cs = 1.0
   if side == 'R' : ctrlStartAngle = 180
   if cmds.objExists('ctrlParameter.fingerCtrlScale'): cs = cmds.getAttr('ctrlParameter.fingerCtrlScale')
   self.ctrlArc(ch*0.5*cs,ch*0.08*cs,ctrlStartAngle,45,ch*0.3*cs,0,'ctrl_'+gCtrl+side,2,[2,2,2,0,0,0,1,1,1,0],[0.3,0.3,0.2])
   ctrlOffset = -.45
   if side == 'R' : ctrlOffset = 0.45 ; 
   #if side == 'R' and x180 == 0 : ctrlOffset = -.45
   self.ctrlOffset('ctrl_'+gCtrl+side,[0,ch*ctrlOffset*cs,0])
   cmds.connectAttr('ctrl_move.bodyCtrlVisibility','ctrlTrans_'+gCtrl+side+'.v')

   cmds.parentConstraint(eJo,'ctrlCons_'+gCtrl+side)
   ga = cmds.getAttr(bJo[4]+'.tx')
   cmds.setAttr('ctrl_'+gCtrl+side+'.tx',ga)
   cmds.setAttr('ctrl_'+gCtrl+side+'.ty',ga)
   cmds.parent('ctrlTrans_'+gCtrl+side,'ctrl_asset')
   #if side == 'R' and x180 == 0 : cmds.setAttr('ctrl_'+gCtrl+side+'.ty',-ga)
   curlList = [bCtrl[1][:-1],bCtrl[4][:-1],bCtrl[8][:-1],bCtrl[12][:-1],bCtrl[16][:-1]]
   for x in curlList :
    cmds.addAttr('ctrl_'+gCtrl+side,longName=x+'Curl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   #cmds.addAttr('ctrl_'+gCtrl+side,longName='thumbCurl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   #cmds.addAttr('ctrl_'+gCtrl+side,longName='indexCurl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   #cmds.addAttr('ctrl_'+gCtrl+side,longName='middleCurl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   #cmds.addAttr('ctrl_'+gCtrl+side,longName='ringCurl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   #cmds.addAttr('ctrl_'+gCtrl+side,longName='littleCurl',attributeType='double',minValue=-5,maxValue=10,keyable=1)
   for j in range(len(fingerPoseList)):
    cmds.addAttr('ctrl_'+gCtrl+side,longName=fingerPoseList[j],attributeType='double',minValue=0,maxValue=10,keyable=1)
   cmds.addAttr('ctrl_'+gCtrl+side,longName='one',attributeType='double',defaultValue=1)
   cmds.addAttr('ctrl_'+gCtrl+side,longName='ctrl0Vis',attributeType='long',minValue=0,maxValue=1)
   cmds.setAttr('ctrl_'+gCtrl+side+'.ctrl0Vis',e=1,channelBox=1,keyable=0)
   cmds.createNode('plusMinusAverage',name='plus_'+gCtrl+side+'_addAttr')

# Prepare finger pose utility
   for j in range(len(fingerPoseList)):
    posCap = fingerPoseList[j].capitalize() # make pose name firse alphabet to upper case
    cmds.createNode('multDoubleLinear',name='mdl_'+gCtrl+side+posCap)
    cmds.connectAttr('ctrl_'+gCtrl+side+'.'+fingerPoseList[j],'mdl_'+gCtrl+side+posCap+'.input1')
    cmds.setAttr('mdl_'+gCtrl+side+posCap+'.input2',0.1)
    cmds.connectAttr('mdl_'+gCtrl+side+posCap+'.output','plus_'+gCtrl+side+'_addAttr.input1D['+str(j)+']')
   cmds.createNode('condition',name='condi_'+gCtrl+side+'_addAttr')
   cmds.connectAttr('plus_'+gCtrl+side+'_addAttr.output1D','condi_'+gCtrl+side+'_addAttr.firstTerm')
   cmds.setAttr('condi_'+gCtrl+side+'_addAttr.secondTerm',1)
   cmds.setAttr('condi_'+gCtrl+side+'_addAttr.operation',2)
   cmds.setAttr('condi_'+gCtrl+side+'_addAttr.colorIfTrueR',1)
   cmds.connectAttr('plus_'+gCtrl+side+'_addAttr.output1D','condi_'+gCtrl+side+'_addAttr.colorIfFalseR')
   cmds.createNode('reverse',name='rvs_'+gCtrl+side+'_addAttr')
   cmds.connectAttr('condi_'+gCtrl+side+'_addAttr.outColorR','rvs_'+gCtrl+side+'_addAttr.inputX')
   
# Prepare each finger scale
   cmds.connectAttr('ctrl_'+gCtrl+side+'.scale',eJo+'.scale')
   cmds.createNode('addDoubleLinear',name='adl_'+gCtrl+side+'Scale0X')
   cmds.createNode('addDoubleLinear',name='adl_'+gCtrl+side+'Scale0Y')
   cmds.createNode('addDoubleLinear',name='adl_'+gCtrl+side+'Scale0Z')
   cmds.setAttr('adl_'+gCtrl+side+'Scale0X.input1',-1)
   cmds.setAttr('adl_'+gCtrl+side+'Scale0Y.input1',-1)
   cmds.setAttr('adl_'+gCtrl+side+'Scale0Z.input1',-1)
   cmds.connectAttr('ctrl_'+gCtrl+side+'.scaleX','adl_'+gCtrl+side+'Scale0X.input2')
   cmds.connectAttr('ctrl_'+gCtrl+side+'.scaleY','adl_'+gCtrl+side+'Scale0Y.input2')
   cmds.connectAttr('ctrl_'+gCtrl+side+'.scaleZ','adl_'+gCtrl+side+'Scale0Z.input2')

# define before each finger ctrl loop
   sizeAList=[0.06,0.05,0.04,0.045,0.06,0.05,0.04,0.045,0.06,0.05,0.04,0.045,0.06,0.05,0.04,0.045,0.06,0.05,0.04]
   sizeBList=[0.15,0.14,0.12,0.125,0.15,0.14,0.12,0.125,0.15,0.14,0.12,0.125,0.15,0.14,0.12,0.125,0.15,0.14,0.12]
   sizeMList=[[0,0.24],[0.16,0],[0.16,0],[-.12,0.1],[0.18,0.15],[0.16,0],[0.16,0],[-.12,0.033],[0.18,0.05],[0.16,0],[0.16,0],[-.12,-.033],[0.18,-.05],[0.16,0],[0.16,0],[-.12,-.1],[0.18,-.15],[0.16,0],[0.16,0]]

   for i in range(0,19) :
    cn = 'ctrl_' + bCtrl[i+1] + side
    sn = bCtrl[i+1] + side
    pn = 'ctrl_' + bCtrl[i] + side # parent name
    if bCtrl[i+1][-1:] in ['0','1'] and bCtrl[i+1] != 'thumb1' and bCtrl[i+1] != 'thumb21' : pn = 'ctrl_'+bCtrl[0]+side # need adjust
    curlAttr = 'ctrl_'+gCtrl+side + '.' + bCtrl[i+1][:-1]+'Curl'
    if bCtrl[i+1] not in ['thumb0','thumb20'] and '0' in bCtrl[i+1] : curlAttr = '' # need adjust

# if self.fingerJo[i] == '' : break
    ctrlDir = 1
    if side == 'R' : ctrlDir = -1
    self.ctrlFinger(cn,ch*sizeAList[i]*cs,ch*sizeBList[i]*ctrlDir*cs,2,[0,0,0,1,1,1,1,1,1,0],[0.3,0.3,0.2])
    cmds.parent('ctrlTrans_'+sn,pn,relative=1)
    #print cn + ' parent to ' + pn
    cmds.createNode('transform',name='ctrlValue_'+sn,parent=pn)
# Basic finger ctrl connect
    cmds.setAttr('ctrlTrans_'+sn+'.tx',ch*sizeMList[i][0]*ctrlDir*cs)
    cmds.setAttr('ctrlTrans_'+sn+'.tz',ch*sizeMList[i][1]*ctrlDir*cs)
    cmds.createNode('multiplyDivide',name='multiply_'+sn+'_default')
    cmds.connectAttr('rvs_'+gCtrl+side+'_addAttr.outputX','multiply_'+sn+'_default.input1X')
    cmds.connectAttr('rvs_'+gCtrl+side+'_addAttr.outputX','multiply_'+sn+'_default.input1Y')
    cmds.connectAttr('rvs_'+gCtrl+side+'_addAttr.outputX','multiply_'+sn+'_default.input1Z')
    cmds.setAttr('multiply_'+sn+'_default.input2X',cmds.getAttr(bJo[i]+'.rx'))
    cmds.setAttr('multiply_'+sn+'_default.input2Y',cmds.getAttr(bJo[i]+'.ry'))
    cmds.setAttr('multiply_'+sn+'_default.input2Z',cmds.getAttr(bJo[i]+'.rz'))
    cmds.createNode('plusMinusAverage',name='plus_'+sn)
    cmds.connectAttr('multiply_'+sn+'_default.output','plus_'+sn+'.input3D[0]')
    cmds.connectAttr('plus_'+sn+'.output3D','ctrlTrans_'+sn+'.rotate')
    cmds.orientConstraint(cn,'ctrlValue_'+sn)
    cmds.connectAttr('ctrlValue_'+sn+'.rotate',bJo[i]+'.rotate')
    cmds.createNode('plusMinusAverage',name='plus_'+sn+'_scale')
    cmds.connectAttr('ctrl_'+sn+'.scale','plus_'+sn+'_scale.input3D[0]')
    cmds.connectAttr('plus_'+sn+'_scale.output3D',bJo[i]+'.scale')
#	connect hand scale to each finger
    cmds.connectAttr('adl_'+gCtrl+side+'Scale0X.output','plus_'+sn+'_scale.input3D[1].input3Dx')
    cmds.connectAttr('adl_'+gCtrl+side+'Scale0Y.output','plus_'+sn+'_scale.input3D[1].input3Dy')
    cmds.connectAttr('adl_'+gCtrl+side+'Scale0Z.output','plus_'+sn+'_scale.input3D[1].input3Dz')
#   connect other scale
    cmds.createNode('addDoubleLinear',name='adl_'+sn+'Trans'+side+'ScaleX',skipSelect=1)
    cmds.setAttr('adl_'+sn+'Trans'+side+'ScaleX.input1',-1)
    cmds.connectAttr('ctrlTrans_'+sn+'.scaleX','adl_'+sn+'Trans'+side+'ScaleX.input2')
    cmds.connectAttr('adl_'+sn+'Trans'+side+'ScaleX.output','plus_'+sn+'_scale.input3D[2].input3Dx')
#	connect curl function on total finger ctrl
    cmds.createNode('plusMinusAverage',name='plus_'+sn+'_sx')
    cmds.connectAttr('ctrl_'+gCtrl+side+'.one','plus_'+sn+'_sx.input1D[0]')
    cmds.connectAttr('plus_'+sn+'_sx.output1D','ctrlTrans_'+sn+'.sx')
    if curlAttr != '' :
     cmds.createNode('multDoubleLinear',name='mdl_'+sn+'_curl')
     try: cmds.connectAttr(curlAttr,'mdl_'+sn+'_curl.input1')
     except: pass
     cmds.setAttr('mdl_'+sn+'_curl.input2',-10)
     cmds.connectAttr('mdl_'+sn+'_curl.output','ctrlCons_'+sn+'.rz')
    else : cmds.connectAttr('ctrl_'+gCtrl+side+'.ctrl0Vis','ctrlTrans_'+sn+'.v')
#									finger pose each finger process
    for j in range(len(fingerPoseList)) :
     if ov != 'default' : break
     posCap = fingerPoseList[j].capitalize()
     posOut = 'mdl_'+gCtrl+side+posCap+'.output'
     #if posCap == 'Fist' and bCtrl[i+1] in ['thumb0','thumb1','thumb2'] :
      #cmds.createNode('multiplyDivide',name='multiply_'+sn+posCap+'Pow')
      #cmds.connectAttr(posOut,'multiply_'+sn+posCap+'Pow.input1X')
      #cmds.setAttr('multiply_'+sn+posCap+'Pow.input2X',5)
      #cmds.setAttr('multiply_'+sn+posCap+'Pow.operation',3)
      #posOut = 'multiply_'+sn+posCap+'Pow.outputX'

     cmds.createNode('multiplyDivide',name='multiply_'+sn+posCap)
     #cmds.connectAttr('mdl_'+gCtrl+side+posCap+'.output','multiply_'+sn+posCap+'.input1X')
     #cmds.connectAttr('mdl_'+gCtrl+side+posCap+'.output','multiply_'+sn+posCap+'.input1Y')
     #cmds.connectAttr('mdl_'+gCtrl+side+posCap+'.output','multiply_'+sn+posCap+'.input1Z')
     cmds.connectAttr(posOut,'multiply_'+sn+posCap+'.input1X')
     cmds.connectAttr(posOut,'multiply_'+sn+posCap+'.input1Y')
     cmds.connectAttr(posOut,'multiply_'+sn+posCap+'.input1Z')

     if cmds.objExists(fingerPoseList[j]+'_'+sn[:-1]) :
      cmds.connectAttr(fingerPoseList[j]+'_'+sn[:-1]+'.rotate','multiply_'+sn+posCap+'.input2')
     cmds.connectAttr('multiply_'+sn+posCap+'.output','plus_'+sn+'.input3D['+str(j+1)+']')
     cmds.createNode('addDoubleLinear',name='adl_'+sn+posCap+'Sx',skipSelect=1)
     cmds.setAttr('adl_'+sn+posCap+'Sx.input1',-1)
     try: cmds.connectAttr(fingerPoseList[j]+'_'+sn[:-1]+'.scaleX','adl_'+sn+posCap+'Sx.input2') # <- problem
     except: print fingerPoseList[j]+'_'+sn[:-1]+'.scaleX'
     cmds.createNode('multDoubleLinear',name='mdl_'+sn+posCap+'Sx')
     cmds.connectAttr('adl_'+sn+posCap+'Sx.output','mdl_'+sn+posCap+'Sx.input1')
     cmds.connectAttr('mdl_'+gCtrl+side+posCap+'.output','mdl_'+sn+posCap+'Sx.input2')
     cmds.connectAttr('mdl_'+sn+posCap+'Sx.output','plus_'+sn+'_sx.input1D['+str(j+1)+']')
 
# if branch is web
  if bType == 'web' :
   heelCtrl = bCtrl[0]
   toeCtrl = bCtrl[1]
   self.ctrlArc(ch*1.6,ch*0.08,-90,20,ch*0.2,0,'ctrl_'+bCtrl[0]+side,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+ikCtrl+side,relative=1)
   cmds.xform('ctrlTrans_'+bCtrl[0]+side,t=cmds.xform(bJo[5],q=1,ws=1,t=1),a=1,ws=1)
   cmds.ikHandle(startJoint=eJo,endEffector=bJo[4], p=2, w=1,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[0]+side)
   cmds.parent('ik_'+bCtrl[0]+side,'ctrl_'+bCtrl[0]+side)
   self.ctrlAttrPara('ik_'+bCtrl[0]+side,[3,3,3,3,3,3,3,3,3,1])
   cmds.setAttr('ik_'+bCtrl[0]+side+'.v',0)
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ik_'+bCtrl[0]+side+'.ikBlend')
   cmds.setAttr('ik_'+ikCtrl+side+'.translate',lock=0)
   cmds.parent('ik_'+ikCtrl+side,'ctrl_'+heelCtrl+side)
   self.ctrlAttrPara('ik_'+ikCtrl+side,[3,3,3,3,3,3,3,3,3,1])

   cmds.createNode('transform',name='cons_'+bCtrl[1]+side,parent='ctrlTrans_'+fCtrl+side)
   cmds.parentConstraint('ctrl_'+eCtrl+side,'pin_'+ikCtrl+side,'cons_'+bCtrl[1]+side,name='pCons_'+bCtrl[1]+side)
   cmds.connectAttr('rvs_'+ikCtrl+side+'FKIK.outputX','pCons_'+bCtrl[1]+side+'.ctrl_'+eCtrl+side+'W0')
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','pCons_'+bCtrl[1]+side+'.pin_'+ikCtrl+side+'W1')

   dp = [(bJo[0],bJo[3]),(bJo[0],bJo[3]),(bJo[4],bJo[7]),(bJo[4],bJo[7]),(bJo[8],bJo[11]),(bJo[8],bJo[11])] # distance point
   ikj = [(bJo[0],bJo[1]),(bJo[1],bJo[2]),(bJo[4],bJo[5]),(bJo[5],bJo[6]),(bJo[8],bJo[9]),(bJo[9],bJo[10])] # ik target joint
   cn = [bCtrl[2]+'1',bCtrl[2]+'2',bCtrl[3]+'1',bCtrl[3]+'2',bCtrl[4]+'1',bCtrl[4]+'2'] # ctrl name
   cnp = ['cons_'+bCtrl[1],'ctrl_'+bCtrl[2]+'1','cons_'+bCtrl[1],'ctrl_'+bCtrl[3]+'1','cons_'+bCtrl[1],'ctrl_'+bCtrl[4]+'1']
   for i in range(6):
    cn[i] = cn[i] + side ; cnp[i] = cnp[i] + side
    sa = 90 # ctrl start angle
    if side == 'R' : sa = -90
    ga = self.distance(dp[i][0],dp[i][1])
    cmds.ikHandle(startJoint=ikj[i][0],endEffector=ikj[i][1],p=2,solver='ikSCsolver',sticky='sticky',name='ik_'+cn[i])
    self.ctrlArc(ch*ga*0.5,ch*0.06,sa,20,ch*0.15,0,'ctrl_'+cn[i],1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
    cmds.parent('ctrlTrans_'+cn[i],cnp[i])
    cmds.matchTransform('ctrlTrans_'+cn[i],ikj[i][0])
    cmds.parent('ik_'+cn[i],'ctrl_'+cn[i])
    self.ctrlAttrPara('ik_'+cn[i],[3,3,3,3,3,3,3,3,3,1])
    cmds.setAttr('ik_'+cn[i]+'.v',0)

  if bType in ['palm','paw'] :
   if len(bJo) == 16 :
    heelPivot = bJo[4]
    ctrlJo = [0,1,2,4,5,6,8,9,10,12,13,14]
    parJo = [1,2,3,5,6,7,9,10,11,13,14,15]
    duJo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    duParJo = [1,2,3,5,6,7,9,10,11,13,14,15]
    ikEndJo = [1,2,3,5,6,7,9,10,11,13,14,15]
    pConsJo = [0,4,8,12]
   if len(bJo) == 20 :
    heelPivot = bJo[8]
    ctrlJo = [0,1,2,4,5,6,8,9,10,12,13,14,16,17,18]
    parJo = [1,2,3,5,6,7,9,10,11,13,14,15,17,18,19]
    duJo = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    duParJo = [5,6,7,9,10,11,13,14,15,17,18,19]
    ikEndJo = [5,6,7,9,10,11,13,14,15,17,18,19]
    pConsJo = [4,8,12,16]
   self.ctrlPaper('ctrl_'+bCtrl[0]+side,ch*0.8,0.5,'+y',2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.addAttr('ctrl_'+bCtrl[0]+side,longName='follow',attributeType='double',min=0,max=1,defaultValue=1,keyable=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,heelPivot,position=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+ikCtrl+side,rotation=1)
   #cmds.parent('pin_'+ikCtrl+side,'ctrl_'+bCtrl[0]+side)
   cmds.parentConstraint('ctrl_'+bCtrl[0]+side,'pin_'+ikCtrl+side,mo=1)
   cmds.matchTransform('ctrlTrans_'+ikCtrl+side,heelPivot,position=1)
   cmds.parent('ctrlTrans_'+bCtrl[0]+side,'ctrlRot_'+ikCtrl+side)
   
   self.legPivotCirclePreset(ch) # pot lid rotate ctrl
   pCrv = 'crv_'+eCtrl+'PivotCircle'+side ; vCrv = 'crv_'+eCtrl+'Pivot'+side
   if cmds.objExists(pCrv) :
    cmds.duplicate(pCrv,name=vCrv)
    cmds.parent(vCrv,'ctrl_'+ikCtrl+side)
    cmds.setAttr(vCrv+'.v',0)
    bb = cmds.xform(vCrv,q=1,bb=1,worldSpace=1)
    self.ctrlArc(ch*1.2,ch*0.3,-90,30,ch*0.3,0,'ctrl_'+ikCtrl+'Rot'+side,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
    cmds.parent('ctrlTrans_'+ikCtrl+'Rot'+side,'ctrl_'+ikCtrl+side,relative=1)
    cmds.move((bb[0]+bb[3])/2,(bb[1]+bb[4])/2,(bb[2]+bb[5])/2,'ctrlTrans_'+ikCtrl+'Rot'+side,worldSpace=1)
    cmds.createNode('transform',name='pin_'+ikCtrl+'Rot'+side,parent='ctrl_'+ikCtrl+'Rot'+side,skipSelect=1)
    cmds.setAttr('pin_'+ikCtrl+'Rot'+side+'.translateY',ch*1.5)
    pCons = cmds.createNode('transform',name='pCons_'+ikCtrl+'Pivot'+side,parent='ctrl_'+ikCtrl+side,skipSelect=1)
    cmds.pointConstraint('pin_'+ikCtrl+'Rot'+side,pCons)
    cmds.setAttr(pCons+'.inheritsTransform',0)
    cmds.createNode('joint',name='jo_'+ikCtrl+'Rot'+side,parent='ctrlTrans_'+ikCtrl+'Rot'+side,skipSelect=1)
    cmds.createNode('joint',name='jo_'+ikCtrl+'RotTip'+side,parent='jo_'+ikCtrl+'Rot'+side,skipSelect=1)
    cmds.setAttr('jo_'+ikCtrl+'RotTip'+side+'.translateY',ch*1.5)
    cmds.ikHandle(startJoint='jo_'+ikCtrl+'Rot'+side,endEffector='jo_'+ikCtrl+'RotTip'+side,priority=2,weight=1,solver='ikSCsolver',sticky='sticky',name='ik_'+ikCtrl+'Rot'+side)
    cmds.setAttr('jo_'+ikCtrl+'Rot'+side+'.v',0)
    cmds.setAttr('ik_'+ikCtrl+'Rot'+side+'.v',0)
    cmds.parent('ik_'+ikCtrl+'Rot'+side,'ctrlTrans_'+ikCtrl+'Rot'+side)
    cmds.pointConstraint('pin_'+ikCtrl+'Rot'+side,'ik_'+ikCtrl+'Rot'+side)
    npoc = cmds.createNode('nearestPointOnCurve',name='npoc_'+ikCtrl+'Rot'+side)
    cmds.connectAttr(vCrv+'Shape.worldSpace[0]',npoc+'.inputCurve')
    cmds.connectAttr(pCons+'.translate',npoc+'.inPosition')
    v = cmds.createNode('transform',name='v_'+ikCtrl+'Pivot'+side,parent='ctrl_'+ikCtrl+side,skipSelect=1)
    cmds.setAttr(v+'.inheritsTransform',0)
    cmds.connectAttr(npoc+'.position',v+'.translate')
    cmds.createNode('transform',name='v_'+ikCtrl+'RotPivot'+side,parent='ctrl_'+ikCtrl+side,skipSelect=1)
    cmds.pointConstraint(v,'v_'+ikCtrl+'RotPivot'+side)
    cmds.connectAttr('v_'+ikCtrl+'RotPivot'+side+'.translate','ctrlRot_'+ikCtrl+side+'.rotatePivot')
    cmds.connectAttr('jo_'+ikCtrl+'Rot'+side+'.rotate','ctrlRot_'+ikCtrl+side+'.rotate')
   
   rjo1 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'3IK'+side,parent='ctrlRot_'+ikCtrl+side,skipSelect=1)
   rjo2 = cmds.createNode('joint',name='jo_'+eCtrl+'3IK'+side,parent=rjo1,skipSelect=1)
   rjo3 = cmds.createNode('joint',name='jo_'+mCtrl+'3IK'+side,parent=rjo2,skipSelect=1)
   rjo4 = cmds.createNode('joint',name='jo_'+sCtrl+'3IK'+side,parent=rjo3,skipSelect=1)
   cmds.matchTransform(rjo2,eJo,position=1)
   cmds.matchTransform(rjo3,mJo,position=1)
   cmds.matchTransform(rjo4,sJo,position=1)
   cmds.ikHandle(startJoint=rjo1,endEffector=rjo4,p=2,w=1,solver='ikRPsolver',sticky='sticky',name='ik_'+bCtrl[0]+side)
   cmds.parent('ik_'+bCtrl[0]+side,'ctrl_'+fCtrl+side)
   tw = cmds.createNode('transform',name='oCons_'+bCtrl[0]+'Twist'+side,parent=rjo1,skipSelect=1)
   cmds.orientConstraint('ctrl_'+ikCtrl+side,tw)
   cmds.setAttr(tw+'.rotateOrder',3)
   cmds.setAttr(rjo1+'.v',0)
   cmds.setAttr('ik_'+bCtrl[0]+side+'.v',0)
   self.ctrlAttrPara('ik_'+bCtrl[0]+side,[3,3,3,3,3,3,1,1,1,1])
   
   #f = cmds.createNode('transform',name='fol_'+bCtrl[0]+side,parent='ctrl_'+ikCtrl+side)
   #fp = cmds.createNode('transform',name='folPin_'+bCtrl[0]+side,parent='ctrl_'+ikCtrl+side)
   #cmds.parent(fp,'ctrl_'+fCtrl+side)
   #cmds.setAttr(fp+'.ty',0)
   #cmds.aimConstraint(fp,f,aimVector=[0,1,0],upVector=[0,0,1],worldUpType='none')
   fm = cmds.createNode('multiplyDivide',name='mult_'+bCtrl[0]+'Fol'+side)
   #cmds.connectAttr('aCons_'+bCtrl[0]+side+'.rotate',fm+'.input1')
   cmds.connectAttr(rjo1+'.rotate',fm+'.input1')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2X')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2Y')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2Z')
   cmds.connectAttr(fm+'.output','ctrlTrans_'+bCtrl[0]+side+'.rotate')
   fm = cmds.createNode('multDoubleLinear',name='mdl_'+bCtrl[0]+'Fol'+side)
   cmds.connectAttr(tw+'.rotateY',fm+'.input1')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2')
   cmds.connectAttr(fm+'.output','ctrlCons_'+bCtrl[0]+side+'.rotateY')
   
   ctrlGrp = cmds.createNode('transform',name='cons_'+bCtrl[0]+'Ctrl'+side,parent='ctrl_asset')
   cmds.parentConstraint(eJo,ctrlGrp)
   duJoGrp = cmds.createNode('transform',name='cons_'+bCtrl[0]+'Jo'+side,parent='ctrlRot_'+ikCtrl+side)
   cmds.parentConstraint('pin_'+ikCtrl+side,duJoGrp)
   ikGrp = cmds.createNode('transform',name='grp_'+bCtrl[0]+'Ik'+side,parent='ctrlRot_'+ikCtrl+side)
   cmds.setAttr(duJoGrp+'.v',0)
   cmds.setAttr(ikGrp+'.v',0)
   for i,x in enumerate(bJo) :
    if i in ctrlJo :
     self.ctrlCircle('ctrl_'+bCtrl[i+1]+side,ch*0.3,0,2,[0,0,0,1,1,1,0,0,0,0],[0.3,0.3,0.2])
     cmds.matchTransform('ctrlTrans_'+bCtrl[i+1]+side,x)
     if i in parJo : cmds.parent('ctrlTrans_'+bCtrl[i+1]+side,'ctrl_'+bCtrl[i]+side)
     else : cmds.parent('ctrlTrans_'+bCtrl[i+1]+side,ctrlGrp)
     cmds.parentConstraint('ctrl_'+bCtrl[i+1]+side,x)

    if i in duJo :
     cmds.createNode('joint',name='ikJo_'+bCtrl[i+1]+side,parent=duJoGrp)
     cmds.matchTransform('ikJo_'+bCtrl[i+1]+side,bJo[i])
     if i in duParJo :
      cmds.parent('ikJo_'+bCtrl[i+1]+side,'ikJo_'+bCtrl[i]+side)
     cmds.makeIdentity('ikJo_'+bCtrl[i+1]+side,apply=1,rotate=1)
    if i in ikEndJo :
     cmds.ikHandle(startJoint='ikJo_'+bCtrl[i]+side,endEffector='ikJo_'+bCtrl[i+1]+side,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[i]+side)
     cmds.parent('ik_'+bCtrl[i]+side,ikGrp)
     cmds.setAttr('ik_'+bCtrl[i]+side+'.translate',lock=1)
     cmds.setAttr('ik_'+bCtrl[i]+side+'.rotate',lock=1)
    if i in duJo and i in ctrlJo :
     cmds.connectAttr('ikJo_'+bCtrl[i+1]+side+'.rotate','ctrlCons_'+bCtrl[i+1]+side+'.rotate')
	 
  if bType == 'tentacle' :
   heelPivot = bJo[0]
   self.ctrlArc(ch*0.5,ch*0.1,-90,360,ch*0.01,1,'ctrl_'+bCtrl[0]+side,2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.addAttr('ctrl_'+bCtrl[0]+side,longName='autoRotate',attributeType='double',min=0,max=1,defaultValue=0,keyable=1)
   #cmds.setAttr('ctrl_'+bCtrl[0]+side+'.follow',0,lock=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,eJo,position=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+ikCtrl+side,rotation=1)
   cmds.parent('pin_'+ikCtrl+side,'ctrl_'+bCtrl[0]+side)
   
   #nj = cmds.createNode('joint',parent='ctrl_'+ikCtrl+side+'_P')
   #cmds.setAttr(nj+'.drawStyle'.2)
   
   cmds.matchTransform('ctrlTrans_'+ikCtrl+side,heelPivot,position=1)
   self.ctrlAttrPara('ctrlTrans_'+ikCtrl+side,[3,3,3,3,3,3,3,3,3,3])
   cmds.matchTransform('followPin_'+pvCtrl+side,'ctrlTrans_'+pvCtrl+side)
   cmds.parent('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+ikCtrl+side)
   cmds.matchTransform('ctrl_'+bCtrl[0]+side,heelPivot,pivots=1)
   cmds.matchTransform('ctrlCons_'+bCtrl[0]+side,heelPivot,pivots=1)
   
   rjo1 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'3IK'+side,parent='ctrl_'+ikCtrl+side,skipSelect=1)
   rjo2 = cmds.createNode('joint',name='jo_'+eCtrl+'3IK'+side,parent=rjo1,skipSelect=1)
   rjo3 = cmds.createNode('joint',name='jo_'+mCtrl+'3IK'+side,parent=rjo2,skipSelect=1)
   rjo4 = cmds.createNode('joint',name='jo_'+sCtrl+'3IK'+side,parent=rjo3,skipSelect=1)
   cmds.matchTransform(rjo2,eJo,position=1)
   cmds.matchTransform(rjo3,mJo,position=1)
   cmds.matchTransform(rjo4,sJo,position=1)
   cmds.ikHandle(startJoint=rjo1,endEffector=rjo4,p=2,w=1,solver='ikRPsolver',sticky='sticky',name='ik_'+bCtrl[0]+side)
   cmds.parent('ik_'+bCtrl[0]+side,'ctrl_'+fCtrl+side)
   cmds.poleVectorConstraint('ctrl_'+pvCtrl+side,'ik_'+bCtrl[0]+side)
   cmds.setAttr(rjo1+'.v',0)
   cmds.setAttr('ik_'+bCtrl[0]+side+'.v',0)
   self.ctrlAttrPara('ik_'+bCtrl[0]+side,[3,3,3,3,3,3,1,1,1,1])
   
   fm = cmds.createNode('multiplyDivide',name='mult_'+bCtrl[0]+'Fol'+side)
   cmds.connectAttr(rjo1+'.rotate',fm+'.input1')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.autoRotate',fm+'.input2X')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.autoRotate',fm+'.input2Y')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.autoRotate',fm+'.input2Z')
   cmds.connectAttr(fm+'.output','ctrlCons_'+bCtrl[0]+side+'.rotate')
   
   self.ctrlSphere('ctrl_'+bCtrl[1]+side,ch*0.9,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.parent('ctrlTrans_'+bCtrl[1]+side,'ctrl_'+eCtrl+side)
   cmds.matchTransform('ctrlTrans_'+bCtrl[1]+side,bJo[0])
   cmds.orientConstraint('ctrl_'+bCtrl[1]+side,bJo[0])
   cmds.ikHandle(startJoint=bJo[0],endEffector=bJo[2],p=2,w=1,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[1]+side)
   cmds.parent('ik_'+bCtrl[1]+side,'ctrl_'+ikCtrl+side)
   cmds.connectAttr('ctrl_'+fCtrl+side+'.FKIK','ik_'+bCtrl[1]+side+'.ikBlend')
   cmds.setAttr('ik_'+bCtrl[1]+side+'.v',0)
   self.ctrlAttrPara('ik_'+bCtrl[1]+side,[3,3,3,3,3,3,1,1,1,1])

#self.bTypeDic[self.L2R(self.rearAnkleJo,i)][0].append(self.L2R([self.rearBallJo,self.rearToeJo,self.rearHoofJo],i))
#self.bTypeDic[self.L2R(self.rearAnkleJo,i)][0].append(['rearBall','rearToe','rearHoof'])
  if bType == 'hoof':
   self.ctrlPaper('ctrl_'+bCtrl[0]+side,ch*0.8,0.5,'+y',2,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.addAttr('ctrl_'+bCtrl[0]+side,longName='follow',attributeType='double',min=0,max=1,defaultValue=1,keyable=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,bJo[0],position=1)
   cmds.matchTransform('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+ikCtrl+side,rotation=1)
   cmds.parentConstraint('ctrl_'+bCtrl[0]+side,'pin_'+ikCtrl+side,mo=1)
   cmds.matchTransform('ctrlTrans_'+ikCtrl+side,bJo[1],position=1)
   self.ctrlAttrPara('ctrlTrans_'+ikCtrl+side,[3,3,3,3,3,3,3,3,3,1])
   
   self.ctrlArc(ch*0.5,ch*0.08,90-45,36,ch*0.2,0,'ctrl_'+bCtrl[1]+side,1,[0,0,0,1,1,1,0,0,0,0],self.colour(color,2))
   cmds.matchTransform('ctrlTrans_'+bCtrl[1]+side,bJo[1],position=1)
   cmds.parent('ctrlTrans_'+bCtrl[1]+side,'ctrlRot_'+ikCtrl+side)
   cmds.parent('ctrlTrans_'+bCtrl[0]+side,'ctrl_'+bCtrl[1]+side)
   
   cmds.ikHandle(startJoint=eJo,endEffector=bJo[0],p=2,w=1,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[0]+side)
   cmds.ikHandle(startJoint=bJo[0],endEffector=bJo[1],p=2,w=1,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[1]+side)
   cmds.ikHandle(startJoint=bJo[1],endEffector=bJo[2],p=2,w=1,solver='ikSCsolver',sticky='sticky',name='ik_'+bCtrl[2]+side)
   cmds.parent('ik_'+bCtrl[0]+side,'ctrl_'+bCtrl[1]+side)
   cmds.parent('ik_'+bCtrl[1]+side,'ctrl_'+bCtrl[1]+side)
   cmds.parent('ik_'+bCtrl[2]+side,'ctrl_'+ikCtrl+side)
   self.ctrlAttrPara('ik_'+bCtrl[0]+side,[3,3,3,3,3,3,3,3,3,1])
   self.ctrlAttrPara('ik_'+bCtrl[1]+side,[3,3,3,3,3,3,3,3,3,1])
   self.ctrlAttrPara('ik_'+bCtrl[2]+side,[3,3,3,3,3,3,3,3,3,1])
   cmds.setAttr('ik_'+bCtrl[0]+side+'.v',0)
   cmds.setAttr('ik_'+bCtrl[1]+side+'.v',0)
   cmds.setAttr('ik_'+bCtrl[2]+side+'.v',0)
   
   #rjo0 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'IkRoot'+side,parent='ctrl_'+bCtrl[1]+side,skipSelect=1)
   #rjoTip = cmds.createNode('joint',name='jo_'+bCtrl[0]+'IkTip'+side,parent=rjo0,skipSelect=1)
   #rjo1 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'3IK'+side,parent=rjo0,skipSelect=1)
   #rjo2 = cmds.createNode('joint',name='jo_'+eCtrl+'3IK'+side,parent=rjo1,skipSelect=1)
   #rjo4 = cmds.createNode('joint',name='jo_'+sCtrl+'3IK'+side,parent=rjo2,skipSelect=1)
   
   nrjo0 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'R0IK'+side,parent='ctrl_'+bCtrl[1]+side,skipSelect=1)
   cmds.matchTransform(nrjo0,bJo[0],position=1)
   nrjo1 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'R1IK'+side,parent=nrjo0,skipSelect=1)
   nrjo2 = cmds.createNode('joint',name='jo_'+bCtrl[0]+'R2IK'+side,parent=nrjo1,skipSelect=1)
   dis = self.distance(sJo,bJo[0])
   cmds.setAttr(nrjo1+'.ty',dis/2)
   cmds.setAttr(nrjo2+'.ty',dis/2)
   if cmds.getAttr(mJo+'.rx') > 0 :
    cmds.setAttr(nrjo1+'.rx',2)
    cmds.setAttr(nrjo1+'.preferredAngleX',2)
   else :
    cmds.setAttr(nrjo1+'.rx',-2)
    cmds.setAttr(nrjo1+'.preferredAngleX',-2)
   cmds.ikHandle(startJoint=nrjo0,endEffector=nrjo2,p=2,w=1,solver='ikRPsolver',sticky='sticky',name='ik_N'+eCtrl+side)
   cmds.parent('ik_N'+eCtrl+side,'ctrl_'+fCtrl+side)
   cmds.setAttr(nrjo0+'.v',0)
   
   fm = cmds.createNode('multiplyDivide',name='mult_'+bCtrl[0]+'Fol'+side)
   #cmds.connectAttr(rjo1+'.rotate',fm+'.input1')
   cmds.connectAttr(nrjo0+'.rotate',fm+'.input1')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2X')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2Y')
   cmds.connectAttr('ctrl_'+bCtrl[0]+side+'.follow',fm+'.input2Z')
   cmds.connectAttr(fm+'.output','ctrlTrans_'+bCtrl[0]+side+'.rotate')

 #self.heelCtrl(heelCtrl,side,'ctrl_'+ikCtrl+side,'crv_heelPivotCircle',heelPivot)
 def heelCtrl(self,ch,heelName,side,hrc,circle,heelPivot,toePin,*a):
  hCtrl = 'ctrl_'+heelName+side
  cmds.addAttr(hCtrl,longName='tipRotate',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
  hPin = cmds.createNode('transform',name='pin_'+heelName+side,parent=hCtrl,skipSelect=1)
  cmds.setAttr(hPin+'.translateY',10)
  hACons = cmds.createNode('transform',name='aCons_'+heelName+side,parent=hrc,skipSelect=1)
  cmds.aimConstraint(hPin,hACons,aimVector=[0,1,0],upVector=[0,1,0],worldUpType='none')
  tPin = cmds.createNode('transform',name='pin_'+heelName+'Trans'+side,parent=hACons,skipSelect=1)
  cmds.setAttr(tPin+'.translateY',ch*5)
  cmds.setAttr(tPin+'.translateZ',cmds.getAttr(circle+'.translateZ'))
  hTrans = cmds.createNode('transform',name='trans_'+heelName+'Trans'+side,parent=hrc,skipSelect=1)
  cmds.setAttr(hTrans+'.translateZ',cmds.getAttr(circle+'.translateZ'))
  htv = cmds.createNode('transform',name='v_'+heelName+'Trans'+side,parent=hTrans,skipSelect=1)
  cmds.pointConstraint(tPin,htv)
  
  cb = cmds.createNode('transform',name='ctrlCons_'+heelName+'Tip'+side,parent=hrc,skipSelect=1)
  cc = cmds.createNode('transform',name='ctrlCons_'+heelName+side,parent=cb,skipSelect=1)
  cTip = cmds.createNode('transform',name='ctrlCons_'+heelName+'Root'+side,parent=cc,skipSelect=1)
  hp = cmds.createNode('transform',name='pin_'+heelName+'Cons'+side,parent=cTip,skipSelect=1)
  
  cmds.matchTransform(cc,heelPivot,pivots=1)
  cmds.matchTransform(hp,hrc.replace('ctrl_','pin_'))
  cmds.parentConstraint(hp,hrc.replace('ctrl_','pin_'))
  cmds.orientConstraint(hrc,hACons,cb,name='oCons_'+heelName+side)
  cmds.orientConstraint(hACons,cc)
  cmds.connectAttr(hCtrl+'.tipRotate','oCons_'+heelName+side+'.'+hACons+'W1')
  rvs = cmds.createNode('reverse',name='rvs_'+heelName+side,skipSelect=1)
  cmds.connectAttr(hCtrl+'.tipRotate',rvs+'.inputX')
  cmds.connectAttr(rvs+'.outputX','oCons_'+heelName+side+'.'+hrc+'W0')
  
  cmds.duplicate(circle,name=circle+side,renameChildren=1) #new
  cmds.setAttr(circle+side+'.v',0)
  cmds.parent(circle+side,hrc)
  if side == 'R':
   cmds.setAttr(circle+side+'.translateX',0)
   cmds.setAttr(circle+side+'.scaleX',-1)
   
  npoc = cmds.createNode('nearestPointOnCurve',name='npoc_'+heelName+'Rot'+side)
  sp = cmds.listRelatives(circle+side,shapes=1)[0]
  cmds.connectAttr(sp+'.worldSpace[0]',npoc+'.inputCurve')
  xCons = cmds.createNode('decomposeMatrix',name='xCons_'+htv,skipSelect=1)
  cmds.connectAttr(htv+'.worldMatrix[0]',xCons+'.inputMatrix')
  cmds.connectAttr(xCons+'.outputTranslate',npoc+'.inPosition')
  npocTip = cmds.createNode('nearestPointOnCurve',name='npoc_'+heelName+'tipRot'+side)
  cmds.connectAttr(sp+'.worldSpace[0]',npocTip+'.inputCurve')
  cmds.createNode('decomposeMatrix',name='xCons_'+heelName+'TipRotate'+side,skipSelect=1)
  cmds.connectAttr('ctrl_'+heelName+'TipRotate'+side+'.worldMatrix[0]','xCons_'+heelName+'TipRotate'+side+'.inputMatrix')
  cmds.connectAttr('xCons_'+heelName+'TipRotate'+side+'.outputTranslate',npocTip+'.inPosition')
  
  cmds.createNode('transform',name='ab_'+heelName+'TipRotate'+side,parent=cb,skipSelect=1)
  cmds.connectAttr(npocTip+'.position','ab_'+heelName+'TipRotate'+side+'.translate')
  cmds.setAttr('ab_'+heelName+'TipRotate'+side+'.inheritsTransform',0) 
  cmds.createNode('transform',name='v_'+heelName+'TipRotate'+side,parent=cb,skipSelect=1)
  cmds.pointConstraint('ab_'+heelName+'TipRotate'+side,'v_'+heelName+'TipRotate'+side)
  
  cmds.connectAttr('v_'+heelName+'TipRotate'+side+'.translate',cTip+'.rotatePivot')
  cmds.connectAttr('ctrl_'+heelName+'TipRotate'+side+'.rotate',cTip+'.rotate')
  
  cmds.createNode('composeMatrix',name='xCon_'+heelName+side,skipSelect=1)
  cmds.connectAttr(npoc+'.position','xCon_'+heelName+side+'.inputTranslate')
  cmds.createNode('multMatrix',name='xMult_'+heelName+side,skipSelect=1)
  cmds.connectAttr('xCon_'+heelName+side+'.outputMatrix','xMult_'+heelName+side+'.matrixIn[0]')
  cmds.connectAttr(hrc+'.worldInverseMatrix[0]','xMult_'+heelName+side+'.matrixIn[1]')
  cmds.createNode('decomposeMatrix',name='xCons_'+heelName+side,skipSelect=1)
  cmds.connectAttr('xMult_'+heelName+side+'.matrixSum','xCons_'+heelName+side+'.inputMatrix')
  
  cmds.connectAttr('xCons_'+heelName+side+'.outputTranslate',cb+'.rotatePivot')
  
  trA = cmds.createNode('transform',name=toePin.replace('pin_','ctrlRotA_'),parent=hrc,skipSelect=1)
  trB = cmds.createNode('transform',name=toePin.replace('pin_','ctrlRotB_'),parent=trA,skipSelect=1)
  trC = cmds.createNode('transform',name=toePin.replace('pin_','ctrlRotC_'),parent=trB,skipSelect=1)
  cmds.connectAttr(cb+'.rotate',trA+'.rotate')
  cdToe = cmds.createNode('condition',name=toePin.replace('pin_','cd_'),skipSelect=1)
  cdHeel = cmds.createNode('condition',name='cd_'+heelName+side,skipSelect=1)
  cmds.connectAttr(htv+'.translateZ',cdToe+'.firstTerm')
  cmds.connectAttr(htv+'.translateZ',cdHeel+'.firstTerm')
  cmds.setAttr(cdToe+'.operation',3)
  cmds.setAttr(cdHeel+'.operation',3)
  cmds.connectAttr(cc+'.rotate',cdToe+'.colorIfFalse')
  cmds.connectAttr('xCons_'+heelName+side+'.outputTranslate',cdHeel+'.colorIfFalse')
  ga = cmds.getAttr(cc+'.rotatePivot')[0]
  cmds.setAttr(cdHeel+'.colorIfTrue',ga[0],ga[1],ga[2],type='double3')
  cmds.connectAttr(cdToe+'.outColor',trB+'.rotate')
  cmds.connectAttr(cdHeel+'.outColor',cc+'.rotatePivot')
  cmds.connectAttr(cTip+'.rotate',trC+'.rotate')
  
  cmds.parent(toePin,trC,relative=1)
  if side == 'R' : cmds.setAttr(toePin+'.rotateX',-180)
   
# pipe type ctrl process module
 def pipeCtrl(self,ch,side,dir,joList,joTip,ctrl,ctrlParent,color,*a):
  jList = [] ; pList = [ctrlParent] ; spanN = 1
  for x in joList :
   if cmds.objExists(x) : jList.append(x)
   else : break
  
  for i,x in enumerate(jList) :
   fkn = ctrl+'FK'+str(i)+side
   cs = 0.4
   if i == 0 : fkn = ctrl+side ; cs = cs * 1.5
   self.ctrlCircle('ctrl_'+fkn,ch*cs,dir,2,[0,0,0,1,1,1,0,0,0,0],color)
   pList.append('ctrl_'+fkn)
   cmds.matchTransform('ctrlTrans_'+fkn,x)
   cmds.parent('ctrlTrans_'+fkn,pList[i])
   cmds.parentConstraint('ctrl_'+fkn,x)
   if i == 0 :
    cmds.addAttr('ctrl_'+fkn,longName='follow',attributeType='double',minValue=0,maxValue=1.0,keyable=1,defaultValue=1)
    cmds.addAttr('ctrl_'+fkn,longName='FKIK',attributeType='double',minValue=0,maxValue=1.0,keyable=1,defaultValue=0)
    rvs = cmds.createNode('reverse',name='rvs_'+fkn)
    cmds.connectAttr('ctrl_'+fkn+'.FKIK','rvs_'+fkn+'.inputX')
   else : cmds.connectAttr(rvs+'.outputX','ctrlTrans_'+fkn+'.v')
  if len(jList) > 6 : spanN = int(math.ceil(float(len(jList))/2.5)) -2
  ikh = cmds.ikHandle(startJoint=joList[0],endEffector=joTip,sol='ikSplineSolver',createCurve=1,numSpans=spanN,parentCurve=0)
  cmds.parent(ikh[0],ikh[2],'ctrl_'+ctrl+side)
  cmds.makeIdentity(ikh[2],apply=True,translate=1,rotate=1)
  cmds.setAttr(ikh[0]+'.v',0)
  cmds.setAttr(ikh[2]+'.v',0)
  cmds.rename(ikh[2],'crv_'+ctrl)
  cmds.connectAttr(pList[1]+'.FKIK',ikh[0]+'.ikBlend')
  cmds.createNode('transform',name='follow0_'+ctrl,parent='ctrlTrans_torso')
  cmds.matchTransform('follow0_'+ctrl,'ctrl_'+ctrl)
  cmds.orientConstraint('follow0_'+ctrl,'ctrlTrans_'+ctrl,'ctrlCons_'+ctrl,name='oCons_'+ctrl+'Follow')  
  cmds.setAttr('oCons_'+ctrl+'Follow.interpType',2)
  cmds.connectAttr('ctrl_'+ctrl+'.follow','rvs_'+ctrl+'.inputY')
  cmds.connectAttr('rvs_'+ctrl+'.outputY','oCons_'+ctrl+'Follow.follow0_'+ctrl+'W0')
  cmds.connectAttr('ctrl_'+ctrl+'.follow','oCons_'+ctrl+'Follow.ctrlTrans_'+ctrl+'W1')
  #oCons_tailFollow.ctrlTrans_tailW1
  #oCons_tailctrlTrans_tailW1
  for i in range(1,spanN+3) :
   ikn = ctrl+'IK'+str(i)+side
   self.ctrlCrystal('ctrl_'+ikn,ch*cs,ch*cs,2,[1,1,1,0,0,0,0,0,0,0],color)
   cmds.xform('ctrlTrans_'+ikn,ws=1,t=cmds.pointPosition('crv_'+ctrl+'Shape.cv['+str(i)+']'))
   cmds.parent('ctrlTrans_'+ikn,pList[1])
   cmds.connectAttr(pList[1]+'.FKIK','ctrlTrans_'+ikn+'.v')
   cmds.createNode('transform',name='v_'+ikn,parent=pList[1],skipSelect=1)
   cmds.pointConstraint('ctrl_'+ikn,'v_'+ikn)
   cmds.connectAttr('v_'+ikn+'.translate','crv_'+ctrl+'Shape.controlPoints['+str(i)+']')

 def stripCtrl(self,ch,name,joHead,joTail,crv,joFront,pDirect,topGroup,color,*a):
  sll = crv
  if cmds.nodeType(sll) == 'nurbsCurve' :
   pass
  elif cmds.nodeType(sll) == 'transform' :
   lr = cmds.listRelatives(sll,noIntermediate=1,shapes=1,fullPath=1,type='nurbsCurve')
   if lr is not None :
    sll = lr[0]
  else :
   sll = ''

  if sll != '' :
   cmds.nurbsPlane(name='plane_'+name,degree=cmds.getAttr(sll+'.degree'),patchesU=cmds.getAttr(sll+'.spans'),axis=[0,1,0])
   aoap = cmds.createNode('transform')
   aoa = cmds.createNode('transform',parent=aoap)
   cmds.setAttr(aoap+'.rotateX',-90)
   pAxis = [0.3,0,0]
   if pDirect != '+x' :
    rcc = cmds.cluster('plane_'+name)
    if pDirect == '+z' :
     cmds.setAttr(rcc[1]+'.rotateY',-90) ; cmds.setAttr(aoap+'.rotateY',-90)
     pAxis = [0,0,0.3]
    if pDirect == '-z' :
     cmds.setAttr(rcc[1]+'.rotateY',90) ; cmds.setAttr(aoap+'.rotateY',90)
     pAxis = [0,0,-0.3]
    if pDirect == '-x' :
     cmds.setAttr(rcc[1]+'.rotateY',180) ; cmds.setAttr(aoap+'.rotateX',180)
     pAxis = [-0.3,0,0]
    cmds.delete('plane_'+name,constructionHistory=1)

   cmds.createNode('transform',name='grp_'+name+'Ctrl',parent=topGroup)
   cmds.createNode('transform',name='grp_'+name+'Cc')
   cmds.parent('grp_'+name+'Cc',topGroup)
   cmds.setAttr('grp_'+name+'Cc.v',0)
   cmds.createNode('transform',name='grp_'+name+'Nurbs',parent=topGroup)
   cmds.setAttr('grp_'+name+'Nurbs.v',0)
   cmds.createNode('transform',name='grp_'+name+'flc',parent=topGroup)
   cmds.setAttr('grp_'+name+'flc.inheritsTransform',0)
   cmds.setAttr('grp_'+name+'flc.v',0)
   cmds.createNode('transform',name='grp_'+name+'Pos',parent=topGroup)

   cmds.parent('plane_'+name,'grp_'+name+'Nurbs')
   lastCtrl = ''
   crvVN = cmds.getAttr(sll+'.degree') + cmds.getAttr(sll+'.spans')
   for i in range(crvVN) :
    pos = cmds.xform(sll+'.cv['+str(i)+']',q=1,worldSpace=1,translation=1)
    ctrl = 'ctrl_'+name+str(i) ; ctrlT = 'ctrlTrans_'+name+str(i)
    self.ctrlCrystal(ctrl,ch*0.1,ch*0.1,2,[1,1,1,1,1,1,0,0,0,0],color)
    cmds.parent(ctrlT,'grp_'+name+'Ctrl',relative=1)
    cmds.xform(ctrlT,worldSpace=1,translation=[pos[0],pos[1],pos[2]])
    if i == (crvVN-1) : lastCtrl = ctrl
    ccc = cmds.cluster(sll+'.cv['+str(i)+']',name='cc_'+ctrl,relative=1)
    ccp = cmds.cluster('plane_'+name+'.cv['+str(i)+'][0:3]',name='cc_'+'plane_'+str(i),relative=1)
    cmds.pointConstraint(ctrl,ccc[1])
    cmds.parentConstraint(ctrl,ccp[1])
    cmds.parent(ccc[1],'grp_'+name+'Cc')
    cmds.parent(ccp[1],'grp_'+name+'Cc')

   cmds.addAttr('ctrl_'+name+str(i),longName='stretchy',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   sAttr = 'ctrl_'+name+str(i)+'.stretchy'
   cmds.addAttr('ctrl_'+name+str(i),longName='keepLengthScale',attributeType='double',minValue=0,maxValue=1.0,defaultValue=1,keyable=1)
   cmds.addAttr('ctrl_'+name+str(i),longName='rotateControl',attributeType='double',minValue=0,maxValue=1.0,defaultValue=0,keyable=1)
   rcAttr = 'ctrl_'+name+str(i)+'.rotateControl'

####### find axis between follicle and joint
   av = [0,0,0]
   frontTrans = ''
   frontScale = ''
   if joFront == 'rb_ascJFX' :
    av = [1,0,0]
    frontTrans = '.tx'
    frontScale = '.sx'
   if joFront == 'rb_ascJFY' :
    av = [0,1,0]
    frontTrans = '.ty'
    frontScale = '.sy'
   if joFront == 'rb_ascJFZ' :
    av = [0,0,1]
    frontTrans = '.tz'
    frontScale = '.sz'
   if joFront == 'rb_ascJFMX' :
    av = [-1,0,0]
    frontTrans = '.tx'
    frontScale = '.sx'
   if joFront == 'rb_ascJFMY' :
    av = [0,-1,0]
    frontTrans = '.ty'
    frontScale = '.sy'
   if joFront == 'rb_ascJFMZ' :
    av = [0,0,-1]
    frontTrans = '.tz'
    frontScale = '.sz'
   uv = [0,1,0]
   aoaa = cmds.createNode('transform')
   cmds.move(av[0],av[1],av[2],aoaa)
   aoau = cmds.createNode('transform')
   cmds.move(uv[0],uv[1],uv[2],aoau)
   cmds.aimConstraint(aoaa,aoa,aimVector=av,upVector=[0,1,0],worldUpType='object',worldUpObject=aoau)
   oRot = cmds.getAttr(aoa+'.rotate')[0]
   cmds.delete(aoap,aoaa,aoau)


##### create joint list
   joList = [joTail]
   for j in range(20) :
    lr = cmds.listRelatives(joList[j],type='joint',noIntermediate=1,parent=1)
    if lr is not None :
     joList.append(lr[0])
     if lr[0] == joHead :
      break
    else :
     break
   joList.reverse()

   joPosList = []
   ikh = cmds.ikHandle(startJoint=joHead, endEffector=joTail,solver='ikSplineSolver',createCurve=0,curve=sll,parentCurve=0)
   for x in joList :
    joPosList.append(cmds.xform(x,q=1,worldSpace=1,translation=1))
   cmds.delete(ikh)

##### lock length curve
   ci = cmds.createNode('curveInfo')
   cmds.connectAttr(sll+'.worldSpace[0]',ci+'.inputCurve')
   dvd = cmds.createNode('multiplyDivide')
   cmds.setAttr(dvd+'.operation',2)
   cmds.connectAttr(ci+'.arcLength',dvd+'.input2X')
   cmds.setAttr(dvd+'.input1X',cmds.getAttr(dvd+'.input2X'))
   cd = cmds.createNode('condition')
   cmds.connectAttr(dvd+'.outputX',cd+'.firstTerm')
   cmds.setAttr(cd+'.secondTerm',1)
   cmds.setAttr(cd+'.operation',4)
   cmds.connectAttr(dvd+'.outputX',cd+'.colorIfTrueR')
   cmds.setAttr(cd+'.colorIfFalseR',1)
   rCrv = cmds.rebuildCurve(sll,name=sll+'Rebuild',constructionHistory=1,replaceOriginal=0,endKnots=1,keepRange=0,keepControlPoints=0 ,spans=20,degree=3)
   dc = cmds.detachCurve(rCrv[0]+'.u[0.5]',constructionHistory=1,replaceOriginal=0)
   cmds.connectAttr(cd+'.outColorR',dc[2]+'.parameter[0]')
   cmds.setAttr(dc[1]+'.v',0)
   dcShape = cmds.listRelatives(dc[0],shapes=1)[0]
   cmds.parent(dc[0],'grp_'+name+'Nurbs')
   cmds.parent(dc[1],'grp_'+name+'Nurbs')
   cmds.parent(rCrv,'grp_'+name+'Nurbs')

   flcList = []
   aConsList = []
   pinList = []
   for i in range(len(joList)) :
    flcN = 'flc_'+name+str(i)+'temp'
    cmds.createNode('follicle',name=flcN)
    cmds.connectAttr('plane_'+name+'Shape.local',flcN+'.inputSurface')
    cmds.connectAttr('plane_'+name+'Shape.worldMatrix[0]',flcN+'.inputWorldMatrix')
    flcP = cmds.listRelatives(flcN,parent=1)[0]
    flcList.append(flcP)
    cmds.connectAttr(flcN+'.outTranslate',flcP+'.translate')
    cmds.connectAttr(flcN+'.outRotate',flcP+'.rotate')
    cmds.parent(flcP,'grp_'+name+'flc')

    cpos = cmds.createNode('closestPointOnSurface',name='cpos_'+name+str(i))
    cmds.connectAttr('plane_'+name+'Shape.worldSpace',cpos+'.inputSurface')
    cmds.setAttr(cpos+'.inPositionX',joPosList[i][0])
    cmds.setAttr(cpos+'.inPositionY',joPosList[i][1])
    cmds.setAttr(cpos+'.inPositionZ',joPosList[i][2])
    pu = cmds.getAttr(cpos+'.parameterU')
    cmds.setAttr(flcN+'.parameterU',pu)
    cmds.setAttr(flcN+'.parameterV',0.5)

    aConsAxis = cmds.createNode('transform',name='aConsAxis_'+name+str(i),parent=flcP)
    cmds.setAttr(aConsAxis+'.rotate',oRot[0],oRot[1],oRot[2], type="double3")
    aCons = cmds.createNode('transform',name='aCons_'+name+str(i),parent=aConsAxis)
    pin = cmds.createNode('transform',name='pin_'+name+str(i),parent=aCons)
#    cmds.parentConstraint(aCons,joList[i],maintainOffset=0)
    cmds.orientConstraint(aCons,joList[i],maintainOffset=0)
    aConsList.append(aCons)
    pinList.append(pin)

##### in joint loop : create pos node on lock length curve
    poc = cmds.createNode('pointOnCurveInfo',name='poc_'+name+str(i))
    cmds.connectAttr(dcShape+'.worldSpace[0]',poc+'.inputCurve')
    cmds.setAttr(poc+'.turnOnPercentage',1)
    pos = cmds.createNode('transform',name='pos_'+name+str(i))
    cmds.connectAttr(poc+'.position',pos+'.translate')
    cmds.parent(pos,'grp_'+name+'Pos')

    npoc = cmds.createNode('nearestPointOnCurve',name='npoc_'+name+str(i))
    cmds.connectAttr(dcShape+'.worldSpace[0]',npoc+'.inputCurve')
    cmds.setAttr(npoc+'.inPositionX',joPosList[i][0])
    cmds.setAttr(npoc+'.inPositionY',joPosList[i][1])
    cmds.setAttr(npoc+'.inPositionZ',joPosList[i][2])
    para = cmds.getAttr(npoc+'.parameter')
    cmds.setAttr(poc+'.parameter',para)
    cmds.delete(npoc)
    cmds.connectAttr(pos+'.translate',cpos+'.inPosition')

    cmds.createNode('setRange',name='sr_'+name+str(i))
    cmds.connectAttr(sAttr,'sr_'+name+str(i)+'.valueX')
    cmds.setAttr('sr_'+name+str(i)+'.oldMinX',0)
    cmds.setAttr('sr_'+name+str(i)+'.oldMaxX',1)
    cmds.connectAttr(cpos+'.parameterU','sr_'+name+str(i)+'.minX')
    cmds.setAttr('sr_'+name+str(i)+'.maxX',pu)
    cmds.connectAttr('sr_'+name+str(i)+'.outValueX',flcN+'.parameterU')

   for i in range(len(aConsList)) :
    if i != (len(aConsList)-1) :
     cmds.aimConstraint(flcList[i+1],aConsList[i],aimVector=av,worldUpType='none')
     cmds.pointConstraint(flcList[i+1],pinList[i])
     dv = cmds.createNode('multiplyDivide')
     cmds.setAttr(dv+'.operation',2)
     cmds.connectAttr(pinList[i]+frontTrans,dv+'.input1X')
     cmds.setAttr(dv+'.input2X',cmds.getAttr(pinList[i]+frontTrans))
     cmds.connectAttr(dv+'.outputX',joList[i]+frontScale)
    if i == (len(aConsList)-1) :
     aConsParent = cmds.listRelatives(aConsList[i],parent=1)[0]
     cons = cmds.orientConstraint(aConsParent,lastCtrl,aConsList[i])[0]
     rvs = cmds.createNode('reverse')
     cmds.connectAttr(rcAttr,rvs+'.inputX')
     cmds.connectAttr(rvs+'.outputX',cons+'.'+aConsParent+'W0')
     cmds.connectAttr(rcAttr,cons+'.'+lastCtrl+'W1')
    pass

# Clean to Mocap Joint
 def mocapJoint(self,*a):
  mjo = cmds.listRelatives(self.rootJo,allDescendents=1,type='joint')
  exjo = cmds.listRelatives('grp_deformer',allDescendents=1,type='joint')
  for j in exjo :
   csk = cmds.listConnections(j,source=0,destination=1,type='skinCluster',skipConversionNodes=1)
   if csk is not None :
    csk = [ii for n,ii in enumerate(csk) if ii not in csk[:n]]
    for sk in csk :
     wdInf = cmds.skinCluster(sk,q=1,weightedInfluence=1)
     if j in wdInf :
      jpn = j[:3] + '00'	#j????weight?joint
      jp = ''	#jp?????joint
      for m in mjo : #??????joint
       if m[:5] == jpn : jp = m 
      inf = cmds.skinCluster(sk,q=1,influence=1)
      if jp in inf :
       for m in inf :
        cmds.setAttr(m+'.lockInfluenceWeights',1)
       print 'Prcess ' + j + ' weight.'
       cmds.select(cl=1)
       cmds.skinCluster(sk,e=1,selectInfluenceVerts=j)
       sel = cmds.ls(selection=1)
       if len(sel) > 0 :
        cmds.setAttr(j+'.lockInfluenceWeights',0)
        cmds.setAttr(jp+'.lockInfluenceWeights',0)
        cmds.skinPercent(sk,sel,transformMoveWeights=(j,jp))
        #cmds.setAttr(j+'.lockInfluenceWeights',1)
        #cmds.setAttr(jp+'.lockInfluenceWeights',1)
      else :
       sys.stderr.write('Please add inference '+jp+' to '+sk+'.')
       self.exit
     
  mjo.append(self.rootJo)
  for x in mjo :
   cmds.setAttr(x+'.rotate',0,0,0)
   nx = 'jo' + x[5:]
   cmds.rename(x,nx)
  cmds.parent(self.rootJo,world=1)
  cmds.parent('grp_geometry',world=1)
  fn = cmds.file(q=1,sceneName=1)
  fn2 = fn.replace('.ma','')
  fn2 = fn.replace('.mb','')
  nn = fn2 + '_mocap'
  cmds.file(rename=nn)
  cmds.file(save=1)

 def lockCrvLlength(self,name,sll,attr,*a):
  ci = cmds.createNode('curveInfo',skipSelect=1)
  cmds.connectAttr(sll+'.worldSpace[0]',ci+'.inputCurve')
  bc = cmds.createNode('blendColors',skipSelect=1)
  cmds.connectAttr(ci+'.arcLength',bc+'.color1R')
  cmds.setAttr(bc+'.color2R',cmds.getAttr(ci+'.arcLength'))
  if attr != '': cmds.connectAttr(attr,bc+'.blender')
  else : cmds.setAttr(bc+'.blender',0)
  dvd = cmds.createNode('multiplyDivide',skipSelect=1)
  cmds.setAttr(dvd+'.operation',2)
  cmds.connectAttr(ci+'.arcLength',dvd+'.input2X')
  #cmds.setAttr(dvd+'.input1X',cmds.getAttr(dvd+'.input2X'))
  cmds.connectAttr(bc+'.outputR',dvd+'.input1X')
  cd = cmds.createNode('condition',skipSelect=1)
  cmds.connectAttr(dvd+'.outputX',cd+'.firstTerm')
  cmds.setAttr(cd+'.secondTerm',1)
  cmds.setAttr(cd+'.operation',4)
  cmds.connectAttr(dvd+'.outputX',cd+'.colorIfTrueR')
  cmds.setAttr(cd+'.colorIfFalseR',1)
  #rCrv = cmds.rebuildCurve(sll,name=sll+'Rebuild',constructionHistory=1,replaceOriginal=0,endKnots=1,keepRange=0,keepControlPoints=0 ,spans=20,degree=3)
  #dc = cmds.detachCurve(rCrv[0]+'.u[0.5]',constructionHistory=1,replaceOriginal=0)
  #cmds.connectAttr(cd+'.outColorR',dc[2]+'.parameter[0]')
  
  cmds.duplicate(sll,name='crv_'+name+'Cl')
  cmds.createNode('rebuildCurve',name='rCrv_'+name,skipSelect=1)
  cmds.setAttr('rCrv_'+name+'.spans',36)
  cmds.connectAttr(sll+'.worldSpace[0]','rCrv_'+name+'.inputCurve')
  cmds.createNode('detachCurve',name='dCrv_'+name,skipSelect=1)
  cmds.connectAttr('rCrv_'+name+'.outputCurve','dCrv_'+name+'.inputCurve')
  #cmds.connectAttr('dCrv_'+name+'.outputCurve[0]','crv_'+name+'ClShape.create')
  cmds.connectAttr(cd+'.outColorR','dCrv_'+name+'.parameter[0]')
  cmds.createNode('rebuildCurve',name='rCrv_'+name+'Re',skipSelect=1)
  cmds.setAttr('rCrv_'+name+'Re.spans',36)
  cmds.setAttr('rCrv_'+name+'Re.keepRange',2)
  cmds.connectAttr('dCrv_'+name+'.outputCurve[0]','rCrv_'+name+'Re.inputCurve')
  cmds.connectAttr('rCrv_'+name+'Re.outputCurve','crv_'+name+'ClShape.create')
  
# Delete Ctrl Process
 def deleteCtrl(self,*a):
  delList = ['ctrlTrans_torso','ctrlTrans_handL','ctrlTrans_handR','ctrlTrans_legL','ctrlTrans_legR','ctrlTrans_fingerL','ctrlTrans_fingerR']
  delList += ['grp_chestCons','grp_rearPelvisCons','ctrlTrans_facial','cons_tongueCtrl']
  delList += ['range_neckCons','multiply_ctrl_handL_len','multiply_ctrl_handR_len','multiply_ctrl_legL_len','multiply_ctrl_legR_len']
  delList += ['multiply_neck2Scale','multiply_neckScale','multiply_jawRot','rag_jaw']
  delList += ['bColor_armLScale','bColor_armRScale','bColor_elbowLScale','bColor_elbowRScale','bColor_hipLScale','bColor_hipRScale','bColor_kneeLScale','bColor_kneeRScale']
  delList += ['dm_neck0','dm_neck1','dm_neck2','dm_head','cons_ballCtrlL','cons_ballCtrlR','cons_plamCtrlL','cons_plamCtrlR']
  delList += ['ctrlTrans_leg2L','ctrlTrans_leg2R','ctrlTrans_hand2L','ctrlTrans_hand2R','bColor_arm2LScale','bColor_elbow2LScale','bColor_arm2RScale','bColor_elbow2RScale','bColor_hip2RScale','bColor_knee2RScale','bColor_hip2LScale','bColor_knee2LScale']
  delList += ['plus_browL','plus_browMidL','plus_browM','plus_browR','plus_browMidR']
  delList += ['cons_heelCtrlL','cons_heelCtrlR','ctrlTrans_finger2L','ctrlTrans_finger2R','mult_tongueScaleRate1','mult_tongueScaleRate4','mult_tongueScaleRate7']
  delList += ['bColor_neck1Ro','bColor_neck1S','bColor_neck1Sr','bColor_neck2Ro','bColor_neck2S','bColor_neck2Sr','bColor_neck3Ro','bColor_neck3S','bColor_neck3Sr']
  delList += ['grp_torsoAround','bColor_tongue0','bColor_tongue1','bColor_tongue2','bColor_tongue3','bColor_tongue4','bColor_tongue5','bColor_tongue6','bColor_tongue7','bColor_tongue8','bColor_tongue9']
  delList += ['bColor_tongueScale1','bColor_tongueScale4','bColor_tongueScale7','bColor_tongueTip']
  delList += ['clp_upLidYL','clp_upLidYR'] #?
  delList += ['srg_jawBs']
  delList += ['srg_uplidUpDnAttrL','srg_uplidUpDnAttrR','srg_uplidUpDnAttrThird','srg_lolipUpDnAttrL','srg_lolipUpDnAttrR','srg_lolipUpDnAttrThird','adl_eyeBallY0L','adl_eyeBallY0R','adl_eyeBallY0Third']
  delList += ['clp_cornerXL','clp_cornerXR','clp_cornerYL','clp_cornerYR','clp_loLidYL','clp_loLidYR']
  delList += ['clp_cheekYL','clp_cheekYR','dvd_freeElbowL','dvd_freeElbowR','dvd_freeKneeL','dvd_freeKneeR']
  delList += ['mult_neck1Trans','mult_headTrans','mult_spine1Trans','mult_spine2Trans','mult_chestTrans']
  delList += ['ctrlTrans_rearLegL','ctrlTrans_rearLegR','bColor_rearHipLScale','bColor_rearKneeLScale','bColor_rearHipRScale','bColor_rearKneeRScale']
  for x in delList :
   if cmds.objExists(x) : cmds.delete(x)

  cmds.joint(self.rootJo,e=1,assumePreferredAngles=1,children=1)
  aj = cmds.listRelatives(self.rootJo,allDescendents=1,type='joint')
  aj.append(self.rootJo)
  for x in aj :
   cmds.setAttr(x+'.scale',1,1,1)
   cmds.setAttr(x+'.shear',0,0,0)
   la = cmds.listAttr(x,userDefined=1)
   if la is not None :
    if 'dtx' in la : cmds.setAttr(x+'.tx',cmds.getAttr(x+'.dtx'))
    if 'dty' in la : cmds.setAttr(x+'.ty',cmds.getAttr(x+'.dty'))
    if 'dtz' in la : cmds.setAttr(x+'.tz',cmds.getAttr(x+'.dtz'))

  if cmds.objExists('grp_facial'):
   fud = cmds.listAttr('grp_facial',userDefined=1)
   if fud is not None :
    for x in cmds.listAttr('grp_facial',userDefined=1):
     if cmds.getAttr('grp_facial.'+x,keyable=1):
      cmds.setAttr('grp_facial.'+x,0)

  dc = []
  for x in cmds.ls(type='controller'):
   if cmds.listConnections(x+'.controllerObject') is None : dc.append(x)
  cmds.delete(dc)

  sys.stderr.write('Delete Ctrl Done.')



##############################################################################################################
################################################# Utility Module #############################################
##############################################################################################################

 def ssParent(self,child,parent):
  ls = cmds.ls(sl=1)
  cmds.parent(child,parent,relative=1,shape=1)
  cmds.select(ls,r=1)

 def createAdj(self,jn,parent,attr,*a): # adj ctrl process
  jnj = cmds.createNode('joint',name=jn+'Adj',skipSelect=1)
  if parent != '' : cmds.parent(jnj,parent)
  cmds.setAttr(jnj+'.radius',0,channelBox=0)
  cmds.setAttr(jnj+'.drawLabel',1)
  cmds.setAttr(jnj+'.type',18)
  cmds.setAttr(jnj+'.otherType',(jnj.replace('Adj','')),type="string")
  cmds.setAttr(jnj+'.overrideEnabled',1)
  cmds.setAttr(jnj+'.overrideColor',22)
  if len(a)>0 :
   if a[0] != 'none' :
    if a[0] == 'fingerPlane' :
     cmds.curve(d=1,p=[(0,-.5,0),(0,.5,0),(1,-.5,0),(0,-.5,0),(1,.5,0),(1,-.5,0),(0,.5,0),(1,.5,0)],k=[0,1,2,3,4,5,6,7],name=jn+'AdjS')
    if a[0] == 'fingerPlaneZ' :
     cmds.curve(d=1,p=[(0,-.5,0),(0,.5,0),(0,-.5,1),(0,-.5,0),(0,.5,1),(0,-.5,1),(0,.5,0),(0,.5,1)],k=[0,1,2,3,4,5,6,7],name=jn+'AdjS')
    elif a[0] == 'jaw' :
     cmds.curve(d=1,p=[(1,0.25,0),(1,0,0.25),(1,-.25,0),(1,0,-.25),(1,0.25,0),(1,-.25,0),(1,0,0),(1,0,0.25),(1,0,-.25),(1,0,0),(-1,0,0),(-1,0.25,0),(-1,0,0.25),(-1,-.25,0),(-1,0,-.25),(-1,0.25,0),(-1,-.25,0),(-1,0,0),(-1,0,0.25),(-1,0,-.25)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],name=jn+'AdjS')
    elif a[0] == 'faceSpot' :
     cmds.curve(d=1,p=[(0,0.1,0),(0.1,0,0),(0,-.1,0),(-.1,0,0),(0,0.1,0),(0,0,0.1),(0,0.1,0),(0,0,0.1),(0.1,0,0),(0,0,0.1),(0,-.1,0),(0,0,0.1),(-.1,0,0)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12],name=jn+'AdjS')
    elif a[0] == 'sphere' :
     ce = 'curve -d 1 '
     for i in range(31) : ce += " -p " + str(0) + " " + str(math.cos(math.radians(12*i+90))*0.25) + " " + str(math.sin(math.radians(12*i+90))*0.25)
     for i in range(31) : ce += " -p " + str(math.cos(math.radians(12*i+90))*0.25) + " " + str(0) + " " + str(math.sin(math.radians(12*i+90))*0.25)
     ce += " -n " + jn+'AdjS'
     mel.eval(ce)
    if a[0] == 'fingerArrow' :
     cmds.curve(d=1,p=[(0,0.5,0),(0,0.5,1),(0,0,1.5),(0,-.5,1),(0,-.5,0)],name=jn+'AdjS')
     cmds.closeCurve(jn+'AdjS',constructionHistory=0,replaceOriginal=1)
    s = cmds.listRelatives(jn+'AdjS',shapes=1)
    cmds.rename(s[0],jn+'AdjShape')
    cmds.parent(jn+'AdjShape',jn+'Adj',relative=1,shape=1)
    cmds.delete(jn+'AdjS')
    cmds.setAttr(jn+'AdjShape.overrideEnabled',1)
    cmds.setAttr(jn+'AdjShape.overrideColor',25)
  else :
   jnjs = cmds.createNode('locator',parent=jnj,name=jn+'AdjShape',skipSelect=1)
   cmds.setAttr(jnjs+'.overrideEnabled',1)
   cmds.setAttr(jnjs+'.overrideColor',25)
   if 'thumb' in jn or 'index' in jn or 'middle' in jn or 'ring' in jn or 'little' in jn :
    cmds.setAttr(jn+'AdjShape.localScaleX',0.25)
    cmds.setAttr(jn+'AdjShape.localScaleY',0.25)
    cmds.setAttr(jn+'AdjShape.localScaleZ',0.25)
  an = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ']
  for i in range(6) :
   if attr[i] == 1 : cmds.setAttr(jnj+an[i],lock=1,keyable=0,channelBox=0)
   if attr[i] == 2 :
    if i == 0 : cmds.transformLimits(jnj,enableTranslationX=(1,1),translationX=(0,0))
    if i == 1 : cmds.transformLimits(jnj,enableTranslationY=(1,1),translationY=(0,0))
    if i == 2 : cmds.transformLimits(jnj,enableTranslationZ=(1,1),translationZ=(0,0))
    if i == 3 : cmds.transformLimits(jnj,enableRotationX=(1,1),rotationX=(0,0))
    if i == 4 : cmds.transformLimits(jnj,enableRotationY=(1,1),rotationY=(0,0))
    if i == 5 : cmds.transformLimits(jnj,enableRotationZ=(1,1),rotationZ=(0,0))
  cmds.setAttr(jnj+'.scaleX',lock=1,keyable=0,channelBox=0)
  cmds.setAttr(jnj+'.scaleY',lock=1,keyable=0,channelBox=0)
  cmds.setAttr(jnj+'.scaleZ',lock=1,keyable=0,channelBox=0)
  cmds.setAttr(jnj+'.visibility',lock=1,keyable=0,channelBox=0)

 def ctrlAttrPara(self,ctrl,para,*a): # for set ctrl attribute
  attr = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
  for i,x in enumerate(attr) :
   if para[i] == 0 : cmds.setAttr(ctrl+x,lock=1,keyable=0,channelBox=0)
   if para[i] == 2 : cmds.setAttr(ctrl+x,lock=0,keyable=0,channelBox=1)
   if para[i] == 3 : cmds.setAttr(ctrl+x,lock=1)

 def ctrlColor(self,ctrl,rbg,*a):
  sp = cmds.listRelatives(ctrl,shapes=1)
  for x in sp :
   cmds.setAttr(x+'.overrideEnabled',1)
   cmds.setAttr(x+'.overrideRGBColors',1)
   cmds.setAttr(x+'.overrideColorR',rbg[0])
   cmds.setAttr(x+'.overrideColorG',rbg[1])
   cmds.setAttr(x+'.overrideColorB',rbg[2])

 def colour(self,hue,level,*a):
  cr = colorsys.hsv_to_rgb(hue,0.5,0.5)
  if level == 1 : cr = colorsys.hsv_to_rgb(hue,0.72,0.32)
  if level == 2 : cr = colorsys.hsv_to_rgb(hue,0.92,0.14)
  return [cr[0],cr[1],cr[2]]
   
 def posingRem(self,list,rem,*a):
  for x in list :
   for y in cmds.listAttr(x,keyable=True) :
    if cmds.objExists(rem+'.'+x+y) == 0 :
     cmds.addAttr(rem,longName=x+y)
    cmds.setAttr(rem+'.'+x+y,cmds.getAttr(x+'.'+y))

 def otherSideNode(self,adj,*a):
  p = cmds.listRelatives(adj,parent=1)[0]
  cmds.createNode('transform',name=adj+'R',parent=p,skipSelect=1)
  mdl = cmds.createNode('multDoubleLinear',name='mdl_'+adj+'R',skipSelect=1)
  cmds.connectAttr(adj+'.tx',mdl+'.input1')
  cmds.setAttr(mdl+'.input2',-1)
  cmds.connectAttr(mdl+'.output',adj+'R'+'.tx')
  cmds.connectAttr(adj+'.ty',adj+'R'+'.ty')
  cmds.connectAttr(adj+'.tz',adj+'R'+'.tz')

 def guildCrv(self,name,adjs,grp,*a):
  close = 0
  if adjs[0] == adjs[-1] :
   adjs.pop()
   close = 1 
  cvp = [ (0,0,0) for i in range(len(adjs)) ]
  crv = cmds.curve(point=cvp,name=name,degree=3)
  cmds.parent(crv,grp,relative=1)
  #cmds.setAttr(crv+'.template',1)
  cmds.setAttr(crv+'.overrideEnabled',1)
  cmds.setAttr(crv+'.overrideDisplayType',2)
  for i,adj in enumerate(adjs) :
   cmds.connectAttr(adj+'.translate',crv+'.controlPoints['+str(i)+']')
  if close == 1 : cmds.closeCurve(crv,replaceOriginal=1,preserveShape=0,constructionHistory=0)
  return crv

 def createJoint(self,name='joint',parent=None,*a):
  print 'ready to create ' + name + '..'
  if parent :
   cmds.createNode('joint',name=name,parent=parent,skipSelect=1)
  else :
   cmds.createNode('joint',name=name)
  print 'Create ' + name + '.'
  if self.joId.get(name[3:]) != None :
   cmds.addAttr(name,longName='orderID',attributeType='long',keyable=1)
   cmds.setAttr(name+'.orderID',self.joId[name[3:]])

 def ctrlTransRem(self,x,*a):
  la = cmds.listAttr(x,userDefined=1)
  if la is None :
   cmds.addAttr(x,longName='dtx',attributeType='double')
   cmds.addAttr(x,longName='dty',attributeType='double')
   cmds.addAttr(x,longName='dtz',attributeType='double')
  if la is not None :
   if 'dtx' not in la : cmds.addAttr(x,longName='dtx',attributeType='double')
   if 'dty' not in la : cmds.addAttr(x,longName='dty',attributeType='double')
   if 'dtz' not in la : cmds.addAttr(x,longName='dtz',attributeType='double')
  cmds.setAttr(x+'.dtx',cmds.getAttr(x+'.tx'))
  cmds.setAttr(x+'.dty',cmds.getAttr(x+'.ty'))
  cmds.setAttr(x+'.dtz',cmds.getAttr(x+'.tz'))
	
 def posingSet(self,list,rem,*a):
  for x in list :
   aex = 0
   for y in cmds.listAttr(x,keyable=True) :
    if cmds.objExists(rem+'.'+x+y) == 1 :
     cmds.setAttr(x+'.'+y,cmds.getAttr(rem+'.'+x+y))
     aex = 1
   if aex == 0 : self.adjusterPosition(x)
   
 def rSideJoint(self,jn,pj,lj,*a): # right side joint
  if cmds.objExists(jn) == 0 :
   cmds.createNode('joint',name=jn,parent=pj)
  else :
   if cmds.listRelatives(jn,parent=1)[0] != pj :
    cmds.parent(jn,pj)
  cmds.setAttr(jn+'.translate',-cmds.getAttr(lj+'.translateX'),-cmds.getAttr(lj+'.translateY'),-cmds.getAttr(lj+'.translateZ'),type="double3")
  cmds.setAttr(jn+'.rotate',cmds.getAttr(lj+'.rotateX'),cmds.getAttr(lj+'.rotateY'),cmds.getAttr(lj+'.rotateZ'),type="double3")
  cmds.setAttr(jn+'.jointOrient',cmds.getAttr(lj+'.jointOrientX'),cmds.getAttr(lj+'.jointOrientY'),cmds.getAttr(lj+'.jointOrientZ'),type="double3")
  cmds.setAttr(jn+'.radius',cmds.getAttr(lj+'.radius'))
  try :
   if a[0] == 'onRoot' :
    jox = cmds.getAttr(lj+'.jointOrientX')
    if jox == 0 : cmds.setAttr(jn+'.jointOrientX',-180)
    elif jox > 0 : cmds.setAttr(jn+'.jointOrientX',jox-180)
    else : cmds.setAttr(jn+'.jointOrientX',jox+180)
    cmds.setAttr(jn+'.jointOrientY',cmds.getAttr(lj+'.jointOrientY')*-1)
    cmds.setAttr(jn+'.jointOrientZ',cmds.getAttr(lj+'.jointOrientZ')*-1)
    cmds.setAttr(jn+'.translateY',cmds.getAttr(lj+'.translateY'))
    cmds.setAttr(jn+'.translateZ',cmds.getAttr(lj+'.translateZ'))
  except :
   pass

 def freezeRotate(self,jo,*a):
  tmp = cmds.createNode('decomposeMatrix',skipSelect=1)
  cmds.connectAttr(jo+'.matrix',tmp+'.inputMatrix')
  ga = cmds.getAttr(tmp+'.outputRotate')[0]
  cmds.delete(tmp)
  cmds.setAttr(jo+'.jointOrient',ga[0],ga[1],ga[2],type='double3')
  cmds.setAttr(jo+'.rotate',0,0,0,type='double3')
   
 def exCheck(self,ec,*a):
  if type(ec) == str :
   return cmds.objExists(ec)
  if type(ec) == list or type(ec) == tuple :
   ex = 0
   for x in ec :
    if cmds.objExists(x) : ex = ex + 1
   if ex == len(ec) : return 1
   else : return 0
  
 def anyCheck(self,ec,*a):
  ex = 0
  for x in ec :
   if cmds.objExists(x) : ex = ex + 1
  if ex > 0 : return 1
  else : return 0

 def analyzeAxis(self,jo,*a):
  x = cmds.getAttr(jo+'.tx')
  y = cmds.getAttr(jo+'.ty')
  z = cmds.getAttr(jo+'.tz')
  axis = 'X' ; vector = [1,0,0] ; dir = 1 ; eAxis = '+x' ; axisOrder = 0
  
  if abs(x) > abs(y) and abs(x) > abs(z):
   if x < 0 : vector = [-1,0,0] ; dir = -1 ; eAxis = '-x' ; axisOrder = 0
  elif abs(y) > abs(z):
   axis = 'Y' ; vector = [0,1,0] ; eAxis = '+y'
   if y < 0 : vector = [0,-1,0] ; dir = -1 ; eAxis = '-y' ; axisOrder = 1
  else:
   axis = 'Z' ; vector = [0,0,1] ; eAxis = '+z'
   if z < 0 : vector = [0,0,-1] ; dir = -1 ; eAxis = '-z' ; axisOrder = 2
  return [axis,vector,dir,eAxis,axisOrder]
  
 def ctrlSquare(self,n,x,y,z,*a):
  x = x * 0.5
  y = y * 0.5
  z = z * 0.5
  ctrl = cmds.curve(d=1,p=[(x,y,z),(x,-y,z),(-x,-y,z),(-x,y,z),(x,y,z),(x,y,-z),(x,-y,-z),(x,-y,z),(x,-y,-z),(-x,-y,-z),(-x,y,-z),(x,y,-z),(-x,y,-z),(-x,y,z),(-x,-y,z),(-x,-y,-z)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],name=n)
  self.ctrlOptimize(n,a)
  
 def ctrlSphere(self,n,x,*a):
  x = x * 0.5
  ctrl = cmds.curve(d=1,p=[(0,0,x),(x*.7,0,x*.7),(x,0,0),(x*.7,0,x*-.7),(0,0,-x),(x*-.7,0,x*-.7),(-x,0,0),(x*-.7,0,x*.7),(0,0,x),(0,x*.7,x*.7),(0,x,0),(0,x*.7,x*-.7),(0,0,-x),(0,x*-.7,x*-.7),(0,-x,0),(0,x*-.7,x*.7),(0,0,x),(0,x*.7,x*.7),(0,x,0),(x*-.7,x*.7,0),(-x,0,0),(x*-.7,x*-.7,0),(0,-x,0),(x*.7,x*-.7,0),(x,0,0),(x*.7,x*.7,0),(0,x,0)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],name=n)
  self.ctrlOptimize(n,a)

 def ctrlFinger(self,name,radius,length,*a):
  r1 = radius*0.5
  r2 = radius* 0.866026
  ctrl = cmds.curve(d=1,p=[(0,r1,r2),(0,r1,-r2),(length,0,0),(0,r1,r2),(0,-radius,0),(length,0,0),(0,-radius,0),(0,r1,-r2)],k=[0,1,2,3,4,5,6,7],name=name)
  self.ctrlOptimize(name,a)

 def ctrlFingerY(self,name,radius,length,*a):
  r1 = radius*0.5
  r2 = radius* 0.866026
  ctrl = cmds.curve(d=1,p=[(r1,0,r2),(r1,0,-r2),(0,-length,0),(r1,0,r2),(-radius,0,0),(0,-length,0),(-radius,0,0),(r1,0,-r2)],k=[0,1,2,3,4,5,6,7],name=name)
  self.ctrlOptimize(name,a)
 
 def ctrlPlay(self,name,weight,height,direction,length,*a): # direction = x,y,z or -x,-y,-z
  h = height * 0.5 ; w = weight * 0.5
  if direction in ['-x','-y','-z'] : length = length * -1
  if direction in ['x','-x'] : ctrl = cmds.curve(d=1,p=[(0,h,w),(length,0,0),(0,-h,w),(0,h,w),(0,h,-w),(length,0,0),(0,-h,-w),(0,h,-w),(0,-h,-w),(0,-h,w)],name=name)
  if direction in ['y','-y'] : ctrl = cmds.curve(d=1,p=[(h,0,w),(0,length,0),(-h,0,w),(h,0,w),(h,0,-w),(0,length,0),(-h,0,-w),(h,0,-w),(-h,0,-w),(-h,0,w)],name=name)
  if direction in ['z','-z'] : ctrl = cmds.curve(d=1,p=[(w,h,0),(0,0,length),(w,-h,0),(w,h,0),(-w,h,0),(0,0,length),(-w,-h,0),(-w,h,0),(-w,-h,0),(w,-h,0)],name=name)
  self.ctrlOptimize(name,a)
  
 def ctrlLocator(self,n,x,*a):
  x = x*0.5
  cmds.curve(d=1,p=[(0,x,0),(0,-x,0),(0,0,0),(x,0,0),(-x,0,0),(0,0,0),(0,0,x),(0,0,-x),(0,0,0),(0,0,0)],k=[0,1,2,3,4,5,6,7,8,9],name=n)
  self.ctrlOptimize(n,a)
  
 def ctrlCircle(self,name,radius,direction,*a): # direction = 0 or 1 or 2
  ce = 'curve -d 1 '
  i = 0
  while (i <= 20) :
   if direction == 0 : ce += " -p 0 " + str(math.cos(math.radians(18*i))*radius) + " " + str(math.sin(math.radians(18*i))*radius)
   if direction == 1 : ce += " -p " + str(math.cos(math.radians(18*i))*radius) + " 0 " + str(math.sin(math.radians(18*i))*radius)
   if direction == 2 : ce += " -p " + str(math.cos(math.radians(18*i))*radius) + " " + str(math.sin(math.radians(18*i))*radius) + " 0" 
   i = i + 1
  ce = ce + " -n " + name
  ctrl = mel.eval(ce)
  self.ctrlOptimize(name,a)

 def ctrlCircleH(self,name,radius,vector,startAngle,*a):
  sa = startAngle
  ce = 'curve -d 1 '
  i = 0
  while (i <= 10) :
   if vector == 0 : ce += " -p 0 " + str(math.cos(math.radians(18*i+sa))*radius) + " " + str(math.sin(math.radians(18*i+sa))*radius)
   if vector == 1 : ce += " -p " + str(math.cos(math.radians(18*i+sa))*radius) + " 0 " + str(math.sin(math.radians(18*i+sa))*radius)
   if vector == 2 : ce += " -p " + str(math.cos(math.radians(18*i+sa))*radius) + " " + str(math.sin(math.radians(18*i+sa))*radius) + " 0" 
   i = i + 1
  ce = ce + " -n " + name
  ctrl = mel.eval(ce)
  cmds.closeCurve(ctrl,constructionHistory=0,replaceOriginal=1)
  self.ctrlOptimize(name,a)
  
 def ctrlArc(self,radius,thickness,startAngle,sweep,width,vector,name,*a):
  s = sweep
  w = width
  r = radius
  t = thickness

  sTime = s/10+1
  sAngle = float(s) / (sTime-1)
  sTimeLoop = int(sTime*4+8)
  ce = 'curve -d 1 '
  i = 0
  adjI = -1
  adjW = w * 0.5

  while (i < sTimeLoop) :
   adjR = r
   phase = i / (sTimeLoop/4) ;
   if phase == 0 :
    adjI = i % (sTime+2)
    if adjI == sTime : adjR = r - t
    if adjI > (sTime-1) : adjI = sTime-1
    adjW = w * 0.5

   if phase == 1 :
    adjI = i % (sTime+2)
    wr = -0.5
    if adjI >= sTime : adjR = r - t
    if adjI == (sTime+1) : wr = 0.5
    if adjI > (sTime-1) : adjI = sTime-1
    adjI = (sTime-1) - adjI
    adjW = w * wr

   if phase == 2 :
    adjI = i % (sTime+2)
    if adjI == sTime : adjR = r + t
    if adjI > (sTime-1) : adjI = sTime - 1
    adjW = w * -.5
    adjR = adjR - t

   if phase == 3 :
    adjI = i % (sTime+2)
    wr = 0.5
    if adjI >= sTime : adjR = r + t
    if adjI == (sTime+1) : wr = -.5
    if adjI > (sTime-1) : adjI = sTime-1
    adjI = (sTime-1) - adjI
    adjW = w * wr
    adjR = adjR - t
  
   if vector < 0 : vector = 0
   if vector > 2 : vector = 2
   angle = startAngle + sAngle * adjI - (s*0.5)

   if vector == 0 : ce += " -p " + str(adjW) + " " + str(math.cos(math.radians(angle))*adjR) + " " + str(math.sin(math.radians(angle))*adjR)
   if vector == 1 : ce += " -p " + str(math.cos(math.radians(angle))*adjR) + " " + str(adjW) + " " + str(math.sin(math.radians(angle))*adjR)
   if vector == 2 : ce += " -p " + str(math.cos(math.radians(angle))*adjR) + " " + str(math.sin(math.radians(angle))*adjR) + " " + str(adjW)
   i = i + 1

  while (i < sTimeLoop) :
   ce = ce + ' -k ' + i ;
   i = i + 1
  ce = ce + " -n " + name ;
  ctrl = mel.eval(ce)

  nc = cmds.listRelatives(ctrl,type='nurbsCurve')[0]
  cmds.rename(nc,ctrl+'Shape')
  if len(a) == 0 :
   cmds.createNode('transform',name=name+'_trans')
   cmds.parent(name,name+'_trans')
  else :
   self.ctrlOptimize(name,a)

 def ctrlStar(self,name,radius,direction,*a):
  r = radius
  x = [0,r*0.866025,r*-0.866025,0,r*0.288658,r*0.866025,0,r*-0.866025,r*0.288658]
  y = [r,r*-0.5,r*-0.5,r,r*0.49997,r*0.5,r*-1,r*0.5,r*0.49997]
  z = [0,0,0,0,0,0,0,0,0]
  if direction == 0 : temp = y[:] ; y = z[:] ; z = temp[:]
  if direction == 2 : temp = x[:] ; x = z[:] ; z = y[:] ; y = temp[:]
  cmds.curve(degree=1,p=[(x[0],z[0],y[0]),(x[1],z[1],y[1]),(x[2],z[2],y[2]),(x[3],z[3],y[3]),(x[4],z[4],y[4]),(x[5],z[5],y[5]),(x[6],z[6],y[6]),(x[7],z[7],y[7]),(x[8],z[8],y[8])],k=[0,1,2,3,4,5,6,7,8],name=name)
  self.ctrlOptimize(name,a)

 def ctrlCrystal(self,name,height,weight,*a):
  h = height ; w = weight
  cmds.curve(d=1,p=[(-w,0,0),(0,h,0),(0,0,w),(0,-h,0),(w,0,0),(0,h,0),(0,0,-w),(0,-h,0),(-w,0,0),(0,0,w),(w,0,0),(0,0,-w),(-w,0,0)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12],name=name)
  self.ctrlOptimize(name,a)

 def ctrlPaper(self,name,radius,offset,vector,*a): 
  angle = math.degrees(math.asin(offset))
  vn = int(math.ceil(angle/10)) # vertex number
  pa = angle / vn
  s = 0
  if vector in ['+x','-y','-z'] : s = 180
  ce = 'curve -d 1 '
  if vector in ['+x','-x'] :
   for i in range(vn*2) : ce += " -p " + str(math.sin(math.radians(angle-pa*i))) + " " + str(offset) + " " + str(math.cos(math.radians(angle-pa*i+s)))
   for i in range(vn*2) : ce += " -p " + str(-offset) + " " + str(math.sin(math.radians(angle-pa*i))) + " " + str(math.cos(math.radians(angle-pa*i+s)))
   for i in range(vn*2) : ce += " -p " + str(math.sin(math.radians(-angle+pa*i))) + " " + str(-offset) + " " + str(math.cos(math.radians(-angle+pa*i+s)))
   for i in range(vn*2) : ce += " -p " + str(offset) + " " + str(math.sin(math.radians(-angle+pa*i))) + " " + str(math.cos(math.radians(-angle+pa*i+s)))
  if vector in ['+y','-y'] :
   for i in range(vn*2) : ce += " -p " + str(math.sin(math.radians(angle-pa*i))) + " " + str(math.cos(math.radians(angle-pa*i+s))) + " " + str(offset)
   for i in range(vn*2) : ce += " -p " + str(-offset) + " " + str(math.cos(math.radians(angle-pa*i+s))) + " " + str(math.sin(math.radians(angle-pa*i)))
   for i in range(vn*2) : ce += " -p " + str(math.sin(math.radians(-angle+pa*i))) + " " + str(math.cos(math.radians(-angle+pa*i+s))) + " " + str(-offset)
   for i in range(vn*2) : ce += " -p " + str(offset) + " " + str(math.cos(math.radians(-angle+pa*i+s))) + " " + str(math.sin(math.radians(-angle+pa*i)))
  if vector in ['+z','-z'] :
   for i in range(vn*2) : ce += " -p " + str(math.cos(math.radians(angle-pa*i+s))) + " " + str(math.sin(math.radians(angle-pa*i))) + " " + str(offset)
   for i in range(vn*2) : ce += " -p " + str(math.cos(math.radians(angle-pa*i+s))) + " " + str(-offset) + " " + str(math.sin(math.radians(angle-pa*i)))
   for i in range(vn*2) : ce += " -p " + str(math.cos(math.radians(-angle+pa*i+s))) + " " + str(math.sin(math.radians(-angle+pa*i))) + " " + str(-offset)
   for i in range(vn*2) : ce += " -p " + str(math.cos(math.radians(-angle+pa*i+s))) + " " + str(offset) + " " + str(math.sin(math.radians(-angle+pa*i)))
  ce = ce + " -n " + name ;
  ctrl = mel.eval(ce)
  cmds.closeCurve(ctrl,constructionHistory=0,replaceOriginal=1)
  self.ctrlScale(ctrl,radius)
  self.ctrlOptimize(name,a)
  
 def ctrlSquareRC(self,name,width,height,dir,*a): # use for torso around
  w = width*0.5 ; h = height*0.5
  s = min(width,height)/3.0
  if dir == 0 : cmds.curve(d=3,p=[(0,h,w-s),(0,h,w),(0,h-s,w),(0,-h+s,w),(0,-h,w),(0,-h,w-s),(0,-h,-w+s),(0,-h,-w),(0,-h+s,-w),(0,h-s,-w),(0,h,-w),(0,h,-w+s)],name=name)
  if dir == 1 : cmds.curve(d=3,p=[(w-s,0,h),(w,0,h),(w,0,h-s),(w,0,-h+s),(w,0,-h),(w-s,0,-h),(-w+s,0,-h),(-w,0,-h),(-w,0,-h+s),(-w,0,h-s),(-w,0,h),(-w+s,0,h)],name=name)
  if dir == 2 : cmds.curve(d=3,p=[(w-s,h,0),(w,h,0),(w,h-s,0),(w,-h+s,0),(w,-h,0),(w-s,-h,0),(-w+s,-h,0),(-w,-h,0),(-w,-h+s,0),(-w,h-s,0),(-w,h,0),(-w+s,h,0)],name=name)
  cmds.closeCurve(name,constructionHistory=0,replaceOriginal=1)
  self.ctrlOptimize(name,a)
  
 def ctrlHexagon(self,name,width,height,thickness,direction,*a): # use for chest
  wd = width * 0.5 ; ht = height * 0.5 ; tkn = thickness * 0.5 ; pList = []
  xo = 0.5 ; zo = 0.866 # standard x Offset and z offset
  x = [wd*xo,wd,wd,wd*xo,wd*xo,wd*-xo,wd*-xo,-wd,-wd,wd*-xo,wd*-xo,wd*xo,wd*xo,wd*-xo,wd*-xo,-wd,-wd,wd*-xo,wd*-xo,wd*xo,wd*xo,wd,wd,wd*xo]
  y = [ht,ht,-ht,-ht,ht,ht,-ht,-ht,ht,ht,-ht,-ht,ht,ht,-ht,-ht,ht,ht,-ht,-ht,ht,ht,-ht,-ht]
  z = [tkn*-zo,0,0,tkn*zo,tkn*zo,tkn*zo,tkn*zo,0,0,tkn*-zo,tkn*-zo,tkn*-zo,tkn*-zo,tkn*-zo,tkn*-zo,0,0,tkn*zo,tkn*zo,tkn*zo,tkn*zo,0,0,tkn*-zo]
  if direction == 'x' : temp = x[:] ; x = y[:] ; y = temp[:]
  if direction == 'z' : temp = y[:] ; y = z[:] ; z = temp[:]
  for i in range(len(x)): pList.append((x[i],y[i],z[i]))
  cmds.curve(degree=1,p=pList,k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],name=name)
  self.ctrlOptimize(name,a)
  
 def ctrlPrism(self,name,width,height,thickness,direction,*a): # use for pelvis
  width = width * 0.5 ; tkn = thickness * 0.5 ; pList = []
  if direction in ['-x','-y','-z'] : height = height * -1
  x = [-width,0,0,width,width,-width,-width,width,width,0,0,-width]
  y = [0,height,height,0,0,0,0,0,0,height,height,0]
  z = [tkn,tkn,-tkn,-tkn,tkn,tkn,-tkn,-tkn,tkn,tkn,-tkn,-tkn]
  if direction in ['x','+x','-x'] : temp = x[:] ; x = y[:] ; y = temp[:]
  if direction in ['z','+z','-z'] : temp = y[:] ; y = z[:] ; z = temp[:]
  for i in range(len(x)): pList.append((x[i],y[i],z[i]))
  cmds.curve(degree=1,p=pList,k=[0,1,2,3,4,5,6,7,8,9,10,11],name=name)
  self.ctrlOptimize(name,a)
  
 def ctrlOptimize(self,ctrl,aInput,*a):
  nc = cmds.listRelatives(ctrl,type='nurbsCurve')[0]
  #cmds.rename(nc,ctrl+'Shape')
  cmds.rename(nc,ctrl.replace('ctrl_','ctrlShape_'))
  if cmds.objExists('ctrlSet') == 0 : cmds.createNode('objectSet',name='ctrlSet',skipSelect=1)
  try :
   for x in cmds.listAnimatable(ctrl.replace('ctrl_','ctrlShape_')):
    cmds.setAttr(x,keyable=0,channelBox=0)
  except : pass
  if len(aInput) > 0 :
   if aInput[0] == 0 : pass
   if aInput[0] == 1 :
    t = cmds.createNode('transform',name=ctrl.replace('ctrl_','ctrlTrans_'))
    cmds.parent(ctrl,t)
   if aInput[0] == 2 :
    t = cmds.createNode('transform',name=ctrl.replace('ctrl_','ctrlTrans_'))
    t = cmds.createNode('transform',name=ctrl.replace('ctrl_','ctrlCons_'),parent=t)
    cmds.parent(ctrl,t)
   if aInput[0] == 3 :
    t = cmds.createNode('transform',name=ctrl.replace('ctrl_','ctrlTrans_'))
    t = cmds.createNode('transform',name=ctrl.replace('ctrl_','ctrlCons_'),parent=t)
    t = cmds.createNode('transform',name=ctrl+'_P',parent=t)
    cmds.parent(ctrl,t)
   if len(aInput) > 1 :
    if type(aInput[1]) == list :
     self.ctrlAttrPara(ctrl,aInput[1])
     if aInput[0] == 3 : self.ctrlAttrPara(ctrl+'_P',aInput[1])
    if type(aInput[2]) == list : self.ctrlColor(ctrl,aInput[2])
  cmds.sets(ctrl,e=1,addElement='ctrlSet')
  
  if self.ctrlPos.get(ctrl[5:]) != None :
   cmds.addAttr(ctrl,longName='warAnim_shape',dt='string')
   cmds.addAttr(ctrl,longName='warAnim_x',attributeType='long')
   cmds.addAttr(ctrl,longName='warAnim_y',attributeType='long')
   cmds.addAttr(ctrl,longName='warAnim_ro',attributeType='double')
   cmds.addAttr(ctrl,longName='warAnim_sx',attributeType='double')
   cmds.addAttr(ctrl,longName='warAnim_sy',attributeType='double')
   cmds.addAttr(ctrl,longName='warAnim_r',attributeType='double')
   cmds.addAttr(ctrl,longName='warAnim_g',attributeType='double')
   cmds.addAttr(ctrl,longName='warAnim_b',attributeType='double')
   cmds.setAttr(ctrl+'.warAnim_shape',self.ctrlPos[ctrl[5:]][0],type='string')
   #
   if type(self.ctrlPos[ctrl[5:]][1]) == list :
    orderList = self.ctrlPos[ctrl[5:]][1]
    cmds.addAttr(ctrl,ln='warAlignObj',at='enum',en=orderList[0]+':',keyable=1)
    cmds.setAttr(ctrl+'.warAnim_x',0)
   else : cmds.setAttr(ctrl+'.warAnim_x',self.ctrlPos[ctrl[5:]][1])
   if type(self.ctrlPos[ctrl[5:]][2]) == str :
    cmds.addAttr(ctrl,ln='warAlignObj',at='string',en=orderList[0]+':',keyable=1)
    
   else: cmds.setAttr(ctrl+'.warAnim_y',self.ctrlPos[ctrl[5:]][2])
   cmds.setAttr(ctrl+'.warAnim_ro',self.ctrlPos[ctrl[5:]][3])
   cmds.setAttr(ctrl+'.warAnim_sx',self.ctrlPos[ctrl[5:]][4])
   cmds.setAttr(ctrl+'.warAnim_sy',self.ctrlPos[ctrl[5:]][5])

 def ctrlOffset(self,ctrl,value,*a):
  nc = cmds.listRelatives(ctrl,type='nurbsCurve')[0]
  s = cmds.getAttr(ctrl+'.spans')+1
  f = cmds.getAttr(ctrl+'.f') ; d = cmds.getAttr(ctrl+'.degree')
  if f == 2 and d == 3 : s = s-1
  for i in range(s) :
   pos = cmds.xform(ctrl+'.cv['+str(i)+']',q=1,objectSpace=1,translation=1)
   cmds.xform(ctrl+'.cv['+str(i)+']',objectSpace=1,translation=[pos[0]+value[0],pos[1]+value[1],pos[2]+value[2]])
  
 def ctrlScale(self,ctrl,rate,*a):
  nc = cmds.listRelatives(ctrl,type='nurbsCurve')[0]
  s = cmds.getAttr(ctrl+'.spans')
  for i in range(s) :
   pos = cmds.xform(ctrl+'.cv['+str(i)+']',q=1,objectSpace=1,translation=1)
   cmds.xform(ctrl+'.cv['+str(i)+']',objectSpace=1,translation=[pos[0]*rate,pos[1]*rate,pos[2]*rate])

 def xCons(self,so,do,*a): # dMatrix Constraint
  dos = do.split('_',1)
  xn = 'xCons_' + dos[1] # matrix name
  gn = 'xTrans_' + dos[1] # group name
  if cmds.objExists(gn) == 0 :
   cmds.createNode('transform',name=gn,parent='grp_deformer',skipSelect=1)
   xd = cmds.createNode('decomposeMatrix',name=xn,skipSelect=1)
   cmds.connectAttr(so+'.worldMatrix[0]',xd+'.inputMatrix')
   cmds.connectAttr(xd+'.outputTranslate',do+'.translate')
   cmds.connectAttr(xd+'.outputRotate',do+'.rotate')
   cmds.connectAttr(xd+'.outputScale',do+'.scale')
   cmds.connectAttr(xd+'.outputShear',do+'.shear')

 def consCheck(self,n,*a):
  dict = {'wristL':self.wristJo[0],'wristR':self.wristJo[1],'hipL':self.hipJo[0],'hipR':self.hipJo[1],'ankleL':self.ankleJo[0],'ankleR':self.ankleJo[1]}
  dict['armL'] = self.armJo[0] ; dict['armR'] = self.armJo[1] ; dict['shoulderL'] = self.shoulderJo[0] ; dict['shoulderR'] = self.shoulderJo[1]
  dict['elbowL'] = self.elbowJo[0] ; dict['elbowR'] = self.elbowJo[1] ; dict['kneeL'] = self.kneeJo[0] ; dict['kneeR'] = self.L2R(self.kneeJo[0])
  dict['pelvis'] = self.pelvisJo ; dict['root'] = self.rootJo ; dict['viceShoulderL'] = self.shoulder2Jo[0] ; dict['viceElbowL'] = self.elbow2Jo[0]
  dict['viceShoulderR'] = self.L2R(self.shoulder2Jo[0]) ; dict['viceElbowR'] = self.L2R(self.elbow2Jo[0]) ; dict['head'] = self.headJo
  dict['neck2'] = self.L2R(self.neckJo[2]) ; dict['rearPelvis'] = self.rearPelvisJo ; dict['rearKneeL'] = self.rearKneeJo ; dict['rearKneeR'] = self.L2R(self.rearKneeJo)
  dict['neck'] = self.L2R(self.neckJo[0]) ; dict['neck1'] = self.L2R(self.neckJo[1])
  
  if n == 'pelvisR' :
   self.consCheck('pelvis')
   if cmds.objExists('pin_'+n) == 0 :
    cmds.createNode('transform',name='pin_'+n,parent='xTrans_pelvis',skipSelect=1)
    cmds.setAttr('pin_'+n+'.rotateX',-180)
    self.ctrlAttrPara('pin_'+n,[0,0,0,0,0,0,0,0,0,1])
   dict['pelvisR'] = 'pin_'+n
   
  if n == 'rearPelvisR' :
   self.consCheck('rearPelvis')
   if cmds.objExists('pin_'+n) == 0 :
    cmds.createNode('transform',name='pin_'+n,parent='xTrans_rearPelvis',skipSelect=1)
    cmds.setAttr('pin_'+n+'.rotateX',-180)
    self.ctrlAttrPara('pin_'+n,[0,0,0,0,0,0,0,0,0,1])
   dict['rearPelvisR'] = 'pin_'+n
  
  if type(n) == str or type(n) == unicode :
   if cmds.objExists('xTrans_'+n)==0:
    #cmds.createNode('transform',name='xTrans_'+n,parent='grp_deformer',skipSelect=1)
    self.xCons(dict[n],'xTrans_'+n)
    return 'xTrans_'+n
  if type(n) == list :
   xn = []
   for x in n :
    if cmds.objExists('xTrans_'+x)==0:
     #cmds.createNode('transform',name='xTrans_'+x,parent='grp_deformer',skipSelect=1)
     self.xCons(dict[x],'xTrans_'+x)
     xn.append('xTrans_'+x)
   return xn
    
 def connectKneeOffset(self,n,jo,*a):
  cmds.addAttr('exp_'+n,longName='offsetWeight',attributeType='double',defaultValue=0,keyable=1)
  cmds.createNode('multiplyDivide',name='mult_'+n,skipSelect=1)
  cmds.connectAttr(jo+'.rotate','mult_'+n+'.input1')
  cmds.connectAttr('exp_'+n+'.offsetWeight','mult_'+n+'.input2X')
  cmds.connectAttr('exp_'+n+'.offsetWeight','mult_'+n+'.input2Y')
  cmds.connectAttr('exp_'+n+'.offsetWeight','mult_'+n+'.input2Z')
  cmds.connectAttr('mult_'+n+'.output','exp_'+n+'.rotate')

 def fingerPosePreset(self,*a): # create finger pose preset
  poseList = ['straight','fist','scrunch']
  if cmds.objExists('grp_fingerPoseJo') == 0 :
   self.consCheck('wristL')
   cmds.createNode('transform',name='grp_fingerPoseJo',parent='xTrans_wristL')
   cmds.duplicate(self.wristJo[0],name='straight_wristL')
   cmds.duplicate(self.wristJo[0],name='fist_wristL')
   cmds.duplicate(self.wristJo[0],name='scrunch_wristL')
   cmds.parent('straight_wristL','grp_fingerPoseJo')
   cmds.parent('fist_wristL','grp_fingerPoseJo')
   cmds.parent('scrunch_wristL','grp_fingerPoseJo')

   cmds.setAttr('straight_wristL.t',0,3,3)
   afp = cmds.listRelatives('straight_wristL',allDescendents=1,fullPath=1)
   af = cmds.listRelatives('straight_wristL',allDescendents=1)
   for i in range(len(af)) :
    sa = af[i].split('_')
    nn = 'straight_'+sa[1]
    nn = nn[:-1]
    cmds.rename(afp[i],nn)
    self.ctrlAttrPara(nn,[0,0,0,1,1,1,1,1,1,0])
    cmds.setAttr(nn+'.rx',0)
    cmds.setAttr(nn+'.ry',0)
    cmds.setAttr(nn+'.rz',0)
   cmds.setAttr('straight_thumb0.rx',45)

   cmds.setAttr('fist_wristL.t',0,3,0)
   afp = cmds.listRelatives('fist_wristL',allDescendents=1,fullPath=1)
   af = cmds.listRelatives('fist_wristL',allDescendents=1)
   for i in range(len(af)) :
    sa = af[i].split('_')
    nn = 'fist_'+sa[1]
    nn = nn[:-1]
    cmds.rename(afp[i],nn)
    self.ctrlAttrPara(nn,[0,0,0,1,1,1,1,1,1,0])
    if '1' in nn : cmds.setAttr(nn+'.rz',-85)
    if '2' in nn : cmds.setAttr(nn+'.rz',-100)
    if '3' in nn : cmds.setAttr(nn+'.rz',-65)
   cmds.setAttr('fist_thumb0.rx',2.5)
   cmds.setAttr('fist_thumb1.rz',-30)
   cmds.setAttr('fist_thumb1.rz',-80)

   cmds.setAttr('scrunch_wristL.t',0,3,-3)
   afp = cmds.listRelatives('scrunch_wristL',allDescendents=1,fullPath=1)
   af = cmds.listRelatives('scrunch_wristL',allDescendents=1)
   for i in range(len(af)) :
    sa = af[i].split('_')
    nn = 'scrunch_'+sa[1]
    nn = nn[:-1]
    cmds.rename(afp[i],nn)
    self.ctrlAttrPara(nn,[0,0,0,1,1,1,1,1,1,0])
    if '1' in nn : cmds.setAttr(nn+'.rz',30)
    if '2' in nn : cmds.setAttr(nn+'.rz',-90)
    if '3' in nn : cmds.setAttr(nn+'.rz',-45)
   cmds.setAttr('straight_thumb0.rx',45)
  else :
   ls = cmds.ls(selection=1)
   if len(ls) > 0 :
    ls = cmds.ls(selection=1)[-1]
    poseInList = cmds.listRelatives('grp_fingerPoseJo',allDescendents=1,type='joint')
    if ls in poseInList :
     lsSp = ls.split('_')
     finName = ['thumb0','thumb1','thumb2','index0','index1','index2','index3','middle0','middle1','middle2','middle3','ring0','ring1','ring2','ring3','little0','little1','little2','little3']
     finJo = [self.thumbJo[0],self.thumbJo[1],self.thumbJo[2],self.indexJo[0],self.indexJo[1],self.indexJo[2],self.indexJo[3],self.middleJo[0],self.middleJo[1],self.middleJo[2],self.middleJo[3],self.ringJo[0],self.ringJo[1],self.ringJo[2],self.ringJo[3],self.littleJo[0],self.littleJo[1],self.littleJo[2],self.littleJo[3]]
     ti = cmds.playbackOptions(q=1,minTime=1)
     ta = cmds.playbackOptions(q=1,maxTime=1)
     for i in range(len(finName)) :
      attrForm = lsSp[0]+'_'+finName[i]
      cmds.setKeyframe(finJo[i],time=ti,attribute='rotateX',value=cmds.getAttr(finJo[i]+'.preferredAngleX'))
      cmds.setKeyframe(finJo[i],time=ta,attribute='rotateX',value=cmds.getAttr(attrForm+'.rotateX'))
      cmds.setKeyframe(finJo[i],time=ti,attribute='rotateY',value=cmds.getAttr(finJo[i]+'.preferredAngleY'))
      cmds.setKeyframe(finJo[i],time=ta,attribute='rotateY',value=cmds.getAttr(attrForm+'.rotateY'))
      cmds.setKeyframe(finJo[i],time=ti,attribute='rotateZ',value=cmds.getAttr(finJo[i]+'.preferredAngleZ'))
      cmds.setKeyframe(finJo[i],time=ta,attribute='rotateZ',value=cmds.getAttr(attrForm+'.rotateZ'))
    else :
     cmds.showHidden('grp_fingerPoseJo',above=1)
   else :
    cmds.showHidden('grp_fingerPoseJo',above=1)

 def legRotatePreset(self,*a): # create leg ctrl rotate pivot preset locator
  if cmds.objExists('grp_legRotatePivotL') == 0 and cmds.objExists(self.toeJo[0]) :
   self.consCheck(['ankleL','ankleR'])
   cmds.createNode('transform',name='grp_legRotatePivotL',parent='xTrans_ankleL',skipSelect=1)
   cmds.createNode('transform',name='grp_legRotatePivotR',parent='xTrans_ankleR',skipSelect=1)
   cmds.setAttr('grp_legRotatePivotR.rx',-180)
   self.ctrlLocator('pv_tipToeL',1)
   self.ctrlLocator('pv_tipToeR',1)
   self.ctrlLocator('pv_tipHeelL',1)
   self.ctrlLocator('pv_tipHeelR',1)
   cmds.parent('pv_tipToeL','grp_legRotatePivotL')
   cmds.parent('pv_tipToeR','grp_legRotatePivotR')
   cmds.parent('pv_tipHeelL','grp_legRotatePivotL')
   cmds.parent('pv_tipHeelR','grp_legRotatePivotR')
   x = cmds.xform(self.toeJo[0],q=1,ws=1,t=1)
   cmds.xform('pv_tipToeL',t=[x[0],0,x[2]],ws=1)
   cmds.connectAttr('pv_tipToeL.t','pv_tipToeR.t')
   cmds.setAttr('pv_tipHeelL.tx',cmds.getAttr('pv_tipToeL.tx'))
   cmds.setAttr('pv_tipHeelL.tz',cmds.getAttr('pv_tipToeL.tz')*-.45)
   cmds.connectAttr('pv_tipHeelL.t','pv_tipHeelR.t')
   self.ctrlAttrPara('pv_tipToeL',[1,1,1,0,0,0,0,0,0,0])
   self.ctrlAttrPara('pv_tipToeR',[1,1,1,0,0,0,0,0,0,0])
   self.ctrlAttrPara('pv_tipHeelL',[1,1,1,0,0,0,0,0,0,0])
   self.ctrlAttrPara('pv_tipHeelR',[1,1,1,0,0,0,0,0,0,0])
  elif cmds.objExists('grp_legRotatePivotL') == 0 and cmds.objExists(self.bigToeJo[0]) :
   #for s in ['L','R'] :
   # self.consCheck(['ankle'+s])
   # cmds.curve(d=3,p=[(0,0,2),(0,0,1),(0,0,0),(0,0,-1),(0,0,-2)],name='crv_heelPivotBack'+s)
   # cmds.curve(d=3,p=[(0,0,-2),(0,0,-1),(0,0,0),(0,0,1),(0,0,2)],name='crv_heelPivotFront'+s)
   # cmds.createNode('transform',name='grp_legRotatePivot'+s,parent='xTrans_ankle'+s,skipSelect=1)
   # cmds.parent('crv_heelPivotBack'+s,'grp_legRotatePivot'+s,relative=1)
   # cmds.parent('crv_heelPivotFront'+s,'grp_legRotatePivot'+s,relative=1)
   self.consCheck(['ankleL'])
   cmds.curve(d=3,p=[(0,0,2),(0,0,1),(0,0,0),(0,0,-1),(0,0,-2)],name='crv_heelPivotBack')
   cmds.curve(d=3,p=[(0,0,-2),(0,0,-1),(0,0,0),(0,0,1),(0,0,2)],name='crv_heelPivotFront')
   cmds.createNode('transform',name='grp_legRotatePivotL',parent='xTrans_ankleL',skipSelect=1)
   cmds.parent('crv_heelPivotBack','grp_legRotatePivotL',relative=1)
   cmds.parent('crv_heelPivotFront','grp_legRotatePivotL',relative=1)
  else :
   cmds.showHidden('grp_legRotatePivotL',above=1)

 def legPivotCirclePreset(self,ch,*a):  
  joList = [self.ankleJo[0],self.wristJo[0]]
  nameList = ['heel','wrist']
  consList = ['ankleL','wristL']
  crvList = [ 'crv_'+x+'PivotCircle' for x in nameList ]
  ch = self.chDefine()[0]
  self.defineBType()
  
  for i in range(len(joList)) :
   if cmds.objExists(joList[i]) == 1 and cmds.objExists(crvList[i]) == 0 :
    bType = '' ; bLen = int(0) ; circlePivot = []
    ad = cmds.listRelatives(joList[i],allDescendents=1,type='joint')
    for y in self.bTypeDic[joList[i]] :
     if self.existCompare(y[1],ad) and bLen < len(y[1]) :
      bType = y[0] ; bLen = 0+len(y[1])
      if bType == 'shoe' : circlePivot = [joList[i],y[1][0]]
      if bType in ['paw','palm'] : circlePivot = [y[1][5],y[1][9],y[1][13],y[1][17]]
      if bType == 'toe' : circlePivot = [y[1][5],y[1][9],y[1][13],y[1][17]]
    self.consCheck(consList[i])
    cc = cmds.curve(d=3,p=[(0,0,ch*0.51),(ch*0.19,0,ch*0.383),(ch*0.137,0,0),(ch*0.126,0,ch*-0.337),(0,0,ch*-0.436),(ch*-0.122,0,ch*-0.34),(ch*-0.154,0,0),(ch*-0.247,0,ch*0.613)],name=crvList[i])
    cmds.closeCurve(cc,constructionHistory=0,preserveShape=0,replaceOriginal=1)
    cmds.parent(cc,'xTrans_'+consList[i],relative=1)
    if len(circlePivot) > 0 : cmds.delete(cmds.pointConstraint(circlePivot,cc))
    cmds.move(0,cc,worldSpace=1,moveY=1)
   else :
    cmds.showHidden(crvList[i],above=1)

 def createCtrlParameter(self,ch,*a):
  self.consCheck('root')
  if cmds.objExists('ctrlParameter')==0 :
   ch = 175.0
   if cmds.objExists('topAdj') : ch = cmds.xform('topAdj',q=1,ws=1,t=1)[1]
   self.ctrlStar('ctrlParameter',ch*0.07,0,0,[0,0,0,0,0,0,0,0,0,0],[0.015,0.015,0.015])
   self.ctrlOffset('ctrlParameter',[0,ch*-.25,ch*-.32])
   cmds.parent('ctrlParameter','xTrans_root')
  else : cmds.select('ctrlParameter',replace=1)
  
  xistList = [self.rootJo,self.headJo,self.neckJo[0],self.shoulderJo,self.shoulderJo]
  attrList = ['torsoCtrlScale','headCtrlScale','neckCtrlScale','shoulderCtrlScale','shoulderCtrlOffset']
  typeList = ['double','double','double','double','double']
  
  xistList += [self.chestJo]
  attrList += ['chestCtrlScale']
  typeList += ['double']
  
  xistList += [self.armJo[0],self.thumbJo[0]]
  attrList += ['armCtrlScale','fingerCtrlScale']
  typeList += ['double','double']
  
  xistList += [self.ankleJo[0]]
  attrList += ['heelCtrlOffset']
  typeList += ['double']

  xistList += [self.wristJo[0],self.wristJo[0]]
  attrList += ['fkCtrlNulling','ikCtrlNulling']
  typeList += ['bool','bool']
  
  xistList += [self.uplidJo[0],self.thirdLidJo[0]]
  attrList += ['upperLidOpenRotate','thirdUpLidOpenRotate']
  typeList += ['double','double']
  
  for i in range(len(xistList)):
   if self.exCheck(xistList[i])==1 and cmds.objExists('ctrlParameter.'+attrList[i])==0 :
    df = 0
    if attrList[i][-5:]=='Scale': df = 1
    cmds.addAttr('ctrlParameter',longName=attrList[i],attributeType=typeList[i],defaultValue=df,keyable=1)
  else:
   pass
	
 def ctrlDefaultRotate(self,ctrl,*a):
  ro = cmds.getAttr(ctrl+'.rotate')
  if ro[0][0] > 0.0004 or ro[0][0] < -.0004 or ro[0][1] > 0.0004 or ro[0][1] < -.0004 or ro[0][2] > 0.0004 or ro[0][2] < -.0004 :
   #cmds.createNode('transform',name=ctrl+'_dro',parent=ctrl)
   cmds.createNode('transform',name='ctrlDro_'+ctrl[5:],parent=ctrl)
   p = cmds.listRelatives(ctrl,parent=1,children=1)[0]
   #cmds.parent(ctrl+'_dro',p)
   cmds.parent('ctrlDro_'+ctrl[5:],p)
   #self.ctrlAttrPara(ctrl+'_dro',[0,0,0,1,1,1,0,0,0,0])
   self.ctrlAttrPara('ctrlDro_'+ctrl[5:],[0,0,0,1,1,1,0,0,0,0])
   #cmds.setAttr(ctrl+'_dro.rotate',lock=1)
   cmds.setAttr('ctrlDro_'+ctrl[5:]+'.rotate',lock=1)

 def fileSaveAs(self,*a): # Unuse now.. Save As finction
  fn = cmds.file(q=1,sceneName=1)
  fna = fn.rsplit('/')
  fns = cmds.file(q=1,sceneName=1,shortName=1)
  fnsa = fns.rsplit('_')  
  mm = ''
  for i in range(len(fna)-1) :
    mm = mm + fna[i] + '/'
  for i in range(len(fnsa)-1) :
    mm = mm + fnsa[i] + '_'
  mm = mm + 'rig' + '.ma'
  cmds.file(rename=mm)
  cmds.file(save=1,type='mayaAscii')

 def L2R(self,jo,*a): # \d is match the number
  ruleL = 'jl[A-Z]\d+_[a-zA-Z0-9]+L'
  #ruleL = 'jo_[a-zA-Z0-9]+L'
  norL = '[a-zA-Z]+_[a-zA-Z0-9]+L'
  rjo = jo[:]
  if type(jo) == str :   
   if len(re.findall(ruleL,jo)) > 0 :
    rjo = rjo[:-1]+'R'
    rjo = 'jr'+rjo[2:]
   if len(re.findall(norL,jo)) > 0 :
    rjo = rjo[:-1]+'R'
  elif type(jo) == list :
   for i,x in enumerate(jo) :
    if len(re.findall(ruleL,x)) > 0 :
     rjo[i] = rjo[i][:-1]+'R'
     rjo[i] = 'jr'+rjo[i][2:]
    if len(re.findall(norL,x)) > 0 :
     rjo[i] = rjo[i][:-1]+'R'
  if len(a)>0 and a[0]==0 : return jo
  else : return rjo

 def joBelong(self,jo,*a):
  ruleC = 'jc[A-Z]\d+_[a-zA-Z0-9]' 
  #ruleL = 'jl[A-Z]\d+_[a-zA-Z0-9]+L' 
  #ruleR = 'jr[A-Z]\d+_[a-zA-Z0-9]+R'
  ruleL = 'jo_[a-zA-Z0-9]+L'
  ruleR = 'jo_[a-zA-Z0-9]+R'
  if len(re.findall(ruleL,jo)) > 0 : return 'L'
  elif len(re.findall(ruleR,jo)) > 0 : return 'R'
  elif len(re.findall(ruleC,jo)) > 0 : return 'C'
  else : return ''
  
 def distance(self,t1,t2,*a):
  x1 = cmds.xform(t1,q=1,ws=1,t=1)
  x2 = cmds.xform(t2,q=1,ws=1,t=1)
  dis = math.pow(x1[0]-x2[0],2) + math.pow(x1[1]-x2[1],2) + math.pow(x1[2]-x2[2],2)
  dis = math.sqrt(dis)
  return dis
  
 def curveCtrled(self,name,ctrls,s,*a):
  pList = []
  for i in range(len(ctrls)) : pList.append((0,0,0))
  cmds.curve(d=3,p=pList,name=name)
  cmds.parent(name,ctrls[0],relative=1)
  cmds.rename(cmds.listRelatives(name,shapes=1)[0],name+'Shape')
  for i in range(1,len(ctrls)) :
   #cmds.createNode('addMatrix',name='mMult_'+ctrls[i],skipSelect=1)
   #cmds.connectAttr(ctrls[0]+'.worldInverseMatrix[0]','mMult_'+ctrls[i]+'.matrixIn[0]')
   #cmds.connectAttr(ctrls[i]+'.worldMatrix[0]','mMult_'+ctrls[i]+'.matrixIn[1]')
   #cmds.createNode('decomposeMatrix',name='dMat_'+ctrls[i],skipSelect=1)
   #cmds.connectAttr('mMult_'+ctrls[i]+'.matrixSum','dMat_'+ctrls[i]+'.inputMatrix')
   cmds.createNode('transform',name='v_'+ctrls[i]+'Cc',parent=ctrls[0],skipSelect=1)
   cmds.pointConstraint(ctrls[i],'v_'+ctrls[i]+'Cc')
   cmds.setAttr('v_'+ctrls[i]+'Cc.intermediateObject',1)
   #cmds.connectAttr('dMat_'+ctrls[i]+'.outputTranslate',name+'Shape.controlPoints['+str(i)+']')
   cmds.connectAttr('v_'+ctrls[i]+'Cc.translate',name+'Shape.controlPoints['+str(i)+']')
   #rCrv = cmds.rebuildCurve('gLine_'+part[0],name='gLine_'+part[0]+'Rebuild',rebuildType=1,constructionHistory=1,replaceOriginal=0,endKnots=1,keepRange=0,keepControlPoints=0 ,spans=20,degree=3)
   #cmds.parent(rCrv[0],hrc,relative=1)
   #cmds.setAttr(rCrv[1]+'.rebuildType',0)
   #cmds.setAttr('gLine_'+part[0]+'Rebuild.template',1)
   #cmds.setAttr('gLine_'+part[0]+'.v',0)
  if s == 1 : cmds.setAttr(name+'.template',1)
  if s == 2 : cmds.setAttr(name+'.v',0)
 
 def existCompare(self,listA,listB,*a):
  ex = 0
  for x in listA :
   xe = 0
   for y in listB :
    if y == x : xe = 1
   if xe == 1 : ex = ex +1
  if ex == len(listA) : return 1
  else : return 0
 
 def quatRot(self,jo,axis,*a):
  if cmds.objExists(jo+'.quatR'+axis)==0:
   e2q = cmds.createNode('eulerToQuat',name='e2q_'+jo.split('_')[1]+axis,skipSelect=1)
   cmds.connectAttr(jo+'.rotate',e2q+'.inputRotate')
   q2e = cmds.createNode('quatToEuler',name='q2e_'+jo.split('_')[1]+axis,skipSelect=1)
   cmds.connectAttr(e2q+'.outputQuat'+axis,q2e+'.inputQuat'+axis)
   cmds.connectAttr(e2q+'.outputQuatW',q2e+'.inputQuatW')
   cmds.addAttr(jo,longName='quat'+axis,attributeType='double',keyable=1)
   cmds.connectAttr(q2e+'.outputRotate'+axis,jo+'.quat'+axis)
   ga = cmds.getAttr(jo+'.quat'+axis)
   if round(ga)!=0 :
    cmds.addAttr(jo,longName='quat'+axis+'0',attributeType='double',keyable=1)
    add = cmds.createNode('addDoubleLinear',name='adl_'+jo[6:]+axis+'0',skipSelect=1)
    cmds.connectAttr(jo+'.quat'+axis,add+'.input1')
    cmds.setAttr(add+'.input2',ga*-1)
    cmds.connectAttr(add+'.output',jo+'.quat'+axis+'0')
 
 def assignHairCtrl(self,*a):
  sel = cmds.ls(selection=1)
  if cmds.objExists(sel[-1]+'.control') == 0 :
   cmds.addAttr(sel[-1],longName='control',attributeType='bool',keyable=1)
  for i in range(0,len(sel)-1):
   if cmds.objExists(sel[i]+'.controlled') == 0 :
    cmds.addAttr(sel[i],longName='controlled',attributeType='bool',keyable=1)
    cmds.connectAttr(sel[-1]+'.control',sel[i]+'.controlled')
 
 def ctrlOnCurve(self,*a):
  sl = cmds.ls(selection=1) ; oCtrlList = []
  for n,x in enumerate(sl):
   vn = cmds.getAttr(x+'.spans') + cmds.getAttr(x+'.degree')
   #hue = 0+((n%2)*0.5)+(n*0.025)
   hue = n * 0.05
   ci = cmds.createNode('curveInfo',skipSelect=1)
   cmds.connectAttr(x+'Shape.worldSpace[0]',ci+'.inputCurve')
   cnList = [] ; cvPr = [0] ; npocList = [] ; tagList = []
   grpA = cmds.createNode('transform',name=x.replace('crv_','grp_'),skipSelect=1)
   grpAb = cmds.createNode('transform',name=x.replace('crv_','abTrans_'),parent=grpA,skipSelect=1)
   grpCh = cmds.createNode('transform',name=x.replace('crv_','cons_')+'Head',parent=grpA,skipSelect=1)
   cmds.setAttr(grpAb+'.inheritsTransform',0)
   rPin = cmds.createNode('transform',name=x.replace('crv_','pin_')+'Root',skipSelect=1)
   cmds.parent(rPin,grpA)
   if cmds.objExists(self.headJo):
    cmds.parentConstraint(self.headJo,grpCh)
    cmds.scaleConstraint(self.headJo,grpCh)
   cmds.xform(rPin,t=cmds.xform(x+'.cv[0]',q=1,ws=1,t=1),ws=1,a=1)
   pin0 = cmds.createNode('transform',name='pin_'+x.replace('crv_','')+'0',parent=grpCh,skipSelect=1) # create cv 0 movement
   v0 = cmds.createNode('transform',name='v_'+x.replace('crv_','')+'0',parent=grpA,skipSelect=1)
   cmds.xform(pin0,t=cmds.xform(x+'.cv[0]',q=1,ws=1,t=1),ws=1,a=1)
   cmds.pointConstraint(pin0,v0)
   cmds.connectAttr(v0+'.translate',x+'Shape.controlPoints[0]')
   for i in range(1,vn): # create main ctrl
    cn = x.replace('crv_','')+str(i) ; cnList.append(cn)
    rgb = colorsys.hsv_to_rgb(hue,0.9,0.65)
    self.ctrlCrystal('ctrl_'+cn,2.5,2.5,2,[1,1,1,0,0,0,0,0,0,0],[rgb[0],rgb[1],rgb[2]])
    cmds.createNode('transform',name='ctrlFollow_'+cn,parent='ctrlTrans_'+cn,skipSelect=1)
    cmds.parent('ctrlCons_'+cn,'ctrlFollow_'+cn)
    cmds.createNode('controller',name='ctrlTag_'+cn,skipSelect=1) ; tagList.append('ctrlTag_'+cn)
    cmds.connectAttr('ctrl_'+cn+'.message','ctrlTag_'+cn+'.controllerObject')
    if i > 1 :
     cmds.connectAttr(tagList[-2]+'.prepopulate',tagList[-1]+'.prepopulate')
     cmds.connectAttr(tagList[-1]+'.parent',tagList[-2]+'.children[0]')
    cmds.createNode('joint',name='gJo_'+cn,parent='ctrl_'+cn,skipSelect=1)
    cmds.createNode('joint',name='gJo_'+cn+'Tip',parent='gJo_'+cn,skipSelect=1)
    cmds.setAttr('gJo_'+cn+'.radius',0) ; cmds.setAttr('gJo_'+cn+'.template',1) ; cmds.setAttr('gJo_'+cn+'Tip.radius',0)
    if i == 1 : cmds.pointConstraint(pin0,'gJo_'+cn+'Tip')
    else : cmds.pointConstraint('ctrl_'+cnList[-2],'gJo_'+cn+'Tip')
    cmds.xform('ctrlTrans_'+cn,t=cmds.xform(x+'.cv['+str(i)+']',q=1,ws=1,t=1),ws=1,a=1)
    cc = cmds.cluster(x+'Shape.controlPoints['+str(i)+']',name='cc_'+cn+str(i),relative=1)
    cmds.parent(cc[1],grpA) ; cmds.setAttr(cc[1]+'.v',0)
    cmds.pointConstraint('ctrl_'+cn,cc[1])
    npoc = cmds.createNode('nearestPointOnCurve',name='npoc_'+cn,skipSelect=1) ; npocList.append(npoc)
    cmds.connectAttr(x+'.worldSpace[0]',npoc+'.inputCurve')
    cmds.connectAttr(ci+'.controlPoints['+str(i)+']',npoc+'.inPosition')
    cvPr.append(cmds.getAttr(npoc+'.parameter'))
    if cmds.objExists(self.headJo):
     cmds.addAttr('ctrl_'+cn,longName='follow',attributeType='double',minValue=0,maxValue=1,defaultValue=1-cvPr[-1],keyable=1)  # main ctrl follow function
     cmds.createNode('transform',name='follow_'+cn,parent='ctrlTrans_'+cn,skipSelect=1)
     cmds.createNode('transform',name='pin_'+cn,parent='ctrlTrans_'+cn,skipSelect=1)
     cmds.parent('pin_'+cn,grpCh)
     cmds.pointConstraint('pin_'+cn,'follow_'+cn,name='pCons_'+cn)
     cmds.createNode('multiplyDivide',name='mult_'+cn+'Follow',skipSelect=1)
     cmds.connectAttr('follow_'+cn+'.translate','mult_'+cn+'Follow.input1')
     cmds.connectAttr('ctrl_'+cn+'.follow','mult_'+cn+'Follow.input2X')
     cmds.connectAttr('ctrl_'+cn+'.follow','mult_'+cn+'Follow.input2Y')
     cmds.connectAttr('ctrl_'+cn+'.follow','mult_'+cn+'Follow.input2Z')
     cmds.connectAttr('mult_'+cn+'Follow.output','ctrlFollow_'+cn+'.translate')

    cmds.parent('ctrlTrans_'+cn,grpA)
   cmds.delete(npocList)
   self.ctrlScale('ctrl_'+cnList[-1],1.5)
   oCtrlList.append('ctrlTrans_'+cnList[-1]) # prepare after main ctrl
   cmds.addAttr('ctrl_'+cnList[-1],longName='stretchy',attributeType='double',minValue=0,maxValue=1,keyable=1)
   cmds.addAttr('ctrl_'+cnList[-1],longName='subCtrl',attributeType='bool',keyable=1)
   cmds.createNode('transform',name='ctrlVTrans_'+cnList[-1],parent=grpA,skipSelect=1)
   cmds.createNode('transform',name='ctrlV_'+cnList[-1],parent='ctrlVTrans_'+cnList[-1],skipSelect=1)
   cmds.matchTransform('ctrlVTrans_'+cnList[-1],'ctrl_'+cnList[-1],position=1)
   cmds.pointConstraint('ctrl_'+cnList[-1],'ctrlV_'+cnList[-1])
   cmds.createNode('transform',name='rax_'+cnList[-1],parent='ctrlCons_'+cnList[-1],skipSelect=1)
   cmds.connectAttr('rax_'+cnList[-1]+'.rotate','ctrl_'+cnList[-1]+'.rotateAxis')
   for i in range(len(cnList)-1): # each ctrl move with tail ctrl
     cmds.addAttr('ctrl_'+cnList[-1],longName='ctrl'+str(i+1)+'Weight',attributeType='double',minValue=0,maxValue=1,defaultValue=cvPr[i+1],keyable=1)
     mult = cmds.createNode('multiplyDivide',skipSelect=1)
     cmds.connectAttr('ctrlV_'+cnList[-1]+'.translate',mult+'.input1')
     cmds.connectAttr('ctrl_'+cnList[-1]+'.ctrl'+str(i+1)+'Weight',mult+'.input2X')
     cmds.connectAttr('ctrl_'+cnList[-1]+'.ctrl'+str(i+1)+'Weight',mult+'.input2Y')
     cmds.connectAttr('ctrl_'+cnList[-1]+'.ctrl'+str(i+1)+'Weight',mult+'.input2Z')
     cmds.connectAttr(mult+'.output','ctrlCons_'+cnList[i]+'.translate')
   rCrv = cmds.rebuildCurve(x,name=x+'De',rebuildType=0,constructionHistory=1,replaceOriginal=0,endKnots=1,keepRange=0,keepControlPoints=0,spans=(vn-2)*4,degree=3)
   cmds.parent(rCrv[0],grpA)
   # dvn = (vn-2)*3 + 3 # compute sub ctrl number
   dvn = (vn-2)*4 + 3 # compute sub ctrl number
   tagList = [] ; subList = []
   for i in range(0,dvn): # sub ctrl loop
    cn = x.replace('crv_','')+'Sub'+str(i) ; subList.append(cn)
    rgb = colorsys.hsv_to_rgb(hue,1.0,0.2)
    self.ctrlSquare('ctrl_'+cn,1.5,1,5,1,5,2,[1,1,1,0,0,0,0,0,0,0],[rgb[0],rgb[1],rgb[2]])
    cmds.createNode('controller',name='ctrlTag_'+cn,skipSelect=1) ; tagList.append('ctrlTag_'+cn)
    cmds.connectAttr('ctrl_'+cn+'.message','ctrlTag_'+cn+'.controllerObject')
    if i > 1 :
     cmds.connectAttr(tagList[-2]+'.prepopulate',tagList[-1]+'.prepopulate')
     cmds.connectAttr(tagList[-1]+'.parent',tagList[-2]+'.children[0]')
     cmds.createNode('joint',name='gJo_'+cn,parent='ctrl_'+cn,skipSelect=1)
     cmds.createNode('joint',name='gJo_'+cn+'Tip',parent='gJo_'+cn,skipSelect=1)
     cmds.setAttr('gJo_'+cn+'.radius',0) ; cmds.setAttr('gJo_'+cn+'.template',1) ; cmds.setAttr('gJo_'+cn+'Tip.radius',0)
     if i == 1 : cmds.pointConstraint(pin0,'gJo_'+cn+'Tip')
     else : cmds.pointConstraint('ctrl_'+subList[-2],'gJo_'+cn+'Tip')
    poc = cmds.createNode('pointOnCurveInfo',name='poc_'+cn,skipSelect=1)
    cmds.setAttr(poc+'.parameter',1.0/(dvn-1)*i)
    cmds.connectAttr(rCrv[1]+'.outputCurve',poc+'.inputCurve')
    #cmds.connectAttr(poc+'.position','ctrlTrans_'+cn+'.translate')
    ab = cmds.createNode('transform',name='abTrans_'+cn,parent=grpAb,skipSelect=1)
    cmds.connectAttr(poc+'.position',ab+'.translate')
    v = cmds.createNode('transform',name='locV_'+cn,parent=grpA,skipSelect=1)
    cmds.pointConstraint(ab,v)
    cmds.connectAttr(v+'.translate','ctrlTrans_'+cn+'.translate')
    cmds.parent('ctrlTrans_'+cn,grpA)
    cmds.connectAttr('ctrl_'+cnList[-1]+'.subCtrl','ctrlTrans_'+cn+'.v')
   cmds.delete(rCrv[0],constructionHistory=1)
   for i in range(0,dvn):
    cn = x.replace('crv_','')+'Sub'+str(i)
    cmds.createNode('transform',name='v_'+cn,skipSelect=1)
    cmds.pointConstraint('ctrl_'+cn,'v_'+cn)
    cmds.connectAttr('v_'+cn+'.translate',x+'DeShape.controlPoints['+str(i)+']')
    cmds.parent('v_'+cn,grpA)
    #cmds.createNode('decomposeMatrix',name='xCons_'+cn,skipSelect=1)
    #cmds.connectAttr('ctrl_'+cn+'.worldMatrix[0]','xCons_'+cn+'.inputMatrix')
    #cmds.connectAttr('xCons_'+cn+'.outputTranslate',x+'DeShape.controlPoints['+str(i)+']')
   self.lockCrvLlength(x.replace('crv_',''),x+'DeShape','ctrl_'+cnList[-1]+'.stretchy')
   cmds.setAttr(x+'.v',0)
   cmds.setAttr(rCrv[0]+'.v',0) 
   #cmds.sets(x+'Cl',e=1,addElement=clCrvSet)
   cmds.setAttr(x+'Cl.v',0)


   if cmds.objExists(x+'.control') :
    ctrled = cmds.listConnections(x+'.control')
    cmds.select(ctrled,replace=1)
    cmds.select(x+'Cl',add=1)
    self.crvFollowCrv(grpA,grpAb)
   
  leftList = [] ; backList = [] ; lowList = [] ; rightList = [] # whole ctrl part
  for i,x in enumerate(oCtrlList) :
   kn = x[10:-2]
   print kn
   if kn == 'leftHair' : leftList.append(x)
   if kn == 'backHair' : backList.append(x)
   if kn == 'lowHair' : lowList.append(x)
   if kn == 'rightHair' : rightList.append(x)
  nameList = ['leftHair','backHair','lowHair','rightHair']
  wholeList = [leftList,backList,lowList,rightList]
  #print wholeList
  for i in range(len(nameList)):
   if wholeList[i] :
    self.ctrlSphere('ctrl_'+nameList[i],15,2,[1,1,1,1,1,1,1,1,1,0],[0.7,0.7,0.7])
    cmds.delete(cmds.pointConstraint(wholeList[i],'ctrlCons_'+nameList[i]))
    cmds.createNode('transform',name='v_'+nameList[i],parent='ctrlTrans_'+nameList[i],skipSelect=1)
    cmds.parentConstraint('ctrl_'+nameList[i],'v_'+nameList[i])
    cmds.scaleConstraint('ctrl_'+nameList[i],'v_'+nameList[i])
    xCons = cmds.createNode('decomposeMatrix',name='xCons_'+nameList[i],skipSelect=1)
    cmds.connectAttr('v_'+nameList[i]+'.matrix',xCons+'.inputMatrix')
    isMult = cmds.createNode('multiplyDivide',name='mult_'+nameList[i]+'InverseScale',skipSelect=1)
    cmds.setAttr(isMult+'.operation',2)
    cmds.setAttr(isMult+'.input1',1,1,1,type='double3')
    cmds.connectAttr('ctrl_'+nameList[i]+'.scale',isMult+'.input2')
    for j in range(len(wholeList[i])):
     #cmds.parent(wholeList[i][j],'ctrl_'+nameList[i])
     p = cmds.listRelatives(wholeList[i][j],parent=1)[0]
     cons = cmds.createNode('transform',name=wholeList[i][j].replace('ctrlTrans_','cons_'),parent=p,skipSelect=1)
     cmds.connectAttr(xCons+'.outputTranslate',cons+'.translate')
     cmds.connectAttr(xCons+'.outputRotate',cons+'.rotate')
     cmds.connectAttr(xCons+'.outputScale',cons+'.scale')
     cmds.connectAttr(xCons+'.outputShear',cons+'.shear')
     cmds.parent(wholeList[i][j],cons)
     cmds.orientConstraint('ctrlTrans_'+nameList[i],wholeList[i][j].replace('ctrlTrans_','rax_'))
     cmds.connectAttr(isMult+'.output',wholeList[i][j].replace('ctrlTrans_','ctrl_')+'.scale')

 def crvFollowCrv(self,grp,grpAb,*a): # need xTrans_head grp_abTrans, ctrl curve must be 0toSpens
  sel = cmds.ls(selection=1)
  ci = sel[-1].replace('crv_','ci_') # curveInfo name
  cvn = cmds.getAttr(sel[-1]+'.spans') + cmds.getAttr(sel[-1]+'.degree') # cv number
  joGrp = cmds.createNode('transform',name=sel[-1].replace('crv_','grp_')+'Jo',parent=grp,skipSelect=1) ; cmds.setAttr(joGrp+'.v',0)
  pocJoList = []
  for i in range(0,cvn):
   poc = cmds.createNode('pointOnCurveInfo',name=sel[-1].replace('crv_','poc_')+'_'+str(i),skipSelect=1)
   cmds.connectAttr(sel[-1]+'Shape.worldSpace[0]',poc+'.inputCurve')
   #cmds.setAttr(poc+'.turnOnPercentage',1)
   if i == 0 : pv = 0.0
   elif i == 1 : pv = 1.0/3
   elif i == (cvn-1) : pv = float(cvn)-3
   elif i == (cvn-2) : pv = (float(cvn)-4)+(1.0/3*2)
   else : pv = float(i)-1
   cmds.setAttr(poc+'.parameter',pv)
   loc = cmds.createNode('transform',name=sel[-1].replace('crv_','loc_')+'_'+str(i),skipSelect=1)
   pocJo = cmds.createNode('joint',name=sel[-1].replace('crv_','jo_')+'_'+str(i),skipSelect=1)
   pocJoList.append(pocJo)
   cmds.connectAttr(poc+'.result.position',loc+'.translate')
   cmds.pointConstraint(loc,pocJo)
   cmds.parent(pocJo,joGrp)
   cmds.parent(loc,grpAb)
  if cmds.objExists(ci)==0:
   cmds.createNode('curveInfo',name=ci,skipSelect=1) # it will be delete when npoc delete
   cmds.connectAttr(sel[-1]+'Shape.worldSpace[0]',ci+'.inputCurve')
  for i in range(len(sel)-1): # each curve loop
   sk = cmds.skinCluster(pocJoList,sel[i],toSelectedBones=1,removeUnusedInfluence=0)
   cit = cmds.createNode('curveInfo',skipSelect=1)
   cmds.connectAttr(sel[i]+'Shape.worldSpace[0]',cit+'.inputCurve')
   vn = cmds.getAttr(sel[i]+'.spans') + cmds.getAttr(sel[i]+'.degree')
   npocList = [] ; paraList = []
   for j in range(1,vn): # each cv loop
    npoc = cmds.createNode('nearestPointOnCurve',skipSelect=1) ; npocList.append(npoc)
    cmds.connectAttr(sel[-1]+'Shape.worldSpace[0]',npoc+'.inputCurve')
    cmds.connectAttr(cit+'.controlPoints['+str(j)+']',npoc+'.inPosition')
    para = cmds.getAttr(npoc+'.parameter')
    paCv = str(int(round(para)))
    #print paCv
    if paCv == '0' : paCv = '1'
    if paraList :
     if paCv == paraList[-1] : paCv = str(int(paCv)+1)
     elif int(paCv)<int(paraList[-1]) : paCv = str(int(paraList[-1])+1)
    #print paCv
    paraList.append(paCv)
    cmds.skinPercent(sk[0],sel[i]+'.cv['+str(j)+']',transformValue=[(pocJoList[int(paCv)],1)])
   cmds.delete(npocList)
   
 def crvFollowCrvBackUp(self,*a): # need xTrans_head grp_abTrans, ctrl curve must be 0toSpens
  sel = cmds.ls(selection=1)
  ci = sel[-1].replace('crv_','ci_') # curveInfo name
  cvn = cmds.getAttr(sel[-1]+'.spans') + cmds.getAttr(sel[-1]+'.degree') # cv number
  if cmds.objExists(ci)==0:
   cmds.createNode('curveInfo',name=ci,skipSelect=1) # it will be delete when npoc delete
   cmds.connectAttr(sel[-1]+'Shape.worldSpace[0]',ci+'.inputCurve')
  for i in range(len(sel)-1): # each curve loop
   cit = cmds.createNode('curveInfo',skipSelect=1)
   cmds.connectAttr(sel[i]+'Shape.worldSpace[0]',cit+'.inputCurve')
   vn = cmds.getAttr(sel[i]+'.spans') + cmds.getAttr(sel[i]+'.degree')
   npocList = [] ; paraList = []
   for j in range(1,vn): # each cv loop
    npoc = cmds.createNode('nearestPointOnCurve',skipSelect=1) ; npocList.append(npoc)
    cmds.connectAttr(sel[-1]+'Shape.worldSpace[0]',npoc+'.inputCurve')
    cmds.connectAttr(cit+'.controlPoints['+str(j)+']',npoc+'.inPosition')
    para = cmds.getAttr(npoc+'.parameter')
    paCv = str(int(round(para)))
    #print paCv
    if paCv == '0' : paCv = '1'
    if paraList :
     if paCv == paraList[-1] : paCv = str(int(paCv)+1)
     elif int(paCv)<int(paraList[-1]) : paCv = str(int(paraList[-1])+1)
    #print paCv
    paraList.append(paCv)
    ab = cmds.createNode('transform',name='abTrans_'+sel[i]+str(j),parent='grp_abTrans',skipSelect=1)
    cmds.connectAttr(ci+'.controlPoints['+paCv+']',ab+'.translate')
    v = cmds.createNode('transform',name='v_'+sel[i]+'_'+str(j),parent='xTrans_head',skipSelect=1)
    #cmds.pointConstraint(ab,v)
    cmds.delete(cmds.pointConstraint(ab,v))
    vTrans = cmds.createNode('transform',name='vTrans_'+sel[i]+str(j),parent='xTrans_head',skipSelect=1)
    cmds.matchTransform(vTrans,v)
    #cmds.parent(v,vTrans)
    #cmds.connectAttr(v+'.translate',sel[i]+'.controlPoints['+str(j)+']')
    # new method
    xCon = cmds.createNode('composeMatrix',name='xCon_'+sel[i]+'_'+str(j),skipSelect=1)
    xMult = cmds.createNode('multMatrix',name='xMult_'+sel[i]+'_'+str(j),skipSelect=1)
    cmds.connectAttr(ci+'.controlPoints['+paCv+']',xCon+'.inputTranslate')
    cmds.connectAttr(xCon+'.outputMatrix',xMult+'.matrixIn[0]')
    cmds.connectAttr(vTrans+'.worldInverseMatrix[0]',xMult+'.matrixIn[1]')
    xCons = cmds.createNode('decomposeMatrix',name='xCons_'+sel[i]+'_'+str(j),skipSelect=1)
    cmds.connectAttr(xMult+'.matrixSum',xCons+'.inputMatrix')
    cmds.connectAttr(xCons+'.outputTranslate',sel[i]+'.controlPoints['+str(j)+']')
   cmds.delete(npocList)
 
##############################################################################################################

warRig()

