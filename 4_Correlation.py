import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine
import seaborn as sns

# --- MySQL Connection ---
engine = create_engine('mysql+mysqlconnector://3RpS6E8vJViaNcJ.root:5mAbJNUlK8UUO6DW@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/nifty50_db')

# Load your data
sql_df = pd.read_sql("SELECT * FROM nifty50_tb", con=engine)

df = sql_df.sort_values(['Ticker', 'date'])
# Calculate daily percentage return per stock
df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
# df['daily_return'] = (df['daily_return'] * 100).round(2)  # Convert to %
#Pivot the data: rows = date, columns = stocks, values = daily returns
returns_pivot = df.pivot(index='date', columns='Ticker', values='daily_return')
#Calculate Correlation Matrix using pandas .corr()
corr_matrix = returns_pivot.corr()

corr_matrix = corr_matrix.round(2)
corr_matrix.to_csv("Correlation_matrix_stock.csv", index=False)

st.title("Stock Price Correlation Heatmap")

plt.figure(figsize=(20, 16))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True,
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 7}  # smaller font size for annotations
            )
plt.xticks(rotation=45, fontsize=9)
plt.yticks(rotation=0, fontsize=9)


st.pyplot(plt)