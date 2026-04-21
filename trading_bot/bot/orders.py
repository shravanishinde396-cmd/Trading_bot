from binance.exceptions import BinanceAPIException, BinanceRequestException
from .client import get_binance_client
from .exceptions import BinanceAPIError
from .logging_config import logger

def _format_response(response: dict) -> dict:
    # Handle both new order response format and get order format
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty", "0"),
        "avgPrice": response.get("avgPrice", "0")
    }

def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    try:
        client = get_binance_client()
        logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
        
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        logger.info(f"MARKET order placed successfully. Order ID: {response.get('orderId')}")
        return _format_response(response)
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception during market order: {e.message}")
        raise BinanceAPIError(f"API Error: {e.message}")
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception during market order: {e.message}")
        raise BinanceAPIError(f"Network Error: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error during market order: {str(e)}")
        raise BinanceAPIError(f"Unexpected error: {str(e)}")

def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    try:
        client = get_binance_client()
        logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} at {price}")
        
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        
        logger.info(f"LIMIT order placed successfully. Order ID: {response.get('orderId')}")
        return _format_response(response)
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception during limit order: {e.message}")
        raise BinanceAPIError(f"API Error: {e.message}")
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception during limit order: {e.message}")
        raise BinanceAPIError(f"Network Error: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error during limit order: {str(e)}")
        raise BinanceAPIError(f"Unexpected error: {str(e)}")
