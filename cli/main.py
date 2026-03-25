import argparse
from client.binance_client import BinanceFuturesClient

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--order_type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    client = BinanceFuturesClient()

    response = client.place_order(
        args.symbol,
        args.side,
        args.order_type,
        args.quantity,
        args.price
    )

    order_id = response.get("orderId")

    print(f"\n📌 Order ID: {order_id}")

    if not order_id:
        raise ValueError("Order ID is None → order failed")

    final_order = client.wait_for_fill(args.symbol, order_id)

    print("\n✅ Final Order Status:")
    if final_order:
        print(f"Status         : {final_order.get('status')}")
        print(f"Executed Qty   : {final_order.get('executedQty')}")
        print(f"Avg Price      : {final_order.get('avgPrice')}")
    else:
        print("❌ Could not fetch order details")

if __name__ == "__main__":
    main()
