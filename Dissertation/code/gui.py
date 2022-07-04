# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 09:59:17 2022

@author: reece
"""

from tkinter import *
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class HomePage:
	def __init__(self, home):
		self.home = home
		self.home.title("Psxrc6 - Crypto Trading Bot") #create gui window
		self.home.geometry("1920x1080")
		self.background_image = PhotoImage(file='imgs/background.png') #import background image
		self.background_label = Label(home, image=self.background_image)
		self.background_label.place(x=0,y=0,relwidth=1,relheight=1)
		self.frame=Frame(home, bg="#9A989A")
		self.frame.place(relx=0.25, rely=0.15,relwidth=0.5,relheight=0.7)

		self.dropDown = StringVar(self.frame)
		self.dropDown.set("2018-2021") # default value of option menu
		self.menu = OptionMenu(self.frame, self.dropDown, "2018-2021", "2021-2022", "Live Run")
		self.menu.config(font=65)
		self.menu.place(relx=0.25, rely=0.05,relwidth=0.5, relheight=0.05)

		self.button = Button(self.frame, text="Support Vector Machine Bot", bg="#8800FF", font=70, fg='white', command=lambda: self.ButtonClicked("SVM")) #setup buttons that when clicked open up a new page
		self.button2 = Button(self.frame, text="Artificial Neural Network Bot", bg="#8800FF", font=70, fg='white', command=lambda: self.ButtonClicked("ANN"))
		self.button3 = Button(self.frame, text="Moving Average Bot", bg="#D9381E", font=70, fg='white', command=lambda: self.ButtonClicked("MA"))
		self.button4 = Button(self.frame, text="Relative Strength Index Bot", bg="#D9381E", font=70, fg='white', command=lambda: self.ButtonClicked("RSI"))
		self.label = Label(self.frame, text="Time period:", bg="yellow", font=70)
		self.label2 = Label(self.frame, text="Click a bot Below", bg="green", font=70)

		self.label.place(relx=0.01,rely=0.055, relwidth=0.2) #set the placement of the labels and buttons on the page
		self.label2.place(relx=0.35,rely=0.2, relwidth=0.3)
		self.button.place(rely=0.3, relx= 0.35, relwidth=0.3, relheight=0.08)
		self.button2.place(rely=0.4, relx= 0.35, relwidth=0.3, relheight=0.08)
		self.button3.place(rely=0.5, relx= 0.35, relwidth=0.3, relheight=0.08)
		self.button4.place(rely=0.6, relx= 0.35, relwidth=0.3, relheight=0.08)

	def ButtonClicked(self,clicked): #when a bot button is clicked...
		print(self.dropDown.get() + " " + clicked)
		root = Tk() #create a new page
		if(clicked =="SVM"):
			if(self.dropDown.get() == "2018-2021"):
				page = SVM2018(root) #set the new page as one of the bot classes
			if(self.dropDown.get() == "2021-2022"):
				page = SVM2022(root)
			if(self.dropDown.get() == "Live Run"):
				page = SVMLive(root)

		elif(clicked == "ANN"):
			if(self.dropDown.get() == "2018-2021"):
				page = ANN2018(root)
			if(self.dropDown.get() == "2021-2022"):
				page = ANN2022(root)
			if(self.dropDown.get() == "Live Run"):
				page = ANNLive(root)

		elif(clicked == "MA"):
			if(self.dropDown.get() == "2018-2021"):
				page = MA2018(root)
			if(self.dropDown.get() == "2021-2022"):
				page = MA2022(root)
			if(self.dropDown.get() == "Live Run"):
				page = MALive(root)

		elif(clicked == "RSI"):
			if(self.dropDown.get() == "2018-2021"):
				page = RSI2018(root)
			if(self.dropDown.get() == "2021-2022"):
				page = RSI2022(root)
			if(self.dropDown.get() == "Live Run"):
				page = RSILive(root)

		self.close_window() #close the current window
		root.mainloop() #open up the new window

	def close_window(self):
		self.home.destroy()


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

	def Home(self):
		root = Tk()
		home = HomePage(root)
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
		try:
			pd.read_csv("./data/"+ coin + '2018.csv',sep=';')
			print("file found")
		except:
			print("no file") #if there's no data then call the api request
			url = 'https://rest.coinapi.io/v1/ohlcv/COINBASE_SPOT_' + apiRequest +'_USD/history?period_id=1DAY&time_start=2018-01-01T00:00:00&time_end=2020-12-31T00:00:00&limit=2000'
			#headers = {'X-CoinAPI-Key' : 'F7F21667-42EE-466D-B32D-DB4E2D15E9EE'}
			headers = {'X-CoinAPI-Key' : '8C728603-6D0B-45CF-87CE-5D56F7D95BC8'}
			r = requests.get(url, headers=headers)
			data = r.json()
			#print(data)

			file = open("./data/"+ coin + '2018.csv', 'w') #create the new file
			file.write("time_period_start;time_period_end;time_open;time_close;price_open;price_high;price_low;price_close;volume_traded;trades_count")

			count = 0 
			for dictionary in data:
				count = 0
				for datapoint in dictionary: #loop through the file and add the data points
					count = count + 1
					#print(dictionary.get(datapoint))
					entry = dictionary.get(datapoint)

					if(count == 1 or count == 2): #remove useless timestamps
						new = entry.split("T")
						file.write(str(new[0]))

					elif(count == 9):
						file.write(str(entry))

					else:
						file.write(str(entry)+ ";")
				file.write('\n')
			file.close()
		finally:
			data = pd.read_csv("./data/"+ coin + '2018.csv',sep=';', usecols=[0,1,4,5,6,7,8,9]) #strip the important data
			df = pd.DataFrame(data)
			#print(data)
			plot = {'Date' : [row[0] for index , row in df.iterrows()],
					 'Price': [row[4] for index , row in df.iterrows() ] 
					 } #create a dictionary with dates and open values
			dfPlot = pd.DataFrame(plot, columns = ['Date', 'Price'])
			figure = plt.Figure(figsize=(6, 4), dpi=125)
			figure_canvas = FigureCanvasTkAgg(figure, self.page)
			NavigationToolbar2Tk(figure_canvas, self.page)
			axes = figure.add_subplot()
			axes.set_title('Price data from 2018-2021 for: ' + coin)
			axes.set_xlabel('Date')
			axes.set_ylabel('Price in USD')
			dfPlot = dfPlot[['Date','Price']].groupby('Date').sum() #group the axis together
			dfPlot.plot(kind='line', legend='true', ax=axes) #plot the graph
			figure_canvas.get_tk_widget().place(relx= 0.025, rely= 0.1)
	


class SVM2022:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - SVM 2022 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="SVM 2022 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class SVMLive:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - SVM Live Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="SVM Live Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class ANN2018:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - ANN 2018 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="ANN 2018 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class ANN2022:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - ANN 2022 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="ANN 2022 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class ANNLive:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - ANN Live Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="ANN Live Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class MA2018:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - MA 2018 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="MA 2018 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

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

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class MALive:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - MA Live Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="MA Live Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class RSI2018:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - RSI 2018 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="RSI 2018 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class RSI2022:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - RSI 2022 Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="RSI 2022 Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)

class RSILive:
	def __init__(self, page):
		self.page = page
		self.page.title("Psxrc6 - RSI Live Trading Bot") #create gui window
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


		self.label2 = Label(self.frame, text="RSI Live Trading Bot", bg="yellow", font=70)
		self.label2.place(relx=0.38,rely=0.22, relwidth=0.15, relheight = 0.5)

	def Home(self):
		root = Tk()
		home = HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)


def main():
	root = Tk()
	home = HomePage(root)
	root.mainloop()

if __name__ == '__main__':
    main()
