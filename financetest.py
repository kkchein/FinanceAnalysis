"""
This program draw finance data with matPlotDraw.
"""
import datetime
import numpy
import financeData as fd
import financeMath as fm
import matPlotDraw as mpd
import dataCenter as dc

if __name__=="__main__":
    plotObj=mpd.MPLTDraw()
    line1=fd.FinanceLine()
    if True:
        startPos=-300
        settemp=fd.FinanceDataSet()
        #settemp.getDataFromFile("./history/Index_TaiwanWI_google_1_day.csv")
        settemp.getDataFromFile("./history/Stock_ChinaSteel_google_1_day.csv")
        line1=settemp.closeValue[startPos:]
        line2=settemp.highValue[startPos:]
        line3=settemp.lowValue[startPos:]
    else:
        for icount in range(50):
            line1.add(fd.FinancePoint(datetime.datetime(2016,8,1)+datetime.timedelta(days=icount+1),
                                      numpy.sin((icount+1)*0.13)*1000))
            line2.add(fd.FinancePoint(datetime.datetime(2016,8,1)+datetime.timedelta(days=icount+1),
                                      (numpy.sin((icount+1)*0.13)+5)*1000))
            line1.add(fd.FinancePoint(datetime.datetime(2016,8,1)+datetime.timedelta(days=icount+1),
                                      (numpy.sin((icount+1)*0.13)-5)*1000))
    plotObj.addLine(line1)

    #fobj=fm.FinanceMathFunction()
    #resultline=fd.FinanceLine()
    #for icount in range(len(line1)):
    #    try:
    #        fobj.calMA(line1,resultline,icount,int(90*fm.FinanceMathFunction.fibo))
    #    except fm.FinanceMathFunctionPosBelowPeriod:
    #        continue
    #plotObj.addLine(resultline)

    #fobj=fm.FinanceMathFunction()
    #resultline=fd.FinanceLine()
    #for icount in range(len(line1)):
    #    try:
    #        fobj.calWMA(line1,resultline,icount,int(90*fm.FinanceMathFunction.fibo))
    #    except fm.FinanceMathFunctionPosBelowPeriod:
    #        continue
    #plotObj.addLine(resultline)

    #fobj=fm.FinanceMathFunction()
    #resultline=fd.FinanceLine()
    #for icount in range(len(line1)):
    #    try:
    #        fobj.calEMA(line1,resultline,icount,int(90*fm.FinanceMathFunction.fibo))
    #    except fm.FinanceMathFunctionPosBelowPeriod:
    #        continue
    #plotObj.addLine(resultline)

    #fobj=fm.FinanceMathFunction()
    #resultline=fd.FinanceLine()
    #for icount in range(len(line1)):
    #    try:
    #        fobj.calHMA(line1,resultline,icount,int(30*fm.FinanceMathFunction.fibo))
    #    except fm.FinanceMathFunctionPosBelowPeriod:
    #        continue
    #plotObj.addLine(resultline)

    #fobj=fm.FinanceMathFunction()
    #hmatemp=fd.FinanceLine()
    #ematemp=fd.FinanceLine()
    #diftemp=fd.FinanceLine()
    #for icount in range(len(line1)):
    #    try:
    #        fobj.calKKMACD(line1,hmatemp,ematemp,diftemp,icount,int(12*fm.FinanceMathFunction.fibo),int(8*fm.FinanceMathFunction.fibo))
    #    except fm.FinanceMathFunctionPosBelowPeriod:
    #        continue
    #plotObj.addLine(hmatemp)
    #plotObj.addLine(ematemp)
    #for item in diftemp:
    #    print(item.time,item.value)

    fobj=fm.FinanceMathFunction()
    midline=fd.FinanceLine()
    hiline=fd.FinanceLine()
    loline=fd.FinanceLine()
    for icount in range(len(line1)):
        try:
            fobj.calHMABand(line1,line2,line3,midline,hiline,loline,icount,
                            int(30*fm.FinanceMathFunction.fibo),fm.FinanceMathFunction.fibo*3)
        except fm.FinanceMathFunctionPosBelowPeriod:
            continue
    plotObj.addLine(midline)
    plotObj.addLine(hiline)
    plotObj.addLine(loline)

    fobj=fm.FinanceMathFunction()
    midline=fd.FinanceLine()
    hiline=fd.FinanceLine()
    loline=fd.FinanceLine()
    for icount in range(len(line1)):
        try:
            fobj.calHMABand(line1,line2,line3,midline,hiline,loline,icount,
                            int(90*fm.FinanceMathFunction.fibo),fm.FinanceMathFunction.fibo*10)
        except fm.FinanceMathFunctionPosBelowPeriod:
            continue
    plotObj.addLine(midline)
    plotObj.addLine(hiline)
    plotObj.addLine(loline)

    plotObj.show()
    

