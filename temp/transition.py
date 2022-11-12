from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

class transWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(transWidget, self).__init__() # Call the inherited classes __init__ method
        widget_dir = "resources/ui/transition.ui"
        self.twidget = uic.loadUi(widget_dir, self) # Load the .ui file
        self.isWidgetType = uic.loadUi(widget_dir, self) # Load transition widget
        self.setWindowIcon(QtGui.QIcon('resources/ico/market_icon.ico'))