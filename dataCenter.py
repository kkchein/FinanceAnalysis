# -*- coding: utf-8 -*-
"""
.. module:: dataCenter
    :synopsis: A module help to get finance data from internet or file.
.. author: K.K.Chien
"""
import datetime
import urllib.parse
import urllib.request
import re
import time
import configparser
import sys
import financeData

class DataCenterConfigError(Exception): pass
class DataCenterConfigCollectError(Exception): pass
class DataCenterError(Exception): pass
class DataCenterFileNotExist(DataCenterError): pass

class DataCenterConfig():
    """This class contain DataCenter configuration.
    
    This class contain DataCenter configuration.

    Attributes:
        Name: datacenter reconized name
        dataSource: internet data source name
        symbol: interet finance data symbol
        timeType: The data time unit.
        period: The data period.
        historyDir: The directory keeps data history file.
    """
    dataSourceDict={"yahoo":"yahoo",
                    "google":"google"}
    def __init__ (self, Name, dataSource, symbol, timeType="day", period=1,
                  historyDir="./history"):
        """DataCenterConfig initial function

        DataCenterConfig initial function.

        Args:
            Name: a reconized string for the config
            dataSource: the internet data source. the data source are listed in
                      dictionary DataCenterConfig.dataSourceDict
            symbol: the finance data sysmbol. This symbol is used by internet
                  source, like Yahoo or Google.
            timeType: The data time unit. Default value is "day".
                    The timeType are listed in
                    financeData.FinanceDataSet.timeTypeDict.
            period: the data period. Default value is 1.
            historyDir: The directory keeps data history file.
                      Default value is "./history".

        Returns:
            None

        Raise:
            DataCenterConfigError: An error occured intialing instance.
        """
        if not isinstance(Name, str):
            raise DataCenterConfigError("{0:s} is not a string"
                                        .format(str(Name)))
        if dataSource not in DataCenterConfig.dataSourceDict.values():
            raise DataCenterConfigError("{0:s} is not a defined data source."
                                        .format(str(dataSource)))
        if not isinstance(symbol, str):
            raise DataCenterConfigError("{0:s} is not a string"
                                        .format(str(symbol)))
        if timeType not in financeData.FinanceDataSet.timeTypeDict.values():
            raise DataCenterConfig("{0:s} is not a defined time type."
                                   .format(str(timeType)))
        if not isinstance(period, int):
            raise DataCenterConfig("{0:s} is not a integer."
                                   .format(str(period)))
        if not isinstance(historyDir, str):
            raise DataCenterConfigError("{0:s} is not a string"
                                        .format(str(historyDir)))
        self.Name=Name
        self.dataSource=dataSource
        self.symbol=symbol
        self.timeType=timeType
        self.period=period
        self.historyDir=historyDir
    def __str__ (self):
        """DataCenterConfig string function

        DataCenterConfig string function.

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        #return str("ConfigName : {0:s}\nDataSource : {1:s}\nSymbol : "
        #           "{2:s}\nTimeType : {3:s}\nPeriod : {4:d}\nHistoryDir : {5:s}"
        #           .format(self.Name,
        #                   self.dataSource,
        #                   self.symbol,
        #                   self.timeType,
        #                   self.period,
        #                   self.historyDir))
        return str("ConfigName : %s\nDataSource : %s\nSymbol : "
                   "%s\nTimeType : %s\nPeriod : %d\nHistoryDir : %s"
                   %(self.Name,
                           self.dataSource,
                           self.symbol,
                           self.timeType,
                           self.period,
                           self.historyDir))
    def fileNameStr (self):
        """Generate filename string for history file.

        Generate filename string.

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        return "{0:s}_{1:s}_{2:s}_{3:s}.csv".format(self.Name, self.dataSource, str(self.period), self.timeType)
class DataCenterCofigCollect():
    """This class contain a list of DataCenterConfig.
    
    The list container for DataCenterConfig.

    Attributes:
    """
    def __init__ (self):
        """Initial function.

        Initial function.

        Args:
            None

        Returns:
            None

        Raise:
            None
        """
        self.__configs=[]
    def __getitem__ (self, k):
        return self.__configs[k]
    def __len__ (self):
        return len(self.__configs)
    def addConfig (self, iconfig):
        """Add a DataCenterConfig into list

        Add a DataCenterConfig into list

        Args:
            iconfig: datacenter configuration. It must be a DataCenterConfig class.

        Returns:
            None

        Raise:
            DataCenterConfigCollectError: An error occured adding the configuration.
        """
        if not isinstance(iconfig,DataCenterConfig):
            raise DataCenterConfigCollectError("{0:s} is not a DataCenterConfig class".format(iconfig))
        for item in self.__configs:
            if iconfig.Name==item.Name:
                raise DataCenterConfigCollectError("Config section name {0:s} is repeated".format(iconfig.Name))
        self.__configs.append(iconfig)
    def saveToFile (self, fileName):
        """Save all configuration into a ini file.

        Save all configuration into a ini file.

        Args:
            fileName: ini filename

        Returns:
            None

        Raise:
            DataCenterConfigCollectError: An error occured saving the
                                        configuration.
        """
        if not isinstance(fileName,str):
            raise DataCenterConfigCollectError("{0:s} is not a string"
                                               .format(str(fileName)))
        for item in self.__configs:
            config=configparser.ConfigParser()
            config[item.Name]={}
            config[item.Name]["dataSource"]=item.dataSource
            config[item.Name]["symbol"]=item.symbol
            config[item.Name]["timeType"]=item.timeType
            config[item.Name]["period"]=str(item.period)
            config[item.Name]["historyDir"]=item.historyDir
        with open(fileName,"w") as configFile:
            config.write(configFile)
    def loadFromFile (self, fileName):
        """Load datacenter configuration from ini file.

        Load datacenter configuration from ini file.

        Args:
            fileName: ini filename

        Returns:
            None

        Raise:
            DataCenterConfigCollectError: An error occured saving the
                                        configuration.
        """
        if not isinstance(fileName,str):
            raise DataCenterConfigCollectError("{0:s} is not a string"
                                               .format(str(fileName)))
        config=configparser.ConfigParser()
        config.read(fileName)
        for name in config.sections():
            configtemp=DataCenterConfig(name,
                                        config[name]["dataSource"],
                                        config[name]["symbol"],
                                        config[name]["timeType"],
                                        int(config[name]["period"]),
                                        config[name]["historyDir"])
            self.__configs.append(configtemp)
