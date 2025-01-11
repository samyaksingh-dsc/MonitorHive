from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List, Annotated
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Website Schemas
class WebsiteBase(BaseModel):
    url: HttpUrl
    name: str
    monitoring_interval: Optional[int] = 300  # default 5 minutes

class WebsiteCreate(WebsiteBase):
    pass

class Website(WebsiteBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Monitoring Result Schemas
class MonitoringResultBase(BaseModel):
    response_time: float
    status_code: int
    is_up: bool
    error_message: Optional[str] = None

class MonitoringResultCreate(MonitoringResultBase):
    website_id: int

class MonitoringResult(MonitoringResultBase):
    id: int
    website_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# SSL Check Schemas
class SSLCheckBase(BaseModel):
    is_valid: bool
    expires_at: datetime
    issuer: str
    error_message: Optional[str] = None

class SSLCheckCreate(SSLCheckBase):
    website_id: int

class SSLCheck(SSLCheckBase):
    id: int
    website_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Security Header Schemas
class SecurityHeaderBase(BaseModel):
    headers: dict
    score: Annotated[int, Field(ge=0, le=100)]  # Score between 0 and 100

class SecurityHeaderCreate(SecurityHeaderBase):
    website_id: int

class SecurityHeader(SecurityHeaderBase):
    id: int
    website_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None