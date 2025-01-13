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
    
    # Clear existing text to avoid clutter
    for txt in ax.texts:
        txt.remove()
    
    # Add text for the current point, change for company name or curve value after color
    if i < len(dates):  # Ensure index is within range
        ax.text(dates[i], investement[i], f'{round(investement[i])} Investit', color='#884b8f', fontsize=8)
        ax.text(dates[i], values2[i], f'{round(values2[i])} IBM', color='orange', fontsize=8)

    # Ensure that we're not passing empty lists to min() and max()
    if i > 0:  # Start adjusting limits only when there is data
        current_min = min(min(investement[:i]), min(values2[:i]))  # Find the current min value of both lines
        current_max = max(max(investement[:i]), max(values2[:i]))  # Find the current max value of both lines
        padding = (current_max - current_min) * 0.1  # Add padding to the y-limits for better visualization

        # Update the y-axis limits dynamically to zoom in on the data
        ax.set_ylim(current_min - padding, current_max + padding)
        
        # Dynamically update the x-axis (date scale)
        # Focus the x-axis on the portion of the date range that corresponds to the current frame
        if i < 36:
            start_date = dates[0]
            end_date = dates[36]
        else:
            start_date = dates[i-36]
            end_date = dates[i]

        ax.set_xlim(start_date, end_date)  # Zoom in on the date range based on current frame

        # Adjust the x-ticks for dynamic scaling: Show every Nth date (e.g., every 6th date)
        date_range = pd.date_range(start_date, end_date, freq='6ME')  # Show ticks every 6 months
        ax.set_xticks(date_range)  # Set x-ticks to these dates

        # Format the date labels
        ax.set_xticklabels(date_range.strftime('%Y-%m'), ha='right')
        

    return [line, line2]

# Fetching data from the Alpha Vantage API, enter a key for the API, change the symbol to stock name (e.g., Apple = AAPL)
url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo"
r = requests.get(url)
data = r.json()

if "Weekly Adjusted Time Series" in data:
    monthly_data = data["Weekly Adjusted Time Series"]
    # Extract the "5. adjusted close" value for each month
    close_prices = {date: float(details["5. adjusted close"]) for date, details in monthly_data.items()}

# Prepare dates and values
key_list = sorted(close_prices.keys())  # Ensure dates are sorted
values = [close_prices[date] for date in key_list]
dates = pd.to_datetime(key_list)

x = 1000
values2 = []
new_value = x / values[0]
for value in values:
    
    values2.append(new_value * value)


investement = []
for value in values:
    investement.append(x)
print(dates[0])
# Setting up the figure and line object
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')  # Background of the entire figure
ax.set_facecolor('black')
line, = ax.plot([], [], color='#884b8f', linestyle='-')  # Set up an empty line
line2, = ax.plot([], [], color='orange', linestyle='-', label='Scaled Closing Price')

# Setting axis limits and labels
ax.set_xlim(dates[0], dates[-1])
ax.set_ylim(min(values2), max(values2))
ax.set_title("Monthly Closing Prices for IBM", color="white")
ax.set_xlabel("Date", color="white")
ax.set_ylabel("Closing Price", color="white")
ax.tick_params(colors='white')

# Creating the animation
ani = FuncAnimation(
    fig=fig,
    func=animate,
    frames=len(dates),
    init_func=init,
    blit=False,
    interval=80,
    repeat=False
)

plt.show()