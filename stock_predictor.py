# %%
#This program predicts stock prices by using machine leaning models

#Install the dependencies
import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

# %%
#Get the stock data
import yfinance as yf
from datetime import datetime  # Import datetime module

# Define today's date
today = datetime.today().strftime('%Y-%m-%d')
df = yf.download("META", start="2010-01-01", end=today)
#Take a look at the data
print(df.head())

# %%
#Get the adjusted close price
df=df[['Adj Close']]
#Take a look at the new data
print(df.head())
# %%
#A variable for predicting 'n' days out into the future
forecast_out=30
#Create another column (the target or dependent varaible) shifted 'n' units up
df['Prediction']=df[['Adj Close']].shift(-forecast_out)
#print the new data set
print(df.columns)
print(df.tail())

# %%
### Create the independent data set (x) ######
#Convert the dataframe to a numpy array
X=np.array(df.drop(['Prediction'], axis=1))
#Remove the last 'n' rows
X=X[:-forecast_out]
print(X)
# %%
###Create the dependent data set (y) #####
#Convert the dataframe to a number array (All of the values including NaN's)
y=np.array(df['Prediction'])
#Get all of the y values except the last 'n' rows
y=y[:-forecast_out]
print(y)
# %%
#Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test=train_test_split(X,y, test_size=0.2)

# %%
#Create and train the Support Vector Machine(Regressor)
svr_rbf=SVR(kernel='rbf',C=1e3, gamma=0.1)
svr_rbf.fit(x_train, y_train)

# %%
# Testing Model:Score returns the coefficient of determination R^2 of the prediction
# The best possible score is 1.0
svm_confidence=svr_rbf.score(x_test, y_test)
print("svm confidence:", svm_confidence)

# %%
#Create and train the Linear Regression Model
lr=LinearRegression()
#Train the model
lr.fit(x_train, y_train)
# %%
# Testing Model:Score returns the coefficient of determination R^2 of the prediction
# The best possible score is 1.0
lr_confidence=lr.score(x_test, y_test)
print("lr confidence:", lr_confidence)
# %%
# Set x_forecast equal to the last 30 rows of the original data set from Adj. Close column
x_forecast=np.array(df.drop(['Prediction'],axis=1))[-forecast_out:]
print(x_forecast)
# %%
#Print the predictions for the next 'n' days
lr_Prediction=lr.predict(x_forecast)
print(lr_Prediction)
# %%
#Print support vector regressor model predictions for the next 'n' days
svm_Prediction=svr_rbf.predict(x_forecast)
print(svm_Prediction)

