import yfinance as yf
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

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

    # Calculate key inputs for portfolio metrics
    average_daily_returns = daily_returns.mean()
    covariance_matrix = daily_returns.cov()

    # Monte Carlo simulation settings
    num_portfolios = 20000
    num_stocks = len(portfolio_tickers)

    # Initialize lists to store results
    returns_list = []
    volatility_list = []
    weights_list = []

    # Run Monte Carlo simulation
    print(f"\nRunning Monte Carlo simulation with {num_portfolios} portfolios...")

    for i in range(num_portfolios):
        # Generate random portfolio weights
        weights = np.random.random(num_stocks)
        weights = weights / np.sum(weights)  # Normalize to sum to 1

        # Calculate portfolio return and risk
        portfolio_return = np.dot(weights, average_daily_returns) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights))) * np.sqrt(252)

        # Store results
        returns_list.append(portfolio_return)
        volatility_list.append(portfolio_volatility)
        weights_list.append(weights)

        # Progress indicator
        if (i + 1) % 5000 == 0:
            print(f"Completed {i + 1} portfolios...")

    print("Simulation complete!")
    print(f"Generated {len(returns_list)} portfolio combinations")
    print(f"Return range: {min(returns_list)*100:.2f}% to {max(returns_list)*100:.2f}%")
    print(f"Volatility range: {min(volatility_list)*100:.2f}% to {max(volatility_list)*100:.2f}%")

    # Convert results lists to NumPy arrays for efficient calculations
    returns_array = np.array(returns_list)
    volatility_array = np.array(volatility_list)

    # Calculate Sharpe Ratios
    # Assuming risk-free rate is 0
    sharpe_ratios = returns_array / volatility_array

    # Plotting the Efficient Frontier
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(volatility_array, returns_array, c=sharpe_ratios, cmap='viridis', marker='o', s=10, alpha=0.5)

    # Find optimal portfolios indices
    max_sharpe_idx = np.argmax(sharpe_ratios)
    min_vol_idx = np.argmin(volatility_array)

    # Plot optimal portfolios with different shades of bright red
    plt.scatter(volatility_array[max_sharpe_idx], returns_array[max_sharpe_idx],
               marker='*', color='crimson', s=300, label='Max Sharpe Ratio', edgecolors='white', linewidth=2)
    plt.scatter(volatility_array[min_vol_idx], returns_array[min_vol_idx],
               marker='*', color='red', s=300, label='Min Volatility', edgecolors='white', linewidth=2)

    plt.title('Efficient Frontier - Monte Carlo Simulation')
    plt.xlabel('Annualized Volatility (Risk)')
    plt.ylabel('Annualized Return')
    plt.colorbar(scatter, label='Sharpe Ratio')
    plt.legend()
    plt.grid(True)
    plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
    print("\nEfficient Frontier plot saved as 'efficient_frontier.png'")

    # Find and display the optimal portfolios
    # 1. Max Sharpe Ratio Portfolio
    max_sharpe_return = returns_array[max_sharpe_idx]
    max_sharpe_volatility = volatility_array[max_sharpe_idx]
    max_sharpe_weights = weights_list[max_sharpe_idx]

    print("\n--- Max Sharpe Ratio Portfolio ---")
    print(f"Return: {max_sharpe_return*100:.2f}%")
    print(f"Volatility: {max_sharpe_volatility*100:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratios[max_sharpe_idx]:.2f}")
    print("Optimal Weights:")
    for ticker, weight in zip(portfolio_tickers, max_sharpe_weights):
        print(f"  {ticker}: {weight*100:.2f}%")

    # 2. Min Volatility Portfolio
    min_vol_idx = np.argmin(volatility_array)
    min_vol_return = returns_array[min_vol_idx]
    min_vol_volatility = volatility_array[min_vol_idx]
    min_vol_weights = weights_list[min_vol_idx]

    print("\n--- Minimum Volatility Portfolio ---")
    print(f"Return: {min_vol_return*100:.2f}%")
    print(f"Volatility: {min_vol_volatility*100:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratios[min_vol_idx]:.2f}")
    print("Optimal Weights:")
    for ticker, weight in zip(portfolio_tickers, min_vol_weights):
        print(f"  {ticker}: {weight*100:.2f}%")


if __name__ == "__main__":
    main()