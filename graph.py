import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests
import pandas as pd
import random


def init():  # Initialization function
    line.set_data([], [])
    line2.set_data([], [])
    return [line, line2]

def animate(i):  # Animation function
    line.set_data(dates[:i], investement[:i])
    line2.set_data(dates[:i], values2[:i])  # Set data for second line
    return [line, line2]

# Fetching data from the Alpha Vantage API
url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=AAPL&apikey=********"
r = requests.get(url)
data = r.json()


if "Monthly Time Series" in data:
    monthly_data = data["Monthly Time Series"]
    # Extract the "4. close" value for each month
    close_prices = {date: float(details["4. close"]) for date, details in monthly_data.items()}

# Prepare dates and values
key_list = sorted(close_prices.keys())  # Ensure dates are sorted
values = [close_prices[date] for date in key_list]
dates = pd.to_datetime(key_list)

#values2 = [value * 1.1 for value in values]

x = 50
values2 = []
new_value = 0
for value in values:
    new_value += x / value

    values2.append(new_value*value)
    print(new_value)
investement = []
for value in values:
    investement.append(x)
    x+= random.randint(0,150)
print(investement[-1])
# Setting up the figure and line object
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')  # Background of the entire figure
ax.set_facecolor('black') 
line, = ax.plot([], [], color='#884b8f', linestyle='-')  # Set up an empty line
line2, = ax.plot([], [], color='orange', linestyle='-', label='Scaled Closing Price')
# Setting axis limits and labels
ax.set_xlim(dates[0], dates[-1])
ax.set_ylim(min(values2)), max(values2)
ax.set_ylim(min(values2), max(values2))
ax.set_title("Monthly Closing Prices for IBM",color = "white")
ax.set_xlabel("Date",color = "white")
ax.set_ylabel("Closing Price",color = "white")
ax.tick_params(colors='white')



# Creating the animation
ani = FuncAnimation(
    fig=fig, 
    func=animate, 
    frames=len(dates), 
    init_func=init, 
    blit=True,
    interval = 100
)


plt.show()
