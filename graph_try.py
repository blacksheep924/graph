import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import requests
import pandas as pd

def moving_average(data, window_size):
    """Calculate the moving average with a given window size."""
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def init():  # Initialization function
    line.set_data([], [])
    line2.set_data([], [])
    return [line, line2]

def animate(i):  # Animation function
    line.set_data(dates[:i], investement[:i])
    line2.set_data(dates[:i], values2[:i])  # Set data for second line
    
    # Clear existing text to avoid clutter
    for txt in ax.texts:
        txt.remove()
    
    if i < len(dates):  # Ensure index is within range
        ax.text(dates[i], investement[i], f'{round(investement[i])} Investit', color='#884b8f', fontsize=8)
        ax.text(dates[i], values2[i], f'{round(values2[i])} IBM', color='orange', fontsize=8)

    if i > 0:  # Start adjusting limits only when there is data
        current_min = min(min(investement[:i]), min(values2[:i]))
        current_max = max(max(investement[:i]), max(values2[:i]))
        padding = (current_max - current_min) * 0.1

        ax.set_ylim(current_min - padding, current_max + padding)
        
        if i < 36:
            start_date = dates[0]
            end_date = dates[36]
        else:
            start_date = dates[i-36]
            end_date = dates[i]

        ax.set_xlim(start_date, end_date)
        date_range = pd.date_range(start_date, end_date, freq='6ME')
        ax.set_xticks(date_range)
        ax.set_xticklabels(date_range.strftime('%Y-%m'), ha='right')
        
    return [line, line2]

# Fetching data
url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo"
r = requests.get(url)
data = r.json()

if "Weekly Adjusted Time Series" in data:
    monthly_data = data["Weekly Adjusted Time Series"]
    close_prices = {date: float(details["5. adjusted close"]) for date, details in monthly_data.items()}

# Prepare dates and values
key_list = sorted(close_prices.keys())
values = [close_prices[date] for date in key_list]
dates = pd.to_datetime(key_list)

# Apply moving average for smoothing
window_size = 20  # Change this value to control smoothing
smoothed_values = moving_average(values, window_size)
smoothed_dates = dates[window_size - 1:]  # Adjust dates for the reduced length

x = 1000
values2 = []
new_value = x / smoothed_values[0]
for value in smoothed_values:
    values2.append(new_value * value)

investement = [x] * len(smoothed_values)

# Setting up the figure and line object
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
line, = ax.plot([], [], color='#884b8f', linestyle='-')
line2, = ax.plot([], [], color='orange', linestyle='-', label='Scaled Closing Price')

ax.set_xlim(smoothed_dates[0], smoothed_dates[-1])
ax.set_ylim(min(values2), max(values2))
ax.set_title("Monthly Closing Prices for IBM", color="white")
ax.set_xlabel("Date", color="white")
ax.set_ylabel("Closing Price", color="white")
ax.tick_params(colors='white')

# Creating the animation
ani = FuncAnimation(
    fig=fig,
    func=animate,
    frames=len(smoothed_dates),
    init_func=init,
    blit=False,
    interval=80,
    repeat=False
)

plt.show()