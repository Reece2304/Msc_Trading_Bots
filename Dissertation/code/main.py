# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 09:59:17 2022

@author: reece
"""

from tkinter import *
import os
from svm.svm2k18 import *
from svm.svm2k22 import *
from svm.svmLive import *
from ann.ann2k18 import *
from ann.ann2k22 import *
from ann.annLive import *
from MA.ma2k18 import *
from MA.ma2k22 import *
from MA.maLive import *
from RSI.rsi2k18 import *
from RSI.rsi2k22 import *
from RSI.rsiLive import *

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




def main():
	root = Tk()
	home = HomePage(root)
	root.mainloop()

if __name__ == '__main__':
    main()
