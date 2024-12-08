from pydantic import BaseModel, Field


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=25)
    description: str = Field(None)


class CampaignUpdate(BaseModel):
    name: str = Field(None, min_length=4, max_length=2)
    description: str = Field(None)