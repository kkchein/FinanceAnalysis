# -*- coding: utf-8 -*-
"""
.. module:: financeData
    :synopsis: Data structure for finance data
.. author: K.K.Chien
"""
import datetime
import copy
import csv
import time
import os
import sys
import unittest

class FinanceDataError(Exception): pass
class FinanceDataOutOfIndex(FinanceDataError): pass
class FinanceDataSetDataWrong(FinanceDataError): pass
class FinanceDataSetHighValueWrong(FinanceDataError): pass
class FinanceDataSetFileNotExist(FinanceDataError): pass

class FinancePoint:
    """This class finance data element "Point".
    
    This is basic element for finance data. It containse time and value.
    This class can't add any other more attribute in run time.

    Attributes:
        time: finace data time. must be datetime.datetime.
        value: finance data value. must be type which can be transform to float
    """
    __slots__=("__time","__value")  #make attribute only "__time" and "__value"
    def __init__(self, time, value):
        """FinancePoint initial function

        FinancePoint initial function.

        Args:
            time: finance data time. must be datetime.datetime
            value: finance data value. must be type which can be transform to 
                   float

        Returns:
            None

        Raise:
            FinanceDataError: An error occured intialing instance.
        """
        if isinstance(time, datetime.datetime):
            self.__time=time
        else:
            raise FinanceDataError("FinnacePoint variable time error.")
        self.__value=float(value)
    @property
    def value (self):
        return self.__value
    @value.setter
    def value (self, value):
        self.__value=float(value)
    @property
    def time (self):
        return self.__time
    @time.setter
    def time (self, time):
        if isinstance(time, datetime.datetime):
            self.__time=time
        else:
            raise FinanceDataError("{0:s} is not a datetime class."
                                   .format(str(time)))
    def __gt__ (self, other):
        if not isinstance(other, FinancePoint):
            raise FinanceDataError("FinnacePoint > error.")
        return self.value>other.value
    def __str__ (self):
        return ("FinancePoint Time: {} Value: {}".format(self.time, self.value))

