# -*- coding: utf-8 -*-
"""
.. module:: qtDrawQuote
    :synopsis: draw finance data wiht PYQT
.. author: K.K.Chien
"""
import os
import sys
import configparser
import traceback
import datetime
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import financeData
import financeMath

class QtDrawError(Exception):pass
class DrawItemError(Exception):pass

class DrawItem():
    """This class is draw item for QtDraw
    
    This class is draw item for QtDraw

    Attributes:
        line: contain finance data. fianceData.FinanceLine class
        drawType: draw type in QtDraw.
                Draw Type:
                DrawItem.drawtypeDict["line"]: line type
                DrawItem.drawtypeDict["peakvale"]: peak vale type
        pen: drawing pen style. QtGui.QPen class
        brush: drawing brush style. QtGui.QBrush class
    """
    drawtypeDict={"line":1,"peakvale":2,"value":3}
    def __init__ (self, line, name="", drawType="line", 
                  pen=QtGui.QPen(QtGui.QColor(255,255,255),
                                 0, 
                                 QtCore.Qt.SolidLine, 
                                 QtCore.Qt.RoundCap, 
                                 QtCore.Qt.RoundJoin),
                  brush=QtGui.QBrush(QtGui.QColor(255,0,0))):
        """DrawItem initial function

        DrawItem initial function.

        Args:
            line: finance data. must be financeData.FinanceLine class
            name: item name for reconize
            drawType: draw type in QtDraw.
                    Draw Type:
                    DrawItem.drawtypeDict["line"]: line type
                    DrawItem.drawtypeDict["peakvale"]: peak vale type
            pen: drawing pen style. QtGui.QPen class
            brush: drawing brush style. QtGui.QBrush class

        Returns:
            None

        Raise:
            DrawItemError: An error occured intialing instance.
        """
        if not isinstance(line,financeData.FinanceLine):
            raise DrawItemError("line {0:s} is not a financeData.FinanceLine "
                                "class".format(str(line)))
        if isinstance(drawType,str):
            if drawType not in DrawItem.drawtypeDict.keys():
                raise DrawItemError("drawType {0:s} is not a member in "
                                    "drawtypeDict.".format(str(drawType)))
            self.drawtype=DrawItem.drawtypeDict[drawType]
        elif isinstance(drawType,int):
            if drawType not in DrawItem.drawtypeDict.values():
                raise DrawItemError("drawType {0:s} is not a member in "
                                    "drawtypeDict.".format(str(drawType)))
            self.drawtype=drawType
        else:
            raise DrawItemError("drawType {0:s} is not a member in "
                                "drawtypeDict.".format(str(drawType)))
        if not isinstance(pen,QtGui.QPen):
            raise DrawItemError("pen {0:s} is not a QtGui.QPen class"
                                .format(str(pen)))
        if not isinstance(brush,QtGui.QBrush):
            raise DrawItemError("brush {} is not a QtGui.QBrush class"
                                .format(str(brush)))
        self.line=line
        self.pen=pen
        self.brush=brush
        self.name=name
