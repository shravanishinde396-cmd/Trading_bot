import streamlit as st
import requests
import os
from pathlib import Path

# Provide standard API URL (default 8000)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Binance Bot Dashboard", layout="wide")

st.title("📈 Binance Futures Bot")
st.markdown("Trade on Binance Futures Testnet (USDT-M)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Place Order")
    with st.form("order_form"):
        symbol = st.text_input("Symbol", value="BTCUSDT").upper()
        side = st.selectbox("Side", ["BUY", "SELL"])
        order_type = st.selectbox("Type", ["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", min_value=0.001, step=0.001, format="%.3f")
        price = st.number_input("Price (Required for LIMIT)", min_value=0.0, step=0.5, format="%.2f")
        
        submitted = st.form_submit_button("Place Order")
        
        if submitted:
            payload = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }
            if order_type == "LIMIT":
                payload["price"] = price

            with st.spinner("Placing order..."):
                try:
                    response = requests.post(f"{API_URL}/order", json=payload)
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success("✅ Order Placed Successfully")
                        st.subheader("Response")
                        
                        # Show last order response summary beautifully
                        st.info(f"""
                        **Order ID:** {data.get('orderId')}  
                        **Status:** {data.get('status')}  
                        **Executed Qty:** {data.get('executedQty')}  
                        **Avg Price:** {data.get('avgPrice')}
                        """)
                    else:
                        st.error("❌ Order Failed")
                        st.write(data.get("error", "Unknown error"))
                except requests.exceptions.ConnectionError:
                    st.error(f"❌ Could not connect to API at {API_URL}. Is FastAPI running?")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("Logs Preview")
    log_file = Path("logs/trading_bot.log")
    
    if st.button("Refresh Logs"):
        pass # Streamlit natively reruns the script on button click
        
    try:
        if log_file.exists():
            # Get last 20 lines
            with open(log_file, "r") as f:
                lines = f.readlines()
                log_preview = "".join(lines[-20:])
            st.code(log_preview, language="text")
        else:
            st.info("No logs found yet.")
    except Exception as e:
        st.error(f"Error reading logs: {str(e)}")
