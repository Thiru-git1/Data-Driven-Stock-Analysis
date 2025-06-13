import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine
import seaborn as sns
import plotly.express as px

# --- MySQL Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/nifty50_db')
# Load your data
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
st.title("📊 Monthly Top 5 Gainers and Losers")
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