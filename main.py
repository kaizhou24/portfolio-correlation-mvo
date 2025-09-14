import yfinance as yf
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

def main():
    portfolio_tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOG']
    
    close_prices = {}

    for ticker in portfolio_tickers:
        stock_obj = yf.Ticker(ticker)
        stock_data = stock_obj.history(period="1y")
        close_prices[ticker] = stock_data['Close']
    
    portfolio_df = pd.DataFrame(close_prices)
    daily_returns = portfolio_df.pct_change().dropna()

    correlation_matrix = daily_returns.corr()
    print(correlation_matrix)

    plt.figure(figsize=(10, 8))
    sn.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix of Portfolio Stocks')
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("Heatmap saved as 'correlation_heatmap.png'")


if __name__ == "__main__":
    main()