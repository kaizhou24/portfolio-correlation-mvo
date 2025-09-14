import yfinance as yf
import pandas as pd

def main():
    portfolio_tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOG']
    
    close_prices = {}

    for ticker in portfolio_tickers:
        stock_obj = yf.Ticker(ticker)
        stock_data = stock_obj.history(period="1y")
        close_prices[ticker] = stock_data['Close']
    
    portfolio_df = pd.DataFrame(close_prices)
    daily_returns = portfolio_df.pct_change().dropna()
    print("Daily Returns (%):")
    print(daily_returns * 100)


if __name__ == "__main__":
    main()