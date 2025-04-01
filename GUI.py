import tkinter as tk 
from tkinter import messagebox
import threading
import time
import json
from StockRader import Rader

class RaderGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("股票雷達GUI介面")
        self.window.geometry("400x400")  

        self.stock_symbol_label = tk.Label(self.window, text="股票代碼:")
        self.stock_symbol_label.pack(pady=5)

        self.stock_symbol_entry = tk.Entry(self.window)
        self.stock_symbol_entry.pack(pady=5)

        self.email_label = tk.Label(self.window, text="通知 Email:")
        self.email_label.pack(pady=5)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack(pady=5)

        self.price_threshold_label = tk.Label(self.window, text="股價閾值:")
        self.price_threshold_label.pack(pady=5)

        self.price_threshold_entry = tk.Entry(self.window)
        self.price_threshold_entry.pack(pady=5)

        self.start_button = tk.Button(self.window, text="開始雷達", command=self.start_notifier)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(self.window, text="等待中...", fg="green")
        self.status_label.pack(pady=10)

        self.stock_price_label = tk.Label(self.window, text="當前股價: N/A")
        self.stock_price_label.pack(pady=5)

        self.load_saved_email() 

    def load_saved_email(self):
        try:
            with open("email_address.json", "r") as file:
                data = json.load(file)
                if "email" in data:
                    self.email_entry.insert(0, data["email"])
        except FileNotFoundError:
            pass

    def save_email(self, email):
        with open("email_address.json", "w") as file:
            json.dump({"email": email}, file)

    def run_notifier(self, stock_notifier):
        while True:
            stock_notifier.main()
            current_price = stock_notifier.get_stock_price()
            if current_price is not None:
                self.stock_price_label.config(text=f"當前股價: {current_price}")
            time.sleep(30)

    def start_notifier(self):
        stock_symbol = self.stock_symbol_entry.get()
        email = self.email_entry.get()
        price_threshold = self.price_threshold_entry.get()
        if not stock_symbol or not email or not price_threshold:
            messagebox.showerror("輸入錯誤", "請重新輸入所有欄位")
            return
        try:
            float(price_threshold)
        except ValueError:
            messagebox.showerror("輸入錯誤", "請輸入有效的股價閾值")
            return
        self.save_email(email) 
        stock_notifier = Rader(stock_symbol, email, price_threshold)
        threading.Thread(target=self.run_notifier, args=(stock_notifier,), daemon=True).start()
        self.status_label.config(text=f"開始偵測股票 {stock_symbol} 的股價，當股價達到 {price_threshold} 時會發送通知。", fg="blue")

if __name__ == "__main__":
    window = tk.Tk()
    app = RaderGUI(window)
    window.mainloop()