class QtDraw(QtGui.QMainWindow):
    """This class is main Qt windows.
    
    This class is main Qt windows.

    Attributes:
        None
    """
    posW=8
    stickW=6
    dotW=6
    def __init__ (self, parent=None, inputFile=None):
        #self.candleData=financeData.FinanceDataSet()
        #self.drawItems=[]
        self.clearData()
        ###
        self.scaleXOffset=0
        self.scaleYRation=1.0
        self.unit=1.0
        self.lastPos=None
        ###
        self.crossTempLine=[]
        self.drawTempLine=[]
        self.drawTempPoint=[]
        self.drawMoveTempLine=[]
        self.drawItemTemp=[]
        ###
        self.cltKey=False
        self.zoomPos=None
        ###
        super(QtDraw,self).__init__(parent)
        self.ui=uic.loadUi("./res/quoteViewMainWindow.ui", self)  #load ui
        self.ui.graphicsView.setScene(QtGui.QGraphicsScene(self))  #set scene
        (self.ui.graphicsView.viewport()
            .installEventFilter(self.ui))  #install event filter
        ###scene rect
        self.sceneRect=QtCore.QRectF()
        self.sceneRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(0)))
        self.sceneRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(10000)))
        self.viewRect=QtCore.QRectF()
        self.viewRect.setBottomRight(QtCore.QPointF(0,self.value2Scene(0)))
        self.viewRect.setTopLeft(QtCore.QPointF(-100,self.value2Scene(10000)))
        ###
        self.resizeFlag=False   #resize event flag
        ###load toolbar button
        self.actionLoad = QtGui.QAction(QtGui.QIcon('./res/Actions-document-'
                                                    'open-icon.png'),
                                        "Open stick data", 
                                        self,
                                        triggered=self.loadBtnClicked)
        self.ui.toolBar.addAction(self.actionLoad)
        ###clear log toolbar button
        self.actionClearLog = QtGui.QAction(QtGui.QIcon('./res/Actions-edit-'
                                                        'clear-icon.png'),
                                            "Clear log window", 
                                            self, 
                                            triggered=self.clearBtnClicked)
        self.ui.toolBar.addAction(self.actionClearLog)
        ###fit windows toolbar button
        self.actionFitWindow = QtGui.QAction(QtGui.QIcon('./res/Printing-Fit-'
                                                         'To-Width-icon.png'),
                                             "Fit window", 
                                             self,
                                             triggered=self.fitBtnClicked)
        self.ui.toolBar.addAction(self.actionFitWindow)
        ###zoom in toolbar button
        self.actionZoomIn = QtGui.QAction(QtGui.QIcon('./res/Zoom-In-icon.png'),
                                          "Zoom In", self, 
                                          triggered=self.zoomInBtnClicked)
        self.ui.toolBar.addAction(self.actionZoomIn)
        ###zoom out toolbar button
        self.actionZoomOut = QtGui.QAction(QtGui.QIcon('./res/Zoom-Out-'
                                                       'icon.png'),
                                           "Zoom Out", 
                                           self, 
                                           triggered=self.zoomOutBtnClicked)
        self.ui.toolBar.addAction(self.actionZoomOut)
        ###go left toolbar button
        self.actionGoLeft = QtGui.QAction(QtGui.QIcon('./res/Actions-go-'
                                                      'previous-icon.png'),
                                          "Go left one stick bbar (Ctrl+,)", 
                                          self, 
                                          triggered=self.goLeftBtnClicked)
        self.actionGoLeft.setShortcut("Ctrl+,")
        self.ui.toolBar.addAction(self.actionGoLeft)
        ###go right toolbar button
        self.actionGoRight = QtGui.QAction(QtGui.QIcon('./res/Actions-go-'
                                                       'next-icon.png'),
                                           "Go right one stick bbar(Ctrl+.)", 
                                           self, 
                                           triggered=self.goRightBtnClicked)
        self.actionGoRight.setShortcut("Ctrl+.")
        self.ui.toolBar.addAction(self.actionGoRight)
        ###cross line  toolbar button
        self.actionCrossLine = QtGui.QAction(QtGui.QIcon('./res/add-icon.png'),
                                             "Assistant cross line", 
                                             self, 
                                             triggered=self.checkBoxCrossLineChanged)
        self.actionCrossLine.setCheckable(True)
        self.ui.toolBar.addAction(self.actionCrossLine)
        ###drag toolbar button
        self.actionDrag = QtGui.QAction(QtGui.QIcon('./res/Drag-icon.png'),
                                        "Drag view", 
                                        self, 
                                        triggered=self.checkBoxDragChanged)
        self.actionDrag.setCheckable(True)
        self.ui.toolBar.addAction(self.actionDrag)
        ###draw line toolbar button
        self.actionDrawLine = QtGui.QAction(QtGui.QIcon('./res/Line-icon.png'),
                                            "Draw line", 
                                            self, 
                                            triggered=self.checkBoxDrawLineChanged)
        self.actionDrawLine.setCheckable(True)
        self.ui.toolBar.addAction(self.actionDrawLine)
        ###Find Significant point toolbar button
        self.actionSignificantPnt = QtGui.QAction(QtGui.QIcon(),
                                                  "Sig", 
                                                  self, 
                                                  triggered=self.findSigPoingBtnClicked)
        self.ui.toolBar.addAction(self.actionSignificantPnt)
        ###Scan Band Arg toolbar button
        self.actionScanBand = QtGui.QAction(QtGui.QIcon(),
                                            "Scan Band", 
                                            self, 
                                            triggered=self.scanBandBtnClicked)
        self.ui.toolBar.addAction(self.actionScanBand)
        ###Scan ratio toolbar button
        self.actionScanRatio = QtGui.QAction(QtGui.QIcon(),
                                            "Scan Ratio", 
                                            self, 
                                            triggered=self.scanRatioBtnClicked)
        self.ui.toolBar.addAction(self.actionScanRatio)
        ###Scan MACD toolbar button
        self.actionScanMacd = QtGui.QAction(QtGui.QIcon(),
                                            "Scan MACD", 
                                            self, 
                                            triggered=self.scanMacdBtnClicked)
        self.ui.toolBar.addAction(self.actionScanMacd)
        ###setup status bar
        self.labelCurrent=QtGui.QLabel(self)
        self.labelCurrent.setMinimumWidth(150)
        self.ui.statusbar.addWidget(self.labelCurrent)
        self.labelValue=QtGui.QLabel(self)
        self.ui.statusbar.addWidget(self.labelValue)
        #
        self.beginDataFile=inputFile
    def keyPressEvent(self, event):
        if event.key()==0x1000021:
            self.cltKey=True
    def keyReleaseEvent (self, event):
        if event.key()==0x1000021:
            self.cltKey=False
            self.zoomPos=None
    def eventFilter(self, source, event):
        """graphic view event filter function

        graphic view event filter function

        Args:
            source: source object
            event: event

        Returns:
            None

        Raises:
            None
        """
        if (event.type() == QtCore.QEvent.MouseButtonPress):
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            
            if event.button() == QtCore.Qt.LeftButton:
                if self.actionCrossLine.isChecked()==True:
                    ipos=self.scene2pos(pos.x())
                    if ipos<len(self.candleData):
                        self.toLog("{0:s} Start:{1:.2f}  High:{2:.2f} Low:{3:.2f} "
                                   "End:{4:.2f} Vol:{5:.2f}"
                                   .format(datetime.datetime
                                           .strftime(
                                               self.candleData.openValue[ipos].time
                                               , '%Y%m%d%H%M%S'),
                                           self.candleData.openValue[ipos].value,
                                           self.candleData.highValue[ipos].value,
                                           self.candleData.lowValue[ipos].value,
                                           self.candleData.closeValue[ipos].value,
                                           self.candleData.volumeValue[ipos].value)
                                   )
                    iverpos=ipos-len(self.candleData)
                    if iverpos<0:
                        for item in self.drawItems:
                            if iverpos+len(item.line)<0:
                                continue
                            self.toLog("{0:s} : {1:f}".format(item.name, item.line[iverpos].value))
                                
                if self.actionDrawLine.isChecked()==True:
                    self.drawTempPoint.append(pos)
                    if len(self.drawMoveTempLine)!=0:
                        for icount in range(len(self.drawMoveTempLine)):
                            self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                        self.drawMoveTempLine=[]
                    if len(self.drawTempPoint)>=2:
                        self.drawTempLine.append(self.ui.graphicsView.scene().addLine(self.drawTempPoint[0].x(),
                                                                                      self.drawTempPoint[0].y(),
                                                                                      self.drawTempPoint[1].x(),
                                                                                      self.drawTempPoint[1].y()))
                        del self.drawTempPoint
                        self.drawTempPoint=[]
            elif event.button() == QtCore.Qt.RightButton:
                if self.actionCrossLine.isChecked()==False:
                    self.actionCrossLine.setChecked(True)
                    self.checkBoxDragChanged()
                    self.drawCrossLineAndText(pos)
                else:
                    self.actionCrossLine.setChecked(False)
                    self.checkBoxDragChanged()
                    self.clearCrossLine()
        elif (event.type() == QtCore.QEvent.Resize):
            self.resizeFlag=True
        elif (event.type() == QtCore.QEvent.Paint):
            if self.resizeFlag:
                self.resizeFlag=False
                self.getRealViewRect()
                #self.setView(self.getViewRightPos())
                if self.beginDataFile:
                    try:
                        if not os.path.exists(self.beginDataFile):
                            self.toLog(self.beginDataFile+" doesn't exist")
                        else:
                            if self.beginDataFile.endswith('.ini'):
                                self.loadFromIni(self.beginDataFile)
                            elif self.beginDataFile.endswith('.csv'):
                                self.loadFromCsv(self.beginDataFile)
                            self.drawCandle()
                            self.drawFinanceItems()
                            self.setScene()
                            self.setView(len(self.candleData)+2)
                            self.fitBtnClicked()
                    except:
                        self.toLog(traceback.format_exc())
                    self.beginDataFile=None
        elif (event.type() == QtCore.QEvent.MouseMove):
            pos = QtCore.QPointF(self.ui.graphicsView.mapToScene(event.pos()))
            self.labelCurrent.setText("Pos:{0:d} Value:{1:.2f}"
                                      .format(self.scene2pos(pos.x()), 
                                              self.scene2Value(pos.y())
                                              *self.unit))
            if self.actionCrossLine.isChecked()==True:
                self.drawCrossLineAndText(pos)
            if self.candleData:
                if self.cltKey==True:
                    if self.zoomPos==None:
                        self.zoomPos=event.pos()
                    else:
                        posoffy=event.pos().y()-self.zoomPos.y()
                        self.zoomPos=event.pos()
                        if posoffy<0:
                            self.zoomInBtnClicked()
                        elif posoffy>0:
                            self.zoomOutBtnClicked()
                        self.setView(self.getViewRightPos())
            if self.actionDrawLine.isChecked()==True:
                if len(self.drawMoveTempLine)!=0:
                    for icount in range(len(self.drawMoveTempLine)):
                        self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                    self.drawMoveTempLine=[]
                if len(self.drawTempPoint)==1:
                    self.drawMoveTempLine.append(self.ui.graphicsView.scene().addLine(self.drawTempPoint[0].x(),
                                                                                      self.drawTempPoint[0].y(),
                                                                                      pos.x(),
                                                                                      pos.y()))
        return QtGui.QWidget.eventFilter(self, source, event)
    def getValueBoundary (self, istart, istop=-1):
        """get (max,min) value in boundary

        get (max,min) value in boundary

        Args:
            istart: start index in data
            istop: stop index in data

        Returns:
            return tuple (maxvalue, minvalue)

        Raise:
            None
        """
        maxvalue=None
        minvalue=None
        start=int(istart)
        stop=int(istop)
        if len(self.candleData)!=0:
            for linetemp in (self.candleData.openValue[start:stop],
                self.candleData.highValue[start:stop],
                self.candleData.lowValue[start:stop],
                self.candleData.closeValue[start:stop]):
                if len(linetemp)==0:
                    continue
                vtemp=max(linetemp).value
                if maxvalue==None or maxvalue<vtemp:
                    maxvalue=vtemp
                vtemp=min(linetemp).value
                if minvalue==None or minvalue>vtemp:
                    minvalue=vtemp
        itemcount=1
        for ditem in self.drawItems:
            if ditem.drawtype==DrawItem.drawtypeDict["peakvale"]:
                itemcount+=1
                continue
            elif ditem.drawtype==DrawItem.drawtypeDict["value"]:
                continue
            else:
                item=ditem.line
                lendif=len(self.candleData)-len(item)
                starttemp=start-lendif
                if starttemp<0:
                    starttemp=0
                if stop<0:
                    stoptemp=stop
                else:
                    stoptemp=stop-lendif
                    if stoptemp<0:
                        continue
                linetemp=item[starttemp:stoptemp]
                #linetemp=item[start:stop]
                if len(linetemp)==0:
                    continue
                vtemp=max(linetemp).value
                if maxvalue==None or maxvalue<vtemp:
                    maxvalue=vtemp
                vtemp=min(linetemp).value
                if minvalue==None or minvalue>vtemp:
                    minvalue=vtemp
        #wtemp=QtDraw.dotW
        #self.scaleYRation=10
        #htemp=abs(self.value2Scene(wtemp*self.scaleYRation))*itemcount*self.unit
        htemp=abs(maxvalue-minvalue)*0.01*itemcount
        return (maxvalue+htemp, minvalue-htemp)
            
    def toLog (self, istr):
        self.ui.textBrowser.append(str(istr))
    def x2Scene (self, ix):
        return ix
    def pos2X (self, ipos):
        if ipos>=0:
            return ipos*QtDraw.posW#+QtDraw.posW/2
        else:
            return (len(self.candleData)+ipos)*QtDraw.posW
    def pos2Scene (self, ipos):
        return self.x2Scene(self.pos2X(ipos))
    def scene2pos (self, ivalue):
        ftemp=ivalue/QtDraw.posW
        result=round(ftemp)
        if result>len(self.candleData):
            result=len(self.candleData)
        return result
    def y2Scene (self, iy):
        return (0-iy)
    def value2Y (self, ivalue):
        return (ivalue/self.unit)
    def value2Scene (self, ivalue):
        return self.y2Scene(self.value2Y(ivalue))
    def scene2Value (self, ivalue):
        return (0.0-ivalue)
    def getRealViewRect (self):
        self.realViewRect=self.ui.graphicsView.rect()
    def clearScene (self):
        self.ui.graphicsView.scene().clear()
        self.scaleXOffset=0
    def clearData (self):
        if "candleData" in self.__dict__.keys():
            del self.candleData
        self.candleData=financeData.FinanceDataSet()
        if "drawItems" in self.__dict__.keys():
            del self.drawItems
        self.drawItems=[]
    def setScene (self):
        viewVisibleBar=self.realViewRect.width()/QtDraw.posW
        datawidth=(len(self.candleData)+1)*QtDraw.posW
        #set scene
        self.sceneRect.setRight(datawidth)
        ltemp=datawidth-self.realViewRect.width()
        if ltemp<0:
            self.sceneRect.setLeft(ltemp)
        else:
            self.sceneRect.setLeft(0)
        maxmintemp=self.getValueBoundary(0)
        self.sceneRect.setTop(self.value2Scene(maxmintemp[0]))
        self.sceneRect.setBottom(self.value2Scene(maxmintemp[1]))
        self.ui.graphicsView.setSceneRect(self.sceneRect)
    def setView (self, rpos=-1):
        try:
            #set view
            posr=rpos
            if posr==-1:
                posr=len(self.candleData)
            #wtemp1=self.ui.graphicsView.mapToScene(QtCore.QPoint(self.realViewRect.width(),0)).x()
            #wtemp2=self.ui.graphicsView.mapToScene(QtCore.QPoint(0,0)).x()
            #wtemp=wtemp1-wtemp2
            #self.toLog("w {0:f} {1:f} {2:f} {3:f} {4:f}".format(posr, self.realViewRect.width(), wtemp, wtemp1, wtemp2))
            realBarNum=self.realViewRect.width()/QtDraw.posW
            #realBarNum=wtemp/QtDraw.posW
            if self.scaleXOffset!=0:
                realBarNum+=self.scaleXOffset
            posl=posr-realBarNum
            if posl<0:
                posl=0
            if posl>posr:
                posl=posr
            btemp=self.getValueBoundary(posl, posr)
            if btemp==(None,None):
                maxtemp=self.value2Scene(10000)
                mintemp=self.value2Scene(1)
            else:
                maxtemp=self.value2Scene(btemp[0])
                mintemp=self.value2Scene(btemp[1])
            self.viewRect.setTop(maxtemp)
            self.viewRect.setBottom(mintemp)
            self.scaleYRation=(mintemp-maxtemp)/self.realViewRect.height()
            rtemp=posr*QtDraw.posW
            #lptemp=posr*QtDraw.posW-(realBarNum+self.scaleXOffset)*QtDraw.posW
            lptemp=rtemp-int(realBarNum)*QtDraw.posW
            if rtemp<=lptemp+10:
                return
            self.viewRect.setRight(rtemp)
            self.viewRect.setLeft(lptemp)
            #self.toLog("ltop{0:.2f} bottom{1:.2f} left{2:.2f} right{3:.2f}".format(
            #    self.viewRect.top(), self.viewRect.bottom(), self.viewRect.left(), self.viewRect.right()))
            self.ui.graphicsView.fitInView(self.viewRect)
        except Exception as e:
            self.toLog(traceback.format_exc())
    def getViewRightPos (self):
        rbtemp=self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport()
                                               .rect().bottomRight())
        return self.scene2pos(rbtemp.x())
    def drawCrossLineAndText (self, pos):
        if len(self.candleData)<=0:
            return
        ipos=self.scene2pos(pos.x())
        if ipos!=self.lastPos:
            self.lastPos=ipos
            if ipos<len(self.candleData):
                self.labelValue.setText("{0:s} Start:{1:.2f}  High:{2:.2f} "
                                        "Low:{3:.2f} End:{4:.2f} Vol:{5:.2f}"
                                        .format(datetime.datetime
                                                .strftime(self.candleData
                                                          .openValue[ipos].time, 
                                                          '%Y%m%d%H%M%S'),
                                                self.candleData.openValue[ipos]
                                                .value,
                                                self.candleData.highValue[ipos]
                                                .value,
                                                self.candleData.lowValue[ipos]
                                                .value,
                                                self.candleData.closeValue[ipos]
                                                .value,
                                                self.candleData.volumeValue[ipos]
                                                .value))
            else:
                self.labelValue.setText("")
        self.clearCrossLine()
        self.crossTempLine.append(self.ui.graphicsView.scene()
                                  .addLine(self.pos2Scene(ipos),
                                           self.sceneRect.bottom(),
                                           self.pos2Scene(ipos),
                                           self.sceneRect.top()))

        self.crossTempLine.append(self.ui.graphicsView.scene()
                                  .addLine(self.sceneRect.right(),
                                           pos.y(),
                                           self.sceneRect.left(),
                                           pos.y()))
    def clearCrossLine (self):
        if len(self.crossTempLine)!=0:
            for icount in range(len(self.crossTempLine)):
                self.ui.graphicsView.scene().removeItem(self.
                                                        crossTempLine[icount])
            self.crossTempLine=[]
    def loadBtnClicked (self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", 
                                                     '.', "ini (*.ini);;csv (*.csv)")
        if os.path.exists(fileName)==False:
            self.toLog(fileName+" doesn't exist")
            return
        try:
            if fileName.endswith('.ini'):
                self.clearData()
                self.clearScene()
                self.loadFromIni(fileName)
            elif fileName.endswith('.csv'):
                self.clearData()
                self.clearScene()
                self.loadFromCsv(fileName)
            else:
                return
            self.drawCandle()
            self.drawFinanceItems()
            self.setScene()
            self.setView(len(self.candleData)+2)
            self.fitBtnClicked()
        except Exception as e:
            self.toLog(traceback.format_exc())
    def str2Color (self, istr):
        """convert color string to QtGui.QColor

        convert color string to QtGui.QColor.
        color string must be R,G,B. for example, 255,0,0.

        Args:
            istr: color string must be R,G,B. for example, 255,0,0.

        Returns:
            None

        Raise:
            None
        """
        colorValue=istr.split(',')
        return QtGui.QColor(int(colorValue[0]),int(colorValue[1]), 
                            int(colorValue[2]))
    def loadFromCsv(self, fileName):
        if not isinstance(fileName,str):
            raise QtDrawError("{0:s} is not a string.".format(str(fileName)))
        self.candleData.getDataFromFile(fileName)
        self.unit=0.01
        self.toLog(str(self.candleData))
    def loadFromIni (self, fileName):
        """load data and config from ini file

        load data and config from ini file

        Args:
            fileName: ini file name path

        Returns:
            None

        Raise:
            None
        """
        if not isinstance(fileName,str):
            raise QtDrawError("{0:s} is not a string.".format(str(fileName)))
        config=configparser.ConfigParser()
        config.read(fileName)
        ###
        srcset=financeData.FinanceDataSet()
        srcset.getDataFromFile(config["common"]["file"])
        try:
            periodtemp=int(config["common"]["period"])
        except KeyError:
            periodtemp=5
        try:
            unittemp=float(config["common"]["unitxx"])
        except KeyError:
            unittemp=0.01
        if unittemp>1:
            unittemp=1
        self.unit=unittemp
        settemp=srcset[(0-periodtemp):]
        self.candleData=settemp
        self.toLog(str(self.candleData))
        ###
        for sectionname in config.sections():
            try:
                sindex=sectionname.index("indicator")
            except ValueError:
                continue
            if sindex!=0:
                continue
            indicator=config[sectionname]["indicator"]
            ###
            try:
                pen1color=self.str2Color(config[sectionname]["pencolor"])
            except:
                pen1color=self.str2Color("255,255,255")
            try:
                pen1width=int(config[sectionname]["penwidth"])
            except:
                pen1width=0
            try:
                pen2color=self.str2Color(config[sectionname]["pencolor2"])
            except:
                pen2color=self.str2Color("255,255,255")
            try:
                pen2width=int(config[sectionname]["penwidth2"])
            except:
                pen2width=0
            try:
                brush1color=self.str2Color(config[sectionname]["brushcolor"])
            except:
                brush1color=self.str2Color("255,255,255")
            try:
                period1=int(config[sectionname]["period"])
            except:
                period1=5
            try:
                period2=int(config[sectionname]["period2"])
            except:
                period2=5
            try:
                multiplier1=float(config[sectionname]["multiplier"])
            except:
                multiplier1=financeMath.FinanceMathFunction.goldRatio*3
            ###
            if (indicator=="ma" or indicator=="wma" or indicator=="ema" or 
                indicator=="hma"):
                fobj=financeMath.FinanceMathFunction()
                linetemp=financeData.FinanceLine()
                for icount in range(len(self.candleData.closeValue)):
                    try:
                        if indicator=="ma":
                            fobj.calMA(self.candleData.closeValue, linetemp, 
                                       icount, period1)
                        elif indicator=="wma":
                            fobj.calWMA(self.candleData.closeValue, linetemp, 
                                        icount, period1)
                        elif indicator=="ema":
                            fobj.calEMA(self.candleData.closeValue, linetemp, 
                                        icount, period1)
                        elif indicator=="hma":
                            fobj.calHMA(self.candleData.closeValue, linetemp, 
                                        icount, period1)
                        else:
                            continue
                    except financeMath.FinanceMathFunctionPosBelowPeriod:
                        continue
                self.drawItems.append(DrawItem(linetemp,
                                               name=sectionname[10:-1],
                                               pen=QtGui.QPen(pen1color,
                                                              pen1width,
                                                              QtCore.Qt.SolidLine,
                                                              QtCore.Qt.RoundCap,
                                                              QtCore.Qt.RoundJoin)
                                               )
                                      )
            elif indicator=="kkmacd":
                fobj=financeMath.FinanceMathFunction()
                hmaline=financeData.FinanceLine()
                emaline=financeData.FinanceLine()
                diffline=financeData.FinanceLine()
                macdline=financeData.FinanceLine()
                for icount in range(len(self.candleData.closeValue)):
                    try:
                        fobj.calKKMACD(self.candleData.closeValue, hmaline, 
                                       emaline, diffline, icount, period1, 
                                       period2)
                    except financeMath.FinanceMathFunctionPosBelowPeriod:
                        continue
                for icount in range(len(diffline)):
                    try:
                        fobj.calHMA(diffline, macdline, icount, int(period2*financeMath.FinanceMathFunction.cjGRation))
                    except financeMath.FinanceMathFunctionPosBelowPeriod:
                        continue
                macdline.peakLine=diffline.findPeak()
                macdline.valeLine=diffline.findVale()
                self.drawItems.append(DrawItem(macdline,
                                               name=sectionname[10:-1],
                                               drawType="peakvale",
                                               brush=QtGui.QBrush(brush1color)
                                               )
                                      )
            elif indicator=="emaband" or indicator=="hmaband":
                fobj=financeMath.FinanceMathFunction()
                midtemp=financeData.FinanceLine()
                hightemp=financeData.FinanceLine()
                lowtemp=financeData.FinanceLine()
                for icount in range(len(self.candleData.closeValue)):
                    try:
                        if indicator=="emaband":
                            fobj.calEMABand(self.candleData.closeValue, 
                                            self.candleData.highValue, 
                                            self.candleData.lowValue,
                                            midtemp, hightemp, lowtemp, 
                                            icount, period1, multiplier1)
                        elif indicator=="hmaband":
                            fobj.calHMABand(self.candleData.closeValue, 
                                            self.candleData.highValue, 
                                            self.candleData.lowValue,
                                            midtemp, hightemp, lowtemp, 
                                            icount, period1, multiplier1)
                    except financeMath.FinanceMathFunctionPosBelowPeriod:
                        continue
                self.drawItems.append(DrawItem(hightemp,
                                               name=sectionname[10:-1]+"_h",
                                               pen=QtGui.QPen(pen2color,
                                                              pen2width,
                                                              QtCore.Qt.SolidLine,
                                                              QtCore.Qt.RoundCap,
                                                              QtCore.Qt.RoundJoin)
                                               )
                                      )
                self.drawItems.append(DrawItem(midtemp,
                                               name=sectionname[10:-1]+"_m",
                                               pen=QtGui.QPen(pen1color,
                                                              pen1width,
                                                              QtCore.Qt.SolidLine,
                                                              QtCore.Qt.RoundCap,
                                                              QtCore.Qt.RoundJoin)
                                               )
                                      )
                self.drawItems.append(DrawItem(lowtemp,
                                               name=sectionname[10:-1]+"_l",
                                               pen=QtGui.QPen(pen2color,
                                                              pen2width,
                                                              QtCore.Qt.SolidLine,
                                                              QtCore.Qt.RoundCap,
                                                              QtCore.Qt.RoundJoin)
                                               )
                                      )
            elif indicator=="atr":
                fobj=financeMath.FinanceMathFunction()
                atrtemp=financeData.FinanceLine()
                for icount in range(len(self.candleData.closeValue)):
                    try:
                        fobj.calATR(self.candleData.closeValue,self.candleData.highValue,self.candleData.lowValue,atrtemp,icount,period1, multiplier1)
                    except financeMath.FinanceMathFunctionPosBelowPeriod:
                        continue
                self.drawItems.append(DrawItem(atrtemp,
                                               name=sectionname[10:-1],
                                               drawType="value"
                                               )
                                      )
            self.setWindowTitle(os.path.basename(fileName))
    def getCurrentValueBoundary (self):
        posr=self.getViewRightPos()
        realBarNum=self.realViewRect.width()/QtDraw.posW
        posl=posr-realBarNum
        if posl<0:
            posl=0
        if posl>posr:
            posl=posr
        return self.getValueBoundary(posl, posr)
    def drawFinanceItems (self):
        fulllen=len(self.candleData)
        wtemp=QtDraw.dotW
        btemp=self.getCurrentValueBoundary()
        #self.toLog('b %f %f' %(btemp[0], btemp[1]))
        boffset=(btemp[0]-btemp[1])
        if boffset>10:
            self.scaleYRation=boffset/300
        else:
            self.scaleYRation=boffset/400
        self.toLog('b:%f %f' %(btemp[0],btemp[1]))
        htemp=abs(self.value2Scene(wtemp*self.scaleYRation))
        otemp=abs(self.value2Scene(wtemp/2*self.scaleYRation))
        for item in self.drawItems:
            if item.drawtype==DrawItem.drawtypeDict["line"]:
                for icount in range(len(item.line)-1):
                    #self.toLog("{0:d} {1:f}".format(icount,item.line[-1-icount].value))
                    self.drawItemTemp.append(self.ui.graphicsView.scene()
                                             .addLine(self.pos2Scene(fulllen-1-icount),
                                             self.value2Scene(item.line[-1-icount].value),
                                             self.pos2Scene(fulllen-2-icount),
                                             self.value2Scene(item.line[-2-icount].value),
                                             pen=item.pen))
            elif item.drawtype==DrawItem.drawtypeDict["peakvale"]:
                if "peakLine" not in item.line.__dict__.keys():
                    continue
                if "valeLine" not in item.line.__dict__.keys():
                    continue
                #if "drawItemTemp" in self.__dict__.keys():
                    #for item in self.drawItemTemp:
                    #    self.ui.graphicsView.scene().removeItem(item)
                for revcount in range(-1, 1-len(item.line.peakLine), -1):
                    ihigh=self.candleData[revcount].highValue[0].value
                    ilow=self.candleData[revcount].lowValue[0].value
                    if (item.line.peakLine[revcount].value==financeData
                        .FinanceLine.peakValeDict["slope"]):
                        continue
                    if (item.line.peakLine[revcount].value==financeData
                        .FinanceLine.peakValeDict["peak"]):
                        (self.drawItemTemp
                            .append(self.ui.graphicsView.scene()
                                    .addEllipse(self.pos2Scene(revcount)-wtemp/2,
                                                self.value2Scene(ihigh)-htemp-otemp,
                                                wtemp,
                                                htemp,
                                                brush=QtGui.QBrush(QtGui
                                                                   .QColor(255,0,0)))))
                for revcount in range(-1, 1-len(item.line.valeLine), -1):
                    ihigh=self.candleData[revcount].highValue[0].value
                    ilow=self.candleData[revcount].lowValue[0].value
                    if (item.line.valeLine[revcount].value==financeData
                        .FinanceLine.peakValeDict["slope"]):
                        continue
                    if (item.line.valeLine[revcount].value==financeData
                        .FinanceLine.peakValeDict["vale"]):
                        (self.drawItemTemp
                            .append(self.ui.graphicsView.scene()
                                    .addEllipse(self.pos2Scene(revcount)-wtemp/2,
                                                self.value2Scene(ilow)+otemp,
                                                wtemp,
                                                htemp,
                                                brush=QtGui
                                                .QBrush(QtGui.QColor(255,0,0)))))
    def drawCandle (self):
        try:
            if len(self.candleData)==0:
                return
            for icount in range(len(self.candleData)):
                istart=self.candleData[icount].openValue[0].value
                ihigh=self.candleData[icount].highValue[0].value
                ilow=self.candleData[icount].lowValue[0].value
                iend=self.candleData[icount].closeValue[0].value
                self.ui.graphicsView.scene().addLine(self.pos2Scene(icount),
                                                     self.value2Scene(ihigh),
                                                     self.pos2Scene(icount),
                                                     self.value2Scene(ilow))
                if istart<=iend:
                    brushtemp=QtGui.QBrush(QtGui.QColor(255,0,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(icount)
                                                         -QtDraw.stickW/2,
                                                         self.value2Scene(iend),
                                                         QtDraw.stickW,
                                                         self.value2Scene(istart)
                                                         -self.value2Scene(iend),
                                                         brush=brushtemp)
                else:
                    brushtemp=QtGui.QBrush(QtGui.QColor(0,255,0))
                    self.ui.graphicsView.scene().addRect(self.pos2Scene(icount)
                                                         -QtDraw.stickW/2,
                                                         self.value2Scene(istart),
                                                         QtDraw.stickW,
                                                         self.value2Scene(iend)
                                                         -self.value2Scene(istart),
                                                         brush=brushtemp)
        except Exception as e:
            self.toLog(traceback.format_exc())
    def clearBtnClicked (self):
        ###open file dialog
        #fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", './', "ini (*.ini)")
        #self.ui.textBrowser.append(fileName)
        #self.ui.graphicsView.scene().addRect(0, 0, 100, 100, brush=QtGui.QBrush(QtGui.QColor(255,0,0)))
        #self.ui.graphicsView.scene().setSceneRect(QtCore.QRectF(-3000, -3000, 5000, 5000))
        #self.ui.graphicsView.scene().addRect(150, -500, 100, -300, brush=QtGui.QBrush(QtGui.QColor(255,0,0)))
        #self.ui.graphicsView.scene().addRect(20, 20, 100, 50)
        #recttemp.setX(100)
        #recttemp.setWidth(100)
        #recttemp.setHeight(100)
        #self.ui.graphicsView.fitInView(recttemp)
        #self.ui.graphicsView.centerOn(0,0)
        #self.ui.graphicsView.scale(0.5,0.5)
        #recttemp=self.ui.graphicsView.sceneRect()
        #self.toLog("x:{0:f} y:{1:f} w:{2:f} h:{3:f}".format(recttemp.x(),
        #                                                    recttemp.y(),
        #                                                    recttemp.width(),
        #                                                    recttemp.height()))
        #recttemp=self.ui.graphicsView.rect()
        #self.toLog("x:{0:f} y:{1:f} w:{2:f} h:{3:f}".format(recttemp.x(),
        #                                                    recttemp.y(),
        #                                                    recttemp.width(),
        #                                                    recttemp.height()))
        #trans=self.ui.graphicsView.transform()
        #self.toLog("m11:{0:f}   m12:{1:f}   m13:{2:f} \nm21:{3:f}   m22:{4:f}   m23:{5:f} \nm31:{6:f}   m32:{7:f}   m33:{8:f}".format(
        #        trans.m11(),trans.m12(),trans.m13(),trans.m21(),trans.m22(),trans.m23(),trans.m31(),trans.m32(),trans.m33()))
        self.ui.textBrowser.clear()
    def fitBtnClicked (self):
        #self.ui.graphicsView.scale(0.9,1)
        self.setView(self.getViewRightPos())
    def zoomInBtnClicked (self):
        self.scaleXOffset=self.scaleXOffset-2
        self.setView(self.getViewRightPos())
    def zoomOutBtnClicked (self):
        self.scaleXOffset=self.scaleXOffset+2
        self.setView(self.getViewRightPos())
    def goLeftBtnClicked (self):
        self.setView(self.getViewRightPos()-1)
    def goRightBtnClicked (self):
        self.setView(self.getViewRightPos()+1)
    def checkBoxCrossLineChanged (self):
        if self.actionCrossLine.isChecked()==False:
            if len(self.crossTempLine)!=0:
                for icount in range(len(self.crossTempLine)):
                    (self.ui.graphicsView.scene()
                        .removeItem(self.crossTempLine[icount]))
                self.crossTempLine=[]
    def checkBoxDragChanged (self):
        if self.actionDrag.isChecked()==True:
            self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        else:
            self.ui.graphicsView.setDragMode(QtGui.QGraphicsView.NoDrag)
    def checkBoxDrawLineChanged (self):
        try:
            if self.actionDrawLine.isChecked()==False:
                self.drawTempPoint=[]
                if len(self.drawTempLine)!=0:
                    for icount in range(len(self.drawTempLine)):
                        self.ui.graphicsView.scene().removeItem(self.drawTempLine[icount])
                    self.drawTempLine=[]
                if len(self.drawMoveTempLine)!=0:
                    for icount in range(len(self.drawMoveTempLine)):
                        self.ui.graphicsView.scene().removeItem(self.drawMoveTempLine[icount])
                    self.drawMoveTempLine=[]
        except Exception as e:
            self.toLog(traceback.format_exc())
    def findSigPoingBtnClicked (self):
        try:
            inputPeriod, ok = QtGui.QInputDialog.getInt(self, 'Input period', 'Enter HMA period (must be integer):', value=16)
            if not ok:
                return
            mobj=financeMath.FinanceMathFunction()
            hmalineHi=financeData.FinanceLine()
            hmalineLo=financeData.FinanceLine()
            hmaline=financeData.FinanceLine()
            for icount in range(len(self.candleData.closeValue)):
                try:
                    mobj.calHMA(self.candleData.highValue, hmalineHi, icount, inputPeriod)
                except financeMath.FinanceMathFunctionPosBelowPeriod:
                    pass
                try:
                    mobj.calHMA(self.candleData.lowValue, hmalineLo, icount, inputPeriod)
                except financeMath.FinanceMathFunctionPosBelowPeriod:
                    pass
                try:
                    mobj.calHMA(self.candleData.closeValue, hmaline, icount, inputPeriod)
                except financeMath.FinanceMathFunctionPosBelowPeriod:
                    pass
            peakL, valeL=mobj.getHighLowSignificantPoint(hmalineHi, hmalineLo, self.candleData.highValue, self.candleData.lowValue, int(inputPeriod*financeMath.FinanceMathFunction.cjGRation))
            hmaline.peakLine=peakL
            hmaline.valeLine=valeL
            for item in self.drawItemTemp:
                self.ui.graphicsView.scene().removeItem(item)
            self.drawItemTemp=[]
            self.drawItems=[]
            self.drawItems.append(DrawItem(hmalineHi,
                                          name="HMA%d_hi" %inputPeriod,
                                          drawType="line",
                                          pen=QtGui.QPen(QtGui.QColor(255,0,0),
                                                           0, 
                                                           QtCore.Qt.SolidLine, 
                                                           QtCore.Qt.RoundCap, 
                                                           QtCore.Qt.RoundJoin)
                                           )
                                  )
            self.drawItems.append(DrawItem(hmalineLo,
                                          name="HMA%d_lo" %inputPeriod,
                                          drawType="line",
                                          pen=QtGui.QPen(QtGui.QColor(100,100,0),
                                                           0, 
                                                           QtCore.Qt.SolidLine, 
                                                           QtCore.Qt.RoundCap, 
                                                           QtCore.Qt.RoundJoin)
                                           )
                                  )
            self.drawItems.append(DrawItem(hmaline,
                                          name="HMA%d_PV" %inputPeriod,
                                          drawType="peakvale",
                                          brush=QtGui.QBrush(QtGui.QColor(255,0,0))
                                          )
                                  )
            self.drawFinanceItems()
        except:
            self.toLog(traceback.format_exc())
    def scanBandBtnClicked (self):
        try:
            if QtGui.QMessageBox.warning(None, "Scan band arg.","This will take a lost of time. Are you sure?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel) != QtGui.QMessageBox.Ok:
                return
            #hmaPeriod, ok = QtGui.QInputDialog.getInt(self, 'Input period', 'Enter HMA period (must be integer):', value=16)
            #if not ok:
            #    return
            self.toLog('Band Scan')
            goldRatio=financeMath.FinanceMathFunction.goldRatio
            cgRation=financeMath.FinanceMathFunction.cjGRation
            finalValue=[]
            lastperiod=None
            for icount in range(5, 100):
                periodtemp=int(icount*goldRatio)
                if lastperiod==None:
                    lasperiod=periodtemp
                elif lasperiod==periodtemp:
                    lasperiod=periodtemp
                    continue
                hmaPeriod=int(cgRation*periodtemp)
                for jcount in range(2, 41):
                    multemp=jcount*cgRation
                    mobj=financeMath.FinanceMathFunction()
                    hmalineHi=financeData.FinanceLine()
                    hmalineLo=financeData.FinanceLine()
                    for kcount in range(len(self.candleData.closeValue)):
                        try:
                            mobj.calHMA(self.candleData.highValue, hmalineHi, kcount, hmaPeriod)
                        except financeMath.FinanceMathFunctionPosBelowPeriod:
                            pass
                        try:
                            mobj.calHMA(self.candleData.lowValue, hmalineLo, kcount, hmaPeriod)
                        except financeMath.FinanceMathFunctionPosBelowPeriod:
                            pass
                    pLine, vLine=mobj.getHighLowSignificantPoint(hmalineHi, hmalineLo, self.candleData.highValue, self.candleData.lowValue, int(hmaPeriod*financeMath.FinanceMathFunction.cjGRation))
            
                    wtemp=mobj.calHMABandWeight(self.candleData.closeValue, self.candleData.highValue, 
                                  self.candleData.lowValue, pLine, vLine, periodtemp, multemp)
                    #self.toLog('Period:%d Mul:%f WValue:%f' % (periodtemp, multemp, wtemp))
                    #if len(finalValue)==0 or wtemp<finalValue[-1][0]:
                    #    finalValue.append([wtemp, periodtemp, multemp])
                    finalValue.append([wtemp, periodtemp, multemp])
            finalValue.sort(key=lambda t: t[0])
            for item in finalValue:
                self.toLog('Final Period:%d Mul:%f WValue:%f' % (item[1], item[2], item[0]))
        except Exception as e:
            self.toLog(traceback.format_exc())
    def scanRatioBtnClicked (self):
        try:
            malist=[]
            malist.append('hma')
            malist.append('ema')
            matemp, ok=QtGui.QInputDialog.getItem(self, 'MA Type', 'Select a ma type:', ['hma','ema'], editable=False)
            if not ok:
                return
            self.toLog('Ration scan. %s' %matemp)
            goldRatio=financeMath.FinanceMathFunction.goldRatio
            cgRation=financeMath.FinanceMathFunction.cjGRation
            result=[]
            for icount in range(10, 120):
                periodtemp=int(icount*goldRatio)
                for jcount in range(1, 21):
                    multemp=jcount*cgRation
                    mobj=financeMath.FinanceMathFunction()
                    rtemp, otemp=mobj.calRatio(self.candleData.closeValue,self.candleData.highValue,self.candleData.lowValue, periodtemp,multemp,matype=matemp)
                    result.append((periodtemp, multemp, rtemp, otemp))
            result.sort(key=lambda t: t[2])
            for item in result:
                self.toLog('%f %f %f' %(item[0], item[1], item[2]))

        except Exception:
            self.toLog(traceback.format_exc())
    def scanMacdBtnClicked (self):
        try:
            if QtGui.QMessageBox.warning(None, "Scan MACD arg.","This will take a lost of time. Are you sure?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel) != QtGui.QMessageBox.Ok:
                return
            self.toLog('Scanning...')
        except Exception as e:
            self.toLog(traceback.format_exc())
if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    window=QtDraw(inputFile="./ini/test.ini")
    window.show()
    app.exec_()

