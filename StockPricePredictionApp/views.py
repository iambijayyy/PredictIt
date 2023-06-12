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
