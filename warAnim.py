import sys
import math
from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance

global colorIndexList
colorIndexList = ['gray','black','darkgray','lightgray','red','darkblue'
     ,'blue','darkgreen','darkpurple','magenta','brown','darkbrown','tan'
     ,'red','green','indigo','white','lightyellow','lightblue','lightgreen'
     ,'pink','orange','lightyellow','green','brown','darkyellow','grass'
     ,'green','lightpink','gold','teal','magenta']

def mayaMainWindow():
    """Get the Maya main window as parent"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget) 
    
class CustomButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButton, self).__init__(text, parent)
        self.ns = ''
        ts = text.split(':')
        print(ts)
        if len(ts) >= 2 :
         self.setText(ts[-1])
         self.ns = ts[0]+':'
        self.clicked.connect(self.select)
        
    def select(self):
        cmds.select(self.ns+self.text(),r=1)

class CustomPolygonItem(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, selObj, parent=None):
        super(CustomPolygonItem, self).__init__(parent)
        
        self.setPen(QtGui.QPen(QtGui.QColor('gray'),0.5))
        
        shape = 'rect' # default shape
        if cmds.objExists(selObj+'.warShape') : shape = cmds.getAttr(selObj+'.warShape',asString=1)
        w = 10
        if cmds.objExists(selObj+'.warWidth') : w = cmds.getAttr(selObj+'.warWidth')
        h = 10
        if cmds.objExists(selObj+'.warHeight') : h = cmds.getAttr(selObj+'.warHeight')
        
        points = [(-1*w,-1*h),(-1*w,1*h),(1*w,1*h),(1*w,-1*h)]# default shape is rect
        if shape == 'circle' : points = self.circleShape(w,h)
        elif shape == 'trigU' : points = self.trigUShape(w,h)
        elif shape == 'trigD' : points = self.trigDShape(w,h)
        elif shape == 'trigL' : points = self.trigLShape(w,h)
        elif shape == 'trigR' : points = self.trigRShape(w,h)
        elif shape == 'diamond' : points = self.diamondShape(w,h)
        elif shape == 'trapezoidU' : points = self.trapezoidUShape(w,h)
        elif shape == 'trapezoidD' : points = self.trapezoidDShape(w,h)
        elif shape == 'hexagon' : points = self.hexagonShape(w,h)
        polygon = QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in points])
        self.setPolygon(polygon)
        
        colorName='darkblue'
        s = cmds.listRelatives(selObj,shapes=1)[0]
        if cmds.getAttr(s+'.overrideEnabled') :
         ci = cmds.getAttr(s+'.overrideColor')
         if cmds.getAttr(s+'.overrideRGBColors'):
          cr = cmds.getAttr(s+'.overrideColorR') * 255
          cg = cmds.getAttr(s+'.overrideColorG') * 255
          cb = cmds.getAttr(s+'.overrideColorB') * 255
          self.setBrush(QtGui.QBrush(QtGui.QColor(cr,cg,cb)))
         else:
          colorName = colorIndexList[ci]
          self.setBrush(QtGui.QBrush(QtGui.QColor(colorName)))
        else: self.setBrush(QtGui.QBrush(QtGui.QColor(colorName)))
        
        self.setFlags(
         #QGraphicsRectItem.ItemIsMovable |
         QtWidgets.QGraphicsPolygonItem.ItemIsSelectable
         #QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.selObj = selObj
        
    def circleShape(self,w,h):
        posList = []
        i = 0
        while (i <= 20) :
         cos = math.cos(math.radians(18*i))
         sin = math.sin(math.radians(18*i))
         posList.append((cos*w,sin*h))
         i = i + 1
        return posList
        
    def trigUShape(self,w,h):
        return [(0,-1*h),(-1*w,1*h),(1*w,1*h)]
        
    def trigDShape(self,w,h):
        return [(-1*w,-1*h),(0,1*h),(1*w,-1*h)]
        
    def trigLShape(self,w,h):
        return [(-1*w,-1*h),(-1*w,1*h),(1*w,0)]
        
    def trigRShape(self,w,h):
        return [(1*w,-1*h),(-1*w,0),(1*w,1*h)]
        
    def diamondShape(self,w,h):
        return [(0,-1*h),(-1*w,0),(0,1*h),(1*w,0)]
        
    def trapezoidUShape(self,w,h):
        return [(-0.8*w,-1*h),(-1*w,1*h),(1*w,1*h),(0.8*w,-1*h)]

    def trapezoidDShape(self,w,h):
        return [(-1*w,-1*h),(-0.8*w,1*h),(0.8*w,1*h),(1*w,-1*h)]
        
    def hexagonShape(self,w,h):
        return [(-0.67*w,-1*h),(-1*w,0),(-0.67*w,1*h),(0.67*w,1*h),(1*w,0),(0.67*w,-1*h)]

class CustomGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        super(CustomGraphicsView, self).__init__(scene, parent)
        self.setScene(scene)

        self.start_pos = None
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
        self.scene().selectionChanged.connect(self.selectItemChange)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
         # Start panning mode
         self._is_panning = True
         self._pan_start = event.pos()
         self.setCursor(QtCore.Qt.ClosedHandCursor)
         return
         
        elif event.button() == QtCore.Qt.LeftButton:
         # Start selection rectangle
         self.start_pos = self.mapToScene(event.pos())
         self.selection_rect.setRect(QtCore.QRectF(self.start_pos, self.start_pos))
         self.selection_rect.setVisible(True)
         item = self.scene().itemAt(self.start_pos, QtGui.QTransform())
         if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
          if item : item.setSelected(True)
          return
         if item is None : cmds.select(cl=1)
         
        elif event.button() == QtCore.Qt.RightButton:
         if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier:
          # Start scaling mode
          self._is_scaling = True
          self._scale_start = event.pos()
          self.setCursor(QtCore.Qt.SizeHorCursor)
         return
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
         self.selectItemInRect(self.selection_rect.rect())
         self.start_pos = None
         self.selection_rect.setVisible(False)
        super(CustomGraphicsView, self).mouseReleaseEvent(event)

    def selectItemInRect(self, rect):
        """Select items within the rectangle"""
        itemsInRect = self.scene().items(rect, QtCore.Qt.IntersectsItemShape)
        itemsInRect = itemsInRect[1:]
        
        for item in itemsInRect:
         item.setSelected(True)
        
        if itemsInRect:
         for item in itemsInRect:
          item.setSelected(True)
        #else :
        # area = rect.width() * rect.height()
        # if area > 2 : cmds.select(cl=1)
         
    def selectItemChange(self):
        selItem = self.scene().selectedItems()
        objList = [ x.selObj for x in selItem ]
        #print(objList)
        cmds.select(objList,r=1)
        
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        actDef = menu.addAction("Set Default Value")
        action = menu.exec_(event.globalPos())
        
        if action == actDef:
         selItem = self.scene().selectedItems()
         objList = [ x.selObj for x in selItem ]
         #print(objList)
         for obj in objList : self.setDefaultValue(obj)
          
    def setDefaultValue(self, obj):
        la = cmds.listAttr(obj,keyable=1,unlocked=1)
        for x in la :
         if x == 'translateX' : cmds.setAttr(obj+'.'+x,0)
         elif x == 'translateY' : cmds.setAttr(obj+'.'+x,0)
         elif x == 'translateZ' : cmds.setAttr(obj+'.'+x,0)
         elif x == 'rotateX' : cmds.setAttr(obj+'.'+x,0)
         elif x == 'rotateY' : cmds.setAttr(obj+'.'+x,0)
         elif x == 'rotateZ' : cmds.setAttr(obj+'.'+x,0)
         elif x in ['scaleX','scaleY','scaleZ'] : cmds.setAttr(obj+'.'+x,1)
        print('Set '+obj+' default value.')
        
class warAnimUI(QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(warAnimUI, self).__init__(parent)
        self.setObjectName('win_aspw')
        self.setWindowTitle('warAnim')
        
        self.ctrlTop = 'ctrl_location'
        self.dropdownList = cmds.ls(self.ctrlTop,'*:'+self.ctrlTop,showNamespace=1)[1::2]
        if not self.dropdownList :
         self.ctrlTop = 'MotionSystem' # advSkeleton
         self.dropdownList = cmds.ls(self.ctrlTop,'*:'+self.ctrlTop,showNamespace=1)[1::2]
        
        self.createUi()
        self.connectDropdownChange()
        
    def createUi(self):
        vLayout = QtWidgets.QVBoxLayout(self)
        self.dropdown = QtWidgets.QComboBox()       
        #self.dropdown.addItems(["1", "2", "3", "4", "5"])
        if self.dropdownList : self.dropdown.addItems(self.dropdownList)
        vLayout.addWidget(self.dropdown)
        
        self.toolBar = QtWidgets.QToolBar()
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        vLayout.addWidget(self.toolBar)
        
        self.tab_widget = QtWidgets.QTabWidget()
        vLayout.addWidget(self.tab_widget)
        if self.dropdownList : self.updateTabs()
    
        self.resize(410,550)
        
    def connectDropdownChange(self):
     self.dropdown.currentIndexChanged.connect(self.dropdownChange)

    def dropdownChange(self):
     self.updateTabs()
    
    def updateTabs(self):
     selTxt = self.dropdown.currentText()
     print('Start update '+selTxt+' tabs.')
     topName = selTxt+':'+self.ctrlTop
     if selTxt == ':' : topName = self.ctrlTop
     allCrv = cmds.listRelatives(topName,allDescendents=1,type='nurbsCurve')
     if self.ctrlTop == 'MotionSystem' :
      faceTopName = selTxt+':FaceMotionSystem'
      faceCrv = cmds.listRelatives(faceTopName,allDescendents=1,type='nurbsCurve')
      allCrv.extend(faceCrv)
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
      self.tab_widget.addTab(tab, x)
      tabCtrl = []
      for y in allCtrl :
       if cmds.objExists(y+'.warTab'):
        tab = cmds.getAttr(y+'.warTab',asString=1)
        if tab == x : tabCtrl.append(y)
      
      gScene = QtWidgets.QGraphicsScene()
      gView = CustomGraphicsView(gScene, self)
      gBorder = self.add_items(gScene,tabCtrl) # [+x(right),-x(left),+y(bottom),-y(top)]
      tab_layout.addWidget(gView)
      #print(gBorder)
      gScene.setSceneRect(gBorder[1],gBorder[3],gBorder[0]+-gBorder[1],gBorder[2]+-gBorder[3])
      gradient = QtGui.QLinearGradient(0,0,0,gBorder[3]+-gBorder[2])
      gradient.setColorAt(0,QtGui.QColor(20,20,20))
      gradient.setColorAt(1,QtGui.QColor(40,40,40))
      gScene.setBackgroundBrush(QtGui.QBrush(gradient))
      gView.scale(1.2,1.2)
    
    def add_items(self,scene,ctrls):
     ci = 5 # default color index
     ns = self.dropdown.currentText()
     if ns == ':' : ns = ''
     else : ns = ns + ':'
     gBorder = [100,-100,100,-100] # default sSize
     
     ''' Start ctrl loop '''
     #print(ctrls) # ctrl list before sorting
     for i in range(len(ctrls)):
      if cmds.objExists(ctrls[i]+'.warAttach') :
       en = cmds.addAttr(ctrls[i]+'.warAttach',q=1,enumName=1)
       eList = en.split(':')
       for j in range(len(eList)):
        eStr = ns + eList[j]
        if eStr in ctrls:
         eIndex = ctrls.index(eStr)
         if eIndex > i :
          ctrls[i],ctrls[eIndex] = ctrls[eIndex],ctrls[i]
          j = j - 1
     print(ctrls) # ctrl list after sorting
     
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
      
      ''' Set existing coordinates '''
      posX = 0
      posY = 0
      if cmds.objExists(x+'.warPosX'): posX = cmds.getAttr(x+'.warPosX')
      if cmds.objExists(x+'.warPosY'): posY = cmds.getAttr(x+'.warPosY')
      
      ''' Finding attach object  '''
      if cmds.objExists(x+'.warAttach') and cmds.objExists(x+'.warAttachSide') :    
       ac = cmds.getAttr(x+'.warAttach',asString=1)
       enumList = cmds.addAttr(x+'.warAttach',q=1,enumName=1).split(':')
       for y in enumList :
        nsY = ns + y
        if nsY in ctrls:
         ac = y
         cmds.setAttr(x+'.warAttach',enumList.index(y))
         break
       ac = ns + ac
       
       al = cmds.getAttr(x+'.warAttachSide',asString=1)
       ''' Calculate X '''
       if cmds.objExists(ac+'.warPosX'):
        acX = cmds.getAttr(ac+'.warPosX')
        acw = cmds.getAttr(ac+'.warWidth')
        posX = acX
        if al in ['right','topRight','bottomRight','rightToTop'] :
         posX = acX + acw + w + 2
        if al in ['left','topLeft','bottomLeft','leftToTop'] :
         posX = acX - acw - w - 2
        if al in ['topToRight','bottomToRight'] :
         posX = acX + acw - w + 2
        if al in ['topToLeft','bottomToLeft'] :
         posX = acX - acw + w - 2
        cmds.setAttr(x+'.warPosX',posX)
        xBorder = round((posX+w)*1.2)
        if xBorder > 0 and xBorder > gBorder[0] : gBorder[0] = xBorder
        if xBorder < 0 and xBorder < gBorder[1] : gBorder[1] = xBorder
        
       ''' Calculate Y '''
       if cmds.objExists(ac+'.warPosY'):
        acY = cmds.getAttr(ac+'.warPosY')
        ach = cmds.getAttr(ac+'.warHeight')
        posY = acY
        if al in ['top','topLeft','topRight','topToLeft','topToRight']:
         posY = acY - ach - h - max(round(max(ach,h)*0.2),2)
        if al in ['bottom','bottomLeft','bottomRight','bottomToRight','bottomToLeft']:
         posY = acY + ach + h + max(round(max(ach,h)*0.2),2)
        if al in ['leftToTop','rightToTop']:
         posY = acY - ach + h
        if al in ['leftToBottom','rightToBottom']:
         posY = acY + ach - h
        cmds.setAttr(x+'.warPosY',posY)
        yBorder = round((posY+h)*1.2)
        if yBorder > 0 and yBorder > gBorder[2] : gBorder[2] = yBorder
        if yBorder < 0 and yBorder < gBorder[3] : gBorder[3] = yBorder
      
      gItem = CustomPolygonItem(x)
      gItem.setPos(posX,posY)
      scene.addItem(gItem)
     return gBorder

def warAnim():
 global ui
 try:
  ui.close()  # Close the existing window if it exists
 except:
  pass
 ui = warAnimUI()
 ui.show()

warAnim()