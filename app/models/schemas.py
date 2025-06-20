"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, Any
from datetime import datetime

# 🌟 MODELOS GERAIS

class APIResponse(BaseModel):
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# 🌟 MODELOS DE ITEM

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., ge=0, description="Item price (must be >= 0)")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Price must be greater than or equal to 0')
        return round(v, 2)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = Field(None)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and (not v.strip()):
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v

    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be >= 0')
        return round(v, 2) if v is not None else v

class ItemResponse(ItemBase):
    id: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# 🌟 MODELO DE SAÚDE

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# 🌟 MODELOS DE USUÁRIO

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
