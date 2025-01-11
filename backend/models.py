from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    websites = relationship("Website", back_populates="owner")

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    monitoring_interval = Column(Integer, default=300)  # in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="websites")
    monitoring_results = relationship("MonitoringResult", back_populates="website")
    ssl_checks = relationship("SSLCheck", back_populates="website")

class MonitoringResult(Base):
    __tablename__ = "monitoring_results"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    response_time = Column(Float)  # in seconds
    status_code = Column(Integer)
    is_up = Column(Boolean)
    error_message = Column(String, nullable=True)
    
    website = relationship("Website", back_populates="monitoring_results")

class SSLCheck(Base):
    __tablename__ = "ssl_checks"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_valid = Column(Boolean)
    expires_at = Column(DateTime(timezone=True))
    issuer = Column(String)
    error_message = Column(String, nullable=True)
    
    website = relationship("Website", back_populates="ssl_checks")

class SecurityHeader(Base):
    __tablename__ = "security_headers"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    headers = Column(JSON)  # Stores all security headers
    score = Column(Integer)  # Security score based on headers 
    error_message = Column(String, nullable=True)  # Add this field
