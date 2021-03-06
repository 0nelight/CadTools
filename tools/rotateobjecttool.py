# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import math
from cadtools import resources

## Import own classes and tools.
from vertexandobjectfindertool import VertexAndObjectFinderTool
from rotateobjectgui import RotateObjectGui
import cadutils

class RotateObjectTool:
    
    def __init__(self, iface,  toolBar):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.p1 = None
        self.m1 = None
        self.feat = None
        self.rb = None
        
        self.act_rotateobject = QAction(QIcon(":/plugins/cadtools/icons/rotatefeature.png"), QCoreApplication.translate("ctools", "Rotate Object"),  self.iface.mainWindow())
        self.act_selectvertexandobject= QAction(QIcon(":/plugins/cadtools/icons/selectvertexandfeature.png"), QCoreApplication.translate("ctools", "Select Vertex and Object"),  self.iface.mainWindow())
        self.act_selectvertexandobject.setCheckable(True)     
             
        self.act_rotateobject.triggered.connect(self.showDialog)
        self.act_selectvertexandobject.triggered.connect(self.selectvertexandobject)
        self.canvas.mapToolSet.connect(self.deactivate)

        toolBar.addSeparator()
        toolBar.addAction(self.act_selectvertexandobject)
        toolBar.addAction(self.act_rotateobject)
                    
        self.tool = VertexAndObjectFinderTool(self.canvas)   


    def selectvertexandobject(self):
        mc = self.canvas
        mc.setMapTool(self.tool)
        
        self.act_selectvertexandobject.setChecked(True)       
 
        self.tool.vertexAndObjectFound.connect(self.storeVertexAndObject)
 
        pass
        
    def storeVertexAndObject(self,  result):
        self.p1 = result[0]
        self.feat = result[1]
        self.m1 = result[2]
        self.rb = result[3]
    
    
    def showDialog(self):

        if self.p1 == None or self.feat == None:
            QMessageBox.information(None, QCoreApplication.translate("ctools", "Cancel"), QCoreApplication.translate("ctools", "Not enough objects selected."))
        else:
            #az = Azimuth.calculate(self.p1,  self.p2)
            
            flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  
            self.ctrl = RotateObjectGui(self.iface.mainWindow(),  flags)
            self.ctrl.initGui()
            self.ctrl.show()

            self.ctrl.okClicked.connect(self.rotateObject)
            self.ctrl.unsetTool.connect(self.unsetTool)
        
        pass


    def rotateObject(self,  angle):
        geom = cadutils.rotate(self.feat.geometry(), self.p1,  angle * math.pi / 180)
        if geom <> None:
            cadutils.addGeometryToCadLayer(geom)
            self.canvas.refresh()

        
    def unsetTool(self):
        self.m1 = None
        self.rb.reset()
        mc = self.canvas
        mc.unsetMapTool(self.tool)             
        
        
    def deactivate(self):
        self.p1 = None
        self.act_selectvertexandobject.setChecked(False)
    
