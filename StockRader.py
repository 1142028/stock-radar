import requests
from bs4 import BeautifulSoup

class Rader:
    def __init__(self, stock_symbol, line_token, price_threshold):
        self.stock_symbol = stock_symbol
        self.price_threshold = float(price_threshold)
        self.line_token = line_token
        self.last_price = None
        
    def line_message(self, message):
        line_url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {self.line_token}"}
        payload = {"message": message}
        requests.post(line_url, headers=headers, data=payload)

    def main(self):
            current_price = self.get_stock_price()
            if current_price is not None:
                if current_price >= self.price_threshold:
                    if self.last_price is None or current_price != self.last_price:
                        message = f"{self.stock_symbol} 的股價達到了設定的閾值! 當前股價是: {current_price}"
                        print(message)
                        self.line_message(message)
                        self.last_price = current_price
                    else:
                        print(f"{self.stock_symbol} 股價持續在 {current_price} (已發送通知)")
                else:
                    print(f"{self.stock_symbol} 當前股價: {current_price} (未達閾值)")
            else:
                print("無法獲取股價")

    def get_stock_price(self):
        url = f"https://finance.yahoo.com/quote/{self.stock_symbol}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
            if price_tag:
                return float(price_tag.text.replace(",", ""))
        return None

    