from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class OrderRequest(BaseModel):
    symbol: str
    side: str
    type: str
    quantity: float
    price: Optional[float] = None
    
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError("Symbol must be uppercase")
        return v
        
    @field_validator("side")
    @classmethod
    def validate_side(cls, v: str) -> str:
        v = v.upper()
        if v not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")
        return v

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        v = v.upper()
        if v not in ("MARKET", "LIMIT"):
            raise ValueError("Type must be MARKET or LIMIT")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v
        
    @model_validator(mode='after')
    def validate_price(self) -> 'OrderRequest':
        if self.type == "LIMIT" and self.price is None:
            raise ValueError("Price is required for LIMIT orders")
        
        if self.price is not None and self.price <= 0:
            raise ValueError("Price must be greater than 0")
            
        return self
