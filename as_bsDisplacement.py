import maya.cmds as cmds

class as_bsDisplacement:
 def __init__(self):
  if(cmds.window('win_bsSourcedisplacement',exists=1)):
   cmds.deleteUI('win_bsSourcedisplacement')
  cmds.window('win_bsSourcedisplacement',title='BlendShape Targets Displacement')
  
  cmds.gridLayout(numberOfColumns=1,cellWidth=200)
  cmds.button('bssdBtn_org',label='Load Original Geometry :',backgroundColor=[0.55,0.55,0.55],command=self.loadOrg)
  cmds.textField('bssdTf_org')
  cmds.button('bssdBtn_new',label='Load New Geometry :',backgroundColor=[0.55,0.55,0.55],command=self.loadNew)
  cmds.textField('bssdTf_new')
  cmds.button('bssdBtn_exe',label='select deformed and Execute',command=self.execute)
  cmds.showWindow('win_bsSourcedisplacement')

 def loadOrg(self,*a):
  sl = cmds.ls(selection=1,long=1)
  if len(sl) > 0 :
   cmds.textField('bssdTf_org',e=1,text=sl[0])

 def loadNew(self,*a):
  sl = cmds.ls(selection=1,long=1)
  if len(sl) > 0 :
   cmds.textField('bssdTf_new',e=1,text=sl[0])

 def execute(self,*a):
  org = cmds.textField('bssdTf_org',q=1,text=1)
  new = cmds.textField('bssdTf_new',q=1,text=1)
  sl = cmds.ls(selection=1,long=1)
  sls = cmds.ls(selection=1)
  
  for i,x in enumerate(sl) :
   bs = cmds.blendShape(org,x,weight=[0,1])
   cmds.duplicate(new,name='bssd_dTemp')
   cmds.delete(cmds.parentConstraint(x,'bssd_dTemp'))
   cmds.select(['bssd_dTemp',x],r=1)
   cmds.CreateWrap()
   cmds.setAttr(bs[0]+'.envelope',0)
   cmds.rename(x,sls[i]+'_old')
   n = cmds.duplicate('bssd_dTemp',name=sls[i])
   cmds.select(n,r=1)
   cmds.delete('bssd_dTemp')
   cmds.delete(bs[0])
   cmds.delete(sls[i]+'_old')

as_bsDisplacement().__init__()
