from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
model = load_model('first_model.h5')
model.summary()
import pandas as pd

# df = pd.read_csv('test.csv')
# X = df.iloc[:, 0:5]  
# Y = df.iloc[:,5:9]
# print(X.head())
# print(Y.head())
# score = model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))

x = pd.DataFrame([0,1,0,1])
x = x.transpose()
print(model.predict_classes(x[0:4]))


x = pd.DataFrame([1,0,0,1])
x = x.transpose()
print(model.predict_classes(x[0:4]))


x = pd.DataFrame([1,1,1,0])
x = x.transpose()
print(model.predict_classes(x[0:4]))

x = pd.DataFrame([1,1,1,1])
x = x.transpose()
print(model.predict_classes(x[0:4]))
