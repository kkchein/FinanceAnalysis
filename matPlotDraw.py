# -*- coding: utf-8 -*-
"""
.. module:: matPlotDraw
    :synopsis: draw finance data with matplotlib
.. author: K.K.Chien
"""
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import financeData

class MPLTDrawError(Exception): pass

class MPLTDraw:
    """This class process finance data and draw in matplotlib
    
    This class process finance data and draw in matplotlib

    Attributes:
        None
    """
    def __init__ (self):
        self.__data=[]
    def addLine (self, iline):
        """add a FinanceLine into plot

        add a FinanceLine into plot

        Args:
            iline: input FinanceLine

        Returns:
            None

        Raise:
            MPLTDrawError: An error occured adding line.
        """
        if not isinstance(iline, financeData.FinanceLine):
            raise MPLTDrawError("{0:s} is not a FinanceDataLine class"
                                .format(str(iline)))
        self.__data.append(iline)
    def show (self):
        """show matplotlib result

        show matplotlib result

        Args:
            None

        Returns:
            None

        Raise:
            MPLTDrawError: An error occured adding line.
        """
        fig=plt.figure()
        ax1=plt.subplot2grid((1,1), (0,0), rowspan=1, colspan=1)
        for item in self.__data:
            ax1.plot(item.getTimeList(),item.getValueList(),linewidth=1.5)
        ax1.grid(True)
        #plt.ylabel(self.ylabel)
        #plt.legend(loc=3,prop={'size':7},fancybox=True)
        #ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%y%m%d'))
        #for label in ax1.xaxis.get_ticklabels():
        #    label.set_rotation(45)

        plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, 
                            wspace=.20, hspace=0)
        #plt.xlabel(self.xlable)
        #plt.suptitle('')
        #plt.setp(ax1.get_xticklabels(), visible=False)
        plt.show()

if __name__=="__main__":
    plotObj=MPLTDraw()
    ttt=financeData.FinanceDataSet()
    ttt.getDataFromFile("./history/Index_TaiwanWI_google_1_day.csv")
    print(str(ttt[1]))
    ttt2=ttt[:]
    plotObj.addLine(ttt2.closeValue)
    plotObj.show()
    

