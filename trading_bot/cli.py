import typer
from typing import Optional
from bot.orders import place_market_order, place_limit_order
from bot.validators import OrderRequest
from pydantic import ValidationError
from bot.exceptions import BinanceAPIError

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")

@app.command()
def info():
    """Show information about the trading bot."""
    typer.echo("Binance Futures Testnet Trading Bot v1.0")

@app.command()
def trade(
    symbol: str = typer.Option(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="Order side: BUY or SELL"),
    type: str = typer.Option(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, help="Price for LIMIT orders")
):
    """
    Place a trade on Binance Futures Testnet.
    """
    click_echo_output = f"==== ORDER REQUEST ====\n"
    click_echo_output += f"Symbol: {symbol}\n"
    click_echo_output += f"Side: {side}\n"
    click_echo_output += f"Type: {type}\n"
    click_echo_output += f"Quantity: {quantity}\n"
    
    if price is not None:
        click_echo_output += f"Price: {price}\n"
        
    typer.echo(click_echo_output)
    
    try:
        # Validate using pydantic
        req = OrderRequest(
            symbol=symbol,
            side=side,
            type=type,
            quantity=quantity,
            price=price
        )
        
        # Execute
        if req.type == "MARKET":
            response = place_market_order(
                symbol=req.symbol,
                side=req.side,
                quantity=req.quantity
            )
        elif req.type == "LIMIT":
            response = place_limit_order(
                symbol=req.symbol,
                side=req.side,
                quantity=req.quantity,
                price=req.price
            )
            
        typer.echo("==== RESPONSE ====")
        typer.echo(f"Order ID: {response['orderId']}")
        typer.echo(f"Status: {response['status']}")
        typer.echo(f"Executed Qty: {response['executedQty']}")
        typer.echo(f"Avg Price: {response['avgPrice']}")
        typer.echo("\n[SUCCESS] Success")
        
    except ValidationError as e:
        typer.echo("==== ERROR ====")
        for err in e.errors():
            typer.echo(f"[ERROR] {err['loc'][-1]}: {err['msg']}")
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo("==== ERROR ====")
        typer.echo(f"[ERROR] {str(e)}")
        raise typer.Exit(code=1)
    except BinanceAPIError as e:
        typer.echo("==== ERROR ====")
        typer.echo(f"[ERROR] {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo("==== ERROR ====")
        typer.echo(f"[ERROR] Unexpected Error: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
