import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# 3. Sector-wise Performance:
# ●	Objective: Provide a breakdown of stock performance by sector (sector data shared as csv).
# ●	Reason: Investors and analysts often look at sector performance to gauge market sentiment in specific industries (e.g., IT, Financials, Energy, etc.).
# Metrics:
# ●	Classify each stock by its sector (this can be done by adding a separate dataset or manually mapping sectors to stocks).
# ●	Calculate the average yearly return for each sector.
# ●	Plot a bar chart showing the average performance for each sector.

df1= pd.read_csv("D:\Data_Driven_stock_project\comb_sector.csv",parse_dates=['date'])
# Ensure clean columns
df1['Ticker'] = df1['Ticker'].str.strip().str.upper()
df1['sector'] = df1['sector'].str.strip().str.title()
# Sort for group operations
df1 = df1.sort_values(by=['Ticker', 'date'])
# Calculate daily return
df1['daily_return'] = df1.groupby('Ticker')['close'].pct_change()
# Calculate cumulative return (total growth from start to end of year)
df1['avg_yearly_return'] = df1.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)
# Get the last available cumulative return per stock
yearly_returns = df1.groupby('Ticker').last().reset_index()
# Keep only needed columns
yearly_returns = yearly_returns[['Ticker', 'sector', 'avg_yearly_return']]
# Average yearly return per sector
sector_avg_return = (yearly_returns.groupby('sector')['avg_yearly_return'].mean().reset_index() 
                     .sort_values(by='avg_yearly_return', ascending=False))
sector_avg_return['avg_yearly_return'] = (sector_avg_return['avg_yearly_return'] * 100).round(2)
#save to CSV file for PowerBI
sector_avg_return.to_csv("avg_yearly_return_sector.csv", index=False)

# Colors: red for negative returns
colors = ['crimson' if val < 0 else 'steelblue' for val in sector_avg_return['avg_yearly_return']]

st.subheader("3. Sector-wise Performance by Bar Chart")

fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(sector_avg_return['sector'], sector_avg_return['avg_yearly_return'], color=colors)
ax.set_title("Average Yearly Return by Sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Avg Yearly Return (%)")
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(fig)



