from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers of interest
        self.tickers = ["SPY", "QQQ"]
        
        # OHLCV data objects for each ticker
        self.data_list = [OHLCV(i) for i in self.tickers]

    @property
    def interval(self):
        # Set the data interval to '1day' for daily analysis
        return "1day"

    @property
    def assets(self):
        # Interested in trading SPY and QQQ
        return self.tickers

    @property
    def data(self):
        # Return the data objects required for analysis
        return self.data_list

    def run(self, data):
        # Retrieve closing prices for SPY and QQQ
        spy_close_prices = [i["SPY"]["close"] for i in data["ohlcv"]]
        qqq_close_prices = [i["QQQ"]["close"] for i in data["ohlcv"]]

        # Convert to DataFrame for correlation analysis
        df = pd.DataFrame({"SPY": spy_close_prices, "QQQ": qqq_close_prices})
        # Compute the correlation over the defined period (e.g., last 30 days)
        correlation = df.tail(30).corr().iloc[0, 1]

        # Define the allocation dictionary
        allocation_dict = {"SPY": 0, "QQQ": 0}

        # Trading logic based on correlation
        if correlation > 0.8:
            # High correlation detected; no clear trading signal, remain neutral or implement additional logic
            pass
        elif correlation < 0.5:
            # If the correlation drops significantly, consider it a signal to trade
            # This part can be replaced with a more sophisticated logic
            # For example, allocate more to SPY assuming it might outperform or vice versa
            allocation_dict["SPY"] = 0.5  # Allocate 50% to SPY
            allocation_dict["QQQ"] = 0.5  # Allocate 50% to QQQ

        # Return the target allocation
        return TargetAllocation(allocation_dict)