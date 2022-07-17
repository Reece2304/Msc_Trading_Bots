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
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)

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
		home = main.HomePage(root)
		self.close_window()
		root.mainloop()

	def close_window(self):
		self.page.destroy()

	def trade(self, coin):
		print(coin)