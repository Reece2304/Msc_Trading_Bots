from tkinter import *
import numpy as np
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
from matplotlib import dates
from matplotlib.dates import DayLocator, DateFormatter
from matplotlib.figure import Figure
from os import path
import main
import time
import xlsxwriter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)

class MA2022:
    def __init__(self, page):
        self.page = page
        self.page.title("Psxrc6 - MA 2022 Trading Bot") #create gui window
        self.page.geometry("1920x1080")
        self.frame=Frame(page, bg="#9A989A")
        self.frame.place(relx=0, rely=0,relwidth=1,relheight=0.08)

        self.dropDown = StringVar(self.frame)
        self.dropDown.set("Bitcoin") # default value of option menu
        self.menu = OptionMenu(self.frame, self.dropDown, "Bitcoin", "Ethereum", "Litecoin", "LoopRing")
        self.menu.config(font=45)
        self.menu.place(relx=0.7, rely=0.3,relwidth=0.1, relheight=0.4)

        self.button = Button(self.frame, text="Begin Trading", bg="#3CB371", font=70, fg='Black', command=lambda: self.trade(self.dropDown.get()))
        self.button.place(rely=0.22, relx= 0.83, relwidth=0.15, relheight=0.5)

        self.button2 = Button(self.frame, text="Home", bg="#D9381E", font=70, fg='Black', command=lambda: self.Home())
        self.button2.place(rely=0.22, relx= 0.05, relwidth=0.2, relheight=0.5)

        self.label = Label(self.frame, text="Coin To Trade:", bg="yellow", font=70)
        self.label.place(relx=0.585,rely=0.32, relwidth=0.1, relheight=0.3)


        self.label2 = Label(self.frame, text="MA 2022 Trading Bot", bg="yellow", font=70)
        self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

                        #frame to place the stats
        self.stats=Frame(page, bg="#9FF4FD")
        self.stats.place(relx=0, rely=0.68,relwidth=1,relheight=0.5)

        self.dateStat = Label(self.stats, text="Current Date: ", font=70 )
        self.dateStat.place(relx=0.02, rely=0.05)
        self.dateStat2 = Label(self.stats, text = "2020-12-31" , font = 70)
        self.dateStat2.place(relx=0.02, rely=0.15)

        self.currentCoinPrice = Label(self.stats, text = "Current Coin Price: ", font= 70)
        self.currentCoinPrice.place(relx=0.2, rely=0.05)
        self.currentCoinPrice2 = Label(self.stats, text = "10,000" , font = 70)
        self.currentCoinPrice2.place(relx=0.2, rely=0.15)

        self.MA5Price = Label(self.stats, text = "5 day Moving Average: ", font= 70)
        self.MA5Price.place(relx=0.2, rely=0.3)
        self.MA5Price2 = Label(self.stats, text = "0" , font = 70)
        self.MA5Price2.place(relx=0.2, rely=0.4)

        self.MA10Price = Label(self.stats, text = "10 day Moving Average: ", font= 70)
        self.MA10Price.place(relx=0.2, rely=0.5)
        self.MA10Price2 = Label(self.stats, text = "0" , font = 70)
        self.MA10Price2.place(relx=0.32, rely=0.5)

        self.action = Label(self.stats, text = "Bot Action: ", font= 70)
        self.action.place(relx=0.4, rely=0.05)
        self.action2 = Label(self.stats, text = "Buy" , font = 70)
        self.action2.place(relx=0.4, rely=0.15)

        self.profit = Label(self.stats, text = "profit: ", bg='#4EFF43', font= 70)
        self.profit.place(relx=0.6, rely=0.05)
        self.profit2 = Label(self.stats, text = "0" , bg='#4EFF43', font = 70)
        self.profit2.place(relx=0.6, rely=0.15)

        self.pProfit = Label(self.stats, text = "percentage profit: ", bg='#4EFF43', font= 70)
        self.pProfit.place(relx=0.6, rely=0.25)
        self.pProfit2 = Label(self.stats, text = "0%" , bg='#4EFF43', font = 70)
        self.pProfit2.place(relx=0.6, rely=0.3)

        self.holdProfit = Label(self.stats, text = "Hold profit: ", bg='#4EFF43', font= 70)
        self.holdProfit.place(relx=0.8, rely=0.05)
        self.holdProfit2 = Label(self.stats, text = "0" , bg='#4EFF43', font = 70)
        self.holdProfit2.place(relx=0.8, rely=0.15)

        self.holdpProfit = Label(self.stats, text = "Hold percentage profit: ", bg='#4EFF43', font= 70)
        self.holdpProfit.place(relx=0.8, rely=0.25)
        self.holdpProfit2 = Label(self.stats, text = "0%" , bg='#4EFF43', font = 70)
        self.holdpProfit2.place(relx=0.8, rely=0.3)

        self.currentAssetAmount = Label(self.stats, text = "current Asset Amount: ", font= 70)
        self.currentAssetAmount.place(relx=0.05, rely=0.3)
        self.currentAssetAmount2 = Label(self.stats, text = "0" , font = 70)
        self.currentAssetAmount2.place(relx=0.05, rely=0.4)

        self.currentCurrency = Label(self.stats, text = "current Currency: ", font= 70)
        self.currentCurrency.place(relx=0.4, rely=0.3)
        self.currentCurrency2 = Label(self.stats, text = "0" , font = 70)
        self.currentCurrency2.place(relx=0.4, rely=0.4)

    def Home(self):
        root = Tk()
        home = main.HomePage(root)
        self.close_window()
        root.mainloop()

    def close_window(self):
        self.page.destroy()

    def trade(self, coin):
        print(coin)
        if(coin == "Bitcoin"):
            apiRequest = "BTC"
        elif(coin == "Ethereum"):
            apiRequest = "ETH"
        elif(coin == "Litecoin"):
            apiRequest = "LTC"
        elif(coin == "LoopRing"):
            apiRequest = "LRC"

        #try and load the data
        data = 0
        currentPath = path.dirname(__file__)
        filePath = path.abspath(path.join(currentPath, '..')) #add ../ to get the above file path   

        try:
            pd.read_csv(filePath + "/data/training/"+ coin + '2022.csv',sep=';')
            print("file found")
        except:
            print("no file") #if there's no data then call the api request
            url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_' + apiRequest +'_USD/history?period_id=8HRS&time_start=2021-01-01T00:00:00&time_end=2021-12-31T00:00:00&limit=2000'
            #headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
            headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
            r = requests.get(url, headers=headers)
            data = r.json()
            #print(data)

            file = open(filePath + "/data/training/"+ coin + '2022.csv', 'w') #create the new file
            file.write("time_period_start;time_period_end;time_open;time_close;price_open;price_high;price_low;price_close;volume_traded;trades_count;")
            file.write('\n')
            count = 0 
            for dictionary in data:
                count = 0
                for datapoint in dictionary: #loop through the file and add the data points
                    count = count + 1
                    #print(dictionary.get(datapoint))
                    entry = dictionary.get(datapoint)

                    if(count == 1 or count == 2): #remove useless timestamps
                        new = entry.split("T")
                        file.write(str(new[0]) + ';')

                    else:
                        file.write(str(entry)+ ";")
                file.write('\n')
            file.close()
        finally:
            data = pd.read_csv(filePath + "/data/training/"+ coin + '2022.csv',sep=';', usecols=[0,1,4,5,6,7,8,9]) #strip the important data
            df_train = pd.DataFrame(data)

            df_train['5MA'] = df_train['price_close'].rolling(5).mean() # calcualte a 5 moving average
            df_train['10MA'] = df_train['price_close'].rolling(10).mean() # calcualte a 10 moving average

            Pplot = {'Date' : df_train['time_period_start'],
                    'Actual_Price': df_train['price_close'] 
                    } #create a dictionary with dates and close values

            shortMAplot = { 'Date' : df_train['time_period_start'],
                        '5MA' : df_train['5MA']
                     }

            longMAplot = { 'Date' : df_train['time_period_start'],
                        '10MA' : df_train['10MA']
                     }

            Plot2 = pd.DataFrame(shortMAplot, columns = ['Date', '5MA'])
            Plot3 = pd.DataFrame(longMAplot, columns = ['Date', '10MA'])
            Plot = pd.DataFrame(Pplot, columns = ['Date', 'Actual_Price'])
            Plot.set_index("Date", inplace=True)
            Plot2.set_index("Date", inplace=True)
            Plot3.set_index("Date", inplace=True)
            figure = plt.Figure(figsize=(6, 6), dpi=105)
            figure_canvas = FigureCanvasTkAgg(figure, self.page)
            NavigationToolbar2Tk(figure_canvas, self.page)
            axes = figure.add_subplot()
            axes.set_title('Price data from 2021-2022 for: ' + coin)
            axes.set_xlabel('Date')
            axes.set_ylabel('Price in USD')
            axes.set_xticklabels(Pplot['Date'], fontsize=7)

            dates_ = pd.date_range('2021-01-01', date.today()).to_pydatetime()
            axes.xaxis.set_major_locator(dates.DayLocator(interval=26))
            axes.xaxis.set_major_formatter(dates.DateFormatter('%b - %d : %y'))


            Plot.plot(kind='line', legend='true', ax=axes, rot=90, color='blue') #plot the graph
            Plot2.plot(kind='line',ax=axes, color = 'green', rot=90)
            Plot3.plot(kind='line',ax=axes, color = 'red', rot=90)
            figure_canvas.get_tk_widget().place(relx= 0.025, rely= 0.1)

        try:
            pd.read_csv(filePath + "/data/testing/"+ coin + '2022.csv',sep=';')
            print("file found")
        except:
            print("no file") #if there's no data then call the api request
            url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_' + apiRequest +'_USD/history?period_id=8HRS&time_start=2021-01-01T00:00:00&time_end=2021-12-31T00:00:00&limit=2000'
            headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
            #headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
            r = requests.get(url, headers=headers)
            data = r.json()
            print(data)

            file = open(filePath + "/data/testing/"+ coin + '2022.csv', 'w') #create the new file
            file.write("time_period_start;time_period_end;time_open;time_close;price_open;price_high;price_low;price_close;volume_traded;trades_count;")
            file.write('\n')
            count = 0 
            for dictionary in data:
                count = 0
                for datapoint in dictionary: #loop through the file and add the data points
                    count = count + 1
                    #print(dictionary.get(datapoint))
                    entry = dictionary.get(datapoint)

                    if(count == 1 or count == 2): #remove useless timestamps
                        new = entry.split("T")
                        file.write(str(new[0]) + ';')

                    else:
                        file.write(str(entry)+ ";")
                file.write('\n')
            file.close()
        finally:
            data = pd.read_csv(filePath + "/data/testing/"+ coin + '2022.csv',sep=';', usecols=[0,1,4,5,6,7,8,9]) #strip the important data
            df_test = pd.DataFrame(data)

            self.ComputeMA(coin,df_test, df_train['5MA'], df_train['10MA'])

    def ComputeMA(self,coin, data, MA5, MA10):

        data['5MA'] = data['price_close'].rolling(5).mean() # calcualte a 5 moving average
        data['10MA'] = data['price_close'].rolling(10).mean() # calcualte a 10 moving average

        for i in range(0,4):
            data.loc[i, ['5MA']] = MA5.loc[len(MA5.index) - 4 + i] #write the 5MA from the training data into the first 5 values of the training MA

        for i in range(0,9):
            data.loc[i, ['10MA']] = MA10.loc[len(MA10.index) - 9 + i] #write the 10MA from the training data into the first 10 values of the training MA

        data['BuyOrSell'] = np.where(data['5MA'] > data['10MA'],1,0) #when the shorter moving average is higher than the longer moving average then mark this in the system

        Pplot = {'Date' : data['time_period_start'],
                'Actual_Price': data['price_close'] 
                } #create a dictionary with dates and close values

        shortMAplot = { 'Date' : data['time_period_start'],
                    '5MA' : data['5MA']
                 }

        longMAplot = { 'Date' : data['time_period_start'],
                    '10MA' : data['10MA']
                 }

        Plot2 = pd.DataFrame(shortMAplot, columns = ['Date', '5MA'])
        Plot3 = pd.DataFrame(longMAplot, columns = ['Date', '10MA'])
        Plot = pd.DataFrame(Pplot, columns = ['Date', 'Actual_Price'])
        Plot.set_index("Date", inplace=True)
        Plot2.set_index("Date", inplace=True)
        Plot3.set_index("Date", inplace=True)
        figure = plt.Figure(figsize=(6, 6), dpi=105)
        figure_canvas = FigureCanvasTkAgg(figure, self.page)
        axes = figure.add_subplot()
        axes.set_title('MA Price from 2022 for: ' + coin)
        axes.set_xlabel('Date')
        axes.set_ylabel('Price in USD')
        axes.set_xticklabels(data['time_period_start'], fontsize=7)

        dates_ = pd.date_range('2021-12-31', '2022-12-31').to_pydatetime()
        axes.xaxis.set_major_locator(dates.DayLocator(interval=25))
        axes.xaxis.set_major_formatter(dates.DateFormatter('%b - %d - %y'))

        Plot.plot(kind='line', legend='true', ax=axes, rot=90, color='blue') #plot the graph
        Plot2.plot(kind='line',ax=axes, color = 'green', rot=90)
        Plot3.plot(kind='line',ax=axes, color = 'red', rot=90)
        figure_canvas.get_tk_widget().place(relx= 0.5, rely= 0.1)

        self.saveToFile(coin, data) #save the results to an excel file

        self.runTrading(coin,data, len(data.index)) #run the trading algorithm

    def saveToFile(self, coin, data): #save the results of the prediction to an excel file

        workbook = xlsxwriter.Workbook('results/MA/MA2022-' + coin + '-Predictions.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Date', bold)
        worksheet.write('B1', 'Actual_Close_Price', bold)
        worksheet.write('C1', '5MA', bold)
        worksheet.write('D1', '10MA', bold)

        for i in range(len(data.index)): #loop through the data and write them to the specified row and column
            worksheet.write(i+1,0,data['time_period_start'][i]) 
            worksheet.write(i+1,1,data['price_close'][i])
            worksheet.write(i+1,2,data['5MA'][i])
            worksheet.write(i+1,3,data['10MA'][i])

        workbook.close()


    def runTrading(self, coin, data, numberOfDays):

        startingCurrency = 500 #given 500 to start with as a trading amount


        currentAssetAmount = 0

        currentAssetAmount = startingCurrency/data['price_close'][0] #use the starting currency to buy into the coin at the price of the starting day
        Currency = 0

        HoldAmount = currentAssetAmount #compare with a hold for the whole time period

        action = ""
        profit = 0
        holdProfit = 0
        tradingData= []
        for i in range(0, numberOfDays): #run the trading simulation for as many days as the predictions

            currentCoinPrice = data['price_close'][i] #update the coins new daily price at the start
            holdProfit = (HoldAmount * currentCoinPrice) - startingCurrency

            self.dateStat2.config(text = data['time_period_start'][i]) #update the screen so users can see what's happening
            self.currentCoinPrice2.config(text = currentCoinPrice)
            self.profit2.config(text = profit)
            self.action2.config(text = action)
            self.currentCurrency2.config(text = Currency)
            self.currentAssetAmount2.config(text = currentAssetAmount)
            self.pProfit2.config(text = str(round((profit/ startingCurrency) * 100, 2)) + "%") # calculate percentage profit
            self.MA5Price2.config(text= data['5MA'][i])
            self.MA10Price2.config(text= data['10MA'][i])
            self.holdProfit2.config(text=holdProfit)
            self.holdpProfit2.config(text= str(round((holdProfit/ startingCurrency) * 100, 2)) + "%")
            self.page.update()
            #time.sleep(0.5)

            
            if i < numberOfDays - 2:
                if data['BuyOrSell'][i+2] == 1: #check the buying signals (if the 5 moving average passes over the 10 day moving average, 5 > 10)
                    if(Currency!= 0 ): #if the bot has currency
                        action = "Buying"
                        Currency, currentAssetAmount = self.buyCoins(currentCoinPrice, Currency, currentAssetAmount)
                        profit = (currentAssetAmount * currentCoinPrice) - startingCurrency

                    else:
                        action ="Holding"
                        profit = (currentAssetAmount * currentCoinPrice) - startingCurrency

                elif data['BuyOrSell'][i+2] == 0:#check the selling signals (if the 10 moving average passes over the 5 day moving average - 10 > 5)
                    if(currentAssetAmount != 0): #if there are coins to sell
                        action = "Selling"
                        Currency, currentAssetAmount = self.sellCoins(currentCoinPrice, Currency, currentAssetAmount)
                        profit = Currency - startingCurrency
                    else:
                        action ="Waiting"
                        profit = Currency - startingCurrency

                tradingData.append([data['time_period_start'][i], currentCoinPrice, action, Currency, currentAssetAmount, profit, holdProfit] )

        #at the end of the run if there are any coins left then sell them
        if(currentAssetAmount!= 0):
            Currency, currentAssetAmount = self.sellCoins(currentCoinPrice, Currency, currentAssetAmount)

        print("Final currency amount: " + str(Currency))
        print("Profit made: " + str(Currency - startingCurrency))

        workbook = xlsxwriter.Workbook('results/MA/MA2022-' + coin + '-TradingBot.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'Date', bold)
        worksheet.write('B1', 'Current Coin Price', bold)
        worksheet.write('C1', 'action', bold)
        worksheet.write('D1', 'Current Funds', bold)
        worksheet.write('E1', 'current AssetAmount', bold)
        worksheet.write('F1', 'Profit', bold)
        worksheet.write('G1', 'HoldProfit', bold)

        for i in range(numberOfDays-2): #loop through the data and write them to the specified row and column
            worksheet.write(i+1,0, tradingData[i][0] ) 
            worksheet.write(i+1,1,tradingData[i][1])
            worksheet.write(i+1,2, tradingData[i][2])
            worksheet.write(i+1,3, tradingData[i][3] ) 
            worksheet.write(i+1,4,tradingData[i][4])
            worksheet.write(i+1,5, tradingData[i][5])
            worksheet.write(i+1,6, tradingData[i][6])

        workbook.close()


    def sellCoins(self, currentCoinPrice, startingCurrency, currentAssetAmount):
        startingCurrency = currentAssetAmount * currentCoinPrice #the new amount of funds the bot has is the amount of assest * current price of the coin
        currentAssetAmount = 0 #set asset amount to 0
        return startingCurrency, currentAssetAmount

    def buyCoins(self, currentCoinPrice, startingCurrency, currentAssetAmount):
        currentAssetAmount = startingCurrency/currentCoinPrice #the new assest amount is current funds / current coin price
        startingCurrency = 0
        return startingCurrency, currentAssetAmount