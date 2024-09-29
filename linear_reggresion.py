import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

with sqlite3.connect('Divar.sqlite') as conn:
    cur = conn.cursor()
    b = cur.execute('select * from House_price').fetchall()
    conn.commit()

districts_list = []
for j in b:
    if j[2] not in districts_list:
        districts_list.append(j[2])

for item in districts_list:

    with sqlite3.connect('Divar.sqlite') as conn:
        cur = conn.cursor()
        b = cur.execute('SELECT * FROM House_price WHERE district=?', (item,)).fetchall()
        conn.commit()
    prices = []
    for price in b:
        prices.append(price[1])

    if not prices:
        print(f"No data available for district: {item}")
        continue

    a = list(range(len(prices), 0, -1))

    data = {
        'X': a,
        'y': prices
    }

    df = pd.DataFrame(data)

    X = df[['X']]
    y = df['y']

    if len(X) <= 2:
        print(f"Not enough data to split for district: {item}. Only {len(X)} sample(s) available.")
        continue

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X)

    plt.scatter(X, y, color='blue', label='Actual data')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Predicted line')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title(f'{item}')
    plt.legend()
    plt.show()
    m = model.coef_[0]
    b = model.intercept_

    print(f'line equation for {item}: y = {m:.2f}x + {b:.2f}')
