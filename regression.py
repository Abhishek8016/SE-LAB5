import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model
height=[[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0]]
weight=[  8, 10 , 12, 14, 16, 18, 20]
plt.scatter(height,weight,color='black')
plt.xlabel("height")
plt.ylabel("weight")
reg=linear_model.LinearRegression()
reg.fit(height,weight)
X_height=[[12.0]]
print(reg.predict(X_height)
=================================================
#import modules
import warnings
import pandas as pd
from sklearn import model_selection
import numpy as np
import sklearn
from sklearn import linear_model
X=[[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0]]
y=[  8, 10 , 12, 14, 16, 18, 20]
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state=7)
print("Training Features", X_train);print("Training Labels",y_train);print("Training Data",X_test);print("Testing Data",y_test)
reg=linear_model.LinearRegression()
reg.fit(X_train,y_train)

result = reg.score(X_test, y_test)
print("Accuracy - test set: %.2f%%" % (result*100.0))
X_height=[[12.0]]
print(reg.predict(X_test))

import pandas as pd
x=[[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0]]
y=[  16, 25 , 36, 49,64,81, 100]

from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(x,y)


print(lin_reg.predict([[11]]))
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

polynomial_regression = make_pipeline(
    PolynomialFeatures(degree=1, include_bias=False),
    LinearRegression(),
)
polynomial_regression.fit(x,y)
X_height=[[20.0]]
target_predicted = polynomial_regression.predict(X_height)
print(target_predicted)