class FinanceLine():
    """This class finance line.
    
    This is a container list for finance point.

    Attributes:
        None
    """
    peakValeDict={"slope":0.0,"peak":1.0,"vale":2.0}
    def __init__(self, iline=None):
        """FinanceLine initial function

        FinanceLine initial function.

        Args:
            iline: an input FinanceLine.
                 The instance will copy data from this line.

        Returns:
            None

        Raise:
            FinanceDataError: An error occured intialing instance.
        """
        if not iline:
            self.__points=[]
        elif isinstance(iline, FinanceLine):
            self=copy.copy(iline)
            return
        else:
            raise FinanceDataError("FinanceLine init fail")
    def add (self, ipoint):
        """add a point into list

        add a point into list.

        Args:
            ipoint: an FinancePoint which will be added to list.

        Returns:
            None

        Raise:
            FinanceDataError: An error occured adding point.
        """
        if not isinstance(ipoint, FinancePoint):
            raise FinanceDataError("FinanceLine.add ipoint is not a "
                                   "FinancePoint class.")
        self.__points.append(ipoint)
        #self.__points.sort(key=lambda t: t.time)
    def __getitem__ (self, k):
        """for operator [] to get element or slice a segment

        for operator [] to get element or slice a segment

        Args:
            k: list slice input arg.

        Returns:
            if slice a segment, return a FinanceLine
            if access one element, return a FinancePoint

        Raise:
            None
        """
        result=FinanceLine()
        if isinstance(k,slice):
            for icount in range(*k.indices(len(self))):
                result.add(self.__points[icount])
        else:
            return self.__points[k]
        return result
        
    def __setitem__ (self, k, ipoint):
        """for operator [] to set element

        for operator [] to get element

        Args:
            k: list slice input arg.

        Returns:
            return a FinancePoint

        Raise:
            FinanceDataError: an error occured setting element
        """
        if not isinstance(ipoint,FinancePoint):
            raise FinanceDataError("FinanceLine.__setitem__ ipoint is not "
                                   "a FinancePoint class.")
        if isinstance(k,slice):
            raise FinanceDataError("FinanceLine.__setitem__ can't be sliced.")
        self.__points[k]=ipoint
    def __len__ (self):
        return len(self.__points)
    #def __delitem__ (self, k):
    #    del self.__points[k]
    def __str__ (self):
        return str("FinanceDataSet Size:{0:d} lastdata:{1:s}".format(
            len(self.__points), self.__points.time))
    def index(self, value):
        """search element wiht value

        search element wiht value

        Args:
            value: searching value, muset be datetime.datetime or float

        Returns:
            return index in list which has same value

        Raise:
            FinanceDataOutOfIndex: can't find match element index
        """
        for i, v in enumerate(self):
            if isinstance(value,datetime.datetime):
                if v.time == value:
                    return i
            if isinstance(value,float):
                if v.value == value:
                    return i
        raise FinanceDataOutOfIndex()
    def sortTime (self):
        """sort the list with time

        sort the list with time

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        self.__points.sort(key=lambda t: t.time)
    def getTimeList (self):
        """provide the time list from point list

        provide the time list from point list

        Args:
            None

        Returns:
            return a list which contain the finance time.

        Raise:
            None
        """
        result=[]
        for item in self.__points:
            result.append(item.time)
        return result
    def getValueList (self):
        """provide the value list from point list

        provide the value list from point list

        Args:
            None

        Returns:
            return a list which contain the finance value.

        Raise:
            None
        """
        result=[]
        for item in self.__points:
            result.append(item.value)
        return result
    def removeRepeatItem (self):
        """remove the point whcih have same time.

        remove the point whcih have same time. only keep one in list

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        indextemp=[]
        for icount in range(len(self)-1):
            if self[icount].time == self[icount+1].time:
                indextemp.append(icount)
        for icount in reversed(indextemp):
            del self[icount]
    def findPeak (self):
        """search line peak

        search line peak

        Args:
            None

        Returns:
            return a FinanceLine which contain peak value.
            peakvale value:
                FinanceLine.peakValeDict["slope"]: not peak or value
                FinanceLine.peakValeDict["peak"]: peak

        Raise:
            None
        """
        result=FinanceLine()
        for icount in range(len(self)-1):
            if icount==0:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["slope"]))
                continue
            if self[icount-1].value<=self[icount].value>self[icount+1].value:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["peak"]))
            else:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["slope"]))
        result.add(FinancePoint(self[icount].time, 
                                FinanceLine.peakValeDict["slope"]))
        return result
    def findVale (self):
        result=FinanceLine()
        for icount in range(len(self)-1):
            if icount==0:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["slope"]))
                continue
            elif self[icount-1].value>=self[icount].value<self[icount+1].value:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["vale"]))
            else:
                result.add(FinancePoint(self[icount].time, 
                                        FinanceLine.peakValeDict["slope"]))
        result.add(FinancePoint(self[icount].time, 
                                FinanceLine.peakValeDict["slope"]))
        return result
    def getMaxValueIndex (self, start=0, end=-1):
        if start>=0:
            loopstart=start
        else:
            loopstart=len(self)+start
        if end>=0:
            loopend=end
        else:
            loopend=len(self)+end+1
        if loopstart==loopend:
            return loopstart
        result=None
        for icount in range(loopstart, loopend):
            if icount<0 or icount>=len(self):
                continue
            if result==None or maxValue<self[icount].value:
                result=icount
                maxValue=self[icount].value
        return result
    def getMinValueIndex (self, start=0, end=-1):
        if start>=0:
            loopstart=start
        else:
            loopstart=len(self)+start
        if end>=0:
            loopend=end
        else:
            loopend=len(self)+end+1
        if loopstart==loopend:
            return loopstart
        result=None
        minValue=0
        for icount in range(loopstart, loopend):
            if icount<0 or icount>=len(self):
                continue
            if result==None or minValue>self[icount].value:
                result=icount
                minValue=self[icount].value
        return result

