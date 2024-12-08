from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from schemas.prize import PrizeCreate

def parse_datetime(value: datetime) -> str:
    if value:
        return value.strftime('%Y-%m-%d %H:%M:%S')  # Beispielformat
    return value

class CampaignSchema(BaseModel):
    id: int
    name: str
    user_id: int
    active: bool
    created_at: str  # als String angeben
    max_ticket: int
    min_ticket: int
    max_ticket_per_user: int
    campaign_end: Optional[str]  # ebenfalls als String, da es Optional ist

    @staticmethod
    def parse_datetime(value: datetime) -> str:
        if value:
            return value.strftime('%Y-%m-%d %H:%M:%S')  # Beispielformat
        return value

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: parse_datetime,  # 'created_at' und 'campaign_end' werden zu Strings
        }


class CampaignCreate(BaseModel):
    name: str
    campaign_end: Optional[datetime] = Field(None, description="campaign end date (optional)")
    max_ticket: int = Field(..., description="Maximum number of tickets")
    min_ticket: int = Field(..., description="Minimum number of tickets required to start the campaign")
    max_ticket_per_user: int = Field(..., description="Maximum number of tickets allowed per user")
    prizes: List[PrizeCreate]

    class Config:
        schema_extra = {
            "example": {
                "name": "Summer Giveaway",
                "campaign_end": "2024-12-31T23:59:59",
                "max_ticket": 1000,
                "min_ticket": 10,
                "max_ticket_per_user": 5,
                "prizes": [
                    {
                        "product_name": "Smartphone",
                        "product_description": "Latest generation smartphone"
                    },
                    {
                        "product_name": "Tablet",
                        "product_description": "High-end tablet for work and entertainment"
                    }
                ]
            }
        }


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    max_ticket: Optional[int] = None
    min_ticket: Optional[int] = None
    max_ticket_per_user: Optional[int] = None
    campaign_end: Optional[str] = None
    active: Optional[bool] = None
    class Config:
        orm_mode = True