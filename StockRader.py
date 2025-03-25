import requests
from bs4 import BeautifulSoup

class StockRader:
    def __init__(self, stock_symbol, price_threshold):
        self.stock_symbol = stock_symbol
        self.price_threshold = float(price_threshold)

    def get_stock_price(self):
        url = "https://finance.yahoo.com/quote/" + self.stock_symbol
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
            if tag:
                return float(tag.text.replace(",", ""))
        return None
    
    def main(self):
        price = self.get_stock_price()
        if price is not None:
            if price >= self.price_threshold:
                print(self.stock_symbol + " 股價達到閾值! 當前股價: " + str(price))
            else:
                print(self.stock_symbol + " 當前股價: " + str(price) + " (未達閾值)")
        else:
            print("無法獲取股價")

if __name__ == "__main__":
    stock = "AAPL"
    threshold = 5800
    monitor = StockRader(stock, threshold)
    monitor.main()