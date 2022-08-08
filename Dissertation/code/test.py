# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 13:28:32 2022

@author: reece
"""

import pandas as pd
import matplotlib.pyplot as plt
		#plot the predictions and display to the user
Pplot = {'Date' : ['10:27', '10:45','11:00'],
		'Actual_Price': ['29954','30002', '34000'] 
		} #create a dictionary with dates and close values

Pplot2 = { 'Date' : ['10:27', '10:45','11:00'],
		'Actual_Price': ['29934','30102', '33000'] 
		 }
		 
predictionPlot2 = pd.DataFrame(Pplot2, columns = ['Date', 'Predicted_Price'])
predictionPlot = pd.DataFrame(Pplot, columns = ['Date', 'Actual_Price'])
predictionPlot.set_index("Date", inplace=True)
predictionPlot2.set_index("Date", inplace=True)
figure = plt.Figure(figsize=(6, 6), dpi=105)
axes = figure.add_subplot()
axes.set_title('Prediction Price Live for: ')
axes.set_xlabel('Date')
axes.set_ylabel('Price in USD')
axes.set_xticklabels(['10:27', '10:45','11:00'], fontsize=7)

dates_ = pd.date_range('10:00', '11:00').to_pydatetime()

predictionPlot['Actual_Price'] = predictionPlot['Actual_Price'].astype(float)

predictionPlot.plot(kind='bar', legend='true', ax=axes, rot=90, color='magenta') #plot the graph

predictionPlot2.plot(kind='line',ax=axes, color = 'green', rot=90)
figure_canvas.get_tk_widget().place(relx= 0.5, rely= 0.1)

