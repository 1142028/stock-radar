import os
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

class Rader:
    def __init__(self, stock_symbol, email, price_threshold):
        self.stock_symbol = stock_symbol
        self.price_threshold = float(price_threshold)
        self.email = email
        self.last_price = None

    def send_email(self, subject, message):
        sender_email = os.environ["STOCK_RADAR_EMAIL"]
        sender_password = os.environ["STOCK_RADAR_APP_PASSWORD"]
        
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = self.email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.email, msg.as_string())

    def main(self):
        current_price = self.get_stock_price()
        if current_price is not None and current_price >= self.price_threshold:
            if self.last_price is None or current_price != self.last_price:
                message = f"{self.stock_symbol} 的股價達到了設定的閾值! 當前股價是: {current_price}"
                print(message)
                self.send_email("股價警報", message)
                self.last_price = current_price
            else:
                print(f"{self.stock_symbol} 股價持續在 {current_price} (已發送通知)")
        else:
            print(f"{self.stock_symbol} 當前股價: {current_price} (未達閾值)")

    def get_stock_price(self):
        url = f"https://finance.yahoo.com/quote/{self.stock_symbol}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
            if price_tag:
                return float(price_tag.text.replace(",", ""))
        except Exception as e:
            print("獲取股價失敗:", e)
        return None
