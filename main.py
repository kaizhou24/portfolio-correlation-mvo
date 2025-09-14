import yfinance as yf

def main():
    aapl_ticker = yf.Ticker('AAPL')
    aapl_history = aapl_ticker.history(period="5y")
    print(aapl_history)


if __name__ == "__main__":
    main()
