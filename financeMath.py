# -*- coding: utf-8 -*-
"""
.. module:: financeMath
    :synopsis: finance mathematic function class
.. author: K.K.Chien
"""
import datetime
import math
import sys
import unittest
import financeData

class FinanceMathFunctionError(Exception): pass
class FinanceMathFunctionOutofIndex(FinanceMathFunctionError): pass
class FinanceMathFunctionPosBelowPeriod(FinanceMathFunctionError): pass

class FinanceMathFunction():
    """This class collect finance mathmatical functions.
    
    This class collect finance mathmatical functions.

    Attributes:
        None
    """
    goldRatio=1.6180339
    cjGRation=0.6180339
    ration2Sigma=0.04550026
    def __init__ (self):
        self.clear()
    def clear (self):
        self.tempdic={}
    def calMA (self, inputData, outputData, position=5, period=5):
        """caculate moving average

        caculate moving average

        Args:
            inputData: input source data, FinanceLine class
            outputData: output finance data, FinanceLine class
            position: current caculate position
            period: moving average period, default 5

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period

        """
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(outputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputData)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        if not isinstance(period, int) or period<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        valuetemp=0.0
        for icount in range(period):
            valuetemp+=inputData[position-icount].value
        valuetemp/=period
        outputData.add(financeData.FinancePoint(inputData[position].time, valuetemp))
    def calWMA (self, inputData, outputData, position, period=5):
        """caculate weighted moving average

        caculate weighted moving average

        Args:
            inputData: input source data, FinanceLine class
            outputData: output finance data, FinanceLine class
            position: current caculate position
            period: moving average period, default 5

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(outputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputData)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        if not isinstance(period, int) or period<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        valuetemp=0.0
        divider=0.0
        for icount in range(period):
            valuetemp+=inputData[position-icount].value*(period-icount)
            divider+=(period-icount)
        valuetemp/=divider
        outputData.add(financeData.FinancePoint(inputData[position].time, valuetemp))
    def calEMA (self, inputData, outputData, position, period=5):
        """caculate exponential moving average

        caculate exponential moving average

        Args:
            inputData: input source data, FinanceLine class
            outputData: output finance data, FinanceLine class
            position: current caculate position
            period: moving average period, default 5

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(outputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputData)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        if not isinstance(period, int) or period<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        alpha=2.0/(period+1)
        valuetemp=0.0
        divider=0.0
        for icount in range(period):
            valuetemp+=inputData[position-icount].value*((1-alpha)**icount)
            divider+=((1-alpha)**icount)
        valuetemp/=divider
        outputData.add(financeData.FinancePoint(inputData[position].time, valuetemp))
    def calHMA (self, inputData, outputData, position, period=5):
        """caculate hull moving average

        caculate hull moving average

        Args:
            inputData: input source data, FinanceLine class
            outputData: output finance data, FinanceLine class
            position: current caculate position
            period: moving average period, default 5

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(outputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputData)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        if not isinstance(period, int) or period<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        idstr=str(id(inputData)+id(outputData))
        if idstr not in self.tempdic.keys():
            self.tempdic[idstr]=financeData.FinanceLine()
        wma1=financeData.FinanceLine()
        self.calWMA(inputData,wma1,position,period)
        wma2=financeData.FinanceLine()
        self.calWMA(inputData,wma2,position,int(period/2))
        pointtemp=financeData.FinancePoint(inputData[position].time,wma2[0].value*2-wma1[0].value)
        self.tempdic[idstr].add(pointtemp)
        #self.tempdic[idstr].removeRepeatItem()
        self.calWMA(self.tempdic[idstr],outputData,len(self.tempdic[idstr])-1,int(math.sqrt(period)))
    def calxMACD (self, inputData, inputMA1, inputMA2, outputDiff, position):
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(inputMA1, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputMA1)))
        if len(inputMA1)==0:
            raise FinanceMathFunctionPosBelowPeriod("inputMA1 len is 0.")
        if not isinstance(inputMA2, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputMA2)))
        if len(inputMA2)==0:
            raise FinanceMathFunctionPosBelowPeriod("inputMA2 len is 0.")
        if not isinstance(outputDiff, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputDiff)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        pointtemp=financeData.FinancePoint(inputMA1[-1].time, inputMA1[-1].value-inputMA2[-1].value)
        outputDiff.add(pointtemp)
    def calKKMACD (self, inputData, outputHMA, outputEMA, outputDiff, position, periodHMA, periodEMA):
        """caculate myself moving average convergence divergence

        caculate myself moving average convergence divergence

        Args:
            inputData: input source data, FinanceLine class
            outputHMA: output HMA finance data, FinanceLine class
            outputEMA: output EMA finance data, FinanceLine class
            outputDiff: output (HMA-EMA) finance data, FinanceLine class
            position: current caculate position
            periodHMA: HMA moving average period
            periodEMA: HMA moving average period

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(inputData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(inputData)))
        if not isinstance(outputHMA, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputHMA)))
        if not isinstance(outputEMA, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputEMA)))
        if not isinstance(outputDiff, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputDiff)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(position)))
        if position>=len(inputData):
            raise FinanceMathFunctionOutofIndex()
        if not isinstance(periodHMA, int) or periodHMA<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if not isinstance(periodEMA, int) or periodEMA<=1:
            raise FinanceMathFunctionError("{0:s} is not a integer or <=1.".format(str(period)))
        if position<periodHMA-1 or position<periodEMA-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,periodEMA))
        exceptTemp=False
        try:
            self.calHMA(inputData,outputHMA,position,periodHMA)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        try:
            self.calEMA(inputData,outputEMA,position,periodEMA)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        if exceptTemp:
            raise FinanceMathFunctionPosBelowPeriod()
        pointtemp=financeData.FinancePoint(outputHMA[-1].time, outputHMA[-1].value-outputEMA[-1].value)
        outputDiff.add(pointtemp)
    def calEMABand (self, closeData, highData, lowData, outputMid, outputHigh, outputLow, position, period, multiplier):
        """caculate EMA band

        caculate EMA band

        Args:
            closeData: close source data, FinanceLine class
            highData: high source data, FinanceLine class
            lowData: low source data, FinanceLine class
            outputMid: output middle line finance data, FinanceLine class
            outputHigh: output high line finance data, FinanceLine class
            outputLow: output low line finance data, FinanceLine class
            position: current caculate position
            period: band period
            multiplier: high/low mutiplier

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(closeData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(closeData)))
        if not isinstance(highData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(highData)))
        if not isinstance(lowData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(lowData)))
        if not isinstance(outputMid, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputMid)))
        if not isinstance(outputHigh, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputHigh)))
        if not isinstance(outputLow, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputLow)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a integer.".format(str(position)))
        if position>=len(closeData):
            raise FinanceMathFunctionOutofIndex()
        if period<=1:
            raise FinanceMathFunctionError("{0:s} is <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        if not isinstance(multiplier, float):
            raise FinanceMathFunctionError("{0:s} is not a float.".format(str(multiplier)))
        idhighstr=str(id(highData)+id(outputHigh))
        if idhighstr not in self.tempdic.keys():
            self.tempdic[idhighstr]=financeData.FinanceLine()
        idlowstr=str(id(lowData)+id(outputLow))
        if idlowstr not in self.tempdic.keys():
            self.tempdic[idlowstr]=financeData.FinanceLine()
        exceptTemp=False
        try:
            self.calEMA(closeData,outputMid,position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        try:
            self.calEMA(highData,self.tempdic[idhighstr],position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        try:
            self.calEMA(lowData,self.tempdic[idlowstr],position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        if exceptTemp:
            raise FinanceMathFunctionPosBelowPeriod()
        temph=self.tempdic[idhighstr][-1].value-outputMid[-1].value
        templ=outputMid[-1].value-self.tempdic[idlowstr][-1].value
        if temph>templ:
            offset=temph
        else:
            offset=templ
        pointtemp=financeData.FinancePoint(outputMid[-1].time, outputMid[-1].value+offset*multiplier)
        outputHigh.add(pointtemp)
        pointtemp=financeData.FinancePoint(outputMid[-1].time, outputMid[-1].value-offset*multiplier)
        outputLow.add(pointtemp)
    def calHMABand (self, closeData, highData, lowData, outputMid, outputHigh, outputLow, position, period, multiplier):
        """caculate HMA band

        caculate HMA band

        Args:
            closeData: close source data, FinanceLine class
            highData: high source data, FinanceLine class
            lowData: low source data, FinanceLine class
            outputMid: output middle line finance data, FinanceLine class
            outputHigh: output high line finance data, FinanceLine class
            outputLow: output low line finance data, FinanceLine class
            position: current caculate position
            period: band period
            multiplier: high/low mutiplier

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(closeData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(closeData)))
        if not isinstance(highData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(highData)))
        if not isinstance(lowData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(lowData)))
        if not isinstance(outputMid, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputMid)))
        if not isinstance(outputHigh, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputHigh)))
        if not isinstance(outputLow, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputLow)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a integer.".format(str(position)))
        if position>=len(closeData):
            raise FinanceMathFunctionOutofIndex()
        if period<=1:
            raise FinanceMathFunctionError("{0:s} is <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        if not isinstance(multiplier, float):
            raise FinanceMathFunctionError("{0:s} is not a float.".format(str(multiplier)))
        idhighstr=str(id(highData)+id(outputHigh))
        if idhighstr not in self.tempdic.keys():
            self.tempdic[idhighstr]=financeData.FinanceLine()
        idlowstr=str(id(lowData)+id(outputLow))
        if idlowstr not in self.tempdic.keys():
            self.tempdic[idlowstr]=financeData.FinanceLine()
        exceptTemp=False
        try:
            self.calHMA(closeData,outputMid,position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        try:
            self.calHMA(highData,self.tempdic[idhighstr],position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        try:
            self.calHMA(lowData,self.tempdic[idlowstr],position,period)
        except FinanceMathFunctionPosBelowPeriod as e:
            exceptTemp=True
        if exceptTemp:
            raise FinanceMathFunctionPosBelowPeriod()
        temph=self.tempdic[idhighstr][-1].value-outputMid[-1].value
        templ=outputMid[-1].value-self.tempdic[idlowstr][-1].value
        if temph>templ:
            offset=temph
        else:
            offset=templ
        pointtemp=financeData.FinancePoint(outputMid[-1].time, outputMid[-1].value+offset*multiplier)
        outputHigh.add(pointtemp)
        pointtemp=financeData.FinancePoint(outputMid[-1].time, outputMid[-1].value-offset*multiplier)
        outputLow.add(pointtemp)
    def calATR (self, closeData, highData, lowData, outputATR, position, period, multiplier):
        """caculate average true range

        caculate average true range

        Args:
            closeData: close source data, FinanceLine class
            highData: high source data, FinanceLine class
            lowData: low source data, FinanceLine class
            outputATR: output ATR finance data, FinanceLine class
            position: current caculate position
            period: band period
            multiplier: range mutiplier

        Returns:
            None

        Raise:
            FinanceMathFunctionError: An error occured caculating.
            FinanceMathFunctionOutofIndex: position is larger than inputData 
                                           length
            FinanceMathFunctionPosBelowPeriod:  position is smaller than period
        """
        if not isinstance(closeData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(closeData)))
        if not isinstance(highData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(highData)))
        if not isinstance(lowData, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(lowData)))
        if not isinstance(outputATR, financeData.FinanceLine):
            raise FinanceMathFunctionError("{0:s} is not a FinanceLine class.".format(str(outputATR)))
        if not isinstance(position, int):
            raise FinanceMathFunctionError("{0:s} is not a integer.".format(str(position)))
        if position>=len(closeData):
            raise FinanceMathFunctionOutofIndex()
        if period<=1:
            raise FinanceMathFunctionError("{0:s} is <=1.".format(str(period)))
        if position<period-1:
            raise FinanceMathFunctionPosBelowPeriod("position:{0:d}<(period:{1:d}-1).".format(position,period))
        if not isinstance(multiplier, float):
            raise FinanceMathFunctionError("{0:s} is not a float.".format(str(multiplier)))
        idAtrstr=str(id(closeData)+id(outputATR))
        if idAtrstr not in self.tempdic.keys():
            self.tempdic[idAtrstr]=financeData.FinanceLine()
        if position>=0:
            ptemp=position
        else:
            ptemp=len(closeData)+positio1n
        if ptemp==0:
            rtemp=math.fabs(highData[ptemp].value-lowData[ptemp].value)
            self.tempdic[idAtrstr].add(FinancePoint(closeData[ptemp].time, rtemp*multiplier))
        else:
            rtemp=math.fabs(highData[ptemp].value-lowData[ptemp].value)
            stemp=math.fabs(highData[ptemp].value-closeData[ptemp-1].value)
            if stemp>rtemp:
                rtemp=stemp
            stemp=math.fabs(lowData[ptemp].value-closeData[ptemp-1].value)
            if stemp>rtemp:
                rtemp=stemp
            self.tempdic[idAtrstr].add(financeData.FinancePoint(closeData[ptemp].time, rtemp*multiplier))
        try:
            self.calEMA(self.tempdic[idAtrstr],outputATR,ptemp-period+1,period)
        except FinanceMathFunctionPosBelowPeriod:
            pass
    def getHighLowSignificantPoint (self, inputCheckHigh, inputCheckLow, inputHigh, inputLow, offset=2):
        maxList=[]
        minList=[]
        resultHigh=financeData.FinanceLine()
        resultLow=financeData.FinanceLine()
        hlen=len(inputHigh)
        llen=len(inputLow)
        if hlen!=llen:
            raise Exception()
        for icount in range(-2, 0-hlen, -1):
            checkrange1=icount-offset
            checkrange2=icount+1
            try:
                if inputCheckHigh[icount-1].value<=inputCheckHigh[icount].value>inputCheckHigh[icount+1].value:
                    indextemp=inputHigh.getMaxValueIndex(checkrange1, checkrange2)
                    if indextemp!=None:
                        if len(maxList)==0:
                            maxList.append(indextemp)
                        elif indextemp in maxList:
                            pass
                        elif inputHigh[indextemp].value<inputHigh[indextemp-1].value:
                            pass
                        elif len(minList)==0 or maxList[-1]<minList[-1]:
                            if inputHigh[indextemp].value>inputHigh[maxList[-1]].value:
                                del maxList[-1]
                                maxList.append(indextemp)
                        elif maxList[-1]>=minList[-1]:
                            maxList.append(indextemp)
            except IndexError:
                pass
            try:
                if inputCheckLow[icount-1].value>=inputCheckLow[icount].value<inputCheckLow[icount+1].value:
                    indextemp=inputLow.getMinValueIndex(checkrange1, checkrange2)
                    if indextemp!=None:
                        if not len(minList):
                            minList.append(indextemp)
                        elif indextemp in minList:
                            pass
                        elif inputLow[indextemp].value>inputLow[indextemp-1].value:
                            pass
                        elif len(maxList)==0 or maxList[-1]>minList[-1]:
                            if inputLow[indextemp].value<inputLow[minList[-1]].value:
                                del minList[-1]
                                minList.append(indextemp)
                        elif maxList[-1]<=minList[-1]:
                            minList.append(indextemp)
            except IndexError:
                pass
        for icount in range(len(inputHigh)):
            if icount in maxList:
                resultHigh.add(financeData.FinancePoint(inputHigh[icount].time, 
                                        financeData.FinanceLine.peakValeDict["peak"]))
            else:
                resultHigh.add(financeData.FinancePoint(inputHigh[icount].time, 
                                        financeData.FinanceLine.peakValeDict["slope"]))
            if icount in minList:
                resultLow.add(financeData.FinancePoint(inputHigh[icount].time, 
                                        financeData.FinanceLine.peakValeDict["vale"]))
            else:
                resultLow.add(financeData.FinancePoint(inputHigh[icount].time, 
                                        financeData.FinanceLine.peakValeDict["slope"]))
        return (resultHigh, resultLow)
    def calHMABandWeight (self, inputClose, inputHigh, inputLow, highSigPoint, lowSigPoint, period, multiplier):
        result=0.0
        wcount=0
        midtemp=financeData.FinanceLine()
        hightemp=financeData.FinanceLine()
        lowtemp=financeData.FinanceLine()
        for icount in range(len(inputClose)):
            try:
                self.calHMABand(inputClose,
                       inputHigh, 
                       inputLow,
                       midtemp, hightemp, lowtemp, 
                       icount, period, multiplier)
            except FinanceMathFunctionPosBelowPeriod:
                        continue
        for icount in range(-1, -1-len(midtemp), -1):
            if highSigPoint[icount].value==financeData.FinanceLine.peakValeDict["peak"]:  #high
                if inputHigh[icount].value<midtemp[icount].value:
                    continue
                diff=math.fabs(inputHigh[icount].value-hightemp[icount].value)
                result+=diff
                wcount+=1
            if lowSigPoint[icount].value==financeData.FinanceLine.peakValeDict["vale"]:  #low
                if inputLow[icount].value>midtemp[icount].value:
                    continue
                diff=math.fabs(lowtemp[icount].value-inputLow[icount].value)
                result+=diff
                wcount+=1
        if not wcount:
            return result
        return (result/wcount)
    def calKKMacdWeight (self, inputData, periodHMA, periodEMA, offset=2):
        result=0.0
        hamtemp=financeData.FinanceLine()
        ematemp=financeData.FinanceLine()
        difftemp=financeData.FinanceLine()
        for icount in range(len(inputData)):
            try:
                self.calKKMACD(inputData, hmatemp, ematemp, difftemp, icount, periodHMA, periodEMA)
            except FinanceMathFunctionPosBelowPeriod:
                continue
        ihDiff=len(inputData)-len(hamtemp)
        ieDiff=len(inputData)-len(ematemp)
        idDiff=len(inputData)-len(difftemp)
        peaktemp=[]
        valetemp=[]
        difftemp.peakLine=difftemp.findPeak()
        difftemp.valeLine=difftemp.findVale()
        for icount in range(0-len(difftemp), -1):
            if difftemp.peakLine[icount].value==financeData.FinanceLine.peakValeDict["slope"]:
                continue
            elif difftemp.peakLine[icount].value==financeData.FinanceLine.peakValeDict["peak"]:
                indextemp=inputData.getMaxValueIndex(icount-offset, icount)
                peaktemp.append([icount, indextemp, inputData[indextemp].value])
        return result
    def calRatio (self, closeData, highData, lowData, period, multiplier, matype='hma'):
        midtemp=financeData.FinanceLine()
        hightemp=financeData.FinanceLine()
        lowtemp=financeData.FinanceLine()
        for icount in range(len(closeData)):
            try:
                if matype=='hma':
                    self.calHMABand(closeData, highData, lowData, midtemp, hightemp, lowtemp, icount, period, multiplier)
                elif matype=='ema':
                    self.calEMABand(closeData, highData, lowData, midtemp, hightemp, lowtemp, icount, period, multiplier)
                else:
                    raise Exception()
            except FinanceMathFunctionPosBelowPeriod:
                pass
        outCount=[]
        inCount=[]
        outBoundCnt=[]
        for icount in range(-1,0-len(hightemp),-1):
            if (closeData[icount].value>=midtemp[icount].value
                and highData[icount].value>=hightemp[icount].value):
                outCount.append(closeData[icount])
                if lowData[icount].value>=hightemp[icount].value:
                    outBoundCnt.append(closeData[icount])
            elif (closeData[icount].value<midtemp[icount].value
                and lowData[icount].value<=lowtemp[icount].value):
                outCount.append(closeData[icount])
                if highData[icount].value<=hightemp[icount].value:
                    outBoundCnt.append(closeData[icount])
            else:
                inCount.append(closeData[icount])
        if len(outCount)==0:
            return (0, 0)
        return (len(outCount)/(len(inCount)+len(outCount)) ,len(outBoundCnt)/len(outCount))

class financeMathTest(unittest.TestCase):
    def setUp (self):
        self.sampleSet=financeData.FinanceDataSet()
        self.sampleSet.getDataFromFile('./history/test.csv')
    def xxtest_Atr (self):
        fobj=FinanceMathFunction()
        atrline=financeData.FinanceLine()
        for icount in range(len(self.sampleSet)):
            try:
                fobj.calATR(self.sampleSet.closeValue,self.sampleSet.highValue,self.sampleSet.lowValue,atrline,icount,16, 2.0)
            except FinanceMathFunctionPosBelowPeriod:
                continue
        for item in atrline:
            print('atr %s %f' %(str(item.time), item.value))
        self.assertTrue(True)
    def test_ratio (self):
        fobj=FinanceMathFunction()
        print(fobj.calRatio(self.sampleSet.closeValue,self.sampleSet.highValue,self.sampleSet.lowValue,10,1.0))
        self.assertTrue(True)
if __name__=="__main__":
    unittest.main()
    
