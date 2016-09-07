# -*- coding: utf-8 -*-
"""
.. module:: financeMath
    :synopsis: finance mathematic function class
.. author: K.K.Chien
"""
import datetime
import math
import sys
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
    fibo=1.6180339
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
            ptemp=len(closeData)+position
        if position==0:
            rtemp=math.fabs(highData[ptemp].value-lowData[ptemp].value)
            self.tempdic[idAtrstr].add(FinancePoint(closeData[ptemp].time, rtemp))
        else:
            rtemp=math.fabs(highData[ptemp].value-lowData[ptemp].value)
            stemp=math.fabs(highData[ptemp].value-closeData[ptemp].value)
            if stemp>rtemp:
                rtemp=stemp
            stemp=math.fabs(lowData[ptemp].value-closeData[ptemp].value)
            if stemp>rtemp:
                rtemp=stemp
            self.tempdic[idAtrstr].add(FinancePoint(closeData[ptemp].time, rtemp))
        self.calHMA(self.tempdic[idAtrstr],outputATR,position,period)


if __name__=="__main__":
    fobj=FinanceMathFunction()
    line1=financeData.FinanceLine()
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,1),1.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,2),2.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,3),3.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,4),4.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,5),5.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,6),6.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,7),7.0))
    line1.add(financeData.FinancePoint(datetime.datetime(2016,8,8),8.0))
    resultline=financeData.FinanceLine()
    for icount in range(len(line1)):
        try:
            fobj.calHMA(line1,resultline,icount,5)
        except FinanceMathFunctionPosBelowPeriod:
            continue
    for icount in range(len(resultline)):
        print(icount,resultline[icount].time,resultline[icount].value)



