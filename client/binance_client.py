from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET
import time

class BinanceFuturesClient:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, testnet=True)

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }

        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        response = self.client.futures_create_order(**params)

        print("\n🧾 RAW ORDER RESPONSE:", response)

        return response

    def get_order(self, symbol, order_id):
        try:
            return self.client.futures_get_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
        except BinanceAPIException as e:
            print(f"⚠️ Fetch Error: {e}")
            return None

    def wait_for_fill(self, symbol, order_id, timeout=30):
        if not order_id:
            raise ValueError("Invalid order_id (None)")

        start = time.time()

        while True:
            order = self.get_order(symbol, order_id)

            if order:
                status = order.get("status")

                if status == "FILLED":
                    return order

            if time.time() - start > timeout:
                print("⏱ Timeout reached")
                return order

            time.sleep(2)
