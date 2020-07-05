# encoding: utf-8
import maya.cmds as cmds
import re


class as_naming :
 def __init__(self):
  if(cmds.window('win_anm',exists=1)):
   cmds.deleteUI('win_anm')
  cmds.window('win_anm',title='as Naming')


  cmds.formLayout('form_anmMain')
  cmds.button('btn_anmSN',label='Sequence Naming',width=150,height=30,command=self.sequenceNaming)
  cmds.button('btn_anmCSN',label='Correct Shape Name',width=150,height=30,command=self.correntShapeName)
  cmds.separator('sprt1',style='in')
  cmds.button('btn_anmSSS',label='input same string',width=150,height=20,command=self.sameStringBtn)
  cmds.textField('txt_anmR1',text='',width=150,height=23)
  cmds.textField('txt_anmR2',text='',width=150,height=23,enterCommand=self.searchReplace)
  cmds.button('btn_anmRB',label='Search and Replace',width=150,height=30,command=self.searchReplace)
  cmds.separator('sprt2',style='in')
  cmds.textField('txt_anmPS',text='',width=150,height=23)
  cmds.button('btn_anmAP',label='Prefix',width=75,height=30,command=self.addPrefix)
  cmds.button('btn_anmAS',label='Suffix',width=75,height=30,command=self.addSuffix)


  cmds.formLayout('form_anmMain',e=1,af=[('btn_anmSN','top',5),('btn_anmSN','left',5)])
  cmds.formLayout('form_anmMain',e=1,ac=('btn_anmCSN','top',5,'btn_anmSN'),af=('btn_anmCSN','left',5))
  cmds.formLayout('form_anmMain',e=1,af=[('sprt1','left',5),('sprt1','right',5)],ac=('sprt1','top',5,'btn_anmCSN'))
  cmds.formLayout('form_anmMain',e=1,af=('btn_anmSSS','left',5),ac=('btn_anmSSS','top',3,'sprt1'))
  cmds.formLayout('form_anmMain',e=1,af=('txt_anmR1','left',5),ac=('txt_anmR1','top',5,'btn_anmSSS'))
  cmds.formLayout('form_anmMain',e=1,af=('txt_anmR2','left',5),ac=('txt_anmR2','top',3,'txt_anmR1'))
  cmds.formLayout('form_anmMain',e=1,af=('btn_anmRB','left',5),ac=('btn_anmRB','top',3,'txt_anmR2'))
  cmds.formLayout('form_anmMain',e=1,af=[('sprt2','left',5),('sprt2','right',5)],ac=('sprt2','top',5,'btn_anmRB'))
  cmds.formLayout('form_anmMain',e=1,af=('txt_anmPS','left',5),ac=('txt_anmPS','top',5,'sprt2'))
  cmds.formLayout('form_anmMain',e=1,af=('btn_anmAP','left',5),ac=('btn_anmAP','top',3,'txt_anmPS'))
  cmds.formLayout('form_anmMain',e=1,ac=[('btn_anmAS','left',0,'btn_anmAP'),('btn_anmAS','top',3,'txt_anmPS')])
  
  cmds.window('win_anm',e=1,widthHeight=[200,30],resizeToFitChildren=1)
  cmds.showWindow('win_anm')
  self.sameStringBtn()


 def sequenceNaming(self,*a):
  sa = len(cmds.ls(selection=1))
  setList = []
  for x in cmds.ls(selection=1):
   ts = cmds.sets(x)
   setList.append(ts)
  
  lss = cmds.ls(selection=1)[0]
  if '|' in lss : lss = lss.split('|')[-1]
  num = re.findall(r'\d+',lss)
  numI = [int(i) for i in num]
  strList = re.split(r'\d+',lss)


  i = 0
  for j in range(sa):
   lx = cmds.sets(setList[j],q=1)[0]
   numP = numI[0] + i
   nn = lss.replace(num[0],str(numP))
   cmds.rename(lx,nn)
   i = i + 1
  cmds.delete(setList)


 def sameStringBtn(self,*a):
  sl = cmds.ls(selection=1)
  for i,x in enumerate(sl) :
   sx = x.split('|')[-1]
   sl[i] = sx
  sw = self.findSameString(sl)
  cmds.textField('txt_anmR1',e=1,text=sw)
   
 def searchReplace(self,*a):
  sa = len(cmds.ls(selection=1))
  tf1 = cmds.textField('txt_anmR1',q=1,text=1)
  tf2 = cmds.textField('txt_anmR2',q=1,text=1)
  ts = cmds.sets(cmds.ls(selection=1))
  for i in range(sa) :
   lx = cmds.sets(ts,q=1)[i]
   sx = lx.split('|')[-1]
   rn = sx.replace(tf1,tf2)
   cmds.rename(cmds.sets(ts,q=1)[i],rn)        
  cmds.delete(ts)


 def findSameString(self,list,*a):
  sw = ''
  for h in range(1,len(list)):
   s1 = sw
   if h == 1 : s1 = list[0]
   s2 = list[h]
   sw = ''
   for i,x in enumerate(s1) :
    for j,y in enumerate(s1[i:]) :
     fs = x + s1[i+1:j+i+1]
     if s2.find(fs) >= 0 and len(fs)>len(sw) : sw = fs
  return sw
  
 def addPrefix(self,*a):
  txt = cmds.textField('txt_anmPS',q=1,text=1)
  for x in cmds.ls(selection=1):
   cmds.rename(x,txt+x)


 def addSuffix(self,*a):
  txt = cmds.textField('txt_anmPS',q=1,text=1)
  for x in cmds.ls(selection=1):
   cmds.rename(x,x+txt)
   
 def correntShapeName(self,*a):
  for x in cmds.ls(selection=1):
   s = cmds.listRelatives(x,shapes=1,noIntermediate=1,fullPath=1)
   if len(s)==1:
    cmds.rename(s[0],x.split('|')[-1]+'Shape')
  
as_naming()