class FinanceDataSet():
    """This class contain maket finance line data.
    
    This class contain maket finance line data. A market always have 5 types of 
    data: open, high, low, close, and volume. This class can contain and 
    manipulate these data.

    Attributes:
        openValue: market open value FinanceLine
        highValue: market high value FinanceLine
        lowValue: market low value FinanceLine
        closeValue: market close value FinanceLine
        volumeValue: market volume value FinanceLine
    """
    timeTypeDict={"year":"year",
                  "month":"month",
                  "day":"day",
                  "hour":"hour",
                  "minute":"minute",
                  "second":"second",
                  "tick":"tick"}
    dataStrType="%Y/%m/%d"
    dataStrType2='%Y/%m/%d %H:%M:%S:%f'
    csvHeadString="time,open,high,low,close,volume"
    def __init__ (self, iset=None, timeType="day", period=1):
        """FinanceDataSet initial function

        FinanceDataSet initial function.

        Args:
            iset: input FinanceDataSet or a None.
            timeType: setup time unit type
            period: time period

        Returns:
            None

        Raise:
            FinanceDataError: An error occured intialing instance.
        """
        if iset==None:
            pass
        elif isinstance(iset, FinanceDataSet):
            self.copy(iset)
            return
        else:
            raise FinanceDataError("FinanceDataSet init fail")
        if timeType not in FinanceDataSet.timeTypeDict.values():
            raise FinanceDataError("{0:s} is not a defined time type."
                                   .format(str(timeType)))
        self.__openValue=FinanceLine()
        self.__highValue=FinanceLine()
        self.__lowValue=FinanceLine()
        self.__closeValue=FinanceLine()
        self.__volumeValue=FinanceLine()
        self.timeType=timeType
        self.period=period
    @property
    def openValue (self):
        return self.__openValue
    @property
    def highValue (self):
        return self.__highValue
    @property
    def lowValue (self):
        return self.__lowValue
    @property
    def closeValue (self):
        return self.__closeValue
    @property
    def volumeValue (self):
        return self.__volumeValue
    def __len__ (self):
        return len(self.__closeValue)
    def __delitem__ (self, k):
        del self.__openValue[k]
        del self.__highValue[k]
        del self.__lowValue[k]
        del self.__closeValue[k]
        del self.__volumeValue[k]
    def __getitem__ (self, k):
        result=FinanceDataSet(None,self.timeType,self.period)
        if isinstance(k,slice):
            for icount in range(*k.indices(len(self))):
                result.addset(self[icount])
        else:
            result.add(self.__openValue[k].time,
                       self.__openValue[k].value,
                       self.__highValue[k].value,
                       self.__lowValue[k].value,
                       self.__closeValue[k].value,
                       self.__volumeValue[k].value)
        return result
    def __str__ (self):
        return str("FinanceDataSet Size:{0:d} lastdata:{1:s}".format(
            len(self.__openValue),str(self.__openValue[-1].time)))
    #def index(self, value):
    #    return self.closeValue.index(value)
    def copy (self, iset):
        """copy data from iset

        copy data from iset

        Args:
            iset: input FinanceDataSet

        Returns:
            None

        Raise:
            FinanceDataError: An error occured coping data.
        """
        if not isinstance(iset, FinanceDataSet):
            raise FinanceDataError("copy fail")
        self.__openValue    = copy.copy(iset.__openValue  )
        self.__highValue    = copy.copy(iset.__highValue  )
        self.__lowValue     = copy.copy(iset.__lowValue   )
        self.__closeValue   = copy.copy(iset.__closeValue )
        self.__volumeValue  = copy.copy(iset.__volumeValue)
        self.timeType       = copy.copy(iset.timeType     )
        self.period         = copy.copy(iset.period       )
    def add (self, idatetime, iopen, ihigh, ilow, iclose, ivolume=0):
        """add data into list

        add data into list

        Args:
            idatetime: finance time. must be datetime.datetime
            iopen: open value
            ihigh: high value
            ilow: low value
            iclose: close value
            ivolume: volume value, default 0

        Returns:
            None

        Raise:
            FinanceDataSetDataWrong: An error occured adding data.
            FinanceDataSetHighValueWrong: An error occured adding data.
        """
        if not isinstance(idatetime, datetime.datetime):
            raise FinanceDataError("FinanceDataSet.add idtetime is not a "
                                   "datetime class.")
        try:
            opentemp =float(iopen)
            hightemp =float(ihigh)
            lowtemp  =float(ilow)
            closetemp=float(iclose)
            voltemp  =float(ivolume)
        except ValueError:
            raise FinanceDataSetDataWrong("open, close, high, low, and volume "
                                          "value must be int or float.")
        debugstr=str("{0:s} open:{1:s} high:{2:s} low:{3:s} close:{4:s} "
                     "vol:{5:s}".format(str(idatetime), str(iopen), str(ihigh), 
                                        str(ilow), str(iclose), str(ivolume)))
        if opentemp==0 or hightemp==0 or lowtemp==0 or closetemp==0:
            raise FinanceDataSetDataWrong("open, close, high, and low value "
                                          "can't be 0."+debugstr)
        if hightemp<opentemp or hightemp<lowtemp or hightemp<closetemp:
            raise FinanceDataSetHighValueWrong("high value is not highest "
                                               "value"+debugstr)
        if lowtemp>opentemp or lowtemp>hightemp or lowtemp>closetemp:
            raise FinanceDataSetHighValueWrong("low value is not lowest value"
                                               +debugstr)
        self.__openValue.add(FinancePoint(idatetime, opentemp))
        self.__highValue.add(FinancePoint(idatetime, hightemp))
        self.__lowValue.add(FinancePoint(idatetime, lowtemp))
        self.__closeValue.add(FinancePoint(idatetime, closetemp))
        self.__volumeValue.add(FinancePoint(idatetime, voltemp))
    def addset (self, idataset):
        """add a FinanceDataSet into list

        add a FinanceDataSet into list

        Args:
            idataset: input FinanceDataSet

        Returns:
            None

        Raise:
            FinanceDataError: An error occured adding data.
        """
        if not isinstance(idataset,FinanceDataSet):
            raise FinanceDataError("FinanceDataSet.addset idataset is not a "
                                   "FinanceDataSet class.")
        for icount in range(len(idataset)):
            self.add(idataset.openValue[icount].time,
                     idataset.openValue[icount].value,
                     idataset.highValue[icount].value,
                     idataset.lowValue[icount].value,
                     idataset.closeValue[icount].value,
                     idataset.volumeValue[icount].value,)
        #self.sortTime()
        #self.removeRepeatItem()
    def removeRepeatItem (self):
        """remove items which have same repeat finance time

        remove item which have same repeat finance time

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        indextemp=[]
        for icount in range(len(self.openValue)):
            if icount==0:
                continue
            if self.openValue[icount].time == self.openValue[icount-1].time:
                indextemp.append(icount)
        for icount in reversed(indextemp):
            del self[icount]
    def getLastTime (self):
        """get the latest finance time

        get the latest finance time

        Args:
            None

        Returns:
            return latest finance time.

        Raise:
            None
        """
        try:
            return self.__openValue[-1].time
        except IndexError:
            return datetime.datetime(1976,1,1)
    def changePeriod (self, iperiod):
        """change period and recalculate the data

        change period and recalculate the data

        Args:
            iperiod: new period

        Returns:
            None

        Raise:
            None
        """
        if self.period>iperiod:
            raise FinanceDataError("{0:s} is not a defined time type."
                                   .format(str(timeType)))
        newset=FinanceDataSet(None, self.timeType, iperiod)
        timetemp=self.openValue[0].time
        opentemp=self.openValue[0].value
        hightemp=0
        lowtemp=99999999999999.99999
        closetemp=self.closeValue[0].value
        voltemp=0
        for icount in range(len(self)):
            voltemp+=self.volumeValue[icount].value
            if hightemp<self.highValue[icount].value:
                hightemp=self.highValue[icount].value
            if lowtemp>self.lowValue[icount].value:
                lowtemp=self.lowValue[icount].value
            if icount%iperiod==0:
                opentemp=self.openValue[icount].value
            elif icount%iperiod==iperiod-1 or icount==len(self)-1:
                closetemp=self.closeValue[icount].value
                timetemp=self.openValue[icount].time
                newset.add(timetemp, opentemp, hightemp, lowtemp, closetemp, 
                           voltemp)
                hightemp=0
                lowtemp=99999999999999.99999
                voltemp=0         
        self.copy(newset)
    def getDataFromFile (self, dataFile):
        """get finance data from csv file

        get finance data from csv file

        Args:
            dataFile: csv file path

        Returns:
            None

        Raise:
            FinanceDataSetFileNotExist: an error occured getting data from file
        """
        if isinstance(dataFile,str):
            #if not os.path.exists(os.path.dirname(dataFile)):
            #    os.makedirs(os.path.dirname(dataFile))
            strtemp=dataFile
        else:
            raise FinanceDataSetFileNotExist("{0:s} is not a file name string."
                                             .format(str(dataFile)))
        try:
            csvFileR=open(strtemp, "r")
        except FileNotFoundError:
            raise FinanceDataSetFileNotExist("{0:s} is not exist."
                                             .format(str(strtemp)))
        csvContent=csv.reader(csvFileR, delimiter=',')
        for i in csvContent:
            try:
                dt = datetime.datetime.fromtimestamp(time.mktime(
                    time.strptime(i[0], FinanceDataSet.dataStrType)))
            except ValueError:
                try:
                    dt = datetime.datetime.fromtimestamp(time.mktime(
                        time.strptime(i[0], FinanceDataSet.dataStrType2)))
                except:
                    continue
            try:
                openValue=float(i[1].replace(",",""))
            except ValueError:
                openValue=0.0
            try:
                highValue=float(i[2].replace(",",""))
            except ValueError:
                highValue=0.0
            try:
                lowValue=float(i[3].replace(",",""))
            except ValueError:
                lowValue=0.0
            try:
                closeValue=float(i[4].replace(",",""))
            except ValueError:
                closeValue=0.0
            try:
                volValue=float(i[5].replace(",",""))
            except ValueError:
                volValue=0.0
            self.add(dt,openValue, highValue, lowValue, closeValue, volValue)
        self.sortTime()
    def saveDataToFile (self, dataFile):
        """save finance data to csv file

        save finance data to csv file

        Args:
            dataFile: csv file path

        Returns:
            None

        Raise:
            None
        """
        if isinstance(dataFile,str):
            if not os.path.exists(os.path.dirname(dataFile)):
                os.makedirs(os.path.dirname(dataFile))
            strtemp=dataFile
        else:
            raise FinanceDataSetFileNotExist("{0:s} is not a file name string."
                                             .format(str(dataFile)))
        csvFileW=open(strtemp, "w", newline='')
        csvContent=csv.writer(csvFileW, delimiter=',')
        csvContent.writerow(["time",
                            "open",
                            "high",
                            "low",
                            "close",
                            "volume"])
        for icount in range(len(self.openValue)):
            csvContent.writerow([datetime.datetime.strftime(
                                    self.openValue[icount].time, 
                                    FinanceDataSet.dataStrType2),
                                 str(self.openValue[icount].value),
                                 str(self.highValue[icount].value),
                                 str(self.lowValue[icount].value),
                                 str(self.closeValue[icount].value),
                                 str(self.volumeValue[icount].value)])
        csvFileW.close()
    def sortTime (self):
        """sort the data with time

        sort the data with time

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        self.__openValue.sortTime()
        self.__highValue.sortTime()
        self.__lowValue.sortTime()
        self.__closeValue.sortTime()
        self.__volumeValue.sortTime()
