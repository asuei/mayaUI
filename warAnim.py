import sys
import math
from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

def mayaMainWindow():
    """Get the Maya main window as parent"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget) 
    
class CustomButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButton, self).__init__(text, parent)
        self.clicked.connect(self.select)
        
    def select(self):
        cmds.select(self.text(),r=1)
    
class CustomRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, rect, selObj, colorName='darkblue', parent=None):
        super(CustomRectItem, self).__init__(rect, parent)
        self.setBrush(QtGui.QBrush(QtGui.QColor(colorName)))
        self.setPen(QtGui.QPen(QtGui.QColor('gray'), 1))
        
        self.setFlags(
            #QGraphicsRectItem.ItemIsMovable |
            QtWidgets.QGraphicsRectItem.ItemIsSelectable
            #QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.selObj = selObj
        
    def mousePressEvent(self, event):
        #print(f"Rectangle clicked at {event.pos()}")
        cmds.select(self.selObj,r=1)
        super(CustomRectItem, self).mousePressEvent(event)
        
    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
         if value:
          if cmds.objExists(self.selObj): pass
           #cmds.select(self.selObj, r=True)
          else: pass
           #print('Object '+self.selObj+' does not exist in the scene.')
        return super(CustomRectItem, self).itemChange(change, value)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        actDef = menu.addAction("Set Default Value")
        
        selected_action = menu.exec_(event.screenPos())
        
        if selected_action == actDef:
         #cb = cmds.channelBox('mainChannelBox',q=1,selectedMainAttributes=1)
         la = cmds.listAttr(self.selObj,keyable=1,unlocked=1)
         for x in la :
          if x == 'translateX' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'translateY' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'translateZ' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'rotateX' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'rotateY' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'rotateZ' : cmds.setAttr(self.selObj+'.'+x,0)
          if x == 'scaleX' : cmds.setAttr(self.selObj+'.'+x,1)
          if x == 'scaleY' : cmds.setAttr(self.selObj+'.'+x,1)
          if x == 'scaleZ' : cmds.setAttr(self.selObj+'.'+x,1)
         print('Set '+self.selObj+' default value.')

class CustomGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        super(CustomGraphicsView, self).__init__(scene, parent)
        self.setScene(scene)

        self.start_pos = None
        #self.selection_rect = QtWidgets.QGraphicsRectItem()
        self.selection_rect = QtWidgets.QGraphicsRectItem()
        self.selection_rect.setPen(QtGui.QPen(QtCore.Qt.DashLine))
        self.selection_rect.setBrush(QtGui.QBrush(QtCore.Qt.transparent))
        self.selection_rect.setZValue(1000)
        self.scene().addItem(self.selection_rect)
        self.selection_rect.setVisible(False)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self._is_panning = False
        self._pan_start = None
        self._is_scaling = False
        self._scale_start = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning mode
            self._is_panning = True
            self._pan_start = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
        elif event.button() == QtCore.Qt.LeftButton:
            # Start selection rectangle
            self.start_pos = self.mapToScene(event.pos())
            self.selection_rect.setRect(QtCore.QRectF(self.start_pos, self.start_pos))
            self.selection_rect.setVisible(True)
        elif event.button() == QtCore.Qt.RightButton and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier:
            # Start scaling mode
            self._is_scaling = True
            self._scale_start = event.pos()
            self.setCursor(QtCore.Qt.SizeHorCursor)
        super(CustomGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning and self._pan_start:
            # Pan the view
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        elif self._is_scaling and self._scale_start:
            # Scale the view
            delta_x = event.pos().x() - self._scale_start.x()
            scale_factor = 1.0 + delta_x / 200.0
            self.scale(scale_factor, scale_factor)
            self._scale_start = event.pos()
        elif self.start_pos:
            # Update the selection rectangle
            current_pos = self.mapToScene(event.pos())
            rect = QtCore.QRectF(self.start_pos, current_pos).normalized()
            self.selection_rect.setRect(rect)
        super(CustomGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            # Stop panning mode
            self._is_panning = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif event.button() == QtCore.Qt.RightButton and self._is_scaling:
            # Stop scaling mode
            self._is_scaling = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif event.button() == QtCore.Qt.LeftButton and self.start_pos:
            # Complete selection
            self.select_items_in_rect(self.selection_rect.rect())
            self.start_pos = None
            self.selection_rect.setVisible(False)
        super(CustomGraphicsView, self).mouseReleaseEvent(event)

    def select_items_in_rect(self, rect):
        """Select items within the rectangle"""
        items_in_rect = self.scene().items(rect, QtCore.Qt.IntersectsItemShape)
        items_in_rect = items_in_rect[1:]
        selList = []
        for item in items_in_rect:
         item.setSelected(True)
         selList.append(item.selObj)
         #cmds.select(selList,r=1)
        
        if items_in_rect:
         for item in items_in_rect:
          item.setSelected(True)
          selList.append(item.selObj)
          cmds.select(selList,r=1)
        else :
         cmds.select(cl=1)
        
class warAnimUI(QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(warAnimUI, self).__init__(parent)
        self.setObjectName('win_aspw')
        self.setWindowTitle('warAnim')
        
        self.ctrlTop = 'ctrl_location'
        #self.ctrlTop = 'MotionSystem' # advSkeleton
        self.dropdownList = cmds.ls(self.ctrlTop,'*:'+self.ctrlTop,showNamespace=1)[1::2]
        
        self.create_ui()
        self.create_connections()
        
    def create_ui(self):
        vLayout = QtWidgets.QVBoxLayout(self)
        self.dropdown = QtWidgets.QComboBox()       
        #self.dropdown.addItems(["1", "2", "3", "4", "5"])
        self.dropdown.addItems(self.dropdownList)
        vLayout.addWidget(self.dropdown)
        
        self.toolBar = QtWidgets.QToolBar()
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        emptyAction = QtWidgets.QPushButton('normal')
        self.toolBar.addWidget(emptyAction)
        emptyActionB = QtWidgets.QPushButton('spacial')
        self.toolBar.addWidget(emptyActionB)
        vLayout.addWidget(self.toolBar)
        
        self.tab_widget = QtWidgets.QTabWidget()
        vLayout.addWidget(self.tab_widget)
        self.updateTabs()
    
        self.resize(600,800)
        
    def create_connections(self):
     self.dropdown.currentIndexChanged.connect(self.dropdownChange)

    def dropdownChange(self):
     self.updateTabs()
    
    def updateTabs(self):
     selTxt = self.dropdown.currentText()
     print('Start update '+selTxt+' tabs.')
     topName = selTxt+':'+self.ctrlTop
     if selTxt == ':' : topName = self.ctrlTop
     allCrv = cmds.listRelatives(topName,allDescendents=1,type='nurbsCurve')
     allCtrl = [ cmds.listRelatives(x,parent=1)[0] for x in allCrv ]

     allTabList = []
     self.globalCtrl = []
     for x in allCtrl :
      if cmds.objExists(x+'.warTab'):
       #print(x)
       tab = cmds.getAttr(x+'.warTab',asString=1)
       if tab not in allTabList : allTabList.append(tab)
       if tab == 'global' : self.globalCtrl.append(x)
     tabList = [ x for x in allTabList if x != 'global']
     #print(tabList)
     
     self.toolBar.clear()
     for i,x in enumerate(self.globalCtrl) :
      qButton = CustomButton(x) # add global button
      self.toolBar.addWidget(qButton)
     
     self.tab_widget.clear()
     for x in tabList :
      tab = QtWidgets.QWidget()
      tab_layout = QtWidgets.QVBoxLayout(tab)
      tab_layout.addWidget(QtWidgets.QLabel(x))
      self.tab_widget.addTab(tab, x)
      tabCtrl = []
      for y in allCtrl :
       if cmds.objExists(y+'.warTab'):
        tab = cmds.getAttr(y+'.warTab',asString=1)
        if tab == x : tabCtrl.append(y)
      
      gScene = QtWidgets.QGraphicsScene()
      gView = CustomGraphicsView(gScene, self)
      self.add_items(gScene,tabCtrl)
      tab_layout.addWidget(gView)
    
    def add_items(self,scene,ctrls):
     colorList = ['gray','black','darkgray','lightgray','darkred','darkblue'
     ,'blue','darkgreen','darkpurple','magenta','brown','darkbrown','tan'
     ,'red','green','indigo','white','lightyellow','lightblue','lightgreen'
     ,'pink','orange','lightyellow','green','brown','darkyellow','grass'
     ,'green','cyan','blue','purple','darkred']
     ci = 5
     ns = self.dropdown.currentText()
     if ns == ':' : ns = ''
     else : ns = ns + ':'
     ''' Start ctrl loop '''
     print(ctrls)
     for i,x in enumerate(ctrls) :
      #print(x)
      #item = QtWidgets.QGraphicsRectItem(50 + i * 60, 50, 50, 50)
      #item.setBrush(QtGui.QBrush(QtCore.Qt.blue))
      #item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
      #scene.addItem(item)
      
      w = 10
      h = 10
      if cmds.objExists(x+'.warWidth'): w = cmds.getAttr(x+'.warWidth')
      if cmds.objExists(x+'.warHeight'): h = cmds.getAttr(x+'.warHeight')
      
      posX = 0
      posY = 0
      if cmds.objExists(x+'.warPosX'): posX = cmds.getAttr(x+'.warPosX')
      if cmds.objExists(x+'.warPosY'): posX = cmds.getAttr(x+'.warPosY')
      ''' Start finding attach position  '''
      if cmds.objExists(x+'.warAttach') and cmds.objExists(x+'.warAttachSide') :    
       ac = cmds.getAttr(x+'.warAttach',asString=1)
       enumList = cmds.addAttr(x+'.warAttach',q=1,enumName=1).split(':')
       for y in enumList :
        if y in ctrls: ac = y
       al = cmds.getAttr(x+'.warAttachSide',asString=1)
       ac = ns + ac
       if cmds.objExists(ac+'.warPosX'):
        posX = cmds.getAttr(ac+'.warPosX')
        acw = cmds.getAttr(ac+'.warWidth')
        if al in ['right','topRight','bottomRight'] :
         posX = posX + acw + 25
         if cmds.objExists(x+'.warPosX'): cmds.setAttr(x+'.warPosX',posX)
        if al in ['left','topLeft','bottomLeft'] :
         posX = posX - acw - 25
         if cmds.objExists(x+'.warPosX'): cmds.setAttr(x+'.warPosX',posX)
       if cmds.objExists(ac+'.warPosY'):
        posY = cmds.getAttr(ac+'.warPosY')
        ach = cmds.getAttr(ac+'.warHeight')
        if al in ['top','topLeft','topRight'] :
         posY = posY - ach - 25
         if cmds.objExists(x+'.warPosY'): cmds.setAttr(x+'.warPosY',posY)
        if al in ['bottom','bottomLeft','bottomRight'] :
         posY = posY + ach + 25
         if cmds.objExists(x+'.warPosY'): cmds.setAttr(x+'.warPosY',posY)
         
      ''' Start finding color  '''
      s = cmds.listRelatives(x,shapes=1)[0]
      if cmds.getAttr(s+'.overrideEnabled') :
       ci = cmds.getAttr(s+'.overrideColor')
      
      gItem = CustomRectItem(QtCore.QRectF(posX-w,posY-h,w*2,h*2),x,colorName=colorList[ci])
      scene.addItem(gItem)

def warAnim():
 global ui
 try:
  ui.close()  # Close the existing window if it exists
 except:
  pass
 ui = warAnimUI()
 ui.show()

warAnim()