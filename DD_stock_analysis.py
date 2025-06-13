import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
import seaborn as sns

# --- MySQL Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/nifty50_db')

# Load your data
sql_df = pd.read_sql("SELECT * FROM nifty50_tb", con=engine)
df = sql_df.sort_values(['Ticker', 'date'])
df['daily_return'] = df.groupby('Ticker')['close'].pct_change() * 100
# Calculate standard deviation (volatility) for each stock
volatility_df = df.groupby('Ticker')['daily_return'].std().reset_index()
volatility_df.rename(columns={'daily_return': 'volatility'}, inplace=True)
# Sort to get top 10 most volatile stocks
top_10_volatility = volatility_df.sort_values(by='volatility', ascending=False).head(10) # Save to CSV
top_10_volatility.to_csv("top_10_most_volatile_stocks.csv", index=False)
print("✅ Saved top 10 volatile stocks to CSV.")
st.title("1. Top 10 Most Volatile Stocks")# Load data
st.dataframe(top_10_volatility)   # Display table for top10 volatile stocks 
#Plot a bar chart showing the volatility of the top 10 most volatile stocks over the year.
fig_bar= px.bar(
    top_10_volatility,
    x='Ticker',
    y='volatility',
    title='Top 10 Most Volatile Stocks',
    labels={'volatility': 'Volatility (Std Dev of Daily Returns)'},
    color='volatility',
    color_continuous_scale='OrRd')
st.plotly_chart(fig_bar)

# 2. Cumulative Return Over Time:
# Objective: Show the cumulative return of each stock from the beginning of the year to the end.
# Step 1: Sort and calculate daily return
df_c = df.sort_values(by=['Ticker', 'date'])
df_c['daily_return'] = df_c.groupby('Ticker')['close'].pct_change()

# Step 2: Calculate cumulative return
df_c['cumulative_return'] = df_c.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)
df_c['cumulative_return'] = (df_c['cumulative_return'] * 100).round(2)  # Convert to %

# Step 3: Get top 5 stocks by final cumulative return
latest_returns = df_c.groupby('Ticker').last().reset_index()
top_5 = latest_returns.sort_values(by='cumulative_return', ascending=False).head(5)['Ticker'].tolist()

top_5_df = df_c[df_c['Ticker'].isin(top_5)]
latest_top_5_df = top_5_df.groupby('Ticker').last().reset_index()
st.dataframe(latest_top_5_df)
# Optional: save to CSV
latest_top_5_df.to_csv("Cummulative_top5_stocks.csv", index=False)

# Step 5: Display in Streamlit
st.title("2. Top 5 Performing Stocks - Cumulative Return")

# Line chart
st.line_chart(data=top_5_df.pivot(index='date', columns='Ticker', values='cumulative_return'),
              use_container_width=True)

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

st.title("3. Sector-wise Performance by Bar Chart")

fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(sector_avg_return['sector'], sector_avg_return['avg_yearly_return'], color=colors)
ax.set_title("Average Yearly Return by Sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Avg Yearly Return (%)")
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(fig)

#4.

df = sql_df.sort_values(['Ticker', 'date'])
# Calculate daily percentage return per stock
df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
#Pivot the data: rows = date, columns = stocks, values = daily returns
returns_pivot = df.pivot(index='date', columns='Ticker', values='daily_return')
#Calculate Correlation Matrix using pandas .corr()
corr_matrix = returns_pivot.corr()
st.title("4. Stock Price Correlation Heatmap")
plt.figure(figsize=(20, 16))  
sns.heatmap(
    corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True,
    cbar_kws={"shrink": .8},
    annot_kws={"size": 7}  # smaller font size for annotations
)
plt.title('Correlation Matrix of Stock Closing Prices')
plt.xticks(rotation=45, fontsize=9)
plt.yticks(rotation=0, fontsize=9)

st.pyplot(plt)

#5. Top_5_gainers_losers

df = pd.read_sql("SELECT * FROM nifty50_tb", con=engine)
df['date'] = pd.to_datetime(df['date'])
# Extract year-month period
df['year_month'] = df['date'].dt.to_period('M')
# Sort for consistency
df = df.sort_values(by=['Ticker', 'date'])
# Get first and last close per month
monthly = df.groupby(['Ticker', 'year_month'])['close'].agg(['first', 'last']).reset_index()
# Calculate monthly % return
monthly['monthly_return'] = ((monthly['last'] - monthly['first']) / monthly['first']) * 100
monthly['monthly_return'] = monthly['monthly_return'].round(2)
# For each month, get top 5 gainers and losers
top_movers = []
for month, group in monthly.groupby('year_month'):
    top_gainers = group.sort_values('monthly_return', ascending=False).head(5).copy()
    top_gainers['Type'] = 'Top Gainer'
    top_losers = group.sort_values('monthly_return', ascending=True).head(5).copy()
    top_losers['Type'] = 'Top Loser'
    top_movers.append(pd.concat([top_gainers, top_losers]))
top_movers_df = pd.concat(top_movers).reset_index(drop=True)
st.title("5. Monthly Top 5 Gainers and Losers")
months = sorted(top_movers_df['year_month'].astype(str).unique())
selected_month = st.selectbox("Select Month", months)
# Filter for selected month
monthly_view = top_movers_df[top_movers_df['year_month'].astype(str) == selected_month]
# Plot
fig = px.bar(
    monthly_view,
    x='Ticker',
    y='monthly_return',
    color='Type',
    barmode='group',
    title=f"Top 5 Gainers and Losers - {selected_month}",
    text='monthly_return',
    height=500
)
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.update_layout(yaxis_title='Monthly Return (%)', xaxis_title='Stock', showlegend=True)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(monthly_view)

top_movers_df.to_csv("5_monthly_top_gainers_losers.csv", index=False)