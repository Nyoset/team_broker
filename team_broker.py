# -*- coding: utf-8 -*-

import finnhub
import pandas as pd
import tensorflow as tf
import numpy as np
import random
import datetime as dt
import pandas_market_calendars as mcal
from datetime import datetime, timedelta
import random

from data_gatherer import *

token = "bslf58frh5rb8ivktbpg"
finnhub_client = finnhub.Client(api_key=token)

maxWeeks = 4
maxDays = maxWeeks * 7 #4 setmanes * 7 dies
maxWorkDays = maxWeeks * 5
numberOfFeatures = maxWorkDays * 4

#Data mínima // 1 Gener 2015
minDate = datetime(2018, 1, 1)
#Data màxima // 1 Juny 2020
maxDate = datetime.today()-timedelta(days=30)
#Calendari de dies habils
nyse = mcal.get_calendar('NYSE')
#Calendari de dies festius
schedule = nyse.schedule(start_date=minDate, end_date=maxDate)
holidays = nyse.holidays().holidays
# if np.datetime64(datetime(2018, 3, 30)) in holidays:
# getRandomMonthData("AAPL",minDate,maxDate,maxDays)

def getRandomMonth(minDate,maxDate,maxDays=maxDays):
  #Funció que recollira les dades de 20 dies laborals començant per dilluns excloent festius
  #Param:
  #EntName: int/ data mínima per recollir dades
  #EntName: int/ data màxima per recollir dades
  #EntName: str/ nom o acrònim de l'empresa a recollir les dades
  res = False
  errors = 0
  maxErrors = 5

    # Agafem un dilluns random dintre de les nostres dates
  date = getRandomMonday(minDate,maxDate)
  i = 0
  #Mentres les dades del mes que volem recuperar no compleixin els requisits...
  while errors < maxErrors:

    # Calculem el dia final del rang temporal el qual obtindrem dades
    finalDate = date + timedelta(days=maxDays-1 + i)

    # Obtenim la quantitat de dies laborals dintre del nostre rang temporal
    schedule_range = schedule.loc[date.strftime("%Y-%m-%d"):finalDate.strftime("%Y-%m-%d") : ]
    LaborDays = mcal.date_range(schedule_range, frequency='1D')
    
    # Si no arribem a maxWorkDays dies vol dir que hi ha algun festiu pel mig i descartem la mostra(de moment).
    if len(LaborDays) == maxWorkDays:
      return (date, finalDate)
    else:
      i += 1
      errors+=1

  print("FAIL")
  print(date)
  print(finalDate)
  return (None, None)

def getRandomMonday(minDate,maxDate):
  while True:
    randomday = random.randrange((maxDate - minDate).days)
    randomdate = minDate + timedelta(days = randomday)
    if randomdate.weekday() == 0:
      break
  return randomdate

def getFeatures(symbol, initialRange, finalRange):
  print(symbol)
  (initialDate, finalDate) = getRandomMonth(initialRange, finalRange)
  if initialDate is None or finalDate is None:
    return None
  data = get_candles(symbol, initialDate, finalDate)
  stockIncrement = getFutureIncrement(symbol, finalDate) 
  if data is None or stockIncrement is None:
    print(symbol + " DISCARDED")
    return None
  features = data[['o', 'c', 'h', 'l']]
  features = ((features / features['o'][0]) - 1) * 100
  return (tf.convert_to_tensor(pd.concat([features[col] for col in features.columns])), stockIncrement)

def getModel():
  model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(numberOfFeatures)),
    tf.keras.layers.Dense(80, activation=tf.nn.sigmoid),
    tf.keras.layers.Dense(40, activation=tf.nn.sigmoid),
    tf.keras.layers.Dense(10, activation=tf.nn.sigmoid),
    tf.keras.layers.Dense(1)
  ])
  model.summary()
  model.compile(optimizer='Adam',
                loss="mse", 
                metrics=['mae', 'accuracy'],
                )
  
  return model

def getFutureIncrement(symbol, date):
  nextDays = get_candles(symbol, date, date + timedelta(days=7))
  if nextDays is None:
    return None
  initial = float(nextDays.iloc[[0]]['o'])
  final = float(nextDays.iloc[[-1]]['c'])
  return ((final - initial) / initial)*100

def obtainData(symbols):
  dataList = list(map(lambda symbol: getFeatures(symbol, min_date, max_date), symbols))
  filteredData = list(filter(lambda x: x[0].shape == numberOfFeatures, list(filter(None, dataList))))
  symbolData = tf.stack([features[0] for features in filteredData])
  result = tf.stack([features[1] for features in filteredData])
  return (symbolData, result)

# Main
print("Main")
model = getModel()
symbols = get_symbol_list()
(training, result) = obtainData(random.sample(list(symbols), 200))
print("Using " + str(training.shape[0]) + " samples with " + str(training.shape[1]) + " data")

#Testing
(features, solution) = obtainData(['AAPL'])
if features.shape != 0:
  print("Prediction")
  print(model.predict(features))
  print("Solution")
  print(solution[0])
else:
  print("Wrong sample :(")

full_training = tf.concat([full_training, training], axis=0)
full_result = tf.concat([full_result, result], axis= 0)

model = getModel2()
model.fit(full_training[500:,], full_result[500:,], epochs=3, batch_size=batch_size)

batch_size = 15
time_steps = 40
feature_size = 4

model = tf.keras.models.Sequential([
  tf.keras.layers.LSTM(60, input_shape=(time_steps, feature_size)),
  tf.keras.layers.Dense(20, activation=tf.nn.sigmoid),
  tf.keras.layers.Dense(1)
])
model.summary()
model.compile(optimizer='adam',
              loss="mse", 
              metrics=['mae', 'accuracy'],
              )
batch = tf.reshape(training, [training.shape[0], time_steps, feature_size])
model.fit(batch, result, epochs=50, batch_size=batch_size, validation_split=0.1)

training.shape
batch = training[1:19, ]
batch.shape[0]

