# Data-Driven-Stock-Analysis
The project will analyze daily stock data, including open, close, high, low, and volume values. Clean and process the data, generate key performance insights, and visualize the top-performing stocks in terms of price changes, as well as average stock metrics. The solution will offer interactive dashboards using Streamlit and Power BI to help Investors, analysts, and enthusiasts make informed decisions based on the stock performance trends.

Business Use Cases:
-------------------
>Stock Performance Ranking: Identify the top 10 best-performing stocks (green stocks) and the top 10 worst-performing stocks (red stocks) over the past year.
>Market Overview: Provide an overall market summary with average stock performance and insights into the percentage of green vs red stocks.
>Investment Insights: Help investors quickly identify which stocks showed consistent growth and which ones had significant declines.
>Decision Support: Provide insights on average prices, volatility, and overall stock behavior, useful for both retail and institutional traders.

1. Volatility Analysis:
●	Objective: Visualize the volatility of each stock over the past year by calculating the standard deviation of daily returns.
●	Reason: Volatility gives insight into how much the price fluctuates, which is valuable for risk assessment. Higher volatility often indicates more risk, while lower volatility indicates a more stable stock.
Metrics:
●	Calculate daily returns for each stock: (Close Price - Previous Close Price) / Previous Close Price.
●	Compute the standard deviation of daily returns for each stock to measure volatility.
●	Plot a bar chart showing the volatility of the top 10 most volatile stocks over the year.
Visualization:
●	Top 10 Most Volatile Stocks: A bar chart with the stock ticker on the x-axis and volatility (standard deviation) on the y-axis.
2. Cumulative Return Over Time:
●	Objective: Show the cumulative return of each stock from the beginning of the year to the end.
●	Reason: The cumulative return is an important metric to visualize overall performance and growth over time. This helps users compare how different stocks performed relative to each other.
Metrics:
●	For each stock, calculate the cumulative return by applying a running total of daily returns.
●	Plot a line chart for the top 5 performing stocks (based on cumulative return) over the course of the year.
Visualization:
●	Cumulative Return for Top 5 Performing Stocks: A line chart displaying cumulative returns for each stock over the year (increasing trend indicates positive performance).
3. Sector-wise Performance:
●	Objective: Provide a breakdown of stock performance by sector (sector data shared as csv).
●	Reason: Investors and analysts often look at sector performance to gauge market sentiment in specific industries (e.g., IT, Financials, Energy, etc.).
Metrics:
●	Classify each stock by its sector (this can be done by adding a separate dataset or manually mapping sectors to stocks).
●	Calculate the average yearly return for each sector.
●	Plot a bar chart showing the average performance for each sector.
Visualization:
●	Average Yearly Return by Sector: A bar chart where each bar represents a sector and its height indicates the average yearly return for stocks within that sector.
4. Stock Price Correlation:
●	Objective: Visualize the correlation between the stock prices of different companies.
●	Reason: This analysis is valuable to understand if certain stocks tend to move in tandem (e.g., correlated with market trends or sector performance).
Metrics:
●	Calculate the correlation coefficient between the closing percentage of different stocks. For this, use the pandas.DataFrame.corr() method.
●	Create a correlation matrix to identify how stocks are related to each other.
●	Plot a heatmap of the correlation matrix to visualize these relationships.
Visualization:
●	Stock Price Correlation Heatmap: A heatmap to show the correlation between the closing prices of various stocks. Darker colors represent higher correlations.
5. Top 5 Gainers and Losers (Month-wise):
●	Objective: Provide monthly breakdowns of the top-performing and worst-performing stocks.
●	Reason: This analysis will allow users to observe more granular trends and understand which stocks are gaining or losing momentum on a monthly basis.
Metrics:
●	Group the stock data by month and calculate the monthly return for each stock.
●	For each month, identify the top 5 gainers and top 5 losers based on percentage change.
●	Create a dashboard-style visualization with 5 charts showing top gainers and losers for each month (12 months total).
Visualization:
●	Top 5 Gainers and Losers by Month: Create a set of 12 bar charts for each month showing the top 5 gainers and losers based on percentage return.


Project Deliverables:
1.	SQL Database: Contains clean and processed data.
2.	Python Scripts: For data cleaning, analysis, and database interaction.
3.	Power BI Dashboard: Visualizations for stock performance.
4.	Streamlit Application: Interactive dashboard for real-time analysis.

