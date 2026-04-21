class TradingBotException(Exception):
    """Base exception for the trading bot."""
    pass

class ValidationError(TradingBotException):
    """Raised when input validation fails."""
    pass

class BinanceAPIError(TradingBotException):
    """Raised when the Binance API returns an error."""
    pass
