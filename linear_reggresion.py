import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = {
    'X': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10]
}

df = pd.DataFrame(data)

X = df[['X']]
y = df['y']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X)

plt.scatter(X, y, color='blue', label='Actual data')
plt.plot(X, y_pred, color='red', linewidth=2, label='Predicted line')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression')
plt.legend()
plt.show()
m = model.coef_[0]
b = model.intercept_

print(f'line equation: y = {m:.2f}x + {b:.2f}')
