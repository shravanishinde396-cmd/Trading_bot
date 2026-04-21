import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from .exceptions import BinanceAPIError
from .logging_config import logger

load_dotenv()

def get_binance_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("Binance API keys not found in environment variables")
        raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET are required in .env")
        
    try:
        # Connect to Binance Futures Testnet
        client = Client(api_key, api_secret, testnet=True)
        # Verify connection by pinging the server
        client.futures_ping()
        return client
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception during initialization: {e.message}")
        raise BinanceAPIError(f"API Error: {e.message}")
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception during initialization: {e.message}")
        raise BinanceAPIError(f"Network Error: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error during client initialization: {str(e)}")
        raise BinanceAPIError(f"Unexpected error: {str(e)}")
