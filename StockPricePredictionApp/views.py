import re
from django.shortcuts import render,HttpResponse
import yfinance as yf
import math
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten,Dense,Dropout,BatchNormalization,LSTM,Bidirectional
from keras import regularizers
from tensorflow.keras.optimizers import Adam,RMSprop,SGD,Adamax
import csv
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras import optimizers
import pandas as pd
from datetime import timedelta, date
from django.core.paginator import Paginator


df=None
df1=None
df2=None
def home(request):
    global df
    context={"flag":False}
    if request.method == 'POST':
        stocks = str(request.POST.get('company1'))
        start_date = str(request.POST.get('start_date'))
        close_date= str(request.POST.get('close_date'))
    

        apple = yf.Ticker(stocks)
        des=apple.info
        temp_des={}
        for key in des:
            if des[key]!='None' and des[key]!=[]:
                temp_des[key]=des[key]
        des=temp_des
       
        df=apple.history(start=str(start_date), end=str(close_date), actions=False)
        
        df['Date']=df.index.strftime('%d-%m-%Y')
        x=list(map(str,df.index.strftime('%d-%m-%y')))
        
        y_high=list(df['High'])
        y_open=list(df['Open'])
        y_low=list(df['Low'])
        y_close=list(df['Close'])
        y_volume=list(df['Volume'])
        
    
        context={
            'x':x,
            'y_high':y_high,
            'y_low':y_low,
            'y_open':y_open,
            'y_close':y_close,
            'y_volume':y_volume,
            'company':stocks,
            'df':df,
            'predicted_x':[1,2,3,4,5],
            'predicted_y':[5,4,3,2,1],
            'max_price':round(max(y_high),2),
            'min_price':round(min(y_low),2),
            'last_day_price':round(y_close[-1],2),
            'change_in_price':round(y_high[-1]-y_high[0],2),
            'change_in_precentage':round(((y_high[-1]-y_high[0])/y_high[0])*100,2),
            "description":des,
            "flag":True,
            'company':stocks,
            'start_date':start_date,
            'close_date':close_date
        }
    
    return render(request,'home2.html',context)

def compare(request):
    stocks1="MSFT"
    stocks2="AAPL"
    start_date='2021-06-19'
    close_date='2022-08-13'
    context={
        "flag":False
    }
    if request.method == 'POST':
        stocks1 = request.POST.get('company1')
        stocks2 = request.POST.get('company2')
        start_date = str(request.POST.get('start_date'))
        close_date= str(request.POST.get('close_date'))
       
        global df1,df2
        data1 = yf.Ticker(stocks1)
        df1=data1.history(start=str(start_date), end=str(close_date), actions=False)
        df1['Date']=df1.index.strftime('%d-%m-%y')
 
        x_stock1=list(map(str,df1.index.strftime('%d-%m-%y')))
   
        y_high_stock1=list(df1['High'])
        y_open_stock1=list(df1['Open'])
        y_low_stock1=list(df1['Low'])
        y_close_stock1=list(df1['Close']) 
        y_volume_stock1=list(df1['Volume'])
        data2 = yf.Ticker(stocks2)
        df2=data2.history(start=str(start_date), end=str(close_date), actions=False)
        df2['Date']=df2.index.strftime('%d-%m-%y')
  
        x_stock2=list(map(str,df2.index.strftime('%d-%m-%y')))
      
        y_high_stock2=list(df2['High'])
        y_open_stock2=list(df2['Open'])
        y_low_stock2=list(df2['Low'])
        y_close_stock2=list(df2['Close'])  
        y_volume_stock2=list(df2['Volume'])
        x_final=x_stock2[:]
        if len(x_stock2)<len(x_stock1):
            y_high_stock2=y_high_stock2[-len(x_stock2):]
            y_open_stock2=y_open_stock2[-len(x_stock2):]
            y_low_stock2=y_low_stock2[-len(x_stock2):]
            y_close_stock2=y_close_stock2[-len(x_stock2):]
            y_volume_stock2=y_volume_stock2[-len(x_stock2):]
            x_final=x_stock2[:]
        elif len(x_stock2)>len(x_stock1) :
            y_high_stock1=y_high_stock1[-len(x_stock1):]
            y_open_stock1=y_open_stock1[-len(x_stock1):]
            y_low_stock1=y_low_stock1[-len(x_stock1):]
            y_close_stock1=y_close_stock1[-len(x_stock1):]
            y_volume_stock1=y_volume_stock1[-len(x_stock1):]
            x_final=x_stock1[:]
        context={
            'x':x_final,
            'y_high_stock1':y_high_stock1,
            'y_open_stock1':y_open_stock1,
            'y_low_stock1':y_low_stock1,
            'y_close_stock1':y_close_stock1,
            'y_high_stock2':y_high_stock2,
            'y_open_stock2':y_open_stock2,
            'y_low_stock2':y_low_stock2,
            'y_close_stock2':y_close_stock2,
            'y_volume_stock1':y_volume_stock1,
            'y_volume_stock2':y_volume_stock2,
            'company1':stocks1,
            'company2':stocks2,
            'df1':df1,
            'df2':df2,
            'max_price_stock1':round(max(y_high_stock1),2),
            'min_price_stock1':round(min(y_low_stock1),2),
            'last_day_price_stock1':round(y_close_stock1[-1],2),
            'change_in_price_stock1':round(y_high_stock1[-1]-y_high_stock1[0],2),
            'change_in_precentage_stock1':round(((y_high_stock1[-1]-y_high_stock1[0])/y_high_stock1[0])*100,2),
            'max_price_stock2':round(max(y_high_stock2),2),
            'min_price_stock2':round(min(y_low_stock2),2),
            'last_day_price_stock2':round(y_close_stock2[-1],2),
            'change_in_price_stock2':round(y_high_stock2[-1]-y_high_stock2[0],2),
            'change_in_precentage_stock2':round(((y_high_stock2[-1]-y_high_stock2[0])/y_high_stock2[0])*100,2),
            'flag':True,
            "start_date":start_date,
            "close_date":close_date
        }
    return render(request,'compare2.html',context)


def download(request,id):
    global df,df1,df2
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"' # your filename
    
    if id=='0':
        writer = csv.writer(response)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for ind in df.index:
            writer.writerow([ind,df['Open'][ind],df['High'][ind],df['Low'][ind],df['Close'][ind],df['Volume'][ind]])
    elif id=='1':
        writer = csv.writer(response)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for ind in df1.index:
            writer.writerow([ind,df1['Open'][ind],df1['High'][ind],df1['Low'][ind],df1['Close'][ind],df1['Volume'][ind]])
    elif id=='2':
        writer = csv.writer(response)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for ind in df2.index:
            writer.writerow([ind,df2['Open'][ind],df2['High'][ind],df2['Low'][ind],df2['Close'][ind],df2['Volume'][ind]])
    elif id=='3':
        writer = csv.writer(response)
        writer.writerow(['', 'Date','Prediction'])
        for ind in df.index:
            writer.writerow([ind,df['Date'][ind],df['Prediction'][ind]])
    elif id=='4':
        writer = csv.writer(response)
        writer.writerow(['', 'Symbol','Name','High','Low','Open','Close','Net Change','% Change','Industory','Country'])
        for ind in df.index:
            writer.writerow([ind,df['symbol'][ind],df['name'][ind],df['high'][ind],df['low'][ind],df['open'][ind],df['close'][ind],df['net change'][ind],df['% Change'][ind],df['industory'][ind],df['country'][ind]])
    return response

