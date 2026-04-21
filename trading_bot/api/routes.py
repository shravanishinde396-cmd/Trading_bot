from fastapi import APIRouter, HTTPException
from bot.validators import OrderRequest
from bot.orders import place_market_order, place_limit_order
from bot.logging_config import logger

router = APIRouter()

@router.post("/order")
async def create_order(request: OrderRequest):
    logger.info(f"Received API request for order: {request.dict()}")
    
    try:
        if request.type == "MARKET":
            response = place_market_order(
                symbol=request.symbol,
                side=request.side,
                quantity=request.quantity
            )
        elif request.type == "LIMIT":
            if request.price is None:
                raise ValueError("Price is required for LIMIT orders")
            response = place_limit_order(
                symbol=request.symbol,
                side=request.side,
                quantity=request.quantity,
                price=request.price
            )
        else:
            raise ValueError(f"Unsupported order type: {request.type}")
            
        logger.info(f"API successfully processed order: {response}")
        return response
        
    except Exception as e:
        # Ensure we log the issue before it propagates to the exception handlers
        logger.error(f"Error handling API order request: {str(e)}")
        raise
