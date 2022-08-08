from tkinter import *
import numpy as np
import os
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
from matplotlib import dates
from matplotlib.dates import DayLocator, DateFormatter
from matplotlib.figure import Figure
from os import path
import main
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import xlsxwriter
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import f1_score

class SVM2018:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - SVM 2018 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="SVM 2018 Trading Bot", bg="yellow", font=70)
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

		self.predictedCoinPrice = Label(self.stats, text = "Predicted Price: ", font= 70)
		self.predictedCoinPrice.place(relx=0.2, rely=0.3)
		self.predictedCoinPrice2 = Label(self.stats, text = "0" , font = 70)
		self.predictedCoinPrice2.place(relx=0.2, rely=0.4)

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
			pd.read_csv(filePath + "/data/training/"+ coin + '2018.csv',sep=';')
			print("file found")
		except:
			print("no file") #if there's no data then call the api request
			url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_' + apiRequest +'_USD/history?period_id=1DAY&time_start=2018-01-01T00:00:00&time_end=2020-12-31T00:00:00&limit=2000'
			#headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
			headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
			r = requests.get(url, headers=headers)
			data = r.json()
			#print(data)

			file = open(filePath + "/data/training/"+ coin + '2018.csv', 'w') #create the new file
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
			data = pd.read_csv(filePath + "/data/training/"+ coin + '2018.csv',sep=';', usecols=[0,1,4,5,6,7,8,9]) #strip the important data
			df_train = pd.DataFrame(data)
			x_train = df_train[['price_open', 'price_high', 'price_low', 'volume_traded', 'trades_count']] #Test on open, high, low, volume and trade count values
			#print(x_train)
			y_train = [row[5] for index, row in df_train.iterrows()]#predict the close value of each day
			#print(data)
			plot = {'Date' : [row[0] for index , row in df_train.iterrows()],
					 'Price': [row[5] for index , row in df_train.iterrows() ] 
					 } #create a dictionary with dates and close values

			dfPlot = pd.DataFrame(plot, columns = ['Date', 'Price'])
			dfPlot.set_index("Date", inplace=True)
			figure = plt.Figure(figsize=(6, 6), dpi=105)
			figure_canvas = FigureCanvasTkAgg(figure, self.page)
			NavigationToolbar2Tk(figure_canvas, self.page)
			axes = figure.add_subplot()
			axes.set_title('Price data from 2018-2020 for: ' + coin)
			axes.set_xlabel('Date')
			axes.set_ylabel('Price in USD')
			axes.set_xticklabels(plot['Date'], fontsize=7)

			dates_ = pd.date_range('2018-01-01', '2020-12-31').to_pydatetime()
			axes.xaxis.set_major_locator(dates.DayLocator(interval=25))
			axes.xaxis.set_major_formatter(dates.DateFormatter('%b - %d - %y'))


			dfPlot.plot(kind='line', legend='true', ax=axes, rot=90) #plot the graph
			figure_canvas.get_tk_widget().place(relx= 0.025, rely= 0.1)

			
		try:
			pd.read_csv(filePath + "/data/testing/"+ coin + '2018.csv',sep=';')
			print("file found")
		except:
			print("no file") #if there's no data then call the api request
			url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_' + apiRequest +'_USD/history?period_id=1DAY&time_start=2020-12-31T00:00:00&time_end=2021-12-31T00:00:00&limit=400' #get training data
			headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
			#headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
			r = requests.get(url, headers=headers)
			data = r.json()
			print(data)

			file = open(filePath + "/data/testing/"+ coin + '2018.csv', 'w') #create the new file
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
			data = pd.read_csv(filePath + "/data/testing/"+ coin + '2018.csv',sep=';', usecols=[0,1,4,5,6,7,8,9]) #strip the important data
			df_test = pd.DataFrame(data)
			x_test_dates = df_test[['time_period_start']]
			x_test = df_test[['price_open', 'price_high', 'price_low', 'volume_traded', 'trades_count']] #Test on open, high, low, volume and trade count values
			# print(x_test)
			y_test = [row[5] for index, row in df_test.iterrows()]#predict the close value of each day

			self.CreateSVM(coin, x_train, x_test, y_train, y_test, x_test_dates)


	def CreateSVM(self, coin, x_train, x_test, y_train, y_test, x_test_dates):
		StdS_X = StandardScaler()
		StdS_y = StandardScaler()
		x_train = StdS_X.fit_transform(x_train)
		y_train = np.array(y_train)
		y_train = StdS_y.fit_transform(y_train.reshape(-1,1)) #normalise the test and training data with preprocessing

		x_test = StdS_X.fit_transform(x_test)
		y_test_normalised = np.array(y_test)
		y_test_normalised = StdS_y.fit_transform(y_test_normalised.reshape(-1,1))


		rbf = SVR(kernel="rbf", C=1e4, gamma=0.00001) #create the model with some parameters
		rbf.fit(x_train, y_train) #train the model
		predictions = rbf.predict(x_test) #get a list of predictions using the test data
		confidence = rbf.score(x_test, y_test_normalised) #confidence score 
		print(confidence) 
		print(predictions)

		#plot the predictions and display to the user
		Pplot = {'Date' : x_test_dates['time_period_start'],
				'Actual_Price': y_test 
				} #create a dictionary with dates and close values

		Pplot2 = { 'Date' : x_test_dates['time_period_start'],
					'Predicted_Price' : StdS_y.inverse_transform(predictions)
				 }
				 
		predictionPlot2 = pd.DataFrame(Pplot2, columns = ['Date', 'Predicted_Price'])
		predictionPlot = pd.DataFrame(Pplot, columns = ['Date', 'Actual_Price'])
		predictionPlot.set_index("Date", inplace=True)
		predictionPlot2.set_index("Date", inplace=True)
		figure = plt.Figure(figsize=(6, 6), dpi=105)
		figure_canvas = FigureCanvasTkAgg(figure, self.page)
		axes = figure.add_subplot()
		axes.set_title('Prediction Price from 2020-2021 for: ' + coin)
		axes.set_xlabel('Date')
		axes.set_ylabel('Price in USD')
		axes.set_xticklabels(x_test_dates['time_period_start'], fontsize=7)

		dates_ = pd.date_range('2020-12-31', '2021-12-31').to_pydatetime()
		axes.xaxis.set_major_locator(dates.DayLocator(interval=25))
		axes.xaxis.set_major_formatter(dates.DateFormatter('%b - %d - %y'))

		predictionPlot.plot(kind='line', legend='true', ax=axes, rot=90, color='magenta') #plot the graph

		predictionPlot2.plot(kind='line',ax=axes, color = 'green', rot=90)
		figure_canvas.get_tk_widget().place(relx= 0.5, rely= 0.1)

		#compute error values 
		mse = mean_squared_error(y_test_normalised,predictions)
		rmse = mean_squared_error(y_test_normalised,predictions, squared=False)
		mae = mean_absolute_error(y_test_normalised,predictions)

		print("mse: " + str(mse))
		print("rmse: " + str(rmse))
		print("mae: " + str(mae))

		predictions = StdS_y.inverse_transform(predictions) #inverse the normalisation to get the predicted price of the coin

		self.saveToFile(coin, predictions, x_test_dates, y_test, mse,rmse,mae, confidence) #save the results to an excel file

		self.runTrading(coin, predictions, y_test, len(predictions), x_test_dates) #try and trade a profit using the predictions


	def saveToFile(self, coin, predictions, x, y, mse, rmse, mae, confidence): #save the results of the prediction to an excel file

		workbook = xlsxwriter.Workbook('results/SVM/SVM2018-' + coin + '-Predictions.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.set_column('A:A', 25)
		worksheet.set_column('B:B', 15)
		worksheet.set_column('C:C', 15)
		bold = workbook.add_format({'bold': True})
		worksheet.write('A1', 'Date', bold)
		worksheet.write('B1', 'Actual_Close_Price', bold)
		worksheet.write('C1', 'Predicted_Close_Price', bold)

		for i in range(len(y)): #loop through the data and write them to the specified row and column
			worksheet.write(i+1,0,x['time_period_start'][i]) 
			worksheet.write(i+1,1,y[i])
			worksheet.write(i+1,2,predictions[i])

		worksheet.write(i+2,0,"mse")
		worksheet.write(i+2,1,mse)

		worksheet.write(i+3,0,"rmse")
		worksheet.write(i+3,1,rmse)

		worksheet.write(i+4,0,"mae")
		worksheet.write(i+4,1,mae)

		worksheet.write(i+5, 0, "confidence")
		worksheet.write(i+5, 1, confidence)

		workbook.close()

	def runTrading(self, coin, predictions, y_test, numberOfDays,x_test_dates):

		startingCurrency = 500 #given 500 to start with as a trading amount


		currentAssetAmount = 0

		currentAssetAmount = startingCurrency/y_test[0] #use the starting currency to buy into the coin at the price of the starting day
		Currency = 0

		HoldAmount = currentAssetAmount #compare with a hold for the whole time period

		action = ""
		profit = 0
		holdProfit = 0
		data= []
		for i in range(0, numberOfDays): #run the trading simulation for as many days as the predictions


			currentCoinPrice = y_test[i] #update the coins new daily price at the start
			holdProfit = (HoldAmount * currentCoinPrice) - startingCurrency

			self.dateStat2.config(text = x_test_dates.iloc[i,0]) #update the screen so users can see what's happening
			self.currentCoinPrice2.config(text = currentCoinPrice)
			self.profit2.config(text = profit)
			self.action2.config(text = action)
			self.currentCurrency2.config(text = Currency)
			self.currentAssetAmount2.config(text = currentAssetAmount)
			self.pProfit2.config(text = str(round((profit/ startingCurrency) * 100, 2)) + "%") # calculate percentage profit
			self.predictedCoinPrice2.config(text= predictions[i])
			self.holdProfit2.config(text=holdProfit)
			self.holdpProfit2.config(text= str(round((holdProfit/ startingCurrency) * 100, 2)) + "%")
			self.page.update()
			time.sleep(0.5)

			
			if i < numberOfDays - 1:
				if predictions[i+1] > predictions[i]: #price predicted higher tomorrow
					if(Currency!= 0 ): #if the bot has currency
						action = "Buying"
						Currency, currentAssetAmount = self.buyCoins(currentCoinPrice, Currency, currentAssetAmount)
						profit = (currentAssetAmount * currentCoinPrice) - startingCurrency

					else:
						action ="Holding"
						profit = (currentAssetAmount * currentCoinPrice) - startingCurrency

				elif predictions[i+1] < predictions[i]: #price predicted lower tomorrow
					if(currentAssetAmount != 0): #if there are coins to sell
						action = "Selling"
						Currency, currentAssetAmount = self.sellCoins(currentCoinPrice, Currency, currentAssetAmount)
						profit = Currency - startingCurrency
					else:
						action ="Waiting"
						profit = Currency - startingCurrency

				data.append([x_test_dates.iloc[i,0], currentCoinPrice, action, Currency, currentAssetAmount, profit, holdProfit] )

		#at the end of the run if there are any coins left then sell them
		if(currentAssetAmount!= 0):
			Currency, currentAssetAmount = self.sellCoins(currentCoinPrice, Currency, currentAssetAmount)

		print("Final currency amount: " + str(Currency))
		print("Profit made: " + str(Currency - startingCurrency))

		workbook = xlsxwriter.Workbook('results/SVM/SVM2018-' + coin + '-TradingBot.xlsx')
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

		for i in range(numberOfDays-1): #loop through the data and write them to the specified row and column
			worksheet.write(i+1,0, data[i][0] ) 
			worksheet.write(i+1,1,data[i][1])
			worksheet.write(i+1,2, data[i][2])
			worksheet.write(i+1,3, data[i][3] ) 
			worksheet.write(i+1,4,data[i][4])
			worksheet.write(i+1,5, data[i][5])
			worksheet.write(i+1,6, data[i][6])

		workbook.close()


	def sellCoins(self, currentCoinPrice, startingCurrency, currentAssetAmount):
		startingCurrency = currentAssetAmount * currentCoinPrice #the new amount of funds the bot has is the amount of assest * current price of the coin
		currentAssetAmount = 0 #set asset amount to 0
		return startingCurrency, currentAssetAmount

	def buyCoins(self, currentCoinPrice, startingCurrency, currentAssetAmount):
		currentAssetAmount = startingCurrency/currentCoinPrice #the new assest amount is current funds / current coin price
		startingCurrency = 0
		return startingCurrency, currentAssetAmount