class DataCenter():
    """This class manipulate finance data get and write.
    
    This class manipulate finance data get and write.
    The object will use DataCenterConfig information to manipulate data.

    Attributes:
        None
    """
    def __init__ (self):
        pass
    def getDataFromFile (self, dataConfig):
        """Get finance data from file.

        This function can get data from file with DataCenterConfig.

        Args:
            dataConfig: must be DataCenterConfig class.
                      This arg can give file information to get data.

        Returns:
            return a class financeData.FinanceDataSet.

        Raise:
            None
        """
        if  isinstance(dataConfig,DataCenterConfig):
            strtemp=dataConfig.historyDir+"/"+dataConfig.fileNameStr()
            result=financeData.FinanceDataSet(None, dataConfig.timeType,
                                              dataConfig.period)
        else:
            raise DataCenterFileNotExist("{0:s} is not a file name string or"
                                         " DataCenterConfig class."
                                         .format(str(dataFile)))
        try:
            result.getDataFromFile(strtemp)
        except financeData.FinanceDataSetFileNotExist:
            pass
        return result     
    def saveDataToFile (self, config, inputdata):
        """save finance data to file.

        This function can save data to file with DataCenterConfig.

        Args:
            dataConfig: must be a DataCenterConfig class.
                      This arg can give file information to save data.
            inputdata: must be a financeData.FinanceDataSet class.
                     The finace data set.

        Returns:
            return a class financeData.FinanceDataSet.

        Raise:
            None
        """
        if not isinstance(config, DataCenterConfig):
            raise DataCenter("{0:s} is not a DataCenterConfig class.".format(str(config)))
        if not isinstance(inputdata, financeData.FinanceDataSet):
            raise DataCenter("{0:s} is not a FinanceDataSet class.".format(str(inputdata)))
        strtemp=config.historyDir+"/"+config.fileNameStr()
        inputdata.saveDataToFile(strtemp)
    def getHistoryDataFromInternet (self, setting, startTime=datetime.datetime(1976,1,1)):
        """get financedata from internet

        This function can get data from internet with DataCenterConfig.

        Args:
            setting: must be a DataCenterConfig class.
                      This arg can give file information to save data.
            startTime: must be a datetime.datetime class.
                     The start time to get data.

        Returns:
            None

        Raise:
            None
        """
        if not isinstance(setting, DataCenterConfig):
            raise DataCenterError("{0:s} is not a dataCenterData class.".format(str(setting)))
        if not isinstance(startTime, datetime.datetime):
            raise DataCenterError("{0:s} is not a datetime class.".format(str(setting)))
        if setting.dataSource==DataCenterConfig.dataSourceDict["google"]:
            return self.__getHistoryDataFromGoogle(setting, startTime)
        if setting.dataSource==DataCenterConfig.dataSourceDict["yahoo"]:
            return self.__getHistoryDataFromYahoo(setting, startTime)
        else:
            raise DataCenterConfigError("Unknown data source")
    def __getHistoryDataFromYahoo (self, setting, startTime=datetime.datetime(1976,1,1)):
        """get financedata from Yahoo finance

        This function can get data from Yahoo finance with DataCenterConfig.

        Args:
            setting: must be a DataCenterConfig class.
                      This arg can give file information to save data.
            startTime: must be a datetime.datetime class.
                     The start time to get data.

        Returns:
            None

        Raise:
            None
        """
        result=financeData.FinanceDataSet(None, setting.timeType, setting.period)
        tempset=financeData.FinanceDataSet(None, setting.timeType, setting.period)
        if setting.timeType==financeData.FinanceDataSet.timeTypeDict["day"]:
            now=datetime.datetime.now()
            diftime=now-startTime
            if diftime.seconds>0:
                timetemp=diftime.days+1
            else:
                timetemp=diftime.days
            if timetemp>300:
                timetemp=300
            urlStr=str('http://chartapi.finance.yahoo.com/instrument/1.0/{0:s}/'
                       'chartdata;type=quote;range={1:d}d/csv'
                       .format(setting.symbol, timetemp))
            print(urlStr)
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Chrome')]
            content = opener.open(urlStr).read().decode("utf-8").split('\n')
            for icount in range(len(content)):
                ltemp=content[icount].split(',')
                try:
                    dt=datetime.datetime.fromtimestamp(int(ltemp[0]))
                except ValueError:
                    continue
                try:
                    openValue=float(ltemp[1].replace(",",""))
                except ValueError:
                    continue
                try:
                    highValue=float(ltemp[2].replace(",",""))
                except ValueError:
                    continue
                try:
                    lowValue=float(ltemp[3].replace(",",""))
                except ValueError:
                    continue
                try:
                    closeValue=float(ltemp[4].replace(",",""))
                except ValueError:
                    continue
                try:
                    volValue=float(ltemp[5].replace(",",""))
                except ValueError:
                    continue
                except urllib.error.HTTPError:
                    pass
                tempset.add(dt,openValue,highValue,lowValue,closeValue,volValue)
            result=tempset
            return result
    def __getHistoryDataFromGoogle (self, setting, startTime=datetime.datetime(1976,1,1)):
        """get financedata from Google finance

        This function can get data from Google finance with DataCenterConfig.

        Args:
            setting: must be a DataCenterConfig class.
                      This arg can give file information to save data.
            startTime: must be a datetime.datetime class.
                     The start time to get data.

        Returns:
            None

        Raise:
            DataCenterError: an error occured getting data from Google
        """
        result=financeData.FinanceDataSet(None, setting.timeType, setting.period)
        displayNum=30
        if setting.timeType==financeData.FinanceDataSet.timeTypeDict["day"]:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Chrome')]
            #urlstr=str("https://www.google.com/finance/historical?q={0:s}"
            #        "&startdate={1:s}&start=0&num={2:d}"
            #        .format(setting.symbol,
            #                datetime.datetime.strftime(startTime, "%m/%d/%Y"),
            #                displayNum))
            urlstr=str("https://www.google.com/finance/historical?q=%s"
                       "&startdate=%s&start=0&num=%d"
                       % (setting.symbol,
                           datetime.datetime.strftime(startTime, "%m/%d/%Y"),
                           displayNum))
            content = opener.open(urlstr).read()
            totalSizeStr=r'google\.finance\.applyPagination\(\s+\d+,\s+\d+,\s+(\d+),\s+'
            reg_row_size =  re.compile( totalSizeStr )
            match_r_sz = reg_row_size.search( content.decode("utf-8") )
            if not match_r_sz:
                raise DataCenterError("{0:s} doesn't have data.".format(urlstr))
            row_size = int (match_r_sz.groups()[0])
            if row_size%displayNum!=0:
                pageSize=int(row_size/displayNum)+1
            else:
                pageSize=int(row_size/displayNum)
            dataStr = r'<td class="lm">(.+)' +  \
                '\s<td class="rgt">(.+)' + \
                '\s<td class="rgt">(.+)' + \
                '\s<td class="rgt">(.+)' + \
                '\s<td class="rgt">(.+)' + \
                '\s<td class="rgt rm">(.+)'
            reg_price = re.compile( dataStr )
            for icount in range(pageSize):
                urlstr="https://www.google.com/finance/historical?q={0:s}&startdate={1:s}&start={2:d}&num={3:d}".format(
                    setting.symbol, datetime.datetime.strftime(startTime, "%m/%d/%Y"), icount*displayNum, displayNum)
                content = opener.open(urlstr).read()
                stock_data = reg_price.findall( content.decode("utf-8") )
                for jcount in range(len(stock_data)):
                    dt = datetime.datetime.fromtimestamp(time.mktime(time.strptime(stock_data[jcount][0], "%b %d, %Y")))
                    try:
                        openValue=float(stock_data[jcount][1].replace(",",""))
                    except ValueError:
                        openValue=0.0
                    try:
                        highValue=float(stock_data[jcount][2].replace(",",""))
                    except ValueError:
                        highValue=0.0
                    try:
                        lowValue=float(stock_data[jcount][3].replace(",",""))
                    except ValueError:
                        lowValue=0.0
                    try:
                        closeValue=float(stock_data[jcount][4].replace(",",""))
                    except ValueError:
                        closeValue=0.0
                    try:
                        volValue=float(stock_data[jcount][5].replace(",",""))
                    except ValueError:
                        volValue=0.0
                    try:
                        result.add(dt,openValue,highValue,lowValue,closeValue,volValue)
                    except financeData.FinanceDataError as e:
                        print(str(e))
            return result
        else:
            raise DataCenterConfigError("data from {0:s} doesn't support {1:s}".format(setting.dataSource, setting.timeType))

if __name__=="__main__":
    ddc=DataCenterCofigCollect()
    ddc.loadFromFile("dataCenter.ini")
    dcenter=DataCenter()
    for item in ddc:
        print(item)
        print("Processing",":",item.Name)
        sys.stdout.flush()
        print("    Get From File",":",item.historyDir+"/"+item.fileNameStr())
        sys.stdout.flush()
        filedata=dcenter.getDataFromFile(item)
        #continue
        print("    Get From Internet",":",item.dataSource)
        sys.stdout.flush()
        if item.timeType==financeData.FinanceDataSet.timeTypeDict["day"]:
            newData=dcenter.getHistoryDataFromInternet(item,filedata.getLastTime()+datetime.timedelta(days=1))
        print("    There are {0:d} new items.".format(len(newData)))
        sys.stdout.flush()
        filedata.addset(newData)
        dcenter.saveDataToFile(item,filedata)

