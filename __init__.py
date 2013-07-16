from cadtools import CadTools
from PyQt4.QtCore import *

def name():
    return "CadTools"

def description():
    return QCoreApplication.translate("init", "Some tools to perform cad like functions.")

def version():
    return "0.6.0"

def qgisMinimumVersion():
    return "1.3"
	
def qgisMaximumVersion():
    return "2.99"

def authorName():
    return "Stefan Ziegler"
    
def icon():
	return "icons/orthopoint.png"        

def classFactory(iface):
    return CadTools(iface)
