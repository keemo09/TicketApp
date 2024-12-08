from pydantic import BaseModel, Field
from typing import Optional


class PrizeCreate(BaseModel):
    product_name: str
    product_description: Optional[str] = Field(None, description="Description of the product (optional)")

class PrizeUpdate(BaseModel):
    product_name: str = Field(None)
    product_description: Optional[str] = Field(None, description="Description of the product (optional)")