class financeDataTest(unittest.TestCase):
    def setUp(self):
        self.sampleLine=FinanceLine()
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,5,25,23,13,11,22),10))
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,5,26),3))
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,6,26),3))
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,1,26),7))
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,8,26),2))
        self.sampleLine.add(FinancePoint(datetime.datetime(2016,2,26),5.5))
        self.sampleSet=FinanceDataSet()
        self.sampleSet.add(datetime.datetime(2015,12,26),9000,9100,8900,9050,100)
        self.sampleSet.add(datetime.datetime(2015,8,26),8000,8100,7900,8050,33)
        self.sampleSet.add(datetime.datetime(2015,10,26),7000,7100,6900,7050,44)
        self.sampleSet.add(datetime.datetime(2015,1,26),6000,6100,5900,6050,55)
    def test_sampleSort (self):
        laspoint=self.sampleLine[-1]
        testline=self.sampleLine[:]
        testline.add(FinancePoint(datetime.datetime(2010,5,25,23,13,11,22),55))
        testline.sortTime()
        self.assertEqual(self.sampleLine[-1], laspoint)
    def test_addSet (self):
        oriSet=self.sampleSet[:]
        testSet=FinanceDataSet()
        testSet.add(datetime.datetime(2000,12,26),9000,9100,8900,9050,100)
        testSet.add(datetime.datetime(2000,5,26),9000,9100,8900,9050,100)
        testSet.add(datetime.datetime(2000,3,26),9000,9100,8900,9050,100)
        testSet.add(datetime.datetime(2015,10,26),7000,7100,6900,7050,44)
        testSet.add(datetime.datetime(2015,1,26),6000,6100,5900,6050,55)
        oriSet.addset(testSet)
        for icount in range(-1, 0-len(testSet), -1):
            self.assertTrue(testSet.openValue[icount].time==oriSet.openValue[icount].time 
                            and testSet.openValue[icount].value==oriSet.openValue[icount].value,
                            msg='icount:%d testset:%s oriset:%s' %(icount, str(testSet.openValue[icount]), oriSet.openValue[icount]))
    def test_findMax (self):
        self.assertTrue(10.0==max(self.sampleLine).value)
    def test_findMin (self):
        self.assertTrue(2.0==min(self.sampleLine).value)
    def test_getIndex (self):
        self.assertTrue(self.sampleLine.index(datetime.datetime(2016,1,26))==3)
if __name__=="__main__":
    unittest.main(verbosity=2)

