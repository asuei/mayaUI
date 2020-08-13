# encoding: utf-8
import sys
import math
import maya.cmds as cmds
import maya.mel as mel
import msvcrt

class warAnim:
 def __init__(self):
  cp = 60
  self.ctrl = []
  self.ctrl.append(['itbtn','btn_asset','asset','sel','ctrl_asset',100,100,-1,['btn_asset','top',5,'oMenu'],['btn_asset','left',5],[],''])
  self.ctrl.append(['btn','btn_location','location','sel','ctrl_location',100,40,-1,['btn_location','top',3,'btn_asset'],['btn_location','left',5],[],''])
  self.ctrl.append(['btn','btn_move','move','sel','ctrl_move',100,40,-1,['btn_move','top',3,'btn_location'],['btn_move','left',5],[],''])
  self.ctrl.append(['btn','btn_spin','spin','sel','ctrl_spin',100,40,-1,['btn_spin','top',3,'btn_move'],['btn_spin','left',5],[],''])

  self.ctrl.append(['btn','btn_head','head','sel','ctrl_head',60,40,0.2,['btn_head','top',30],['btn_head','left',-30,cp],[],''])
  self.ctrl.append(['btn','btn_neck','neck','sel','ctrl_neck',50,15,0.25,['btn_neck','top',0,'btn_neck2'],['btn_neck','left',-25,cp],[],''])
  self.ctrl.append(['btn','btn_neck1','neck1','sel','ctrl_neck1',50,15,0.25,['btn_neck1','top',0,['btn_neck2','btn_head']],['btn_neck1','left',-25,cp],[],''])
  self.ctrl.append(['btn','btn_neck2','neck2','sel','ctrl_neck2',50,15,0.25,['btn_neck2','top',0,'btn_head'],['btn_neck2','left',-25,cp],[],''])
  self.ctrl.append(['btn','btn_eyesAim','eyesAim','sel','ctrl_eyesAim',50,20,0.15,['btn_eyesAim','top',-60,'btn_head'],['btn_eyesAim','left',-25,cp],[],''])

  self.ctrl.append(['btn','btn_chest','chest','sel','ctrl_chest',100,40,0.4,['btn_chest','top',0,['btn_neck1','btn_neck','btn_head']],['btn_chest','left',-50,cp],[],''])
  self.ctrl.append(['btn','btn_waist','waist','sel','ctrl_waist',100,35,0.4,['btn_waist','top',0,'btn_chest'],['btn_waist','left',-50,cp],[],''])
  self.ctrl.append(['btn','btn_abdomen','abdomen','sel','ctrl_abdomen',100,35,0.4,['btn_abdomen','top',0,'btn_waist'],['btn_abdomen','left',-50,cp],[],''])   
  self.ctrl.append(['btn','btn_torso','torso','sel','ctrl_torso',120,40,0.3,['btn_torso','top',0,['btn_abdomen','btn_waist']],['btn_torso','left',-60,cp],[],''])
  self.ctrl.append(['btn','btn_pelvis','pelvis','sel','ctrl_pelvis',60,40,0.4,['btn_pelvis','top',0,'btn_torso'],['btn_pelvis','left',-30,cp],[],''])
  self.ctrl.append(['btn','btn_tail','tail','sel','ctrl_tail',30,50,0.5,['btn_tail','top',0,'btn_pelvis'],['btn_tail','left',-15,cp],[],''])

  self.ctrl.append(['btn','btn_pelvisL','pelL','sel','ctrl_pelvisL',30,40,0,['btn_pelvisL','top',0,'btn_torso'],['btn_pelvisL','left',0,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_thighL','thighL','sel','ctrl_thighL',40,80,0,['btn_thighL','top',0,'btn_pelvisL'],['btn_thighL','left',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_shankL','shankL','sel','ctrl_shankL',40,80,0,['btn_shankL','top',0,'btn_thighL'],['btn_shankL','left',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_ankleL','ankleL','sel','ctrl_ankleL',40,40,0,['btn_ankleL','top',0,'btn_shankL'],['btn_ankleL','left',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_toeL','toeL','sel','ctrl_toeL',40,30,0,['btn_toeL','top',0,'btn_ankleL'],['btn_toeL','left',-20,'btn_ankleL'],[],''])
  self.ctrl.append(['btn','btn_kneeL','kneeL','sel','ctrl_kneeL',40,40,0,['btn_kneeL','top',-20,'btn_thighL'],['btn_kneeL','left',0,'btn_pelvisL'],[],''])
  self.ctrl.append(['btn','btn_legL','legL','sel','ctrl_legL',40,50,0,['btn_legL','top',-50,'btn_ankleL'],['btn_legL','left',0,'btn_pelvisL'],[],'ctrl_legR'])
  self.ctrl.append(['sld','sld_legL','','FKIK','ctrl_pelvisL',50,0,0,['sld_legL','top',10,'btn_torso'],['sld_legL','left',0,'btn_pelvisL'],[],''])
  self.ctrl.append(['btn','btn_heelL','heelL','sel','ctrl_heelL',40,30,0,['btn_heelL','top',-80,'btn_legL'],['btn_heelL','left',-40,'btn_legL'],[],''])
  
  self.ctrl.append(['btn','btn_pelvisR','pelR','sel','ctrl_pelvisR',30,40,0.1,['btn_pelvisR','top',0,'btn_torso'],['btn_pelvisR','right',0,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_thighR','thighR','sel','ctrl_thighR',40,80,0.1,['btn_thighR','top',0,'btn_pelvisL'],['btn_thighR','right',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_shankR','shankR','sel','ctrl_shankR',40,80,0.1,['btn_shankR','top',0,'btn_thighL'],['btn_shankR','right',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_ankleR','ankleR','sel','ctrl_shankR',40,40,0.1,['btn_ankleR','top',0,'btn_shankL'],['btn_ankleR','right',-10,'btn_pelvis'],[],''])
  self.ctrl.append(['btn','btn_toeR','toeR','sel','ctrl_toeR',40,30,0.1,['btn_toeR','top',0,'btn_ankleR'],['btn_toeR','right',-20,'btn_ankleR'],[],''])
  self.ctrl.append(['btn','btn_kneeR','kneeR','sel','ctrl_kneeR',40,40,0.1,['btn_kneeR','top',-20,'btn_thighL'],['btn_kneeR','right',0,'btn_pelvisR'],[],''])
  self.ctrl.append(['btn','btn_legR','legR','sel','ctrl_legR',40,50,0.1,['btn_legR','top',-50,'btn_ankleL'],['btn_legR','right',0,'btn_pelvisR'],[],'ctrl_legL'])
  self.ctrl.append(['sld','sld_legR','','FKIK','ctrl_pelvisR',50,0,0,['sld_legR','top',10,'btn_torso'],['sld_legR','right',0,'btn_pelvisR'],[],''])
  self.ctrl.append(['btn','btn_heelR','heelR','sel','ctrl_heelR',40,30,0.1,['btn_heelR','top',-80,'btn_legR'],['btn_heelR','right',-40,'btn_legR'],[],''])
  
  self.ctrl.append(['btn','btn_shoulderL','shoulderL','sel','ctrl_shoulderL',75,40,0.5,['btn_shoulderL','top',-40,'btn_chest'],['btn_shoulderL','left',0,'btn_chest'],[],'ctrl_shoulderR'])
  self.ctrl.append(['btn','btn_uArmL','uArmL','sel','ctrl_upperarmL',40,80,0.5,['btn_uArmL','top',-40,'btn_shoulderL'],['btn_uArmL','left',0,'btn_shoulderL'],[],''])
  self.ctrl.append(['btn','btn_fArmL','fArmL','sel','ctrl_forearmL',40,80,0.5,['btn_fArmL','left',0,'btn_shoulderL'],['btn_fArmL','top',0,'btn_uArmL'],[],''])
  self.ctrl.append(['btn','btn_wristL','wristL','sel','ctrl_wristL',40,40,0.5,['btn_wristL','left',0,'btn_shoulderL'],['btn_wristL','top',0,'btn_fArmL'],[],''])
  self.ctrl.append(['btn','btn_elbowL','elbowL','sel','ctrl_elbowL',40,40,0.5,['btn_elbowL','left',0,'btn_wristL'],['btn_elbowL','top',-25,'btn_uArmL'],[],''])
  self.ctrl.append(['btn','btn_handL','handL','sel','ctrl_handL',40,55,0.5,['btn_handL','left',0,'btn_wristL'],['btn_handL','top',50,'btn_elbowL'],[],''])
  self.ctrl.append(['sld','sld_armL','','FKIK','ctrl_shoulderL',50,0,0,['sld_armL','top',0,'btn_shoulderL'],['sld_armL','right',11,'btn_chest'],[],''])
  self.ctrl.append(['btn','btn_palmL','palmL','sel','ctrl_plamL',40,30,0.5,['btn_palmL','top',-80,'btn_handL'],['btn_palmL','left',-40,'btn_handL'],[],''])

  self.ctrl.append(['btn','btn_shoulderR','shoulderR','sel','ctrl_shoulderR',75,40,0.6,['btn_shoulderR','top',-40,'btn_chest'],['btn_shoulderR','right',0,'btn_chest'],[],''])
  self.ctrl.append(['btn','btn_uArmR','uArmR','sel','ctrl_upperarmR',40,80,0.6,['btn_uArmR','top',-40,'btn_shoulderR'],['btn_uArmR','right',0,'btn_shoulderR'],[],''])
  self.ctrl.append(['btn','btn_fArmR','fArmR','sel','ctrl_forearmR',40,80,0.6,['btn_fArmR','right',0,'btn_shoulderR'],['btn_fArmR','top',0,'btn_uArmR'],[],''])
  self.ctrl.append(['btn','btn_wristR','wristR','sel','ctrl_wristR',40,40,0.6,['btn_wristR','right',0,'btn_shoulderR'],['btn_wristR','top',0,'btn_fArmR'],[],''])
  self.ctrl.append(['btn','btn_elbowR','elbowR','sel','ctrl_elbowR',40,40,0.6,['btn_elbowR','right',0,'btn_wristR'],['btn_elbowR','top',-25,'btn_uArmR'],[],''])
  self.ctrl.append(['btn','btn_handR','handR','sel','ctrl_handR',40,55,0.6,['btn_handR','right',0,'btn_wristR'],['btn_handR','top',50,'btn_elbowR'],[],''])
  self.ctrl.append(['sld','sld_armR','','FKIK','ctrl_shoulderR',50,0,0,['sld_armR','top',0,'btn_shoulderR'],['sld_armR','left',11,'btn_chest'],[],''])
  self.ctrl.append(['btn','btn_palmR','palmR','sel','ctrl_plamR',40,30,0.6,['btn_palmR','top',-80,'btn_handR'],['btn_palmR','right',-40,'btn_handR'],[],''])

  self.ctrl.append(['btn','btn_fingerL','fingerL','sel','ctrl_fingerL',80,40,0.7,['btn_fingerL','left',-40,'btn_wristL'],['btn_fingerL','top',10,'btn_wristL'],['ctrl_thumb0L','ctrl_thumb1L','ctrl_thumb2L','ctrl_index1L','ctrl_index2L','ctrl_index3L','ctrl_middle1L','ctrl_middle2L','ctrl_middle3L','ctrl_ring1L','ctrl_ring2L','ctrl_ring3L','ctrl_little1L','ctrl_little2L','ctrl_little3L'],''])
  self.ctrl.append(['btn','btn_thumb0L','T0','sel','ctrl_thumb0L',20,40,0.7,['btn_thumb0L','right',0,['btn_fingerL','btn_wristL']],['btn_thumb0L','top',-20,['btn_fingerL','btn_wristL']],['ctrl_thumb0L','ctrl_thumb1L','ctrl_thumb2L'],''])
  self.ctrl.append(['btn','btn_thumb1L','T1','sel','ctrl_thumb1L',20,40,0.7,['btn_thumb1L','right',-20,'btn_thumb0L'],['btn_thumb1L','top',0,'btn_thumb0L'],['ctrl_thumb0L','ctrl_thumb1L','ctrl_thumb2L'],''])
  self.ctrl.append(['btn','btn_thumb2L','T2','sel','ctrl_thumb2L',20,40,0.7,['btn_thumb2L','right',-20,'btn_thumb1L'],['btn_thumb2L','top',0,'btn_thumb1L'],['ctrl_thumb0L','ctrl_thumb1L','ctrl_thumb2L'],''])
  self.ctrl.append(['btn','btn_index1L','I1','sel','ctrl_index1L',20,40,0.7,['btn_index1L','right',-20,['btn_fingerL','btn_wristL']],['btn_index1L','top',0,['btn_fingerL','btn_wristL']],['ctrl_index1L','ctrl_index2L','ctrl_index3L'],''])
  self.ctrl.append(['btn','btn_index2L','I2','sel','ctrl_index2L',20,40,0.7,['btn_index2L','right',-20,'btn_index1L'],['btn_index2L','top',0,'btn_index1L'],['ctrl_index1L','ctrl_index2L','ctrl_index3L'],''])
  self.ctrl.append(['btn','btn_index3L','I3','sel','ctrl_index3L',20,40,0.7,['btn_index3L','right',-20,'btn_index2L'],['btn_index3L','top',0,'btn_index2L'],['ctrl_index1L','ctrl_index2L','ctrl_index3L'],''])
  self.ctrl.append(['btn','btn_middle1L','M1','sel','ctrl_middle1L',20,40,0.7,['btn_middle1L','left',0,'btn_index1L'],['btn_middle1L','top',0,['btn_fingerL','btn_wristL']],['ctrl_middle1L','ctrl_middle2L','ctrl_middle3L'],''])
  self.ctrl.append(['btn','btn_middle2L','M2','sel','ctrl_middle2L',20,40,0.7,['btn_middle2L','left',-20,'btn_middle1L'],['btn_middle2L','top',0,'btn_middle1L'],['ctrl_middle1L','ctrl_middle2L','ctrl_middle3L'],''])
  self.ctrl.append(['btn','btn_middle3L','M3','sel','ctrl_middle3L',20,40,0.7,['btn_middle3L','left',-20,'btn_middle2L'],['btn_middle3L','top',0,'btn_middle2L'],['ctrl_middle1L','ctrl_middle2L','ctrl_middle3L'],''])
  self.ctrl.append(['btn','btn_ring1L','R1','sel','ctrl_ring1L',20,40,0.7,['btn_ring1L','left',0,'btn_middle1L'],['btn_ring1L','top',0,['btn_fingerL','btn_wristL']],['ctrl_ring1L','ctrl_ring2L','ctrl_ring3L'],''])
  self.ctrl.append(['btn','btn_ring2L','R2','sel','ctrl_ring2L',20,40,0.7,['btn_ring2L','left',-20,'btn_ring1L'],['btn_ring2L','top',0,'btn_ring1L'],['ctrl_ring1L','ctrl_ring2L','ctrl_ring3L'],''])
  self.ctrl.append(['btn','btn_ring3L','R3','sel','ctrl_ring3L',20,40,0.7,['btn_ring3L','left',-20,'btn_ring2L'],['btn_ring3L','top',0,'btn_ring2L'],['ctrl_ring1L','ctrl_ring2L','ctrl_ring3L'],''])
  self.ctrl.append(['btn','btn_little1L','L1','sel','ctrl_little1L',20,40,0.7,['btn_little1L','left',0,'btn_ring1L'],['btn_little1L','top',0,['btn_fingerL','btn_wristL']],['ctrl_little1L','ctrl_little2L','ctrl_little3L'],''])
  self.ctrl.append(['btn','btn_little2L','L2','sel','ctrl_little2L',20,40,0.7,['btn_little2L','left',-20,'btn_little1L'],['btn_little2L','top',0,'btn_little1L'],['ctrl_little1L','ctrl_little2L','ctrl_little3L'],''])
  self.ctrl.append(['btn','btn_little3L','L3','sel','ctrl_little3L',20,40,0.7,['btn_little3L','left',-20,'btn_little2L'],['btn_little3L','top',0,'btn_little2L'],['ctrl_little1L','ctrl_little2L','ctrl_little3L'],''])

  self.ctrl.append(['btn','btn_fingerR','fingerR','sel','ctrl_fingerR',80,40,0.7,['btn_fingerR','right',-40,'btn_wristR'],['btn_fingerR','top',10,'btn_wristR'],['ctrl_thumb0R','ctrl_thumb1R','ctrl_thumb2R','ctrl_index1R','ctrl_index2R','ctrl_index3R','ctrl_middle1R','ctrl_middle2R','ctrl_middle3R','ctrl_ring1R','ctrl_ring2R','ctrl_ring3R','ctrl_little1R','ctrl_little2R','ctrl_little3R'],''])
  self.ctrl.append(['btn','btn_thumb0R','T0','sel','ctrl_thumb0R',20,40,0.7,['btn_thumb0R','left',0,['btn_fingerR','btn_wristR']],['btn_thumb0R','top',-20,['btn_fingerR','btn_wristR']],['ctrl_thumb0R','ctrl_thumb1R','ctrl_thumb2R'],''])
  self.ctrl.append(['btn','btn_thumb1R','T1','sel','ctrl_thumb1R',20,40,0.7,['btn_thumb1R','left',-20,'btn_thumb0R'],['btn_thumb1R','top',0,'btn_thumb0R'],['ctrl_thumb0R','ctrl_thumb1R','ctrl_thumb2R'],''])
  self.ctrl.append(['btn','btn_thumb2R','T2','sel','ctrl_thumb2R',20,40,0.7,['btn_thumb2R','left',-20,'btn_thumb1R'],['btn_thumb2R','top',0,'btn_thumb1R'],['ctrl_thumb0R','ctrl_thumb1R','ctrl_thumb2R'],''])
  self.ctrl.append(['btn','btn_index1R','I1','sel','ctrl_index1R',20,40,0.7,['btn_index1R','left',-20,['btn_fingerR','btn_wristR']],['btn_index1R','top',0,['btn_fingerR','btn_wristR']],['ctrl_index1R','ctrl_index2R','ctrl_index3R'],''])
  self.ctrl.append(['btn','btn_index2R','I2','sel','ctrl_index2R',20,40,0.7,['btn_index2R','left',-20,'btn_index1R'],['btn_index2R','top',0,'btn_index1R'],['ctrl_index1R','ctrl_index2R','ctrl_index3R'],''])
  self.ctrl.append(['btn','btn_index3R','I3','sel','ctrl_index3R',20,40,0.7,['btn_index3R','left',-20,'btn_index2R'],['btn_index3R','top',0,'btn_index2R'],['ctrl_index1R','ctrl_index2R','ctrl_index3R'],''])
  self.ctrl.append(['btn','btn_middle1R','M1','sel','ctrl_middle1R',20,40,0.7,['btn_middle1R','right',0,'btn_index1R'],['btn_middle1R','top',0,['btn_fingerR','btn_wristR']],['ctrl_middle1R','ctrl_middle2R','ctrl_middle3R'],''])
  self.ctrl.append(['btn','btn_middle2R','M2','sel','ctrl_middle2R',20,40,0.7,['btn_middle2R','right',-20,'btn_middle1R'],['btn_middle2R','top',0,'btn_middle1R'],['ctrl_middle1R','ctrl_middle2R','ctrl_middle3R'],''])
  self.ctrl.append(['btn','btn_middle3R','M3','sel','ctrl_middle3R',20,40,0.7,['btn_middle3R','right',-20,'btn_middle2R'],['btn_middle3R','top',0,'btn_middle2R'],['ctrl_middle1R','ctrl_middle2R','ctrl_middle3R'],''])
  self.ctrl.append(['btn','btn_ring1R','R1','sel','ctrl_ring1R',20,40,0.7,['btn_ring1R','right',0,'btn_middle1R'],['btn_ring1R','top',0,['btn_fingerR','btn_wristR']],['ctrl_ring1R','ctrl_ring2R','ctrl_ring3R'],''])
  self.ctrl.append(['btn','btn_ring2R','R2','sel','ctrl_ring2R',20,40,0.7,['btn_ring2R','right',-20,'btn_ring1R'],['btn_ring2R','top',0,'btn_ring1R'],['ctrl_ring1R','ctrl_ring2R','ctrl_ring3R'],''])
  self.ctrl.append(['btn','btn_ring3R','R3','sel','ctrl_ring3R',20,40,0.7,['btn_ring3R','right',-20,'btn_ring2R'],['btn_ring3R','top',0,'btn_ring2R'],['ctrl_ring1R','ctrl_ring2R','ctrl_ring3R'],''])
  self.ctrl.append(['btn','btn_little1R','L1','sel','ctrl_little1R',20,40,0.7,['btn_little1R','right',0,'btn_ring1R'],['btn_little1R','top',0,['btn_fingerR','btn_wristR']],['ctrl_little1R','ctrl_little2R','ctrl_little3R'],''])
  self.ctrl.append(['btn','btn_little2R','L2','sel','ctrl_little2R',20,40,0.7,['btn_little2R','right',-20,'btn_little1R'],['btn_little2R','top',0,'btn_little1R'],['ctrl_little1R','ctrl_little2R','ctrl_little3R'],''])
  self.ctrl.append(['btn','btn_little3R','L3','sel','ctrl_little3R',20,40,0.7,['btn_little3R','right',-20,'btn_little2R'],['btn_little3R','top',0,'btn_little2R'],['ctrl_little1R','ctrl_little2R','ctrl_little3R'],''])

  #self.ctrl.append(['btn','btn_bigToe0L','B0','sel','ctrl_bigToe0L',20,35,0.7,['btn_bigToe0L','right',-20,'btn_ankleL'],['btn_bigToe0L','top',0,'btn_ankleL'],[],''])
  #self.ctrl.append(['btn','btn_bigToe1L','B1','sel','ctrl_bigToe1L',20,35,0.7,['btn_bigToe1L','right',-20,'btn_bigToe0L'],['btn_bigToe1L','top',0,'btn_bigToe0L'],[],''])
  #self.ctrl.append(['btn','btn_bigToe2L','B2','sel','ctrl_bigToe2L',20,35,0.7,['btn_bigToe2L','right',-20,'btn_bigToe1L'],['btn_bigToe2L','top',0,'btn_bigToe1L'],[],''])
  self.ctrl.append(['btn','btn_indexToe1L','I1','sel','ctrl_indexToe1L',20,35,0.7,['btn_indexToe1L','right',-20,'btn_ankleL'],['btn_indexToe1L','top',0,'btn_ankleL'],[],''])
  self.ctrl.append(['btn','btn_indexToe2L','I2','sel','ctrl_indexToe2L',20,35,0.7,['btn_indexToe2L','right',-20,'btn_indexToe1L'],['btn_indexToe2L','top',0,'btn_indexToe1L'],[],''])
  self.ctrl.append(['btn','btn_indexToe3L','I3','sel','ctrl_indexToe3L',20,35,0.7,['btn_indexToe3L','right',-20,'btn_indexToe2L'],['btn_indexToe3L','top',0,'btn_indexToe2L'],[],''])
  self.ctrl.append(['btn','btn_middleToe1L','M1','sel','ctrl_middleToe1L',20,35,0.7,['btn_middleToe1L','left',0,'btn_indexToe1L'],['btn_middleToe1L','top',0,'btn_ankleL'],[],''])
  self.ctrl.append(['btn','btn_middleToe2L','M1','sel','ctrl_middleToe2L',20,35,0.7,['btn_middleToe2L','left',-20,'btn_middleToe1L'],['btn_middleToe2L','top',0,'btn_middleToe1L'],[],''])
  self.ctrl.append(['btn','btn_middleToe3L','M1','sel','ctrl_middleToe3L',20,35,0.7,['btn_middleToe3L','left',-20,'btn_middleToe2L'],['btn_middleToe3L','top',0,'btn_middleToe2L'],[],''])
  self.ctrl.append(['btn','btn_fourthToe1L','F1','sel','ctrl_fourthToe1L',20,35,0.7,['btn_fourthToe1L','left',0,'btn_middleToe1L'],['btn_fourthToe1L','top',0,'btn_ankleL'],[],''])
  self.ctrl.append(['btn','btn_fourthToe2L','F2','sel','ctrl_fourthToe2L',20,35,0.7,['btn_fourthToe2L','left',-20,'btn_fourthToe1L'],['btn_fourthToe2L','top',0,'btn_fourthToe1L'],[],''])
  self.ctrl.append(['btn','btn_fourthToe3L','F3','sel','ctrl_fourthToe3L',20,35,0.7,['btn_fourthToe3L','left',-20,'btn_fourthToe2L'],['btn_fourthToe3L','top',0,'btn_fourthToe2L'],[],''])
  self.ctrl.append(['btn','btn_littleToe1L','L1','sel','ctrl_littleToe1L',20,35,0.7,['btn_littleToe1L','left',0,['btn_fourthToe1L','btn_middleToe1L']],['btn_littleToe1L','top',0,'btn_ankleL'],[],''])
  self.ctrl.append(['btn','btn_littleToe2L','L2','sel','ctrl_littleToe2L',20,35,0.7,['btn_littleToe2L','left',-20,'btn_littleToe1L'],['btn_littleToe2L','top',0,'btn_littleToe1L'],[],''])
  self.ctrl.append(['btn','btn_littleToe3L','L3','sel','ctrl_littleToe3L',20,35,0.7,['btn_littleToe3L','left',-20,'btn_littleToe2L'],['btn_littleToe3L','top',0,'btn_littleToe2L'],[],''])

  self.ctrl.append(['btn','btn_indexToe1R','I1','sel','ctrl_indexToe1R',20,35,0.7,['btn_indexToe1R','left',-20,'btn_ankleR'],['btn_indexToe1R','top',0,'btn_ankleR'],[],''])
  self.ctrl.append(['btn','btn_indexToe2R','I2','sel','ctrl_indexToe2R',20,35,0.7,['btn_indexToe2R','left',-20,'btn_indexToe1R'],['btn_indexToe2R','top',0,'btn_indexToe1R'],[],''])
  self.ctrl.append(['btn','btn_indexToe3R','I3','sel','ctrl_indexToe3R',20,35,0.7,['btn_indexToe3R','left',-20,'btn_indexToe2R'],['btn_indexToe3R','top',0,'btn_indexToe2R'],[],''])
  self.ctrl.append(['btn','btn_middleToe1R','M1','sel','ctrl_middleToe1R',20,35,0.7,['btn_middleToe1R','right',0,'btn_indexToe1R'],['btn_middleToe1R','top',0,'btn_ankleR'],[],''])
  self.ctrl.append(['btn','btn_middleToe2R','M2','sel','ctrl_middleToe2R',20,35,0.7,['btn_middleToe2R','right',-20,'btn_middleToe1R'],['btn_middleToe2R','top',0,'btn_middleToe1R'],[],''])
  self.ctrl.append(['btn','btn_middleToe3R','M3','sel','ctrl_middleToe3R',20,35,0.7,['btn_middleToe3R','right',-20,'btn_middleToe2R'],['btn_middleToe3R','top',0,'btn_middleToe2R'],[],''])
  self.ctrl.append(['btn','btn_fourthToe1R','F1','sel','ctrl_fourthToe1R',20,35,0.7,['btn_fourthToe1R','right',0,'btn_middleToe1R'],['btn_fourthToe1R','top',0,'btn_ankleR'],[],''])
  self.ctrl.append(['btn','btn_fourthToe2R','F2','sel','ctrl_fourthToe2R',20,35,0.7,['btn_fourthToe2R','right',-20,'btn_fourthToe1R'],['btn_fourthToe2R','top',0,'btn_fourthToe1R'],[],''])
  self.ctrl.append(['btn','btn_fourthToe3R','F3','sel','ctrl_fourthToe3R',20,35,0.7,['btn_fourthToe3R','right',-20,'btn_fourthToe2R'],['btn_fourthToe3R','top',0,'btn_fourthToe2R'],[],''])
  self.ctrl.append(['btn','btn_littleToe1R','L1','sel','ctrl_littleToe1R',20,35,0.7,['btn_littleToe1R','right',0,'btn_fourthToe1R'],['btn_littleToe1R','top',0,'btn_ankleR'],[],''])
  self.ctrl.append(['btn','btn_littleToe2R','L2','sel','ctrl_littleToe2R',20,35,0.7,['btn_littleToe2R','right',-20,'btn_littleToe1R'],['btn_littleToe2R','top',0,'btn_littleToe1R'],[],''])
  self.ctrl.append(['btn','btn_littleToe3R','L3','sel','ctrl_littleToe3R',20,35,0.7,['btn_littleToe3R','right',-20,'btn_littleToe2R'],['btn_littleToe3R','top',0,'btn_littleToe2R'],[],''])
  
  self.ctrl.append(['btn','btn_selAll','select all','sels','all',100,50,-1,['btn_selAll','top',10,'btn_spin'],['btn_selAll','left',5],[],''])
  self.ctrl.append(['btn','btn_selCtrl','select all ctrl','sels','all',100,50,-1,['btn_selCtrl','top',5,'btn_selAll'],['btn_selCtrl','left',5],[],''])
  self.ctrl.append(['btn','btn_def','set default','def','',100,55,-1,['btn_def','top',5,'btn_selCtrl'],['btn_def','left',5],[],''])
  self.ctrl.append(['btn','btn_tdef','translate default','def','',100,55,-1,['btn_tdef','top',5,'btn_def'],['btn_tdef','left',5],[],''])
  self.ctrl.append(['btn','btn_fkik','sync FK IK','ikfk','sync',100,60,-1,['btn_fkik','top',5,'btn_def'],['btn_fkik','right',5],[],''])

  self.facial = []
  self.facial.append(['itbtn','btn_asset','asset','sel','ctrl_asset',100,100,-1,['btn_asset','top',5,'oMenu'],['btn_asset','left',5],[],''])
  self.facial.append(['btn','btn_faceCam','face camera','sel','ctrl_facial',100,80,-1,['btn_faceCam','top',3,'btn_asset'],['btn_faceCam','left',5],[],''])
  
  self.facial.append(['btn','btn_eyeAimsF','eyesAim','sel','ctrl_eyesAim',50,30,0.4,['btn_eyeAimsF','top',110],['btn_eyeAimsF','left',-25,cp],[],''])
  self.facial.append(['btn','btn_eyeL','eyeL','sel','ctrl_eyeL',40,20,0,['btn_eyeL','top',115],['btn_eyeL','left',00,cp+12],[],''])
  self.facial.append(['btn','btn_eyeR','eyeR','sel','ctrl_eyeR',40,20,0,['btn_eyeR','top',115],['btn_eyeR','right',00,cp-12],[],''])
  self.facial.append(['btn','btn_uplidL','upLidL','sel','ctrl_upLidL',50,30,0.2,['btn_uplidL','bottom',0,'btn_eyeL'],['btn_uplidL','right',-45,'btn_eyeL'],[],''])
  self.facial.append(['btn','btn_lolidL','loLidL','sel','ctrl_loLidL',50,30,0.2,['btn_lolidL','top',0,'btn_eyeL'],['btn_lolidL','right',-45,'btn_eyeL'],[],''])
  self.facial.append(['btn','btn_uplidR','upLidR','sel','ctrl_upLidR',50,30,0.2,['btn_uplidR','bottom',0,'btn_eyeR'],['btn_uplidR','left',-45,'btn_eyeR'],[],''])
  self.facial.append(['btn','btn_lolidR','loLidR','sel','ctrl_loLidR',50,30,0.2,['btn_lolidR','top',0,'btn_eyeR'],['btn_lolidR','left',-45,'btn_eyeR'],[],''])
  
  self.facial.append(['btn','btn_glabella','glabella','sel','ctrl_glabella',50,30,0.6,['btn_glabella','bottom',40,'btn_eyeAimsF'],['btn_glabella','left',-25,cp],[],''])
  self.facial.append(['btn','btn_browL','browsL','sel','ctrl_browL',50,30,0.6,['btn_browL','bottom',40,'btn_eyeAimsF'],['btn_browL','left',0,'btn_glabella'],[],''])
  self.facial.append(['btn','btn_browR','browsR','sel','ctrl_browR',50,30,0.6,['btn_browR','bottom',40,'btn_eyeAimsF'],['btn_browR','right',0,'btn_glabella'],[],''])
  
  self.facial.append(['btn','btn_jaw','jaw','sel','ctrl_jaw',60,40,0.4,['btn_jaw','bottom',80],['btn_jaw','left',-30,cp],[],''])
  
  self.facial.append(['btn','btn_selAllF','select all','sels','all',100,50,-1,['btn_selAllF','top',10,'btn_faceCam'],['btn_selAllF','left',5],[],''])
  
  self.tail = []
  self.tail.append(['btn','btn_tailTT','tail','sel','ctrl_tail',80,50,0.5,['btn_tailTT','top',80],['btn_tailTT','left',-40,cp],[],''])
  self.tail.append(['btn','btn_tailFK1','FK1','sel','ctrl_tailFK1',50,30,0.6,['btn_tailFK1','top',0,'btn_tailTT'],['btn_tailFK1','right',-40,'btn_tailTT'],[],''])
  self.tail.append(['btn','btn_tailFK2','FK2','sel','ctrl_tailFK2',50,30,0.6,['btn_tailFK2','top',0,'btn_tailFK1'],['btn_tailFK2','right',-50,'btn_tailFK1'],[],''])
  self.tail.append(['btn','btn_tailFK3','FK3','sel','ctrl_tailFK3',50,30,0.6,['btn_tailFK3','top',0,'btn_tailFK2'],['btn_tailFK3','right',-50,'btn_tailFK2'],[],''])
  self.tail.append(['btn','btn_tailFK4','FK4','sel','ctrl_tailFK4',50,30,0.6,['btn_tailFK4','top',0,'btn_tailFK3'],['btn_tailFK4','right',-50,'btn_tailFK3'],[],''])
  self.tail.append(['btn','btn_tailFK5','FK5','sel','ctrl_tailFK5',50,30,0.6,['btn_tailFK5','top',0,'btn_tailFK4'],['btn_tailFK5','right',-50,'btn_tailFK4'],[],''])
  self.tail.append(['btn','btn_tailIK1','IK1','sel','ctrl_tailIK1',50,60,0.4,['btn_tailIK1','top',0,'btn_tailTT'],['btn_tailIK1','left',-40,'btn_tailTT'],[],''])
  self.tail.append(['btn','btn_tailIK2','IK2','sel','ctrl_tailIK2',50,60,0.4,['btn_tailIK2','top',0,'btn_tailIK1'],['btn_tailIK2','left',-50,'btn_tailIK1'],[],''])
  self.tail.append(['btn','btn_tailIK3','IK3','sel','ctrl_tailIK3',50,60,0.4,['btn_tailIK3','top',0,'btn_tailIK2'],['btn_tailIK3','left',-50,'btn_tailIK2'],[],''])
  
  if(cmds.window('win_warAnim',exists=1)):
   cmds.deleteUI('win_warAnim')
  cmds.window('win_warAnim',title='warAnim')

  cmds.formLayout('form_warAnimMain',width=550)
  cmds.button('btn_refresh',label='refresh',width=45,height=20,command=self.checkScene)
  cmds.optionMenu('oMenu',label='Character',changeCommand=self.loadB)
  cmds.optionMenu('pMenu',label='',changeCommand=self.loadB)
  cmds.text('txt_ann1',label='Press Ctrl to add selection')
  cmds.setParent( '..' )
  cmds.formLayout('form_warAnimMain',e=1,af=[('btn_refresh','top',5),('btn_refresh','left',5)])
  cmds.formLayout('form_warAnimMain',e=1,af=('oMenu','top',5),ac=('oMenu','left',5,'btn_refresh'))
  cmds.formLayout('form_warAnimMain',e=1,af=('pMenu','top',5),ac=('pMenu','left',5,'oMenu'))
  cmds.formLayout('form_warAnimMain',e=1,af=[('txt_ann1','bottom',5),('txt_ann1','left',5)])

  self.checkScene()
  cmds.showWindow('win_warAnim')

 def checkScene(self,*a):
  am = cmds.optionMenu('oMenu',q=1,itemListLong=1)
  if am is not None :
   for x in am :
    cmds.deleteUI(x,menuItem=1)
  menuList = []
  if cmds.objExists('here') : menuList.append('root')
  ref = cmds.ls(type='reference')
  for x in ref :
   if x != 'sharedReferenceNode' and cmds.referenceQuery(x,isLoaded=True)==1 :
    ns = cmds.referenceQuery(x,namespace=True)
    if cmds.objExists(ns+':here') : menuList.append(ns)
  for x in menuList :
   cmds.menuItem(x,parent='oMenu')
  if len(menuList) > 0 : self.checkCtrl()
  self.loadB()

 def checkCtrl(self,*a):
  am = cmds.optionMenu('pMenu',q=1,itemListLong=1)
  if am is not None :
   for x in am :
    cmds.deleteUI(x,menuItem=1)
  menuList = []
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  if ov :
   if cmds.objExists(ov+':ctrl_torso') :
    menuList.append('body')
   if cmds.objExists(ov+':ctrl_facial') :
    menuList.append('face')
   if cmds.objExists(ov+':ctrl_tail') :
    menuList.append('tail')
   for x in menuList :
    cmds.menuItem(x,parent='pMenu')

 def loadB(self,*a):
  for x in self.ctrl :
   if cmds.nodeIconButton(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.button(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.floatSliderGrp(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
  for x in self.facial :
   if cmds.nodeIconButton(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.button(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.floatSliderGrp(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
  for x in self.tail :
   if cmds.nodeIconButton(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.button(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
   if cmds.floatSliderGrp(x[1],exists=1) : cmds.deleteUI(x[1],control=1)
  if cmds.optionMenu('oMenu',q=1,numberOfItems=1) > 0 :
   if cmds.optionMenu('pMenu',q=1,value=1) == 'body' :
    #self.bodyButton()
    self.generateButton(self.ctrl)
   if cmds.optionMenu('pMenu',q=1,value=1) == 'face' :
    self.generateButton(self.facial)
   if cmds.optionMenu('pMenu',q=1,value=1) == 'tail' :
    self.generateButton(self.tail)

 def generateButton(self,btnList):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  
  for i in range(len(btnList)) :
   s = 0.15
   if btnList[i][7] == -1 : s = 0
   if btnList[i][0] == 'itbtn' :
    if btnList[i][3] == 'sel' :
     if cmds.objExists(ov+':'+btnList[i][4]) :
      cmds.nodeIconButton(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.selCtrlCmd(btnList[i][4]),parent='form_warAnimMain',style='iconAndTextCentered')
   if btnList[i][0] == 'btn' :
    if btnList[i][3] == 'sel' :
     if cmds.objExists(ov+':'+btnList[i][4]) :
      cmds.button(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.selCtrlCmd(btnList[i][4]),parent='form_warAnimMain')
      #cmds.nodeIconButton(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.selCtrlCmd(btnList[i][4]),parent='form_warAnimMain',style='iconAndTextCentered')
      cmds.popupMenu()
      if len(btnList[i][10]) > 0 : cmds.menuItem(label='Select Set',command=self.selCtrlsCmd(btnList[i][10]))
      cmds.menuItem(label='Set Default',command=self.setDefCmd(btnList[i][4]))
      if btnList[i][11] != '' : cmds.menuItem(label='Mirror Attribute',command=self.mirCtrlCmd(btnList[i][4],btnList[i][11]))
    if btnList[i][3] == 'sels' :
      cmds.button(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.selCtrlsCmd(btnList[i][4]),parent='form_warAnimMain')
      #cmds.nodeIconButton(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.selCtrlsCmd(btnList[i][4]),parent='form_warAnimMain',style='iconAndTextCentered')
    if btnList[i][3] == 'def' :
      cmds.button(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.setSelDef,parent='form_warAnimMain')
      #cmds.nodeIconButton(btnList[i][1],label=btnList[i][2],width=btnList[i][5],height=btnList[i][6],backgroundColor=self.hsvRgb(btnList[i][7],s,0.35),command=self.setSelDef,parent='form_warAnimMain',style='iconAndTextCentered')
   if btnList[i][0] == 'sld' :
    if btnList[i][3] == 'FKIK' :
     if cmds.objExists(ov+':'+btnList[i][4]) :
      cmds.floatSliderGrp(btnList[i][1],width=btnList[i][5],minValue=0.0,maxValue=1.0,changeCommand=self.sliderAttrCmd(btnList[i][1],btnList[i][4],'FKIK'),parent='form_warAnimMain')

  for i in range(len(btnList)) :
   if cmds.button(btnList[i][1],exists=1) or cmds.floatSliderGrp(btnList[i][1],exists=1) or cmds.nodeIconButton(btnList[i][1],exists=1) :
#   if cmds.nodeIconButton(btnList[i][1],exists=1) or cmds.floatSliderGrp(btnList[i][1],exists=1) :
    for j in range(8,10):
     if len(btnList[i][j]) == 3 : cmds.formLayout('form_warAnimMain',e=1,af=btnList[i][j])
     if len(btnList[i][j]) == 4 :
      if type(btnList[i][j][3]) == type(0) : cmds.formLayout('form_warAnimMain',e=1,ap=btnList[i][j])
      if type(btnList[i][j][3]) == type('') : cmds.formLayout('form_warAnimMain',e=1,ac=btnList[i][j])
      if type(btnList[i][j][3]) == type([]) :
       aList = btnList[i][j][3]
       tList = btnList[i][j][:]
       for x in aList :
        if cmds.button(x,q=1,exists=1):
         tList[3] = x
         cmds.formLayout('form_warAnimMain',e=1,ac=tList)
         break

  ref = cmds.ls(type='reference')
  for x in ref :
   ns = cmds.referenceQuery(x,namespace=True)
   if ns == ov :
    fp = cmds.referenceQuery(x,filename=1)
    fp = fp.replace('.ma','.jpg')
    fp = fp.replace('.mb','.jpg')
    if cmds.file(fp,q=1,exists=1) :
     cmds.nodeIconButton('btn_asset',e=1,image1=fp,label='')
	 
 def faceButton(self):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'

 def selCtrlCmd(self,ctrl):
  return lambda args:self.selCtrl(ctrl)

 def selCtrl(self,ctrl):
  print ctrl
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  mods = cmds.getModifiers()
  if mods == 4 : cmds.select(ov+':'+ctrl,add=1)
  else : cmds.select(ov+':'+ctrl,replace=1)

 def selCtrlsCmd(self,ctrls):
  if ctrls == 'all' :
   ctrls = []
   for x in self.ctrl :
    ctrls.append(x[4])
  return lambda args:self.selCtrls(ctrls)

 def selCtrls(self,ctrl):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  for i in range(len(ctrl)) :
   cn = ov+':'+ctrl[i]
   if cmds.objExists(cn) :
    if i == 0 : cmds.select(ov+':'+ctrl[i],replace=1)
    else : cmds.select(ov+':'+ctrl[i],add=1)

 def mirCtrlCmd(self,sCtrl,tCtrl):
  return lambda args:self.mirCtrl(sCtrl,tCtrl)

 def mirCtrl(self,sCtrl,tCtrl):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  cb = cmds.listAttr(ov+':'+tCtrl,keyable=1,userDefined=0)
  for x in cb :
   if x in ['tx','translateX'] :
    cmds.setAttr(ov+':'+tCtrl+'.'+x,cmds.getAttr(ov+':'+sCtrl+'.'+x)*-1)
   if x in ['ty','translateY','tz','translateZ'] :
    cmds.setAttr(ov+':'+tCtrl+'.'+x,cmds.getAttr(ov+':'+sCtrl+'.'+x))

 def sliderAttrCmd(self,sld,ctrl,attr):
  return lambda args:self.sliderAttr(sld,ctrl,attr)

 def sliderAttr(self,sld,ctrl,attr):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  cmds.select(ov+':'+ctrl,r=1)
  sv = cmds.floatSliderGrp(sld,q=1,value=1)
  cmds.setAttr(ov+':'+ctrl+'.'+attr,sv)

 def setDefCmd(self,ctrl):
  return lambda args:self.setDef(ctrl)

 def setDef(self,ctrl):
  ov = cmds.optionMenu('oMenu',q=1,value=1)
  if ov == 'root' : ov = ':'
  self.setDefValue(ov+':'+ctrl)

 def setSelDef(self,*arg):
  sl = cmds.ls(selection=1,long=1)
  for x in sl :
   self.setDefValue(x)

 def setDefValue(self,ctrl):
  try :
   cb = cmds.listAttr(ctrl,keyable=1)
   cbUser = cmds.listAttr(ctrl,keyable=1,userDefined=1)
   cbUall = cmds.listAttr(ctrl,userDefined=1)
   for x in cb :
    at = ctrl + '.' + x
    aType = cmds.getAttr(at,type=1)
    if aType != 'enum' and aType != 'bool' and cb != 'FKIK' :
     tv = 0.0
     if aType == 'double' : tv = 1.0
     if cbUser is not None :
      if x in cbUser : tv = cmds.addAttr(at,q=1,defaultValue=1)
     if cbUall is not None :
      if x in ['tx','translateX'] and 'dtx' in cbUall : tv = cmds.getAttr(ctrl + '.dtx')
      if x in ['ty','translateY'] and 'dty' in cbUall : tv = cmds.getAttr(ctrl + '.dty')
      if x in ['tz','translateZ'] and 'dtz' in cbUall : tv = cmds.getAttr(ctrl + '.dtz')
      if x in ['rx','rotateX'] and 'drx' in cbUall : tv = cmds.getAttr(ctrl + '.drx')
      if x in ['ry','rotateY'] and 'dry' in cbUall : tv = cmds.getAttr(ctrl + '.dry')
      if x in ['rz','rotateZ'] and 'drz' in cbUall : tv = cmds.getAttr(ctrl + '.drz')
     cmds.setAttr(at,tv)
   if cmds.objExists(ctrl+'_dro'):
    cmds.delete(cmds.orientConstraint(ctrl+'_dro',ctrl))
  except:
   pass

 def hsvRgb(self,h,s,v):
  i = math.floor(h*6)
  f = h*6 - i
  p = v * (1-s)
  q = v * (1-f*s)
  t = v * (1-(1-f)*s)
  r,g,b = [(v, t, p),(q, v, p),(p, v, t),(p, q, v),(t, p, v),(v, p, q),][int(i%6)]
  return r, g, b

warAnim()

