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


# #4.

# df = sql_df.sort_values(['Ticker', 'date'])
# # Calculate daily percentage return per stock
# df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
# #Pivot the data: rows = date, columns = stocks, values = daily returns
# returns_pivot = df.pivot(index='date', columns='Ticker', values='daily_return')
# #Calculate Correlation Matrix using pandas .corr()
# corr_matrix = returns_pivot.corr()
# st.title("📉 Stock Price Correlation Heatmap")
# plt.figure(figsize=(20, 16))  
# sns.heatmap(
#     corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True,
#     cbar_kws={"shrink": .8},
#     annot_kws={"size": 7}  # smaller font size for annotations
# )
# plt.title('Correlation Matrix of Stock Closing Prices')
# plt.xticks(rotation=45, fontsize=9)
# plt.yticks(rotation=0, fontsize=9)

# st.pyplot(plt)
