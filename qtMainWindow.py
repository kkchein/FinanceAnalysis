import sys
import os
import traceback
from PyQt4 import QtGui
from PyQt4 import QtCore
import qtDrawQuote

class QtMainWindow(QtGui.QWidget):
    def __init__ (self, parent=None):
        try:
            super(QtMainWindow,self).__init__(parent)
            self.layout=QtGui.QVBoxLayout()
            self.setLayout(self.layout)
            self.btn=QtGui.QPushButton('Load',self)
            self.layout.addWidget(self.btn)
            self.browser=QtGui.QTextBrowser(self)
            self.layout.addWidget(self.browser)
            #
            self.connect(self.btn,QtCore.SIGNAL("clicked()"),self.loadBtn)
        except:
            self.toLog(traceback.format_exc())
    def loadBtn (self):
        try:
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", 
                                                         '.', "ini (*.ini);;csv (*.csv)")
            if os.path.exists(fileName)==False:
                self.toLog(fileName+" doesn't exist")
            newwindow=qtDrawQuote.QtDraw(self, inputFile=fileName)
            newwindow.show()
            self.toLog('Load: %s'%fileName)
        except:
            self.toLog(traceback.format_exc())
    def toLog (self, istr):
        self.browser.append(str(istr))

if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    mainw=QtMainWindow()
    mainw.show()
    app.exec_()
